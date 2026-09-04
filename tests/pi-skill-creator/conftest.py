"""Shared offline fixtures and pinned-checkout guards for pi-skill-creator tests."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any

import pytest

PI_REVISION = "a4043c1e332a61e4c8648b97b9b796c57f9db110"
PI_SUBAGENTS_REVISION = "7f569969445bf8bc6fbd7757f18db80b35de0ba9"
PI_DYNAMIC_WORKFLOWS_REVISION = "e9c5a41d9c4234df908aa25a2b49ee9648e896d4"


class CheckoutContractError(ValueError):
    """Raised when a supplied contract checkout violates the pinned contract."""


def find_repository_root(start: Path) -> Path:
    """Resolve the exact repository root from a path inside this checkout."""
    resolved = start.resolve()
    candidate = resolved.parent if resolved.is_file() else resolved
    for root in (candidate, *candidate.parents):
        if (
            (root / ".git").exists()
            and (root / "docs/pi-skill-creator-work-orders/contracts.md").is_file()
            and (root / "skills/pi-skill-creator").is_dir()
        ):
            return root
    raise RuntimeError(f"cannot resolve repository root from {start}")


TEST_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = find_repository_root(TEST_ROOT)
SKILL_ROOT = REPOSITORY_ROOT / "skills/pi-skill-creator"
COMMON_FIXTURES_ROOT = TEST_ROOT / "fixtures/common"


def verify_checkout_revision(path: Path, expected_revision: str, label: str) -> Path:
    """Validate an absolute, exact-root Git checkout at the required revision."""
    if not path.is_absolute():
        raise CheckoutContractError(f"{label} must be an absolute path: {path}")
    if not path.is_dir():
        raise CheckoutContractError(f"{label} is not a directory: {path}")

    try:
        root_result = subprocess.run(
            ["git", "-C", os.fspath(path), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        revision_result = subprocess.run(
            ["git", "-C", os.fspath(path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise CheckoutContractError(f"{label} is not a readable Git checkout: {path}") from error

    resolved_path = path.resolve()
    checkout_root = Path(root_result.stdout.strip()).resolve()
    if checkout_root != resolved_path:
        raise CheckoutContractError(
            f"{label} must name the exact checkout root: {resolved_path} != {checkout_root}"
        )

    actual_revision = revision_result.stdout.strip()
    if actual_revision != expected_revision:
        raise CheckoutContractError(
            f"{label} revision mismatch: expected {expected_revision}, got {actual_revision}"
        )
    return resolved_path


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "contract: requires the pinned local Pi, pi-subagents, and pi-dynamic-workflows checkouts",
    )
    config.addinivalue_line(
        "markers", "live: requires explicit opt-in and may use credentials or model calls"
    )


@pytest.fixture(scope="session")
def repository_root() -> Path:
    return REPOSITORY_ROOT


@pytest.fixture(scope="session")
def skill_root() -> Path:
    return SKILL_ROOT


@pytest.fixture(scope="session")
def contract_checkouts() -> dict[str, Path]:
    requirements = (
        ("PI_CHECKOUT", PI_REVISION, "Pi checkout"),
        ("PI_SUBAGENTS_CHECKOUT", PI_SUBAGENTS_REVISION, "pi-subagents checkout"),
    )
    missing = [name for name, _, _ in requirements if not os.environ.get(name)]
    if missing:
        pytest.skip("contract tests require " + " and ".join(missing))

    checkouts: dict[str, Path] = {}
    for name, revision, label in requirements:
        try:
            checkouts[name] = verify_checkout_revision(
                Path(os.environ[name]), revision, label
            )
        except CheckoutContractError as error:
            pytest.fail(str(error), pytrace=False)
    return checkouts


@pytest.fixture(scope="session")
def pi_checkout(contract_checkouts: dict[str, Path]) -> Path:
    return contract_checkouts["PI_CHECKOUT"]


@pytest.fixture(scope="session")
def pi_subagents_checkout(contract_checkouts: dict[str, Path]) -> Path:
    return contract_checkouts["PI_SUBAGENTS_CHECKOUT"]


@pytest.fixture(autouse=True)
def enforce_test_tier_contracts(request: pytest.FixtureRequest) -> None:
    if request.node.get_closest_marker("live") is not None:
        required_flags = ("PI_SKILL_CREATOR_LIVE_TESTS", "PI_SKILL_CREATOR_REPLAY_ONLY")
        missing_flags = [name for name in required_flags if os.environ.get(name) != "1"]
        if missing_flags:
            pytest.skip("live tests require " + " and ".join(f"{name}=1" for name in missing_flags))
    if request.node.get_closest_marker("contract") is not None:
        try:
            request.getfixturevalue("contract_checkouts")
        except CheckoutContractError as error:
            pytest.fail(str(error), pytrace=False)


@pytest.fixture
def skill_factory(tmp_path: Path) -> Callable[..., Path]:
    """Create isolated synthetic skill directories below pytest's temporary root."""
    skills_root = tmp_path / "skills"

    def create_skill(
        name: str = "example-skill",
        *,
        description: str = "A synthetic skill used by offline tests.",
        files: Mapping[str, str] | None = None,
    ) -> Path:
        root = skills_root / name
        root.mkdir(parents=True, exist_ok=False)
        (root / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
            encoding="utf-8",
        )
        for relative_name, content in (files or {}).items():
            destination = root / relative_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        return root

    return create_skill


