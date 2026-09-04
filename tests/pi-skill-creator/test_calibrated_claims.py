"""Human-reviewed calibration claim and model-pin contracts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest

from conftest import SKILL_ROOT

README_PATH = SKILL_ROOT / "README.md"
RUNTIME_DOCUMENTS = (
    SKILL_ROOT / "SKILL.md",
    *sorted((SKILL_ROOT / "agents").glob("*.md")),
    *sorted((SKILL_ROOT / "references").glob("*.md")),
)
CALIBRATION_REVIEW_SCHEMA = "pi-skill-creator.calibration-review/v1"
ACCEPTED_MACHINERY_CLAIM = (
    "The pi-skill-creator benchmark machinery runs end to end on workflow runtime "
    "pi-subagents at the revisions recorded in campaign.json: setup, two measured RPC "
    "executor processes, two gradings, validation, aggregation, one blind comparison, "
    "and the static viewer export all completed and produced their durable records."
)
POLICY_PINS = {
    "benchmark-analyzer.md": ("openai-codex/gpt-5.6-terra", "medium"),
    "comparator.md": ("claude-bridge/claude-opus-5", "high"),
    "comparison-analyzer.md": ("openai-codex/gpt-5.6-sol", "high"),
    "grader.md": ("openai-codex/gpt-5.6-sol", "high"),
}
RESULT_NUMBER = re.compile(
    r"(?:"
    r"\b\d+(?:\.\d+)?\s*%"
    r"|\b\d+(?:\.\d+)?\s*/\s*\d+"
    r"|\b\d+(?:\.\d+)?\s+of\s+\d+"
    r"|\b\d+\s+(?:reps?|runs?)\b"
    r"|\b\d+(?:\.\d+)?\s+vs\.?\s+\d+(?:\.\d+)?\b"
    r")",
    re.IGNORECASE,
)
CALIBRATED_PI_MODEL = re.compile(
    r"(?:\bcalibrated\b[^.\n]{0,80}\bPi model\b|\bPi model\b[^.\n]{0,80}\bcalibrated\b)",
    re.IGNORECASE,
)


def _frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    block = text.split("---\n", 2)[1]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def _required_path(variable: str) -> Path:
    value = os.environ.get(variable)
    assert value, f"{variable} must name an absolute path"
    path = Path(value)
    assert path.is_absolute(), f"{variable} must name an absolute path: {path}"
    assert path.exists(), f"{variable} does not exist: {path}"
    return path


def _review_data() -> tuple[Path, Path, dict[str, Any]]:
    campaign_dir = _required_path("PI_SKILL_CREATOR_CAMPAIGN_DIR")
    review_path = _required_path("PI_SKILL_CREATOR_HUMAN_REVIEW")
    assert campaign_dir.is_dir(), f"campaign directory is not a directory: {campaign_dir}"
    assert review_path.is_file(), f"review record is not a file: {review_path}"
    return campaign_dir, review_path, json.loads(review_path.read_text(encoding="utf-8"))


def _section_labels(path: Path) -> list[tuple[int, str, str]]:
    """Return result lines with their level-two heading and opening sentence."""
    heading = ""
    opening_lines: list[str] = []
    opening_complete = False
    findings: list[tuple[int, str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## ") and not line.startswith("### "):
            heading = line[3:].strip()
            opening_lines = []
            opening_complete = False
            continue
        if heading and not opening_complete and line.strip():
            opening_lines.append(line.strip())
            if "." in line:
                opening_complete = True
        if RESULT_NUMBER.search(line):
            opening_sentence = " ".join(opening_lines).split(".", 1)[0]
            findings.append((line_number, heading, opening_sentence))
    return findings


def test_every_number_is_labelled_historical_or_absent() -> None:
    documents = (
        README_PATH,
        SKILL_ROOT / "SKILL.md",
        *sorted((SKILL_ROOT / "references").glob("*.md")),
    )
    unlabelled: list[str] = []
    for path in documents:
        for line_number, heading, opening_sentence in _section_labels(path):
            if "historical" not in heading.lower() and "historical" not in opening_sentence.lower():
                unlabelled.append(f"{path.relative_to(SKILL_ROOT)}:{line_number}")
    assert not unlabelled, "result-shaped numbers lack a historical section label: " + ", ".join(unlabelled)


@pytest.mark.contract
def test_agent_pins_resolve_without_a_model_call() -> None:
    executable_value = os.environ.get("PI_EXECUTABLE")
    if not executable_value:
        pytest.skip("PI_EXECUTABLE is unset; model-pin resolution was not requested")
    executable = Path(executable_value)
    assert executable.is_absolute(), f"PI_EXECUTABLE must be absolute: {executable}"
    assert executable.is_file(), f"PI_EXECUTABLE is not a file: {executable}"

    for agent_name, (pin, _) in POLICY_PINS.items():
        provider, model_id = pin.split("/", 1)
        try:
            result = subprocess.run(
                [os.fspath(executable), "--list-models", pin],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            pytest.fail(f"could not resolve {agent_name} pin {pin}: {error}", pytrace=False)
        rows = [line.split() for line in result.stdout.splitlines()]
        assert any(len(row) >= 2 and row[0] == provider and row[1] == model_id for row in rows), (
            f"{agent_name} pin did not resolve to an exact provider/model row: {pin}"
        )


def test_review_record_is_smoke_scoped_and_record_backed() -> None:
    campaign_dir, _, review = _review_data()
    assert review.get("schema_version") == CALIBRATION_REVIEW_SCHEMA
    assert Path(review.get("campaign_dir", "")).resolve() == campaign_dir.resolve()

    campaign = json.loads((campaign_dir / "campaign.json").read_text(encoding="utf-8"))
    assert review.get("campaign_id") == campaign.get("campaign_id")

    records = review.get("records")
    assert isinstance(records, dict) and records
    for relative_path, expected_hash in records.items():
        assert isinstance(relative_path, str) and relative_path
        assert isinstance(expected_hash, str) and re.fullmatch(r"[0-9a-f]{64}", expected_hash)
        record_path = campaign_dir / relative_path
        assert record_path.is_file(), f"reviewed campaign record is missing: {relative_path}"
        actual_hash = hashlib.sha256(record_path.read_bytes()).hexdigest()
        assert actual_hash == expected_hash, f"reviewed campaign record changed: {relative_path}"

    accepted_claims = review.get("accepted_claims")
    assert accepted_claims in ([], [ACCEPTED_MACHINERY_CLAIM])

    accepted_pins = review.get("accepted_pins")
    assert isinstance(accepted_pins, list)
    for entry in accepted_pins:
        assert isinstance(entry, dict), "accepted pin entries must name their supporting record"
        record_path = entry.get("record_path")
        assert isinstance(record_path, str) and record_path in records
        assert (campaign_dir / record_path).is_file()

    rejected_claims = review.get("rejected_claims")
    assert isinstance(rejected_claims, list)
    for entry in rejected_claims:
        assert isinstance(entry, dict)
        assert isinstance(entry.get("claim"), str) and entry["claim"].strip()
        assert isinstance(entry.get("rationale"), str) and entry["rationale"].strip()


def test_runtime_documents_carry_no_unreviewed_pin_or_claim() -> None:
    skill_frontmatter = _frontmatter(SKILL_ROOT / "SKILL.md")
    assert "model" not in skill_frontmatter
    assert "effort" not in skill_frontmatter

    accepted_models: set[str] = set()
    review_path = os.environ.get("PI_SKILL_CREATOR_HUMAN_REVIEW")
    if review_path:
        review = json.loads(Path(review_path).read_text(encoding="utf-8"))
        for entry in review.get("accepted_pins", []):
            if isinstance(entry, dict):
                model = entry.get("model") or entry.get("pin")
                if isinstance(model, str):
                    accepted_models.add(model)

    assert {path.name for path in (SKILL_ROOT / "agents").glob("*.md")} == set(POLICY_PINS)
    for agent_name, (policy_model, policy_thinking) in POLICY_PINS.items():
        fields = _frontmatter(SKILL_ROOT / "agents" / agent_name)
        assert fields.get("model") in {policy_model, *accepted_models}
        if fields.get("model") == policy_model:
            assert fields.get("thinking") == policy_thinking

    for path in RUNTIME_DOCUMENTS:
        text = path.read_text(encoding="utf-8")
        assert not CALIBRATED_PI_MODEL.search(text), f"unreviewed calibrated Pi-model claim: {path}"
