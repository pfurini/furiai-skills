#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version.

Zero-dependency by design: frontmatter is parsed with a small line-based
parser instead of pyyaml, because a bundled validator must not fail on
first use in an environment that never installed anything. The parser
covers what skill frontmatter actually uses: top-level scalar keys
(plain, quoted, or booleans-as-text), nested blocks (e.g. `metadata:`,
whose inner keys are ignored, matching the previous behaviour), and
multiline scalars (`>`, `|`, `>-`, `|-`).
"""

import sys
import re
from pathlib import Path


def parse_frontmatter(frontmatter_text):
    """Parse top-level frontmatter keys into a dict of strings.

    Returns (dict, None) on success or (None, error_message) on failure.
    Indented lines belong to the preceding top-level key and are ignored,
    except as the body of a multiline scalar.
    """
    keys = {}
    lines = frontmatter_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line[0] in " \t":
            # Nested content under the previous key (e.g. metadata entries).
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
        if not m:
            return None, f"Invalid frontmatter line: {line.strip()!r}"
        key, raw = m.group(1), m.group(2).strip()
        if raw in (">", "|", ">-", "|-"):
            continuation = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t")):
                continuation.append(lines[i].strip())
                i += 1
            keys[key] = " ".join(continuation)
            continue
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            raw = raw[1:-1]
        keys[key] = raw
        i += 1
    if not keys:
        return None, "Frontmatter must be a YAML dictionary"
    return keys, None


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter, err = parse_frontmatter(match.group(1))
    if err:
        return False, err

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility', 'disable-model-invocation'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Validate name
    name = frontmatter['name'].strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Validate description
    description = frontmatter['description'].strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility and len(compatibility) > 500:
        return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
