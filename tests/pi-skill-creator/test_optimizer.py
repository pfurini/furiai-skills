"""Regression tests for deterministic description optimization methodology."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

from conftest import SKILL_ROOT

sys.path.insert(0, os.fspath(SKILL_ROOT))

from scripts import generate_report as report_module  # noqa: E402
from scripts import improve_description as improve_module  # noqa: E402
from scripts import run_loop as loop_module  # noqa: E402
from scripts.run_eval import RoleModelConfig  # noqa: E402


def _role(role: str) -> RoleModelConfig:
    return RoleModelConfig(
        role=role,
        requested_model=f"provider/{role}",
        requested_thinking="high",
    )


def _eval_set(per_class: int = 6) -> list[dict[str, Any]]:
    return [
        {"query": f"positive-{index}", "should_trigger": True}
        for index in range(per_class)
    ] + [
        {"query": f"negative-{index}", "should_trigger": False}
        for index in range(per_class)
    ]


def _passing_results(eval_set: list[dict[str, Any]]) -> dict[str, Any]:
    results = [
        {
            "query": item["query"],
            "should_trigger": item["should_trigger"],
            "trigger_rate": 1.0 if item["should_trigger"] else 0.0,
            "triggers": 1 if item["should_trigger"] else 0,
            "runs": 1,
            "pass": True,
        }
        for item in eval_set
    ]
    return {
        "results": results,
        "summary": {"passed": len(results), "failed": 0, "total": len(results)},
    }


def test_hidden_skill_skips_and_final_test_runs_once_after_selection(
    monkeypatch: pytest.MonkeyPatch,
    skill_factory: Any,
    tmp_path: Path,
) -> None:
    calls: list[list[str]] = []

    def fake_run_eval(**kwargs: Any) -> dict[str, Any]:
        queries = kwargs["eval_set"]
        calls.append([item["query"] for item in queries])
        result = _passing_results(queries)
        # Keep the loop running so candidate selection has a real tie to break.
        result["results"][0]["pass"] = False
        result["summary"] = {
            "passed": len(queries) - 1,
            "failed": 1,
            "total": len(queries),
        }
        return result

    monkeypatch.setattr(loop_module, "find_project_root", lambda: Path.cwd())
    monkeypatch.setattr(loop_module, "run_eval", fake_run_eval)
    monkeypatch.setattr(
        loop_module,
        "improve_description",
        lambda **kwargs: f"Candidate {kwargs['iteration'] + 1}",
    )

    hidden_skill = skill_factory("hidden-skill")
    hidden_skill.joinpath("SKILL.md").write_text(
        "---\n"
        "name: hidden-skill\n"
        "description: Clear human-facing summary.\n"
        "disable-model-invocation: true\n"
        "---\n\n# Hidden skill\n",
        encoding="utf-8",
    )
    hidden = loop_module.run_loop(
        eval_set=_eval_set(),
        skill_path=hidden_skill,
        description_override=None,
        num_workers=1,
        timeout=1,
        max_iterations=3,
        runs_per_query=1,
        trigger_threshold=0.5,
        holdout=0.4,
        trigger_config=_role("trigger_consumer"),
        optimizer_config=_role("optimizer"),
        verbose=False,
    )

    assert calls == []
    assert hidden["optimization_skipped"] is True
    assert hidden["validation"] == {
        "kind": "human_readability",
        "status": "passed",
        "checks": {
            "non_empty": True,
            "single_line": True,
            "within_character_limit": True,
            "no_angle_brackets": True,
        },
    }

    campaign_path = tmp_path / "campaign-visible"
    visible = loop_module.run_loop(
        eval_set=_eval_set(),
        skill_path=skill_factory("visible-skill"),
        description_override=None,
        num_workers=1,
        timeout=1,
        max_iterations=3,
        runs_per_query=1,
        trigger_threshold=0.5,
        holdout=0.4,
        trigger_config=_role("trigger_consumer"),
        optimizer_config=_role("optimizer"),
        verbose=False,
        results_dir=campaign_path,
    )

    assert [len(query_set) for query_set in calls] == [10, 10, 10, 2]
    assert visible["partition_counts"] == {
        "train": 8,
        "validation": 2,
        "final_test": 2,
    }
    assert visible["best_description"] == "A synthetic skill used by offline tests."
    assert visible["final_test_call_count"] == 1
    assert visible["final_test_results"]["summary"]["total"] == 2
    assert all("final_test" not in str(item) for item in visible["history"])
    assert len(json.loads((campaign_path / "trigger/train.json").read_text())) == 8
    assert len(json.loads((campaign_path / "trigger/validation.json").read_text())) == 2
    assert len(json.loads((campaign_path / "trigger/final-test.json").read_text())) == 2
    assert json.loads((campaign_path / "trigger/results.json").read_text()) == visible


def test_partitioning_is_stratified_deterministic_and_validates_class_size() -> None:
    first = loop_module.partition_eval_set(_eval_set(), holdout=0.4, seed=42)
    second = loop_module.partition_eval_set(_eval_set(), holdout=0.4, seed=42)

    assert first == second
    train, validation, final_test = first
    assert [len(train), len(validation), len(final_test)] == [8, 2, 2]
    for partition in first:
        assert {item["should_trigger"] for item in partition} == {True, False}

    with pytest.raises(ValueError, match="at least 3 examples per class"):
        loop_module.partition_eval_set(_eval_set(per_class=2), holdout=0.4)


@pytest.mark.parametrize(
    "validation_passes,train_passes,expected_iteration",
    [
        ([1, 2, 2], [4, 3, 4], 3),
        ([2, 2, 2], [4, 4, 4], 1),
    ],
)
def test_candidate_selection_has_deterministic_tie_breaking(
    validation_passes: list[int],
    train_passes: list[int],
    expected_iteration: int,
) -> None:
    history = [
        {
            "iteration": index + 1,
            "validation_passed": validation_passes[index],
            "train_passed": train_passes[index],
        }
        for index in range(3)
    ]

    assert loop_module.select_best_candidate(history)["iteration"] == expected_iteration


def test_optimizer_prompt_uses_capability_first_third_person_doctrine(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    prompts: list[str] = []
    transcript_history: list[dict[str, Any]] = []

    def fake_call(prompt: str, role_config: RoleModelConfig, timeout: int = 300) -> str:
        prompts.append(prompt)
        return "<new_description>Creates focused test descriptions.</new_description>"

    monkeypatch.setattr(improve_module, "_call_pi", fake_call)
    improve_module.improve_description(
        skill_name="example-skill",
        skill_content="# Example",
        current_description="Old description",
        eval_results={"results": [], "summary": {"passed": 0, "failed": 0, "total": 0}},
        history=[
            {
                "description": "Prior",
                "train_passed": 1,
                "train_total": 2,
                "test_passed": 99,
                "test_total": 100,
            }
        ],
        role_config=_role("optimizer"),
        test_results={
            "results": [],
            "summary": {"passed": 98, "failed": 2, "total": 100},
        },
        log_dir=tmp_path,
        iteration=1,
        transcript_history=transcript_history,
    )

    prompt = prompts[0]
    assert "Capability first, in one clause" in prompt
    assert "Third person" in prompt
    assert "one trigger phrase per distinct invocation branch" in prompt
    assert "State what the skill does and when it applies, not how it works" in prompt
    assert 'imperative -- "Use this skill for"' not in prompt
    assert "99/100" not in prompt
    assert "98/100" not in prompt
    transcript = json.loads((tmp_path / "improve_iter_1.json").read_text())
    assert transcript["prompt"] == prompt
    assert transcript["final_description"] == "Creates focused test descriptions."
    assert transcript_history == [transcript]


def test_generate_report_empty_history_does_not_raise_value_error() -> None:
    output = report_module.generate_html(
        {
            "history": [],
            "original_description": "Original",
            "best_description": "Original",
            "iterations_run": 0,
        },
        skill_name="example-skill",
    )

    assert "No optimization iterations were run." in output
    assert "<tbody>" in output


def test_cli_defaults_to_no_report_and_persists_to_explicit_campaign_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    skill_factory: Any,
) -> None:
    eval_path = tmp_path / "evals.json"
    eval_path.write_text(json.dumps(_eval_set()), encoding="utf-8")
    campaign_path = tmp_path / "campaign-example"
    captured: dict[str, Any] = {}
    output = {
        "history": [],
        "best_description": "Description",
        "partition_counts": {"train": 8, "validation": 2, "final_test": 2},
    }

    def fake_run_loop(**kwargs: Any) -> dict[str, Any]:
        captured.update(kwargs)
        return output

    monkeypatch.setattr(loop_module, "run_loop", fake_run_loop)
    monkeypatch.setattr(
        loop_module.webbrowser,
        "open",
        lambda *_args, **_kwargs: pytest.fail("the default CLI must not open a browser"),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_loop.py",
            "--eval-set",
            os.fspath(eval_path),
            "--skill-path",
            os.fspath(skill_factory("cli-skill")),
            "--trigger-consumer-model",
            "provider/trigger",
            "--trigger-consumer-thinking",
            "low",
            "--optimizer-model",
            "provider/optimizer",
            "--optimizer-thinking",
            "high",
            "--results-dir",
            os.fspath(campaign_path),
        ],
    )

    loop_module.main()

    assert captured["live_report_path"] is None
    assert captured["results_dir"] == campaign_path
    assert json.loads((campaign_path / "trigger/results.json").read_text()) == output
