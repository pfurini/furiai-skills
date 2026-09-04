"""Structural contracts for the Pi-grounded skill-authoring doctrine."""

from __future__ import annotations

import re

from conftest import SKILL_ROOT


DOCTRINE_PATH = SKILL_ROOT / "references/writing-principles.md"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
PI_REFERENCE_PATTERN = re.compile(r"@\$\{PI_SKILL_DIR\}/([^\s)`]+\.md)")


def _frontmatter(text: str) -> dict[str, str]:
    _, raw_frontmatter, _ = text.split("---", 2)
    return {
        key.strip(): value.strip()
        for line in raw_frontmatter.strip().splitlines()
        for key, value in [line.split(":", 1)]
    }


def test_doctrine_exposes_pi_authoring_surface_and_resolvable_references() -> None:
    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    frontmatter = _frontmatter(skill_text)
    pi_surface = doctrine.split("## Pi authoring surface", 1)[1].split("\n## ", 1)[0]

    required_pi_surface = (
        "when_to_use",
        "argument-hint",
        "arguments",
        "$ARGUMENTS",
        "$0",
        "user-invocable",
        "allowed-tools",
        "disallowed-tools",
        "model",
        "effort",
        "context: fork",
        "agent",
        "background",
        "paths",
        "shell",
        "hooks",
        "${PI_SKILL_DIR}",
        "/skill:name",
        "/skills",
    )
    missing = [field for field in required_pi_surface if field not in pi_surface]
    assert not missing, f"Pi authoring surface missing from doctrine: {missing}"

    assert "parsed and preserved, never executed" in pi_surface
    assert "0-based" in pi_surface
    assert "listing cost" in doctrine
    assert "capability" in pi_surface and "failure" in pi_surface

    assert frontmatter["disable-model-invocation"] == "true"
    assert frontmatter.get("context", "inline") == "inline"
    assert "model" not in frontmatter
    assert "effort" not in frontmatter
    assert "agent" not in frontmatter
    assert "background" not in frontmatter
    assert frontmatter["description"].startswith("Creates, improves, and tests")
    assert "Use when" not in frontmatter["description"]
    assert len(frontmatter["description"]) <= 160

    references = PI_REFERENCE_PATTERN.findall(skill_text)
    assert references, "SKILL.md must disclose references through ${PI_SKILL_DIR}"
    assert "@references/" not in skill_text
    assert not re.search(r"\]\(references/[^)]+\.md\)", skill_text)
    assert set(references) == {
        "references/benchmarking.md",
        "references/testing.md",
        "references/writing-principles.md",
    }
    for relative_path in references:
        assert len(relative_path.split("/")) == 2
        target = SKILL_ROOT / relative_path
        assert target.is_file(), f"unresolvable skill-local reference: {relative_path}"
