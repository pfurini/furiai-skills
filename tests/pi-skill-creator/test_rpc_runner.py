"""Contract and regression tests for measured Pi RPC execution."""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from conftest import PI_REVISION, SKILL_ROOT, TEST_ROOT

sys.path.insert(0, os.fspath(SKILL_ROOT))

from scripts.rpc_runner import (  # noqa: E402
    PI_REVISION as RUNNER_PI_REVISION,
    PI_VERSION,
    RPC_PROTOCOL_VERSION,
    TRANSCRIPT_FORMAT,
    RpcRunConfig,
    RpcRunnerError,
    RunIdentity,
    _parse_protocol_line,
    build_pi_command,
    profile_arguments,
    run_rpc,
    validate_runtime,
)

SUPERSEDED_PI_REVISION = "a4043c1e332a61e4c8648b97b9b796c57f9db110"
REPINNED_PI_REVISION = "db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee"

RPC_FIXTURES = TEST_ROOT / "fixtures/rpc"


def _config(
    tmp_path: Path,
    *,
    pi_executable: Path | None = None,
    pi_checkout: Path | None = None,
    profile: str = "hermetic-core",
    extensions: tuple[Path, ...] = (),
) -> RpcRunConfig:
    evaluation_cwd = tmp_path / "evaluation"
    evaluation_cwd.mkdir(exist_ok=True)
    skill_path = tmp_path / "skills/example-skill"
    skill_path.mkdir(parents=True, exist_ok=True)
    (skill_path / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Fixture.\ncontext: fork\n---\n\n# Fixture\n",
        encoding="utf-8",
    )
    executable = pi_executable or _fake_pi(tmp_path)
    checkout = pi_checkout or tmp_path
    return RpcRunConfig(
        pi_executable=executable,
        pi_checkout=checkout,
        evaluation_cwd=evaluation_cwd,
        skill_path=skill_path,
        run_dir=tmp_path / "run",
        model="openrouter/auto",
        thinking="high",
        profile=profile,  # type: ignore[arg-type]
        identity=RunIdentity(
            campaign_id="rpc-fixture-1",
            eval_id=1,
            eval_name="forked-skill-dispatch",
            configuration="with_skill",
            run_number=1,
        ),
        extensions=extensions,
        timeout_seconds=2,
    )


def _fake_pi(tmp_path: Path) -> Path:
    destination = tmp_path / "fake-pi"
    shutil.copyfile(RPC_FIXTURES / "fake_pi.py", destination)
    for fixture in RPC_FIXTURES.glob("*.jsonl"):
        shutil.copyfile(fixture, tmp_path / fixture.name)
    destination.chmod(destination.stat().st_mode | stat.S_IXUSR)
    return destination


def _patch_runtime_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("scripts.rpc_runner.validate_runtime", lambda _config: None)


def test_protocol_fixture_preserves_unicode_separators_and_authoritative_usage() -> None:
    raw = (RPC_FIXTURES / "success.jsonl").read_bytes()
    lines = raw.split(b"\n")

    assert len(lines) == 10
    assert "separator and text" in lines[3].decode("utf-8")
    records = [
        _parse_protocol_line(line + b"\n", line_number=index)
        for index, line in enumerate(lines[:-1], start=1)
    ]
    assert records[0]["id"] == "rpc-state-1"
    assert records[1]["id"] == "rpc-prompt-1"
    assert records[-1] == {"messages": [], "type": "agent_end", "willRetry": False}
    assert RPC_PROTOCOL_VERSION == 3
    assert TRANSCRIPT_FORMAT == "pi-json-events-v3"


@pytest.mark.parametrize("profile", ["in-situ", "hermetic-core", "declared-dependencies"])
def test_profile_commands_are_explicit_and_do_not_pass_a_prompt(
    tmp_path: Path, profile: str
) -> None:
    extension = tmp_path / "pi-subagents/src/index.ts"
    extension.parent.mkdir(parents=True)
    extension.write_text("export {};\n", encoding="utf-8")
    extensions = (extension,) if profile == "declared-dependencies" else ()
    config = _config(tmp_path, profile=profile, extensions=extensions)

    command = build_pi_command(config)

    assert command[:4] == [os.fspath(config.pi_executable), "--mode", "rpc", "--no-session"]
    assert "-p" not in command
    assert "--print" not in command
    assert "--skill" in command
    assert os.fspath(config.skill_path) in command
    if profile == "in-situ":
        assert "--no-context-files" not in command
        assert "--no-extensions" not in command
    else:
        for flag in (
            "--no-extensions",
            "--no-skills",
            "--no-prompt-templates",
            "--no-themes",
            "--no-context-files",
        ):
            assert flag in command
    if profile == "declared-dependencies":
        assert command[-2:] == ["-e", os.fspath(extension)]
    else:
        assert "-e" not in command


