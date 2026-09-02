#!/usr/bin/env python3
"""Run one measured Pi prompt through the strict RPC protocol."""

from __future__ import annotations

import argparse
import json
import os
import queue
import re
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Never, cast

from scripts.transcript_metrics import TranscriptMetricsError, parse_transcript

EnvironmentProfile = Literal["in-situ", "hermetic-core", "declared-dependencies"]
Configuration = Literal["with_skill", "without_skill"]

PI_REVISION = "a4043c1e332a61e4c8648b97b9b796c57f9db110"
PI_VERSION = "0.84.4"
RPC_PROTOCOL_VERSION = 3
TRANSCRIPT_FORMAT = "pi-json-events-v3"

_PROFILES: tuple[EnvironmentProfile, ...] = (
    "in-situ",
    "hermetic-core",
    "declared-dependencies",
)
_CONFIGURATIONS: tuple[Configuration, ...] = ("with_skill", "without_skill")
_THINKING_LEVELS = ("off", "minimal", "low", "medium", "high", "xhigh", "max")
_IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
_MODEL = re.compile(r"[^/\s]+/[^\s]+\Z")
_PROMPT_REQUEST_ID = "rpc-prompt-1"
_STATE_REQUEST_ID = "rpc-state-1"
_STDERR_LIMIT = 2000
_DIALOG_METHODS = frozenset({"select", "confirm", "input", "editor"})
_NOTIFICATION_METHODS = frozenset(
    {"notify", "setStatus", "setWidget", "setTitle", "set_editor_text"}
)
_RESOURCE_ISOLATION_ARGS = (
    "--no-extensions",
    "--no-skills",
    "--no-prompt-templates",
    "--no-themes",
    "--no-context-files",
)


class RpcRunnerError(ValueError):
    """Raised when a measured RPC run cannot produce completed metadata."""

    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind
        self.transcript: bytes | None = None
        self.stderr = ""

    def attach_process_output(self, transcript: bytes, stderr: bytes) -> RpcRunnerError:
        """Attach captured diagnostics without exposing unbounded stderr."""
        self.transcript = transcript
        self.stderr = _bounded_text(stderr)
        return self


@dataclass(frozen=True)
class RunIdentity:
    """Stable campaign identity for one executor repetition."""

    campaign_id: str
    eval_id: int
    eval_name: str
    configuration: Configuration
    run_number: int


@dataclass(frozen=True)
class RpcRunConfig:
    """Explicit runtime and environment inputs for one RPC execution."""

    pi_executable: Path
    pi_checkout: Path
    evaluation_cwd: Path
    skill_path: Path
    run_dir: Path
    model: str
    thinking: str
    profile: EnvironmentProfile
    identity: RunIdentity
    extensions: tuple[Path, ...] = ()
    timeout_seconds: float = 300.0


@dataclass(frozen=True)
class _ProtocolResult:
    records: tuple[dict[str, Any], ...]
    state: dict[str, Any]
    stderr: str


def _bounded_text(raw: bytes) -> str:
    return raw[:_STDERR_LIMIT].decode("utf-8", errors="replace").replace("\x00", "")


def _json_object(raw: str, *, location: str) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise RpcRunnerError("protocol_error", f'{location} has duplicate key "{key}"')
            result[key] = value
        return result

    try:
        value = json.loads(raw, object_pairs_hook=unique_object)
    except RpcRunnerError:
        raise
    except (json.JSONDecodeError, ValueError) as error:
        raise RpcRunnerError("protocol_error", f"{location} is malformed JSON: {error}") from error
    if not isinstance(value, dict):
        raise RpcRunnerError("protocol_error", f"{location} must be a JSON object")
    return cast(dict[str, Any], value)


def _absolute(path: Path, *, label: str, kind: str) -> Path:
    if not path.is_absolute():
        raise RpcRunnerError("invalid_input", f"{label} must be an absolute path")
    resolved = path.resolve()
    if kind == "directory" and not resolved.is_dir():
        raise RpcRunnerError("invalid_input", f"{label} is not a directory: {resolved}")
    if kind == "file" and not resolved.is_file():
        raise RpcRunnerError("invalid_input", f"{label} is not a file: {resolved}")
    return resolved


