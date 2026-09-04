"""Regression tests for role-specific model and thinking configuration."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

from conftest import SKILL_ROOT

sys.path.insert(0, os.fspath(SKILL_ROOT))

from scripts import improve_description as improve_module  # noqa: E402
from scripts import run_eval as run_eval_module  # noqa: E402
from scripts import run_loop as run_loop_module  # noqa: E402
from scripts.run_eval import (  # noqa: E402
    RoleConfigurationError,
    RoleModelConfig,
    add_role_arguments,
    record_effective_from_event,
    role_config_from_args,
)


def test_trigger_consumer_and_optimizer_have_distinct_requested_effective_models(
    monkeypatch: pytest.MonkeyPatch,
    skill_factory: Any,
) -> None:
    trigger_config = RoleModelConfig(
        role="trigger_consumer",
        requested_model="provider/trigger-requested",
        requested_thinking="low",
    )
    optimizer_config = RoleModelConfig(
        role="optimizer",
        requested_model="provider/optimizer-requested",
        requested_thinking="high",
    )
    calls: list[tuple[str, str, str]] = []

    monkeypatch.setattr(run_loop_module, "find_project_root", lambda: Path.cwd())

    def fake_run_eval(**kwargs: Any) -> dict[str, Any]:
        config = kwargs["role_config"]
        calls.append((config.role, config.requested_model, config.requested_thinking))
        config.record_effective(
            model="provider/trigger-effective",
            thinking="minimal",
            evidence="pi_event",
        )
        passed = sum(role == "trigger_consumer" for role, _, _ in calls) > 1
        return {
            "results": [
                {
                    "query": "Create a skill",
                    "should_trigger": True,
                    "trigger_rate": 1.0 if passed else 0.0,
                    "triggers": 1 if passed else 0,
                    "runs": 1,
                    "pass": passed,
                }
            ],
            "summary": {
                "total": 1,
                "passed": 1 if passed else 0,
                "failed": 0 if passed else 1,
            },
        }

    def fake_improve_description(**kwargs: Any) -> str:
        config = kwargs["role_config"]
        calls.append((config.role, config.requested_model, config.requested_thinking))
        config.record_effective(
            model="provider/optimizer-effective",
            thinking="medium",
            evidence="pi_event",
        )
        return "Improved description"

    monkeypatch.setattr(run_loop_module, "run_eval", fake_run_eval)
    monkeypatch.setattr(run_loop_module, "improve_description", fake_improve_description)

    output = run_loop_module.run_loop(
        eval_set=[{"query": "Create a skill", "should_trigger": True}],
        skill_path=skill_factory("role-config-skill"),
        description_override=None,
        num_workers=1,
        timeout=1,
        max_iterations=2,
        runs_per_query=1,
        trigger_threshold=0.5,
        holdout=0,
        trigger_config=trigger_config,
        optimizer_config=optimizer_config,
        verbose=False,
    )

    assert calls == [
        ("trigger_consumer", "provider/trigger-requested", "low"),
        ("optimizer", "provider/optimizer-requested", "high"),
        ("trigger_consumer", "provider/trigger-requested", "low"),
    ]
    assert output["roles"] == {
        "trigger_consumer": {
            "requested_model": "provider/trigger-requested",
            "requested_thinking": "low",
            "effective_model": "provider/trigger-effective",
            "effective_thinking": "minimal",
            "model_source": "argument",
            "thinking_source": "argument",
            "effective_evidence": "pi_event",
        },
        "optimizer": {
            "requested_model": "provider/optimizer-requested",
            "requested_thinking": "high",
            "effective_model": "provider/optimizer-effective",
            "effective_thinking": "medium",
            "model_source": "argument",
            "thinking_source": "argument",
            "effective_evidence": "pi_event",
        },
    }


def test_role_cli_mapping_records_environment_defaults_without_model_alias() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    add_role_arguments(parser, "trigger_consumer")
    add_role_arguments(parser, "optimizer")

    args = parser.parse_args([])
    environ = {
        "PI_PROVIDER": "environment-provider",
        "PI_MODEL": "environment-model",
        "PI_REASONING_LEVEL": "medium",
        "PI_SKILL_CREATOR_OPTIMIZER_MODEL": "optimizer-provider/optimizer-model",
        "PI_SKILL_CREATOR_OPTIMIZER_THINKING": "high",
    }
    trigger = role_config_from_args(args, "trigger_consumer", environ=environ)
    optimizer = role_config_from_args(args, "optimizer", environ=environ)

    assert trigger.as_metadata() == {
        "requested_model": "environment-provider/environment-model",
        "requested_thinking": "medium",
        "effective_model": None,
        "effective_thinking": None,
        "model_source": "PI_PROVIDER+PI_MODEL",
        "thinking_source": "PI_REASONING_LEVEL",
        "effective_evidence": None,
    }
    assert optimizer.requested_model == "optimizer-provider/optimizer-model"
    assert optimizer.requested_thinking == "high"
    assert optimizer.model_source == "PI_SKILL_CREATOR_OPTIMIZER_MODEL"
    assert optimizer.thinking_source == "PI_SKILL_CREATOR_OPTIMIZER_THINKING"
    assert "--model" not in parser._option_string_actions


@pytest.mark.parametrize(
    ("role", "model", "thinking", "missing_flag"),
    [
        ("trigger_consumer", None, "low", "trigger-consumer-model"),
        ("trigger_consumer", "provider/trigger", None, "trigger-consumer-thinking"),
        ("optimizer", None, "high", "optimizer-model"),
        ("optimizer", "provider/optimizer", None, "optimizer-thinking"),
    ],
)
def test_missing_role_choices_fail_before_quantitative_execution(
    monkeypatch: pytest.MonkeyPatch,
    role: str,
    model: str | None,
    thinking: str | None,
    missing_flag: str,
) -> None:
    launched = False

    def forbidden_subprocess(*args: Any, **kwargs: Any) -> Any:
        nonlocal launched
        launched = True
        raise AssertionError("subprocess must not launch")

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", forbidden_subprocess)
    monkeypatch.setattr(improve_module.subprocess, "run", forbidden_subprocess)
    args = argparse.Namespace()
    setattr(args, f"{role}_model", model)
    setattr(args, f"{role}_thinking", thinking)

    with pytest.raises(RoleConfigurationError, match=missing_flag):
        role_config_from_args(args, role, environ={})  # type: ignore[arg-type]

    assert launched is False


def test_standalone_subprocesses_receive_explicit_role_model_and_thinking(
    monkeypatch: pytest.MonkeyPatch,
    subprocess_outcome_factory: Any,
) -> None:
    optimizer = RoleModelConfig(
        role="optimizer",
        requested_model="provider/optimizer-requested",
        requested_thinking="high",
    )
    event = {
        "type": "message_end",
        "effective_thinking": "medium",
        "message": {
            "role": "assistant",
            "provider": "provider",
            "model": "optimizer-requested",
            "responseModel": "optimizer-effective",
            "content": [
                {"type": "text", "text": "<new_description>Improved</new_description>"}
            ],
        },
    }
    outcome = subprocess_outcome_factory(
        stdout=json.dumps(event) + "\n",
    )
    captured_command: list[str] = []

    def fake_run(command: list[str], **kwargs: Any) -> Any:
        captured_command.extend(command)
        assert kwargs["input"] == "optimizer prompt"
        return outcome

    monkeypatch.setattr(improve_module.subprocess, "run", fake_run)

    response = improve_module._call_pi("optimizer prompt", optimizer)

    assert response == "<new_description>Improved</new_description>"
    assert captured_command == [
        "pi",
        "--mode",
        "json",
        "--no-session",
        "--model",
        "provider/optimizer-requested",
        "--thinking",
        "high",
    ]
    assert optimizer.effective_model == "provider/optimizer-effective"
    assert optimizer.effective_thinking == "medium"


def test_effective_values_are_never_copied_from_requested_values() -> None:
    config = RoleModelConfig(
        role="trigger_consumer",
        requested_model="provider/requested",
        requested_thinking="high",
    )

    record_effective_from_event(
        config,
        {
            "type": "message_end",
            "message": {
                "role": "assistant",
                "provider": "provider",
                "model": "resolved",
            },
        },
    )

    assert config.effective_model == "provider/resolved"
    assert config.effective_thinking is None
    assert config.effective_model != config.requested_model


def test_trigger_subprocess_receives_only_trigger_role_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_command: list[str] = []

    class FakeProcess:
        stdout = None

        def __init__(self, command: list[str], **kwargs: Any) -> None:
            captured_command.extend(command)

    monkeypatch.setattr(run_eval_module.subprocess, "Popen", FakeProcess)
    trigger = RoleModelConfig(
        role="trigger_consumer",
        requested_model="provider/trigger",
        requested_thinking="low",
    )

    result = run_eval_module.run_single_query(
        query="Create a skill",
        skill_name="sample",
        skill_description="Sample description",
        timeout=1,
        project_root=os.fspath(Path.cwd()),
        role_config=trigger,
    )

    assert result.triggered is False
    assert captured_command[-4:] == [
        "--model",
        "provider/trigger",
        "--thinking",
        "low",
    ]