def test_control_arm_keeps_the_real_skill_path_out_of_model_resources(tmp_path: Path) -> None:
    config = _config(tmp_path)
    control = replace(
        config,
        identity=replace(config.identity, configuration="without_skill"),
    )

    command = build_pi_command(control)

    assert "--skill" not in command
    assert os.fspath(control.skill_path) not in command
    assert "--no-skills" in command


def test_declared_dependencies_rejects_missing_or_relative_extensions(tmp_path: Path) -> None:
    config = _config(tmp_path, profile="declared-dependencies")
    with pytest.raises(RpcRunnerError, match="requires at least one"):
        run_rpc("prompt", config)

    relative = replace(config, extensions=(Path("relative-extension.ts"),))
    with pytest.raises(RpcRunnerError, match="absolute"):
        run_rpc("prompt", relative)


def test_success_writes_transcript_metrics_then_completed_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_runtime_validation(monkeypatch)
    request_path = tmp_path / "requests.jsonl"
    args_path = tmp_path / "args.json"
    monkeypatch.setenv("FAKE_PI_INPUT", os.fspath(request_path))
    monkeypatch.setenv("FAKE_PI_ARGS", os.fspath(args_path))
    config = _config(tmp_path)

    run = run_rpc("-leading @query with   and  ", config)

    requests = [
        json.loads(line)
        for line in request_path.read_text(encoding="utf-8").split("\n")
        if line
    ]
    assert requests == [
        {"id": "rpc-state-1", "type": "get_state"},
        {"id": "rpc-prompt-1", "type": "prompt", "message": "-leading @query with   and  "},
    ]
    command = json.loads(args_path.read_text(encoding="utf-8"))
    assert "-leading @query" not in command
    assert command[command.index("--skill") + 1] == os.fspath(config.skill_path)

    transcript = config.run_dir / "transcript.jsonl"
    metrics_path = config.run_dir / "transcript-metrics.json"
    run_path = config.run_dir / "run.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert transcript.read_bytes() == (RPC_FIXTURES / "success.jsonl").read_bytes()
    assert metrics["tool_calls"] == {"skill": 1}
    assert metrics["usage"] == {
        "cache_read": 50,
        "cache_write": 4,
        "cost_usd": pytest.approx(0.0033),
        "input": 100,
        "output": 20,
        "reasoning": 5,
        "total_tokens": 179,
    }
    assert run == json.loads(run_path.read_text(encoding="utf-8"))
    assert run["effective_model"] == "openrouter/anthropic/claude-opus-4.1"
    assert run["effective_thinking"] == "high"
    assert run["requested_model"] == "openrouter/auto"
    assert run["transcript_format"] == "pi-json-events-v3"
    assert (config.run_dir / "outputs").is_dir()

    # The benchmark's execute stage will not dispatch grading until timing.json is durable,
    # and aggregate_benchmark reads total_duration_seconds from it for every run.
    timing = json.loads((config.run_dir / "timing.json").read_text(encoding="utf-8"))
    assert set(timing) == {"total_duration_seconds"}
    duration = timing["total_duration_seconds"]
    assert isinstance(duration, float) and not isinstance(duration, bool)
    assert math.isfinite(duration) and duration >= 0


@pytest.mark.parametrize(
    ("scenario", "kind", "message"),
    [
        ("dialog", "ui_dialog", "dialog"),
        ("rejected", "protocol_error", "rejected"),
        ("malformed", "protocol_error", "malformed JSON"),
        ("process-error", "process_error", "status 7"),
    ],
)
def test_failed_rpc_never_writes_completed_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    scenario: str,
    kind: str,
    message: str,
) -> None:
    _patch_runtime_validation(monkeypatch)
    monkeypatch.setenv("FAKE_PI_SCENARIO", scenario)
    config = _config(tmp_path)

    with pytest.raises(RpcRunnerError, match=message) as raised:
        run_rpc("fixture prompt", config)

    assert raised.value.kind == kind
    assert (config.run_dir / "transcript.jsonl").is_file()
    assert not (config.run_dir / "run.json").exists()
    assert not (config.run_dir / "transcript-metrics.json").exists()