def _validate_config(config: RpcRunConfig) -> RpcRunConfig:
    executable = _absolute(config.pi_executable, label="Pi executable", kind="file")
    if not os.access(executable, os.X_OK):
        raise RpcRunnerError("invalid_input", f"Pi executable is not executable: {executable}")
    checkout = _absolute(config.pi_checkout, label="Pi checkout", kind="directory")
    cwd = _absolute(config.evaluation_cwd, label="evaluation cwd", kind="directory")
    skill = _absolute(config.skill_path, label="skill path", kind="directory")
    if not config.run_dir.is_absolute():
        raise RpcRunnerError("invalid_input", "run directory must be an absolute path")
    run_dir = config.run_dir.resolve()

    identity = config.identity
    for value, label in (
        (identity.campaign_id, "campaign id"),
        (identity.eval_name, "eval name"),
    ):
        if _IDENTIFIER.fullmatch(value) is None:
            raise RpcRunnerError("invalid_input", f"{label} is invalid: {value!r}")
    if identity.eval_id < 1 or identity.run_number < 1:
        raise RpcRunnerError("invalid_input", "eval id and run number must be positive")
    if identity.configuration not in _CONFIGURATIONS:
        raise RpcRunnerError("invalid_input", "configuration is unsupported")
    if _MODEL.fullmatch(config.model) is None:
        raise RpcRunnerError("invalid_input", "model must use provider/model form")
    if config.thinking not in _THINKING_LEVELS:
        raise RpcRunnerError("invalid_input", "thinking level is unsupported")
    if config.profile not in _PROFILES:
        raise RpcRunnerError("invalid_input", "environment profile is unsupported")
    if not isinstance(config.timeout_seconds, (int, float)) or config.timeout_seconds <= 0:
        raise RpcRunnerError("invalid_input", "timeout must be positive")

    extensions = tuple(
        _absolute(path, label=f"extension {index}", kind="file")
        for index, path in enumerate(config.extensions, start=1)
    )
    if config.profile == "declared-dependencies" and not extensions:
        raise RpcRunnerError(
            "invalid_input", "declared-dependencies requires at least one absolute extension"
        )
    if config.profile != "declared-dependencies" and extensions:
        raise RpcRunnerError(
            "invalid_input", f"{config.profile} does not accept declared extensions"
        )

    return RpcRunConfig(
        pi_executable=executable,
        pi_checkout=checkout,
        evaluation_cwd=cwd,
        skill_path=skill,
        run_dir=run_dir,
        model=config.model,
        thinking=config.thinking,
        profile=config.profile,
        identity=identity,
        extensions=extensions,
        timeout_seconds=float(config.timeout_seconds),
    )


def _command_output(command: list[str], *, label: str) -> str:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RpcRunnerError("invalid_runtime", f"cannot inspect {label}: {error}") from error
    if result.returncode != 0:
        detail = _bounded_text(result.stderr).strip()
        raise RpcRunnerError(
            "invalid_runtime", f"cannot inspect {label}" + (f": {detail}" if detail else "")
        )
    return result.stdout.decode("utf-8", errors="strict").strip()


def validate_runtime(config: RpcRunConfig) -> None:
    """Verify the explicit executable and immutable Pi checkout contract."""
    version = _command_output([os.fspath(config.pi_executable), "--version"], label="Pi executable")
    if version != PI_VERSION:
        raise RpcRunnerError(
            "invalid_runtime", f"Pi version mismatch: expected {PI_VERSION}, got {version}"
        )
    revision = _command_output(
        ["git", "-C", os.fspath(config.pi_checkout), "rev-parse", "HEAD"],
        label="Pi checkout",
    )
    if revision != PI_REVISION:
        raise RpcRunnerError(
            "invalid_runtime", f"Pi revision mismatch: expected {PI_REVISION}, got {revision}"
        )


def profile_arguments(config: RpcRunConfig) -> list[str]:
    """Return resource flags that implement the selected environment profile."""
    arguments: list[str] = []
    if config.profile != "in-situ":
        arguments.extend(_RESOURCE_ISOLATION_ARGS)
    if config.identity.configuration == "with_skill":
        arguments.extend(("--skill", os.fspath(config.skill_path)))
    if config.profile == "declared-dependencies":
        for extension in config.extensions:
            arguments.extend(("-e", os.fspath(extension)))
    return arguments


def build_pi_command(config: RpcRunConfig) -> list[str]:
    """Build a prompt-free Pi RPC command from explicit absolute inputs."""
    return [
        os.fspath(config.pi_executable),
        "--mode",
        "rpc",
        "--no-session",
        "--model",
        config.model,
        "--thinking",
        config.thinking,
        *profile_arguments(config),
    ]


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=2)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()


