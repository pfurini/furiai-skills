#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes Pi to trigger (load the skill)
for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import select
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping

from scripts.utils import parse_skill_md


RoleName = Literal["trigger_consumer", "optimizer"]
EffectiveEvidence = Literal["pi_event", "pi_subagents_invocation"]
THINKING_LEVELS = frozenset({"off", "minimal", "low", "medium", "high", "xhigh", "max"})
_ROLE_ENV = {
    "trigger_consumer": (
        "OPIN_TRIGGER_CONSUMER_MODEL",
        "OPIN_TRIGGER_CONSUMER_THINKING",
    ),
    "optimizer": ("OPIN_OPTIMIZER_MODEL", "OPIN_OPTIMIZER_THINKING"),
}


class RoleConfigurationError(ValueError):
    """Raised when role model configuration is absent or contradictory."""


@dataclass
class RoleModelConfig:
    """Requested role settings plus effective values supported by runtime evidence."""

    role: RoleName
    requested_model: str
    requested_thinking: str
    model_source: str = "argument"
    thinking_source: str = "argument"
    effective_model: str | None = None
    effective_thinking: str | None = None
    effective_evidence: EffectiveEvidence | None = None

    def __post_init__(self) -> None:
        if self.role not in _ROLE_ENV:
            raise RoleConfigurationError(f"unsupported model-consuming role: {self.role!r}")
        self.requested_model = self.requested_model.strip()
        self.requested_thinking = self.requested_thinking.strip()
        if not self.requested_model:
            raise RoleConfigurationError(f"{self.role} requested model is required")
        if self.requested_thinking not in THINKING_LEVELS:
            choices = ", ".join(sorted(THINKING_LEVELS))
            raise RoleConfigurationError(
                f"{self.role} requested thinking must be one of: {choices}"
            )

    def record_effective(
        self,
        *,
        model: str | None = None,
        thinking: str | None = None,
        evidence: EffectiveEvidence,
    ) -> None:
        """Record only values observed in Pi events or invocation records."""
        normalized_model = model.strip() if model is not None else None
        normalized_thinking = thinking.strip() if thinking is not None else None
        if normalized_model == "":
            raise RoleConfigurationError(f"{self.role} effective model evidence is empty")
        if normalized_thinking == "":
            raise RoleConfigurationError(f"{self.role} effective thinking evidence is empty")
        if normalized_thinking is not None and normalized_thinking not in THINKING_LEVELS:
            raise RoleConfigurationError(
                f"{self.role} effective thinking evidence is unsupported: {normalized_thinking!r}"
            )
        if (
            normalized_model is not None
            and self.effective_model is not None
            and normalized_model != self.effective_model
        ):
            raise RoleConfigurationError(
                f"conflicting {self.role} effective model evidence: "
                f"{self.effective_model!r} != {normalized_model!r}"
            )
        if (
            normalized_thinking is not None
            and self.effective_thinking is not None
            and normalized_thinking != self.effective_thinking
        ):
            raise RoleConfigurationError(
                f"conflicting {self.role} effective thinking evidence: "
                f"{self.effective_thinking!r} != {normalized_thinking!r}"
            )
        if normalized_model is not None:
            self.effective_model = normalized_model
        if normalized_thinking is not None:
            self.effective_thinking = normalized_thinking
        if normalized_model is not None or normalized_thinking is not None:
            self.effective_evidence = evidence

    def as_metadata(self) -> dict[str, str | None]:
        """Return durable requested/effective role metadata without inferred values."""
        return {
            "requested_model": self.requested_model,
            "requested_thinking": self.requested_thinking,
            "effective_model": self.effective_model,
            "effective_thinking": self.effective_thinking,
            "model_source": self.model_source,
            "thinking_source": self.thinking_source,
            "effective_evidence": self.effective_evidence,
        }


@dataclass(frozen=True)
class TriggerInvocationResult:
    """Boolean trigger result paired with model evidence from that invocation."""

    triggered: bool
    role_config: RoleModelConfig


def add_role_arguments(parser: argparse.ArgumentParser, role: RoleName) -> None:
    """Add the shared model/thinking CLI mapping for one role."""
    flag_role = role.replace("_", "-")
    parser.add_argument(
        f"--{flag_role}-model",
        default=None,
        help=f"Requested model for the {flag_role} role",
    )
    parser.add_argument(
        f"--{flag_role}-thinking",
        default=None,
        choices=sorted(THINKING_LEVELS),
        help=f"Requested thinking level for the {flag_role} role",
    )


def role_config_from_args(
    args: argparse.Namespace,
    role: RoleName,
    *,
    environ: Mapping[str, str] | None = None,
) -> RoleModelConfig:
    """Resolve one role from explicit arguments, then recorded environment defaults."""
    values = os.environ if environ is None else environ
    destination = role
    argument_model = getattr(args, f"{destination}_model", None)
    argument_thinking = getattr(args, f"{destination}_thinking", None)
    role_model_env, role_thinking_env = _ROLE_ENV[role]

    requested_model = argument_model
    model_source = "argument"
    if requested_model is None:
        requested_model = values.get(role_model_env)
        model_source = role_model_env
    if requested_model is None:
        configured_model = values.get("PI_MODEL")
        configured_provider = values.get("PI_PROVIDER")
        if configured_model:
            if configured_provider and "/" not in configured_model:
                requested_model = f"{configured_provider}/{configured_model}"
                model_source = "PI_PROVIDER+PI_MODEL"
            else:
                requested_model = configured_model
                model_source = "PI_MODEL"

    requested_thinking = argument_thinking
    thinking_source = "argument"
    if requested_thinking is None:
        requested_thinking = values.get(role_thinking_env)
        thinking_source = role_thinking_env
    if requested_thinking is None:
        requested_thinking = values.get("PI_REASONING_LEVEL")
        thinking_source = "PI_REASONING_LEVEL"

    flag_role = role.replace("_", "-")
    if requested_model is None:
        raise RoleConfigurationError(
            f"--{flag_role}-model is required (or set {role_model_env}/PI_MODEL)"
        )
    if requested_thinking is None:
        raise RoleConfigurationError(
            f"--{flag_role}-thinking is required "
            f"(or set {role_thinking_env}/PI_REASONING_LEVEL)"
        )
    return RoleModelConfig(
        role=role,
        requested_model=requested_model,
        requested_thinking=requested_thinking,
        model_source=model_source,
        thinking_source=thinking_source,
    )


