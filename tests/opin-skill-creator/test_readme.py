"""Deterministic product-documentation contracts for opin-skill-creator."""

from __future__ import annotations

import re

from conftest import SKILL_ROOT


README_PATH = SKILL_ROOT / "README.md"
INVOCATION = re.compile(r"/(?:skill:)?opin-skill-creator(?:\b|`)")


def _section(text: str, heading: str) -> str:
    section = text.split(f"## {heading}", 1)[1]
    return section.split("\n## ", 1)[0]


def test_readme_invocations_resolve_and_runtime_requirements_are_truthful() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    good_usage = _section(readme, "Good usage")
    examples = [
        line
        for line in good_usage.splitlines()
        if line.startswith('- "')
    ]

    assert examples
    assert all(INVOCATION.search(example) for example in examples)
    lowered = readme.lower()
    assert "prose naming alone cannot invoke" in lowered
    assert "model-hidden" in lowered

    requirements = _section(readme, "Runtime requirements")
    assert "Python 3.10+" in requirements
    assert "standard library" in requirements
    assert "plain-JavaScript runtime workflow" in requirements
    assert "optional feature dependencies" in requirements
    assert "absolute paths" in requirements
    assert "Pi 0.84.4" in requirements
    assert "pi-subagents 0.19.0" in requirements

    distribution = _section(readme, "Distribution")
    assert "byte-for-byte copy" in distribution
    assert "skills/opin-skill-creator/" in distribution
    assert "Pi-owned skill root" in distribution
    assert "not an archive" in distribution

    assert "historical Claude Code evidence" in readme
    assert "No Pi-native numeric claim or permanent model pin" in readme
    assert "approved calibration and human review" in readme
    assert "ported but not yet verified under Pi" not in readme
    assert "PI_CODING_AGENT_DIR" not in readme

    # Keep inherited measurements intact while making their origin unambiguous.
    for historical_result in ("10/10", "5.00", "4.67 vs 4.78"):
        assert historical_result in readme

    layout = _section(readme, "Layout")
    assert "workflows/" in layout
    assert "benchmark.js" in layout