def _parse_protocol_line(line: bytes, *, line_number: int) -> dict[str, Any]:
    if not line.endswith(b"\n"):
        raise RpcRunnerError(
            "protocol_error", f"RPC stdout line {line_number} is not terminated by LF"
        )
    payload = line[:-1]
    if payload.endswith(b"\r"):
        payload = payload[:-1]
    if not payload:
        raise RpcRunnerError("protocol_error", f"RPC stdout line {line_number} is empty")
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise RpcRunnerError(
            "protocol_error", f"RPC stdout line {line_number} is not strict UTF-8: {error}"
        ) from error
    return _json_object(text, location=f"RPC stdout line {line_number}")


def _read_rpc_process(
    command: list[str], *, cwd: Path, prompt: str, timeout_seconds: float
) -> tuple[bytes, int, bytes]:
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as error:
        raise RpcRunnerError("process_error", f"cannot launch Pi: {error}") from error
    if process.stdin is None or process.stdout is None or process.stderr is None:
        _terminate_process(process)
        raise RpcRunnerError("process_error", "Pi subprocess pipes are unavailable")

    stdout_lines: list[bytes] = []
    stderr_chunks: list[bytes] = []
    stdout_queue: queue.Queue[bytes | None] = queue.Queue()

    def read_stdout() -> None:
        assert process.stdout is not None
        while True:
            line = process.stdout.readline()
            if not line:
                break
            stdout_lines.append(line)
            stdout_queue.put(line)
        stdout_queue.put(None)

    def read_stderr() -> None:
        assert process.stderr is not None
        while True:
            chunk = process.stderr.read(8192)
            if not chunk:
                break
            stderr_chunks.append(chunk)

    stdout_thread = threading.Thread(target=read_stdout, daemon=True)
    stderr_thread = threading.Thread(target=read_stderr, daemon=True)
    stdout_thread.start()
    stderr_thread.start()

    state_command = {"id": _STATE_REQUEST_ID, "type": "get_state"}
    prompt_command = {"id": _PROMPT_REQUEST_ID, "type": "prompt", "message": prompt}
    request = (
        json.dumps(state_command, ensure_ascii=False, separators=(",", ":"))
        + "\n"
        + json.dumps(prompt_command, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    try:
        process.stdin.write(request)
        process.stdin.flush()
    except (BrokenPipeError, OSError) as error:
        _terminate_process(process)
        stdout_thread.join(timeout=2)
        stderr_thread.join(timeout=2)
        detail = _bounded_text(b"".join(stderr_chunks)).strip()
        raise RpcRunnerError(
            "process_error", f"Pi closed stdin before accepting the request: {detail or error}"
        ) from error

    deadline = time.monotonic() + timeout_seconds
    prompt_accepted = False
    final_agent_end = False
    protocol_error: RpcRunnerError | None = None
    line_number = 0
    while not final_agent_end:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            _terminate_process(process)
            protocol_error = RpcRunnerError("timeout", "Pi RPC run timed out")
            break
        try:
            line = stdout_queue.get(timeout=remaining)
        except queue.Empty:
            _terminate_process(process)
            protocol_error = RpcRunnerError("timeout", "Pi RPC run timed out")
            break
        if line is None:
            break
        line_number += 1
        try:
            record = _parse_protocol_line(line, line_number=line_number)
            record_type = record.get("type")
            if record_type == "response" and record.get("id") == _PROMPT_REQUEST_ID:
                if record.get("command") != "prompt" or record.get("success") is not True:
                    message = record.get("error", "prompt was rejected")
                    raise RpcRunnerError("protocol_error", f"Pi rejected the prompt: {message}")
                prompt_accepted = True
            elif record_type == "extension_ui_request":
                method = record.get("method")
                if method in _DIALOG_METHODS:
                    raise RpcRunnerError(
                        "ui_dialog", f"automated RPC run requested UI dialog method {method}"
                    )
                if method not in _NOTIFICATION_METHODS:
                    raise RpcRunnerError(
                        "ui_dialog", f"automated RPC run requested unknown UI method {method!r}"
                    )
            elif record_type == "agent_end":
                if not prompt_accepted:
                    raise RpcRunnerError(
                        "protocol_error", "agent_end arrived before prompt acceptance"
                    )
                will_retry = record.get("willRetry")
                if not isinstance(will_retry, bool):
                    raise RpcRunnerError("protocol_error", "agent_end.willRetry must be boolean")
                final_agent_end = not will_retry
        except RpcRunnerError as error:
            protocol_error = error
            _terminate_process(process)
            break

    if final_agent_end and process.poll() is None:
        process.stdin.close()
        try:
            process.wait(timeout=max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            _terminate_process(process)
            protocol_error = RpcRunnerError("timeout", "Pi did not exit after agent_end")
    elif process.poll() is None:
        _terminate_process(process)

    stdout_thread.join(timeout=2)
    stderr_thread.join(timeout=2)
    stdout = b"".join(stdout_lines)
    stderr = b"".join(stderr_chunks)
    returncode = process.returncode if process.returncode is not None else -1

    if protocol_error is not None:
        raise protocol_error.attach_process_output(stdout, stderr)
    if returncode != 0:
        detail = _bounded_text(stderr).strip()
        raise RpcRunnerError(
            "process_error", f"Pi exited with status {returncode}" + (f": {detail}" if detail else "")
        ).attach_process_output(stdout, stderr)
    if not final_agent_end:
        detail = _bounded_text(stderr).strip()
        raise RpcRunnerError(
            "process_error", "Pi exited before final agent_end" + (f": {detail}" if detail else "")
        ).attach_process_output(stdout, stderr)
    return stdout, returncode, stderr


def _validate_protocol(stdout: bytes, *, stderr: bytes) -> _ProtocolResult:
    parts = stdout.split(b"\n")
    if not parts or parts == [b""]:
        raise RpcRunnerError("protocol_error", "Pi RPC stdout contains no records")
    if parts[-1] != b"":
        raise RpcRunnerError("protocol_error", "final RPC stdout record is not terminated by LF")
    records = tuple(
        _parse_protocol_line(line + b"\n", line_number=index)
        for index, line in enumerate(parts[:-1], start=1)
    )

    state: dict[str, Any] | None = None
    accepted = False
    final_end = False
    for record in records:
        record_type = record.get("type")
        if record_type == "response":
            record_id = record.get("id")
            if record_id == _STATE_REQUEST_ID:
                if record.get("command") != "get_state" or record.get("success") is not True:
                    raise RpcRunnerError("invalid_runtime", "Pi get_state request failed")
                data = record.get("data")
                if not isinstance(data, dict):
                    raise RpcRunnerError("invalid_runtime", "Pi get_state response has no state")
                state = cast(dict[str, Any], data)
            elif record_id == _PROMPT_REQUEST_ID:
                if record.get("command") != "prompt" or record.get("success") is not True:
                    raise RpcRunnerError("protocol_error", "Pi prompt request was not accepted")
                accepted = True
            else:
                raise RpcRunnerError(
                    "protocol_error", f"Pi returned an unknown response id: {record_id!r}"
                )
        elif record_type == "extension_ui_request":
            method = record.get("method")
            if method in _DIALOG_METHODS or method not in _NOTIFICATION_METHODS:
                raise RpcRunnerError("ui_dialog", f"unsupported RPC UI request: {method!r}")
        elif record_type == "extension_error":
            raise RpcRunnerError(
                "process_error", f"Pi extension error: {record.get('error', 'unknown error')}"
            )
        elif record_type == "message_end":
            message = record.get("message")
            if isinstance(message, dict) and message.get("role") == "assistant":
                if message.get("stopReason") in {"error", "aborted"}:
                    raise RpcRunnerError(
                        "model_error", f"assistant stopped with {message.get('stopReason')}"
                    )
        elif record_type == "agent_end" and record.get("willRetry") is False:
            final_end = True

    if state is None:
        raise RpcRunnerError("invalid_runtime", "Pi emitted no matching get_state response")
    if not accepted or not final_end:
        raise RpcRunnerError("protocol_error", "Pi emitted an incomplete prompt lifecycle")
    return _ProtocolResult(records=records, state=state, stderr=_bounded_text(stderr))


def _effective_thinking(state: dict[str, Any]) -> str:
    thinking = state.get("thinkingLevel")
    if not isinstance(thinking, str) or thinking not in _THINKING_LEVELS:
        raise RpcRunnerError("invalid_runtime", "Pi state has no effective thinking level")
    model = state.get("model")
    if not isinstance(model, dict):
        raise RpcRunnerError("invalid_runtime", "Pi state has no effective model")
    provider = model.get("provider")
    model_id = model.get("id")
    if not isinstance(provider, str) or not provider or not isinstance(model_id, str) or not model_id:
        raise RpcRunnerError("invalid_runtime", "Pi state effective model is incomplete")
    return thinking


def _write_json(path: Path, value: dict[str, Any]) -> None:
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ) + "\n"
    path.write_text(serialized, encoding="utf-8", newline="\n")


def run_rpc(prompt: str, config: RpcRunConfig) -> dict[str, Any]:
    """Execute one prompt and write transcript, metrics, then completed run metadata."""
    if not isinstance(prompt, str) or not prompt:
        raise RpcRunnerError("invalid_input", "prompt must be a non-empty string")
    validated = _validate_config(config)
    validated.run_dir.mkdir(parents=True, exist_ok=True)
    (validated.run_dir / "outputs").mkdir(exist_ok=True)
    transcript_path = validated.run_dir / "transcript.jsonl"
    metrics_path = validated.run_dir / "transcript-metrics.json"
    run_path = validated.run_dir / "run.json"
    for stale_path in (run_path, metrics_path, transcript_path):
        stale_path.unlink(missing_ok=True)
    validate_runtime(validated)

    try:
        stdout, _, stderr = _read_rpc_process(
            build_pi_command(validated),
            cwd=validated.evaluation_cwd,
            prompt=prompt,
            timeout_seconds=validated.timeout_seconds,
        )
    except RpcRunnerError as error:
        if error.transcript is not None:
            transcript_path.write_bytes(error.transcript)
        raise
    transcript_path.write_bytes(stdout)
    protocol = _validate_protocol(stdout, stderr=stderr)
    effective_thinking = _effective_thinking(protocol.state)
    try:
        metrics = parse_transcript(transcript_path, source_format=TRANSCRIPT_FORMAT)
    except TranscriptMetricsError as error:
        raise RpcRunnerError("invalid_output", str(error)) from error
    effective_models = metrics.get("effective_models")
    if not isinstance(effective_models, list) or len(effective_models) != 1:
        raise RpcRunnerError(
            "invalid_output", "completed executor transcript must have exactly one effective model"
        )
    effective_model = effective_models[0]
    if not isinstance(effective_model, str) or _MODEL.fullmatch(effective_model) is None:
        raise RpcRunnerError("invalid_output", "effective model is invalid")

    _write_json(metrics_path, metrics)
    identity = validated.identity
    run = {
        "schema_version": "opin.run/v1",
        "campaign_id": identity.campaign_id,
        "eval_id": identity.eval_id,
        "eval_name": identity.eval_name,
        "configuration": identity.configuration,
        "run_number": identity.run_number,
        "environment_profile": validated.profile,
        "status": "completed",
        "role": "executor",
        "requested_model": validated.model,
        "effective_model": effective_model,
        "requested_thinking": validated.thinking,
        "effective_thinking": effective_thinking,
        "transcript_format": TRANSCRIPT_FORMAT,
        "transcript_path": "transcript.jsonl",
        "metrics_path": "transcript-metrics.json",
        "outputs_dir": "outputs",
    }
    _write_json(run_path, run)
    return run


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        _print_error(message)
        raise SystemExit(2)


def _print_error(error: object) -> None:
    message = " ".join(str(error).splitlines())
    encoded = f"error: {message}".encode("utf-8", errors="replace")[:_STDERR_LIMIT]
    print(encoded.decode("utf-8", errors="ignore"), file=sys.stderr)


def _arguments() -> argparse.Namespace:
    parser = _ArgumentParser(description="Run one measured Pi RPC prompt")
    parser.add_argument("--pi-executable", required=True, type=Path)
    parser.add_argument("--pi-checkout", required=True, type=Path)
    parser.add_argument("--evaluation-cwd", required=True, type=Path)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--thinking", required=True, choices=_THINKING_LEVELS)
    parser.add_argument("--profile", required=True, choices=_PROFILES)
    parser.add_argument("--extension", action="append", default=[], type=Path)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--eval-id", required=True, type=int)
    parser.add_argument("--eval-name", required=True)
    parser.add_argument("--configuration", required=True, choices=_CONFIGURATIONS)
    parser.add_argument("--run-number", required=True, type=int)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    prompt = sys.stdin.read()
    config = RpcRunConfig(
        pi_executable=args.pi_executable,
        pi_checkout=args.pi_checkout,
        evaluation_cwd=args.evaluation_cwd,
        skill_path=args.skill_path,
        run_dir=args.run_dir,
        model=args.model,
        thinking=args.thinking,
        profile=args.profile,
        identity=RunIdentity(
            campaign_id=args.campaign_id,
            eval_id=args.eval_id,
            eval_name=args.eval_name,
            configuration=args.configuration,
            run_number=args.run_number,
        ),
        extensions=tuple(args.extension),
        timeout_seconds=args.timeout_seconds,
    )
    try:
        run_rpc(prompt, config)
    except RpcRunnerError as error:
        _print_error(error)
        return 2 if error.kind in {"invalid_input", "invalid_runtime", "protocol_error", "invalid_output"} else 1
    except OSError as error:
        _print_error(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