def record_effective_from_event(config: RoleModelConfig, event: object) -> None:
    """Capture canonical effective values present in a Pi event or invocation record."""
    if not isinstance(event, dict):
        return

    model: str | None = None
    thinking: str | None = None
    message = event.get("message")
    if event.get("type") == "message_end" and isinstance(message, dict):
        if message.get("role") == "assistant":
            provider = message.get("provider")
            response_model = message.get("responseModel")
            message_model = response_model or message.get("model")
            if (
                isinstance(message_model, str)
                and message_model
                and isinstance(provider, str)
                and provider
            ):
                model = f"{provider}/{message_model}"
            message_thinking = message.get("thinkingLevel")
            if isinstance(message_thinking, str):
                thinking = message_thinking

    effective_model = event.get("effective_model", event.get("effectiveModel"))
    effective_thinking = event.get("effective_thinking", event.get("effectiveThinking"))
    if isinstance(effective_model, str):
        model = effective_model
    if isinstance(effective_thinking, str):
        thinking = effective_thinking
    event_thinking = event.get("thinkingLevel")
    if isinstance(event_thinking, str):
        thinking = event_thinking
    evidence: EffectiveEvidence = "pi_event"
    invocation = event.get("invocation")
    if isinstance(invocation, dict):
        invocation_model = invocation.get("modelId")
        invocation_thinking = invocation.get("thinking")
        if isinstance(invocation_model, str):
            model = invocation_model
            evidence = "pi_subagents_invocation"
        if isinstance(invocation_thinking, str):
            thinking = invocation_thinking
            evidence = "pi_subagents_invocation"

    if model is not None or thinking is not None:
        config.record_effective(
            model=model,
            thinking=thinking,
            evidence=evidence,
        )


def find_project_root() -> Path:
    """Return the current project root used for in-situ trigger evaluation."""
    return Path.cwd()


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    role_config: RoleModelConfig,
) -> TriggerInvocationResult:
    """Run a single query and return whether the skill was triggered.

    Creates a temporary SKILL.md, loads it with `pi --skill`, then runs
    `pi --mode json -p` with the raw query. The temporary skill appears in
    Pi's available_skills list. JSON `tool_execution_start` events reveal
    whether Pi invoked the `skill` tool or read that SKILL.md directly.
    """
    clean_name = f"eval-skill-{uuid.uuid4().hex[:8]}"

    with tempfile.TemporaryDirectory(prefix="opin-skill-creator-eval-") as temp_dir:
        skill_file = Path(temp_dir) / "SKILL.md"
        indented_desc = "\n  ".join(skill_description.split("\n"))
        skill_file.write_text(
            f"---\n"
            f"name: {clean_name}\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )

        cmd = [
            "pi",
            "--mode", "json",
            "-p", query,
            "--no-session",
            "--skill", str(skill_file),
            "--model", role_config.requested_model,
            "--thinking", role_config.requested_thinking,
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
        )
        if process.stdout is None:
            return TriggerInvocationResult(False, role_config)

        start_time = time.time()
        buffer = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    record_effective_from_event(role_config, event)
                    if event.get("type") != "tool_execution_start":
                        continue

                    tool_name = event.get("toolName", "")
                    args = event.get("args", {})
                    if tool_name == "skill" and args.get("name") == clean_name:
                        return TriggerInvocationResult(True, role_config)
                    if tool_name == "read" and str(skill_file) in json.dumps(args):
                        return TriggerInvocationResult(True, role_config)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return TriggerInvocationResult(False, role_config)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    role_config: RoleModelConfig,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
) -> dict:
    """Run the full eval set and return results."""
    if role_config.role != "trigger_consumer":
        raise RoleConfigurationError("run_eval requires trigger_consumer role configuration")
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    role_config,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        invocation_configs: list[RoleModelConfig] = []
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                invocation = future.result()
                query_triggers[query].append(invocation.triggered)
                invocation_configs.append(invocation.role_config)
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    effective_models = {
        config.effective_model
        for config in invocation_configs
        if config.effective_model is not None
    }
    effective_thinking = {
        config.effective_thinking
        for config in invocation_configs
        if config.effective_thinking is not None
    }
    if len(effective_models) > 1 or len(effective_thinking) > 1:
        raise RoleConfigurationError("trigger invocations reported conflicting effective role values")
    role_config.record_effective(
        model=next(iter(effective_models), None),
        thinking=next(iter(effective_thinking), None),
        evidence="pi_event",
    )

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "roles": {"trigger_consumer": role_config.as_metadata()},
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    add_role_arguments(parser, "trigger_consumer")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()
    try:
        role_config = role_config_from_args(args, "trigger_consumer")
    except RoleConfigurationError as error:
        parser.error(str(error))

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        role_config=role_config,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
