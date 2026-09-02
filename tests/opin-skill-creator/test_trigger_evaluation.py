"""Regression tests for reliable in-situ trigger evaluation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from conftest import PI_REVISION, SKILL_ROOT

sys.path.insert(0, os.fspath(SKILL_ROOT))

from scripts import run_eval as run_eval_module  # noqa: E402
from scripts.run_eval import RoleModelConfig  # noqa: E402


FIXTURE_ROOT = Path(__file__).parent / "fixtures/trigger"
STATUS_CASES = json.loads((FIXTURE_ROOT / "status-cases.json").read_text(encoding="utf-8"))


def _config() -> RoleModelConfig:
    return RoleModelConfig(
        role="trigger_consumer",
        requested_model="fixture/requested-trigger",
        requested_thinking="low",
    )


def _stdout(case: dict[str, Any]) -> str:
    if "stdout_file" in case:
        return (FIXTURE_ROOT / case["stdout_file"]).read_text(encoding="utf-8")
    return "".join(json.dumps(event) + "\n" for event in case["events"])


class FakeProcess:
    def __init__(
        self,
        command: list[str],
        outcome: subprocess.CompletedProcess[str],
        *,
        timeout: bool = False,
    ) -> None:
        self.command = command
        self.outcome = outcome
        self.returncode = outcome.returncode
        self.stdin = object()
        self.stdout = object()
        self.stderr = object()
        self.timeout = timeout
        self.killed = False
        self.received_input: str | None = None

    def communicate(
        self,
        input: str | None = None,
        timeout: int | None = None,
    ) -> tuple[str, str]:
        self.received_input = input
        if self.timeout and input is not None and not self.killed:
            raise subprocess.TimeoutExpired(
                self.command,
                timeout,
                output=self.outcome.stdout,
                stderr=self.outcome.stderr,
            )
        return self.outcome.stdout, self.outcome.stderr

    def kill(self) -> None:
        self.killed = True

    def poll(self) -> int | None:
        return self.returncode

    def wait(self) -> int:
        return self.returncode


def test_real_name_explicit_cwd_and_infrastructure_status_are_preserved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    evaluation_cwd = (FIXTURE_ROOT / "alternate-cwd").resolve()
    competitor = (evaluation_cwd / ".agents/skills/competing-skill").resolve()
    duplicate = (FIXTURE_ROOT / "duplicate-target").resolve()
    real_target = (FIXTURE_ROOT / "real-target").resolve()
    skill_name, skill_description, _ = run_eval_module.parse_skill_md(real_target)
    captured: dict[str, Any] = {}
    stderr = "discarded-prefix-" + "x" * 5000 + "-diagnostic-tail"

    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        captured.update(command=command, kwargs=kwargs)
        candidate_path = Path(command[command.index("--skill", command.index("--no-skills")) + 1])
        captured["candidate_path"] = candidate_path
        captured["candidate_text"] = candidate_path.read_text(encoding="utf-8")
        outcome = subprocess.CompletedProcess(command, 17, stdout="", stderr=stderr)
        process = FakeProcess(command, outcome)
        captured["process"] = process
        return process

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)

    result = run_eval_module.run_single_query(
        query="- preserve leading punctuation",
        skill_name=skill_name,
        skill_description=skill_description,
        timeout=3,
        project_root=os.fspath(evaluation_cwd),
        role_config=_config(),
        competing_skills=(os.fspath(competitor), os.fspath(duplicate)),
    )

    command = captured["command"]
    assert result.status == "process_error"
    assert result.triggered is False
    assert result.exit_code == 17
    assert result.attempts == 1
    assert result.stderr.endswith("-diagnostic-tail")
    assert len(result.stderr) <= run_eval_module.MAX_STDERR_CHARS
    assert result.skill_name == "real-trigger-skill"
    assert result.evaluation_cwd == os.fspath(evaluation_cwd)
    assert result.environment_profile == "in-situ"
    assert result.pi_revision == PI_REVISION
    assert result.competing_skills == (os.fspath(competitor),)
    assert result.invocation_mechanism is None
    assert captured["kwargs"]["cwd"] == os.fspath(evaluation_cwd)
    assert captured["process"].received_input == "- preserve leading punctuation"
    assert "-p" not in command
    assert "--no-skills" in command
    assert os.fspath(competitor) in command
    assert os.fspath(duplicate) not in command
    assert "name: real-trigger-skill" in captured["candidate_text"]
    assert "eval-skill-" not in captured["candidate_text"]


@pytest.mark.parametrize(
    "expected_status",
    ["triggered", "not_triggered", "process_error", "model_error", "auth_error", "invalid_output"],
)
def test_closed_statuses_are_classified_from_complete_process_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    expected_status: str,
) -> None:
    case = STATUS_CASES[expected_status]

    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        outcome = subprocess.CompletedProcess(
            command,
            case["returncode"],
            stdout=_stdout(case),
            stderr=case["stderr"],
        )
        return FakeProcess(command, outcome)

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)
    result = run_eval_module.run_single_query(
        "fixture query",
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )

    assert result.status == expected_status
    assert result.triggered is (expected_status == "triggered")
    assert result.events == tuple(case.get("events", ()))
    assert set(result.as_dict()) >= {
        "status",
        "attempts",
        "exit_code",
        "stderr",
        "requested_model",
        "effective_model",
        "requested_thinking",
        "effective_thinking",
        "environment_profile",
        "evaluation_cwd",
        "skill_name",
        "competing_skills",
        "pi_revision",
        "events",
        "invocation_mechanism",
    }


def test_timeout_is_not_a_non_trigger_and_keeps_bounded_diagnostics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        outcome = subprocess.CompletedProcess(
            command,
            0,
            stdout='{"type":"fixture"}\n',
            stderr="timed out",
        )
        return FakeProcess(command, outcome, timeout=True)

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)
    result = run_eval_module.run_single_query(
        "fixture query",
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )

    assert result.status == "timeout"
    assert result.triggered is False
    assert result.exit_code is None
    assert result.stderr == "timed out"
    assert result.events == ({"type": "fixture"},)


def test_skill_file_read_is_recorded_as_direct_invocation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        candidate = Path(command[command.index("--skill") + 1])
        events = [
            {"type": "tool_execution_start", "toolName": "read", "args": {"path": os.fspath(candidate)}},
            {
                "type": "message_end",
                "effective_thinking": "low",
                "message": {
                    "role": "assistant",
                    "provider": "fixture",
                    "responseModel": "effective-trigger",
                    "content": [],
                },
            },
        ]
        outcome = subprocess.CompletedProcess(
            command,
            0,
            stdout="".join(json.dumps(event) + "\n" for event in events),
            stderr="",
        )
        return FakeProcess(command, outcome)

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)
    result = run_eval_module.run_single_query(
        "fixture query",
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )

    assert result.status == "triggered"
    assert result.invocation_mechanism == "skill_md_read"


@pytest.mark.parametrize("query", json.loads((FIXTURE_ROOT / "leading-queries.json").read_text()))
def test_queries_use_stdin_and_never_follow_print_flag(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    query: str,
) -> None:
    captured: dict[str, Any] = {}

    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        captured.update(command=command, kwargs=kwargs)
        case = STATUS_CASES["not_triggered"]
        outcome = subprocess.CompletedProcess(command, 0, _stdout(case), "")
        process = FakeProcess(command, outcome)
        captured["process"] = process
        return process

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)
    run_eval_module.run_single_query(
        query,
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )

    assert captured["process"].received_input == query
    assert "-p" not in captured["command"]
    assert query not in captured["command"]


def test_only_explicit_transient_provider_errors_retry_once(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    outcomes = [
        subprocess.CompletedProcess([], 1, "", "rate limit: retryable=true"),
        subprocess.CompletedProcess([], 1, "", "rate limit: retryable=true"),
    ]
    calls = 0

    def fake_popen(command: list[str], **kwargs: Any) -> FakeProcess:
        nonlocal calls
        outcome = outcomes[calls]
        calls += 1
        return FakeProcess(command, outcome)

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", fake_popen)
    result = run_eval_module.run_single_query(
        "fixture query",
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )

    assert result.status == "model_error"
    assert result.attempts == 2
    assert calls == 2

    calls = 0
    outcomes[:] = [subprocess.CompletedProcess([], 1, "", "model provider rejected request")]
    result = run_eval_module.run_single_query(
        "fixture query",
        "real-trigger-skill",
        "Fixture description",
        1,
        os.fspath(tmp_path.resolve()),
        _config(),
    )
    assert result.status == "model_error"
    assert result.attempts == 1
    assert calls == 1


def test_infrastructure_status_invalidates_summary_and_worker_exception_is_process_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class ImmediateFuture:
        def __init__(self, function: Any, args: tuple[Any, ...]) -> None:
            try:
                self.value = function(*args)
                self.error: Exception | None = None
            except Exception as error:  # pragma: no branch - exercised by the fixture
                self.value = None
                self.error = error

        def result(self) -> Any:
            if self.error is not None:
                raise self.error
            return self.value

    class InlineExecutor:
        def __init__(self, **kwargs: Any) -> None:
            pass

        def __enter__(self) -> InlineExecutor:
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def submit(self, function: Any, *args: Any) -> ImmediateFuture:
            return ImmediateFuture(function, args)

    def exploding_worker(*args: Any) -> Any:
        raise RuntimeError("fixture worker exception")

    monkeypatch.setattr(run_eval_module, "ProcessPoolExecutor", InlineExecutor)
    monkeypatch.setattr(run_eval_module, "as_completed", lambda futures: futures)
    monkeypatch.setattr(run_eval_module, "run_single_query", exploding_worker)

    output = run_eval_module.run_eval(
        eval_set=[{"query": "fixture query", "should_trigger": True}],
        skill_name="real-trigger-skill",
        description="Fixture description",
        num_workers=1,
        timeout=1,
        project_root=tmp_path.resolve(),
        role_config=_config(),
    )

    assert output["summary"] == {
        "valid": False,
        "total": 1,
        "passed": 0,
        "failed": 0,
        "invalid": 1,
        "infrastructure_failures": 1,
    }
    assert output["results"][0]["trigger_rate"] is None
    assert output["results"][0]["pass"] is False
    assert output["results"][0]["valid"] is False
    assert output["results"][0]["invocations"][0]["status"] == "process_error"
