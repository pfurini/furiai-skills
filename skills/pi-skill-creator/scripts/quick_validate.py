#!/usr/bin/env python3
"""Validate a skill against the frozen Pi 0.84.4 frontmatter subset."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils import extract_frontmatter, parse_frontmatter


def validate_skill(skill_path: str | Path) -> tuple[bool, str]:
    """Validate one skill directory without runtime dependencies."""
    skill_directory = Path(skill_path)
    skill_md = skill_directory / "SKILL.md"
    if not skill_md.is_file():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return False, f"Could not read SKILL.md: {error}"

    try:
        frontmatter_text = extract_frontmatter(content)
    except ValueError as error:
        return False, str(error)

    frontmatter, parse_error = parse_frontmatter(frontmatter_text)
    if frontmatter is None:
        return False, parse_error or "Invalid frontmatter"

    for field in ("name", "description"):
        value = frontmatter.get(field)
        if field not in frontmatter:
            return False, f"Missing '{field}' in frontmatter"
        if not isinstance(value, str) or value.strip() == "":
            return False, f"'{field}' must be a non-empty string"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
