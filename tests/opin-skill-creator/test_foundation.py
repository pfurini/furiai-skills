"""Foundation tests for the opin-skill-creator project harness."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from conftest import (
    COMMON_FIXTURES_ROOT,
    PI_REVISION,
    PI_SUBAGENTS_REVISION,
    SKILL_ROOT,
    TEST_ROOT,
    CheckoutContractError,
    find_repository_root,
    verify_checkout_revision,
)


def test_repository_root_resolution_is_independent_of_cwd(
    repository_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)

    assert find_repository_root(TEST_ROOT / "test_foundation.py") == repository_root
    assert SKILL_ROOT == repository_root / "skills/opin-skill-creator"
    assert TEST_ROOT == repository_root / "tests/opin-skill-creator"


def test_checkout_helper_requires_exact_root_and_revision(repository_root: Path) -> None:
    current_revision = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    assert (
        verify_checkout_revision(repository_root, current_revision, "fixture checkout")
        == repository_root
    )
    with pytest.raises(CheckoutContractError, match="exact checkout root"):
        verify_checkout_revision(
            repository_root / "skills", current_revision, "fixture checkout"
        )
    with pytest.raises(CheckoutContractError, match="revision mismatch"):
        verify_checkout_revision(repository_root, "f" * 40, "fixture checkout")


def test_shared_factories_construct_isolated_offline_inputs(
    tmp_path: Path,
    skill_factory: Callable[..., Path],
    campaign_factory: Callable[..., Path],
    jsonl_factory: Callable[..., Path],
    subprocess_outcome_factory: Callable[..., subprocess.CompletedProcess[str]],
) -> None:
    first_skill = skill_factory("first-skill", files={"references/example.md": "Example\n"})
    second_skill = skill_factory("second-skill")
    campaign = campaign_factory(
        skill_name="first-skill", campaign_id="foundation-1", repetitions=2
    )
    transcript = jsonl_factory(
        [{"type": "message", "text": "héllo"}, {"type": "agent_end"}]
    )
    outcome = subprocess_outcome_factory(
        args=("fixture-command", "--flag"),
        returncode=2,
        stdout="captured output\n",
        stderr="bounded error\n",
    )

    assert first_skill != second_skill
    assert first_skill.is_relative_to(tmp_path)
    assert second_skill.is_relative_to(tmp_path)
    assert (first_skill / "references/example.md").read_text(encoding="utf-8") == "Example\n"
    assert campaign.is_relative_to(tmp_path)
    assert (campaign / "campaign.json").is_file()
    assert (campaign / "trigger/final-test.json").is_file()
    for configuration in ("with_skill", "without_skill"):
        for run_number in (1, 2):
            run_root = (
                campaign
                / "iteration-1/sample-eval"
                / configuration
                / f"run-{run_number}"
            )
            assert (run_root / "outputs").is_dir()
            assert (run_root / "transcript.jsonl").is_file()
            assert (run_root / "run.json").is_file()

    assert transcript.read_bytes().endswith(b"\n")
    assert [json.loads(line) for line in transcript.read_text(encoding="utf-8").splitlines()] == [
        {"text": "héllo", "type": "message"},
        {"type": "agent_end"},
    ]
    assert outcome.args == ["fixture-command", "--flag"]
    assert outcome.returncode == 2
    assert outcome.stdout == "captured output\n"
    assert outcome.stderr == "bounded error\n"


def test_markers_are_registered(pytestconfig: pytest.Config) -> None:
    marker_lines = pytestconfig.getini("markers")

    assert any(line.startswith("contract:") for line in marker_lines)
    assert any(line.startswith("live:") for line in marker_lines)


def test_project_harness_stays_outside_distributable_skill(
    repository_root: Path, skill_root: Path
) -> None:
    assert COMMON_FIXTURES_ROOT.is_dir()
    assert TEST_ROOT.is_relative_to(repository_root)
    assert not TEST_ROOT.is_relative_to(skill_root)
    assert not (skill_root / "tests").exists()
    assert not (skill_root / "fixtures").exists()
    assert not (skill_root / ".skill-creator").exists()


@pytest.mark.contract
def test_contract_checkouts_match_pinned_revisions(
    pi_checkout: Path, pi_subagents_checkout: Path
) -> None:
    assert verify_checkout_revision(pi_checkout, PI_REVISION, "Pi checkout") == pi_checkout
    assert (
        verify_checkout_revision(
            pi_subagents_checkout, PI_SUBAGENTS_REVISION, "pi-subagents checkout"
        )
        == pi_subagents_checkout
    )