def test_timeout_terminates_process_group_without_run_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_runtime_validation(monkeypatch)
    monkeypatch.setenv("FAKE_PI_SCENARIO", "timeout")
    config = replace(_config(tmp_path), timeout_seconds=0.1)

    with pytest.raises(RpcRunnerError, match="timed out") as raised:
        run_rpc("fixture prompt", config)

    assert raised.value.kind == "timeout"
    assert (config.run_dir / "transcript.jsonl").is_file()
    assert not (config.run_dir / "run.json").exists()


def test_run_directory_refuses_a_second_measured_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One run directory is at most one measured executor call (OSC-18)."""
    _patch_runtime_validation(monkeypatch)
    args_path = tmp_path / "args.json"
    monkeypatch.setenv("FAKE_PI_ARGS", os.fspath(args_path))
    config = _config(tmp_path)

    first = run_rpc("first measured call", config)
    run_path = config.run_dir / "run.json"
    transcript_path = config.run_dir / "transcript.jsonl"
    recorded_run = run_path.read_bytes()
    recorded_transcript = transcript_path.read_bytes()
    args_path.unlink()

    with pytest.raises(RpcRunnerError, match=re.escape(os.fspath(config.run_dir.resolve()))) as raised:
        run_rpc("second measured call", config)

    assert raised.value.kind == "invalid_input"
    assert not args_path.exists(), "no Pi process may launch into a used run directory"
    assert run_path.read_bytes() == recorded_run
    assert transcript_path.read_bytes() == recorded_transcript
    assert first == json.loads(run_path.read_text(encoding="utf-8"))

    # A failed run leaves transcript.jsonl behind, so its directory is refused on retry too.
    failed_dir = tmp_path / "failed-run"
    failed_dir.mkdir()
    (failed_dir / "transcript.jsonl").write_bytes(b'{"type":"fixture"}\n')
    with pytest.raises(RpcRunnerError, match="transcript.jsonl") as refused:
        run_rpc("retry into a failed directory", replace(config, run_dir=failed_dir))
    assert refused.value.kind == "invalid_input"
    assert not args_path.exists()
    assert not (failed_dir / "run.json").exists()


def test_cli_refuses_run_directory_with_existing_run_json(
    skill_root: Path, tmp_path: Path
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "run.json").write_text("{}\n", encoding="utf-8")
    args_path = tmp_path / "args.json"
    evaluation_cwd = tmp_path / "evaluation"
    evaluation_cwd.mkdir()
    skill_path = tmp_path / "skills/example-skill"
    skill_path.mkdir(parents=True)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.rpc_runner",
            "--pi-executable",
            os.fspath(_fake_pi(tmp_path)),
            "--pi-checkout",
            os.fspath(tmp_path),
            "--evaluation-cwd",
            os.fspath(evaluation_cwd),
            "--skill-path",
            os.fspath(skill_path),
            "--run-dir",
            os.fspath(run_dir),
            "--model",
            "provider/model",
            "--thinking",
            "low",
            "--profile",
            "hermetic-core",
            "--campaign-id",
            "cli-1",
            "--eval-id",
            "1",
            "--eval-name",
            "cli-eval",
            "--configuration",
            "without_skill",
            "--run-number",
            "1",
        ],
        cwd=skill_root,
        env={**os.environ, "FAKE_PI_ARGS": os.fspath(args_path)},
        input="fixture prompt",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.count("\n") == 1
    assert "run.json" in result.stderr and os.fspath(run_dir.resolve()) in result.stderr
    assert len(result.stderr.encode()) <= 2048
    assert not args_path.exists(), "the CLI must refuse before launching Pi"
    assert (run_dir / "run.json").read_text(encoding="utf-8") == "{}\n"


def test_rpc_runner_refuses_the_superseded_pi_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """OSC-18 re-pins Pi; the superseded revision is refused as `invalid_runtime`."""
    assert RUNNER_PI_REVISION == REPINNED_PI_REVISION
    assert RUNNER_PI_REVISION == PI_REVISION, "conftest and the runner must agree on the pin"
    assert PI_VERSION == "0.84.4"
    config = _config(tmp_path)

    def fake_output(revision: str):
        def _command_output(command: list[str], *, label: str) -> str:
            if command[1:] == ["--version"]:
                return PI_VERSION
            assert command[:2] == ["git", "-C"] and command[-2:] == ["rev-parse", "HEAD"]
            return revision

        return _command_output

    monkeypatch.setattr("scripts.rpc_runner._command_output", fake_output(SUPERSEDED_PI_REVISION))
    with pytest.raises(RpcRunnerError, match="Pi revision mismatch") as raised:
        validate_runtime(config)
    assert raised.value.kind == "invalid_runtime"
    assert REPINNED_PI_REVISION in str(raised.value)
    assert SUPERSEDED_PI_REVISION in str(raised.value)

    monkeypatch.setattr("scripts.rpc_runner._command_output", fake_output(REPINNED_PI_REVISION))
    validate_runtime(config)


def test_cli_requires_all_absolute_inputs_and_reads_prompt_from_stdin(
    skill_root: Path, tmp_path: Path
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.rpc_runner",
            "--pi-executable",
            "relative-pi",
            "--pi-checkout",
            os.fspath(tmp_path),
            "--evaluation-cwd",
            os.fspath(tmp_path),
            "--skill-path",
            os.fspath(tmp_path),
            "--run-dir",
            os.fspath(tmp_path / "run"),
            "--model",
            "provider/model",
            "--thinking",
            "low",
            "--profile",
            "hermetic-core",
            "--campaign-id",
            "cli-1",
            "--eval-id",
            "1",
            "--eval-name",
            "cli-eval",
            "--configuration",
            "without_skill",
            "--run-number",
            "1",
        ],
        cwd=skill_root,
        input="-leading @prompt",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "absolute" in result.stderr
    assert len(result.stderr.encode()) <= 2048


@pytest.mark.contract
def test_rpc_preserves_fork_mode_and_captures_effective_telemetry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    pi_checkout: Path,
    pi_subagents_checkout: Path,
) -> None:
    supplied_executable = Path(os.environ.get("PI_EXECUTABLE", ""))
    assert supplied_executable.is_absolute() and os.access(supplied_executable, os.X_OK)
    version = subprocess.run(
        [os.fspath(supplied_executable), "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert version.stdout.strip() == "0.84.4"
    assert subprocess.run(
        ["git", "-C", os.fspath(pi_checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip() == PI_REVISION

    session_source = (pi_checkout / "packages/coding-agent/src/core/agent-session.ts").read_text(
        encoding="utf-8"
    )
    rpc_source = (pi_checkout / "packages/coding-agent/src/modes/rpc/rpc-mode.ts").read_text(
        encoding="utf-8"
    )
    resource_source = (pi_checkout / "packages/coding-agent/src/core/resource-loader.ts").read_text(
        encoding="utf-8"
    )
    protocol_source = (pi_subagents_checkout / "src/cross-extension-rpc.ts").read_text(
        encoding="utf-8"
    )
    assert 'mode: "rpc"' in rpc_source
    assert "export const PROTOCOL_VERSION = 3;" in protocol_source
    degrade = session_source.split("private async _shouldDegradeFork", 1)[1].split(
        "return undefined", 1
    )[0]
    assert 'this._extensionMode === "print" || this._extensionMode === "json"' in degrade
    assert 'this._extensionMode === "rpc"' not in degrade
    assert "? this.mergePaths(cliEnabledSkills, this.additionalSkillPaths)" in resource_source

    extension = pi_subagents_checkout / "src/index.ts"
    request_path = tmp_path / "requests.jsonl"
    monkeypatch.setenv("FAKE_PI_INPUT", os.fspath(request_path))
    config = _config(
        tmp_path,
        pi_executable=_fake_pi(tmp_path),
        pi_checkout=pi_checkout,
        profile="declared-dependencies",
        extensions=(extension,),
    )

    run = run_rpc("Invoke the fork-context example-skill.", config)

    command = build_pi_command(config)
    assert command[:4] == [os.fspath(config.pi_executable), "--mode", "rpc", "--no-session"]
    assert command[-2:] == ["-e", os.fspath(extension)]
    assert "--no-extensions" in command
    assert "--no-skills" in command
    assert profile_arguments(config).count("-e") == 1
    assert json.loads(request_path.read_text(encoding="utf-8").splitlines()[1])["type"] == "prompt"
    assert run["effective_model"] == "openrouter/anthropic/claude-opus-4.1"
    assert run["effective_thinking"] == "high"
    metrics = json.loads((config.run_dir / "transcript-metrics.json").read_text(encoding="utf-8"))
    assert metrics["tool_calls"] == {"skill": 1}


def test_rpc_runtime_has_no_sdk_typescript_or_managed_policy_dependency() -> None:
    source = (SKILL_ROOT / "scripts/rpc_runner.py").read_text(encoding="utf-8")
    lowered = source.lower()
    assert "typescript" not in lowered
    assert "@earendil-works" not in lowered
    assert "managed-policy" not in lowered
    assert not list((SKILL_ROOT / "scripts").glob("*.ts"))
