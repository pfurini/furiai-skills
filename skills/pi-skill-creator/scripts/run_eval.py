#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes Pi to trigger (load the skill)
for a set of queries. Outputs results as JSON.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping

from scripts.utils import parse_skill_md


RoleName = Literal["trigger_consumer", "optimizer"]
EffectiveEvidence = Literal["pi_event", "pi_subagents_invocation"]
TriggerStatus = Literal[
    "triggered",
    "not_triggered",
    "timeout",
    "process_error",
    "model_error",
    "auth_error",
    "invalid_output",
]
InvocationMechanism = Literal["skill_tool", "skill_md_read"]
THINKING_LEVELS = frozenset({"off", "minimal", "low", "medium", "high", "xhigh", "max"})
TRIGGER_STATUSES = frozenset(
    {
        "triggered",
        "not_triggered",
        "timeout",
        "process_error",
        "model_error",
        "auth_error",
        "invalid_output",
    }
)
ACCURACY_STATUSES = frozenset({"triggered", "not_triggered"})
INFRASTRUCTURE_STATUSES = TRIGGER_STATUSES - ACCURACY_STATUSES
MAX_STDERR_CHARS = 4096
PI_REVISION = "db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee"
_ROLE_ENV = {
    "trigger_consumer": (
        "PI_SKILL_CREATOR_TRIGGER_CONSUMER_MODEL",
        "PI_SKILL_CREATOR_TRIGGER_CONSUMER_THINKING",
    ),
    "optimizer": ("PI_SKILL_CREATOR_OPTIMIZER_MODEL", "PI_SKILL_CREATOR_OPTIMIZER_THINKING"),
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


@dataclass
class TriggerInvocationResult:
    """One trigger attempt result with complete process and environment evidence."""

    status: TriggerStatus
    attempts: int
    exit_code: int | None
    stderr: str
    role_config: RoleModelConfig
    environment_profile: Literal["in-situ"]
    evaluation_cwd: str
    skill_name: str
    competing_skills: tuple[str, ...]
    pi_revision: str
    events: tuple[dict, ...]
    invocation_mechanism: InvocationMechanism | None
    transient_error: bool = False
    attempt_statuses: tuple[TriggerStatus, ...] = ()

    @property
    def triggered(self) -> bool:
        """Preserve the former convenience property without collapsing errors."""
        return self.status == "triggered"

    def as_dict(self) -> dict[str, object]:
        """Return the durable trigger-result record."""
        return {
            "status": self.status,
            "attempts": self.attempts,
            "attempt_statuses": list(self.attempt_statuses or (self.status,)),
            "exit_code": self.exit_code,
            "stderr": self.stderr,
            "requested_model": self.role_config.requested_model,
            "effective_model": self.role_config.effective_model,
            "requested_thinking": self.role_config.requested_thinking,
            "effective_thinking": self.role_config.effective_thinking,
            "environment_profile": self.environment_profile,
            "evaluation_cwd": self.evaluation_cwd,
            "skill_name": self.skill_name,
            "competing_skills": list(self.competing_skills),
            "pi_revision": self.pi_revision,
            "events": list(self.events),
            "invocation_mechanism": self.invocation_mechanism,
        }


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
    """Return the current directory for legacy callers that already run in-situ."""
    return Path.cwd()


def _bounded_stderr(stderr: str) -> str:
    """Keep the diagnostic tail, where subprocesses normally report the cause."""
    return stderr[-MAX_STDERR_CHARS:]


def _decode_stream(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _parse_events(output: str) -> tuple[tuple[dict, ...], bool]:
    """Parse LF-delimited Pi events without skipping malformed records."""
    events: list[dict] = []
    for raw_line in output.split("\n"):
        line = raw_line[:-1] if raw_line.endswith("\r") else raw_line
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return tuple(events), False
        if not isinstance(event, dict):
            return tuple(events), False
        events.append(event)
    return tuple(events), True


def _error_text(events: tuple[dict, ...], stderr: str) -> str:
    error_events: list[dict] = []
    for event in events:
        message = event.get("message")
        message_failed = (
            isinstance(message, dict)
            and (message.get("stopReason") in {"error", "aborted"} or "errorMessage" in message)
        )
        if (
            event.get("type") in {"error", "agent_error", "model_error"}
            or "error" in event
            or message_failed
        ):
            error_events.append(event)
    return (stderr + "\n" + json.dumps(error_events, sort_keys=True)).lower()


def _is_transient_provider_error(error_text: str) -> bool:
    signals = (
        "rate limit",
        "rate_limit",
        "status 429",
        '"status": 429',
        "retryable=true",
        '"retryable": true',
        "temporarily unavailable",
        "service unavailable",
        "provider overloaded",
    )
    return any(signal in error_text for signal in signals)


def _classify_error(events: tuple[dict, ...], stderr: str) -> tuple[TriggerStatus | None, bool]:
    error_text = _error_text(events, stderr)
    auth_signals = (
        "authentication",
        "unauthorized",
        "forbidden",
        "invalid api key",
        "api key",
        "auth_error",
    )
    if any(signal in error_text for signal in auth_signals):
        return "auth_error", False

    transient = _is_transient_provider_error(error_text)
    model_signals = (
        "model error",
        "model_error",
        "model provider",
        "provider error",
        "unknown model",
        "model not found",
        "failed to resolve model",
    )
    if transient or any(signal in error_text for signal in model_signals):
        return "model_error", transient
    return None, False


def _normalize_competing_skills(
    competing_skills: tuple[str, ...],
    skill_name: str,
) -> tuple[str, ...]:
    """Validate the explicit set and exclude installed copies of the target."""
    normalized: list[str] = []
    for value in competing_skills:
        skill_path = Path(value)
        if not skill_path.is_absolute():
            raise ValueError("competing skill paths must be absolute")
        skill_file = skill_path if skill_path.name == "SKILL.md" else skill_path / "SKILL.md"
        if not skill_file.is_file():
            raise ValueError(f"competing skill has no SKILL.md: {skill_path}")
        competing_name, _, _ = parse_skill_md(skill_file.parent)
        if competing_name != skill_name:
            normalized.append(os.fspath(skill_path))
    return tuple(normalized)


def _candidate_skill_file(
    skill_name: str,
    skill_description: str,
    evaluation_cwd: str,
    competing_skills: tuple[str, ...],
) -> Path:
    """Materialize the candidate at a stable path while preserving its real name."""
    identity = json.dumps(
        [skill_name, skill_description, evaluation_cwd, *competing_skills],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
    skill_dir = Path(tempfile.gettempdir()) / "pi-skill-creator-trigger" / digest / "candidate"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    indented_description = "\n  ".join(skill_description.split("\n"))
    skill_file.write_text(
        f"---\n"
        f"name: {skill_name}\n"
        f"description: |\n"
        f"  {indented_description}\n"
        f"---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {skill_description}\n",
        encoding="utf-8",
        newline="\n",
    )
    return skill_file


def _invocation_mechanism(
    events: tuple[dict, ...],
    skill_name: str,
    skill_file: Path,
) -> InvocationMechanism | None:
    direct_read = False
    for event in events:
        if event.get("type") != "tool_execution_start":
            continue
        tool_name = event.get("toolName", event.get("tool_name"))
        arguments = event.get("args", event.get("arguments", {}))
        if not isinstance(arguments, dict):
            continue
        if tool_name == "skill" and arguments.get("name") == skill_name:
            return "skill_tool"
        if tool_name == "read" and os.fspath(skill_file) in json.dumps(arguments):
            direct_read = True
    return "skill_md_read" if direct_read else None


def _result(
    *,
    status: TriggerStatus,
    attempts: int,
    exit_code: int | None,
    stderr: str,
    role_config: RoleModelConfig,
    evaluation_cwd: str,
    skill_name: str,
    competing_skills: tuple[str, ...],
    events: tuple[dict, ...] = (),
    invocation_mechanism: InvocationMechanism | None = None,
    transient_error: bool = False,
    attempt_statuses: tuple[TriggerStatus, ...] = (),
) -> TriggerInvocationResult:
    return TriggerInvocationResult(
        status=status,
        attempts=attempts,
        exit_code=exit_code,
        stderr=_bounded_stderr(stderr),
        role_config=role_config,
        environment_profile="in-situ",
        evaluation_cwd=evaluation_cwd,
        skill_name=skill_name,
        competing_skills=competing_skills,
        pi_revision=PI_REVISION,
        events=events,
        invocation_mechanism=invocation_mechanism,
        transient_error=transient_error,
        attempt_statuses=attempt_statuses or (status,),
    )


def _run_query_attempt(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    evaluation_cwd: str,
    role_config: RoleModelConfig,
    competing_skills: tuple[str, ...],
    pi_executable: str,
) -> TriggerInvocationResult:
    skill_file = _candidate_skill_file(
        skill_name, skill_description, evaluation_cwd, competing_skills
    )
    command = [
        pi_executable,
        "--mode",
        "json",
        "--no-session",
        "--no-skills",
        "--skill",
        os.fspath(skill_file),
    ]
    for competitor in competing_skills:
        command.extend(("--skill", competitor))
    command.extend(
        (
            "--model",
            role_config.requested_model,
            "--thinking",
            role_config.requested_thinking,
        )
    )

    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=evaluation_cwd,
            text=True,
        )
    except OSError as error:
        return _result(
            status="process_error",
            attempts=1,
            exit_code=None,
            stderr=f"{type(error).__name__}: {error}",
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
        )

    if (
        getattr(process, "stdin", None) is None
        or getattr(process, "stdout", None) is None
        or getattr(process, "stderr", None) is None
    ):
        if hasattr(process, "kill"):
            process.kill()
        return _result(
            status="process_error",
            attempts=1,
            exit_code=getattr(process, "returncode", None),
            stderr="Pi subprocess did not expose all required standard streams",
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
        )

    try:
        stdout, stderr = process.communicate(input=query, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        process.kill()
        final_stdout, final_stderr = process.communicate()
        stdout = _decode_stream(final_stdout) or _decode_stream(error.output)
        stderr = _decode_stream(final_stderr) or _decode_stream(error.stderr)
        events, _ = _parse_events(stdout)
        return _result(
            status="timeout",
            attempts=1,
            exit_code=None,
            stderr=stderr,
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
        )
    except (OSError, subprocess.SubprocessError) as error:
        if process.poll() is None:
            process.kill()
            process.wait()
        return _result(
            status="process_error",
            attempts=1,
            exit_code=getattr(process, "returncode", None),
            stderr=f"{type(error).__name__}: {error}",
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
        )

    events, output_is_valid = _parse_events(stdout)
    if not output_is_valid:
        return _result(
            status="invalid_output",
            attempts=1,
            exit_code=process.returncode,
            stderr=stderr,
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
        )

    try:
        for event in events:
            record_effective_from_event(role_config, event)
    except RoleConfigurationError as error:
        return _result(
            status="invalid_output",
            attempts=1,
            exit_code=process.returncode,
            stderr=f"{stderr}\n{error}",
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
        )

    error_status, transient = _classify_error(events, stderr)
    if error_status is not None:
        return _result(
            status=error_status,
            attempts=1,
            exit_code=process.returncode,
            stderr=stderr,
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
            transient_error=transient,
        )
    if process.returncode != 0:
        return _result(
            status="process_error",
            attempts=1,
            exit_code=process.returncode,
            stderr=stderr,
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
        )

    mechanism = _invocation_mechanism(events, skill_name, skill_file)
    if role_config.effective_model is None or role_config.effective_thinking is None:
        return _result(
            status="invalid_output",
            attempts=1,
            exit_code=process.returncode,
            stderr=f"{stderr}\nPi emitted no complete effective model/thinking evidence",
            role_config=role_config,
            evaluation_cwd=evaluation_cwd,
            skill_name=skill_name,
            competing_skills=competing_skills,
            events=events,
            invocation_mechanism=mechanism,
        )
    return _result(
        status="triggered" if mechanism is not None else "not_triggered",
        attempts=1,
        exit_code=process.returncode,
        stderr=stderr,
        role_config=role_config,
        evaluation_cwd=evaluation_cwd,
        skill_name=skill_name,
        competing_skills=competing_skills,
        events=events,
        invocation_mechanism=mechanism,
    )


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    role_config: RoleModelConfig,
    competing_skills: tuple[str, ...] = (),
    pi_executable: str = "pi",
) -> TriggerInvocationResult:
    """Run one in-situ trigger query with one bounded transient retry."""
    if role_config.role != "trigger_consumer":
        raise RoleConfigurationError("trigger evaluation requires trigger_consumer role configuration")
    evaluation_path = Path(project_root)
    if not evaluation_path.is_absolute() or not evaluation_path.is_dir():
        raise ValueError("evaluation cwd must be an absolute existing directory")
    normalized_competitors = _normalize_competing_skills(competing_skills, skill_name)

    first = _run_query_attempt(
        query,
        skill_name,
        skill_description,
        timeout,
        os.fspath(evaluation_path),
        role_config,
        normalized_competitors,
        pi_executable,
    )
    if first.status != "model_error" or not first.transient_error:
        return first

    second = _run_query_attempt(
        query,
        skill_name,
        skill_description,
        timeout,
        os.fspath(evaluation_path),
        role_config,
        normalized_competitors,
        pi_executable,
    )
    second.attempts = 2
    second.attempt_statuses = (first.status, second.status)
    second.stderr = _bounded_stderr(f"{first.stderr}\n--- retry ---\n{second.stderr}")
    second.events = first.events + second.events
    return second


def _worker_error_result(
    error: Exception,
    *,
    role_config: RoleModelConfig,
    evaluation_cwd: str,
    skill_name: str,
    competing_skills: tuple[str, ...],
) -> TriggerInvocationResult:
    return _result(
        status="process_error",
        attempts=1,
        exit_code=None,
        stderr=f"worker {type(error).__name__}: {error}",
        role_config=role_config,
        evaluation_cwd=evaluation_cwd,
        skill_name=skill_name,
        competing_skills=competing_skills,
    )


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
    competing_skills: tuple[str, ...] = (),
    pi_executable: str = "pi",
) -> dict:
    """Run the full eval set and invalidate summaries on infrastructure results."""
    if role_config.role != "trigger_consumer":
        raise RoleConfigurationError("run_eval requires trigger_consumer role configuration")
    evaluation_cwd = os.fspath(project_root)
    normalized_competitors = _normalize_competing_skills(competing_skills, skill_name)
    results: list[dict] = []

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
                    evaluation_cwd,
                    role_config,
                    normalized_competitors,
                    pi_executable,
                )
                future_to_info[future] = (item, run_idx)

        query_invocations: dict[str, list[TriggerInvocationResult]] = {}
        query_items: dict[str, dict] = {}
        invocation_configs: list[RoleModelConfig] = []
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            query_invocations.setdefault(query, [])
            try:
                invocation = future.result()
            except Exception as error:
                invocation = _worker_error_result(
                    error,
                    role_config=role_config,
                    evaluation_cwd=evaluation_cwd,
                    skill_name=skill_name,
                    competing_skills=normalized_competitors,
                )
            query_invocations[query].append(invocation)
            invocation_configs.append(invocation.role_config)

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

    infrastructure_failures = 0
    for query, invocations in query_invocations.items():
        item = query_items[query]
        valid_invocations = [
            invocation for invocation in invocations if invocation.status in ACCURACY_STATUSES
        ]
        invalid_invocations = [
            invocation for invocation in invocations if invocation.status in INFRASTRUCTURE_STATUSES
        ]
        infrastructure_failures += len(invalid_invocations)
        query_is_valid = not invalid_invocations and len(valid_invocations) == runs_per_query
        trigger_count = sum(invocation.triggered for invocation in valid_invocations)
        trigger_rate = trigger_count / len(valid_invocations) if query_is_valid else None
        should_trigger = item["should_trigger"]
        did_pass = False
        if trigger_rate is not None:
            did_pass = (
                trigger_rate >= trigger_threshold
                if should_trigger
                else trigger_rate < trigger_threshold
            )
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": trigger_count,
                "runs": len(valid_invocations),
                "pass": did_pass,
                "valid": query_is_valid,
                "invocations": [invocation.as_dict() for invocation in invocations],
            }
        )

    passed = sum(1 for result in results if result["valid"] and result["pass"])
    failed = sum(1 for result in results if result["valid"] and not result["pass"])
    invalid = sum(1 for result in results if not result["valid"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "environment_profile": "in-situ",
        "evaluation_cwd": evaluation_cwd,
        "competing_skills": list(normalized_competitors),
        "pi_revision": PI_REVISION,
        "roles": {"trigger_consumer": role_config.as_metadata()},
        "results": results,
        "summary": {
            "valid": invalid == 0,
            "total": total,
            "passed": passed,
            "failed": failed,
            "invalid": invalid,
            "infrastructure_failures": infrastructure_failures,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--evaluation-cwd",
        required=True,
        help="Absolute project directory whose in-situ skill set is evaluated",
    )
    parser.add_argument(
        "--competing-skills",
        nargs="*",
        required=True,
        metavar="ABSOLUTE_SKILL_PATH",
        help="Explicit in-situ competing set (pass the option alone for an empty set)",
    )
    parser.add_argument("--pi-executable", default="pi", help="Pi executable")
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

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)
    evaluation_cwd = Path(args.evaluation_cwd)

    if not (skill_path / "SKILL.md").exists():
        parser.error(f"No SKILL.md found at {skill_path}")
    if not evaluation_cwd.is_absolute() or not evaluation_cwd.is_dir():
        parser.error("--evaluation-cwd must be an absolute existing directory")
    competing_skills = tuple(args.competing_skills)
    for competitor in competing_skills:
        competitor_path = Path(competitor)
        if not competitor_path.is_absolute() or not competitor_path.exists():
            parser.error("--competing-skills entries must be absolute existing paths")

    name, original_description, _content = parse_skill_md(skill_path)
    description = args.description or original_description

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=evaluation_cwd,
        role_config=role_config,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        competing_skills=competing_skills,
        pi_executable=args.pi_executable,
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