@pytest.fixture
def jsonl_factory(tmp_path: Path) -> Callable[..., Path]:
    """Write strict UTF-8 JSONL with an LF after every record."""
    transcripts_root = tmp_path / "transcripts"

    def write_jsonl(
        records: Iterable[Mapping[str, Any]],
        *,
        name: str = "transcript.jsonl",
    ) -> Path:
        destination = transcripts_root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8", newline="\n") as stream:
            for record in records:
                stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
                stream.write("\n")
        return destination

    return write_jsonl


@pytest.fixture
def subprocess_outcome_factory() -> Callable[..., subprocess.CompletedProcess[str]]:
    """Construct deterministic subprocess outcomes without launching a process."""

    def create_outcome(
        *,
        args: Iterable[str] = ("fixture-command",),
        returncode: int = 0,
        stdout: str = "",
        stderr: str = "",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=list(args),
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    return create_outcome


@pytest.fixture
def campaign_factory(tmp_path: Path) -> Callable[..., Path]:
    """Create an isolated campaign tree matching the frozen workspace layout."""
    campaigns_root = tmp_path / "project/.skill-creator"

    def create_campaign(
        *,
        skill_name: str = "example-skill",
        campaign_id: str = "fixture-campaign",
        eval_name: str = "sample-eval",
        repetitions: int = 1,
        iteration: int = 1,
    ) -> Path:
        campaign_root = campaigns_root / skill_name / f"campaign-{campaign_id}"
        trigger_root = campaign_root / "trigger"
        trigger_root.mkdir(parents=True, exist_ok=False)

        skill_path = tmp_path / "deployment" / skill_name
        evaluation_cwd = tmp_path / "deployment"
        campaign = {
            "schema_version": "pi-skill-creator.campaign/v1",
            "campaign_id": campaign_id,
            "created_at": "2026-09-02T12:00:00Z",
            "repository_revision": "0" * 40,
            "pi_revision": PI_REVISION,
            "pi_subagents_revision": PI_SUBAGENTS_REVISION,
            "workflow_runtime": "pi-subagents",
            "workflow_runtime_revision": PI_SUBAGENTS_REVISION,
            "skill_name": skill_name,
            "skill_path": os.fspath(skill_path),
            "evaluation_cwd": os.fspath(evaluation_cwd),
            "environment_profile": "declared-dependencies",
            "declared_extensions": [],
            "treatment": "with_skill",
            "control": "without_skill",
            "repetitions": repetitions,
            "roles": {},
            "partitions": {
                "seed": 42,
                "train": "trigger/train.json",
                "validation": "trigger/validation.json",
                "final_test": "trigger/final-test.json",
            },
        }
        (campaign_root / "campaign.json").write_text(
            json.dumps(campaign, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (campaign_root / "evals.json").write_text("[]\n", encoding="utf-8")
        for name in ("train.json", "validation.json", "final-test.json", "results.json"):
            (trigger_root / name).write_text("[]\n", encoding="utf-8")

        eval_root = campaign_root / f"iteration-{iteration}" / eval_name
        for configuration in ("with_skill", "without_skill"):
            for run_number in range(1, repetitions + 1):
                run_root = eval_root / configuration / f"run-{run_number}"
                (run_root / "outputs").mkdir(parents=True)
                (run_root / "transcript.jsonl").write_text(
                    '{"type":"fixture"}\n', encoding="utf-8", newline="\n"
                )
                for name in (
                    "transcript-metrics.json",
                    "run.json",
                    "timing.json",
                    "grading.json",
                ):
                    (run_root / name).write_text("{}\n", encoding="utf-8")
        iteration_root = campaign_root / f"iteration-{iteration}"
        for name in ("benchmark.json", "feedback.json"):
            (iteration_root / name).write_text("{}\n", encoding="utf-8")
        (iteration_root / "benchmark.md").write_text("# Fixture benchmark\n", encoding="utf-8")
        (iteration_root / "viewer.pid").write_text("12345\n", encoding="utf-8")
        return campaign_root

    return create_campaign
