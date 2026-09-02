"""Shared frontmatter utilities for skill-creator scripts.

This is a zero-dependency copy of the Pi 0.84.4 behavior needed by the
standalone validator. It intentionally supports the JSON-safe YAML subset used
by skill frontmatter rather than trying to be a general YAML implementation.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Final

_KEY_PATTERN: Final = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
_BOOLEAN_FIELDS: Final = (
    "disable-model-invocation",
    "user-invocable",
    "background",
)
_TRUE_VALUES: Final = {"true", "yes", "on", "1"}
_FALSE_VALUES: Final = {"false", "no", "off", "0"}
_OMIT: Final = object()


def normalize_newlines(value: str) -> str:
    """Strip one BOM and normalize line endings as Pi does before parsing."""
    return value.removeprefix("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def extract_frontmatter(content: str) -> str:
    """Return the YAML frontmatter text or raise for an undeclared document."""
    normalized = normalize_newlines(content)
    if not normalized.startswith("---"):
        raise ValueError("No YAML frontmatter found")
    end_index = normalized.find("\n---", 3)
    if end_index == -1:
        raise ValueError("Invalid frontmatter format")
    return normalized[4:end_index]


def _split_inline(value: str) -> list[str]:
    parts: list[str] = []
    start = 0
    quote: str | None = None
    depth = 0
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in "\"'":
            quote = character
        elif character in "[{":
            depth += 1
        elif character in "]}":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced inline collection")
        elif character == "," and depth == 0:
            parts.append(value[start:index].strip())
            start = index + 1
    if quote or depth != 0:
        raise ValueError("unterminated inline collection")
    parts.append(value[start:].strip())
    return parts


def _split_mapping_entry(value: str) -> tuple[str, str]:
    quote: str | None = None
    depth = 0
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in "\"'":
            quote = character
        elif character in "[{":
            depth += 1
        elif character in "]}":
            depth -= 1
        elif character == ":" and depth == 0:
            return value[:index].strip(), value[index + 1 :].strip()
    raise ValueError("inline mapping entry has no colon")


def _parse_scalar(raw: str) -> object:
    value = raw.strip()
    if value == "":
        return None
    if value.startswith("!!") or value.startswith("&") or value.startswith("*"):
        return _OMIT
    if value.startswith('"') or value.endswith('"'):
        if len(value) < 2 or not value.endswith('"'):
            raise ValueError("unterminated double-quoted scalar")
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError("quoted scalar must be a string")
        return parsed
    if value.startswith("'") or value.endswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError("unterminated single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.startswith("[") or value.endswith("]"):
        if not (value.startswith("[") and value.endswith("]")):
            raise ValueError("unterminated inline list")
        body = value[1:-1].strip()
        if not body:
            return []
        result: list[object] = []
        for item in _split_inline(body):
            parsed = _parse_scalar(item)
            if parsed is not _OMIT:
                result.append(parsed)
        return result
    if value.startswith("{") or value.endswith("}"):
        if not (value.startswith("{") and value.endswith("}")):
            raise ValueError("unterminated inline mapping")
        body = value[1:-1].strip()
        if not body:
            return {}
        result: dict[str, object] = {}
        for item in _split_inline(body):
            raw_key, raw_value = _split_mapping_entry(item)
            key_value = _parse_scalar(raw_key)
            parsed = _parse_scalar(raw_value)
            if not isinstance(key_value, str):
                raise ValueError("inline mapping keys must be strings")
            if parsed is not _OMIT:
                result[key_value] = parsed
        return result
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if lowered in {".nan", ".inf", "+.inf", "-.inf"}:
        return _OMIT
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:e[-+]?\d+)?", value, re.IGNORECASE):
        number = float(value)
        return number if math.isfinite(number) else _OMIT
    return value


def _indent(line: str) -> int:
    prefix = line[: len(line) - len(line.lstrip(" \t"))]
    if "\t" in prefix:
        raise ValueError("tabs are not allowed for YAML indentation")
    return len(prefix)


def _next_content(lines: list[str], start: int) -> int | None:
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("#"):
            return index
    return None


def _parse_multiline(
    lines: list[str], start: int, parent_indent: int, indicator: str
) -> tuple[str, int]:
    end = start
    body: list[str] = []
    content_indent: int | None = None
    while end < len(lines):
        line = lines[end]
        if not line.strip():
            if content_indent is not None:
                body.append("")
            end += 1
            continue
        indentation = _indent(line)
        if indentation <= parent_indent:
            break
        if content_indent is None:
            content_indent = indentation
        body.append(line[min(content_indent, indentation) :])
        end += 1
    if indicator.startswith(">"):
        value = " ".join(part.strip() for part in body)
    else:
        value = "\n".join(body)
    if not indicator.endswith("-") and body:
        value += "\n"
    return value, end


def _parse_block(lines: list[str], start: int, indentation: int) -> tuple[object, int]:
    first = _next_content(lines, start)
    if first is None or _indent(lines[first]) < indentation:
        return {}, start
    is_list = lines[first].lstrip().startswith("-")
    collection: object = [] if is_list else {}
    index = start
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        current_indent = _indent(line)
        if current_indent < indentation:
            break
        if current_indent > indentation:
            raise ValueError(f"unexpected indentation: {stripped!r}")
        text = line[indentation:]
        if is_list:
            if not text.startswith("-"):
                raise ValueError("cannot mix YAML list and mapping entries")
            raw = text[1:].strip()
            parsed = _parse_scalar(raw)
            if parsed is not _OMIT:
                assert isinstance(collection, list)
                collection.append(parsed)
            index += 1
            continue
        match = _KEY_PATTERN.match(text)
        if not match:
            raise ValueError(f"Invalid frontmatter line: {stripped!r}")
        key, raw = match.group(1), match.group(2).strip()
        if raw in {">", "|", ">-", "|-"}:
            parsed, index = _parse_multiline(lines, index + 1, indentation, raw)
        elif raw == "":
            next_index = _next_content(lines, index + 1)
            if next_index is not None and _indent(lines[next_index]) > indentation:
                child_indent = _indent(lines[next_index])
                parsed, index = _parse_block(lines, index + 1, child_indent)
            else:
                parsed = None
                index += 1
        elif raw.startswith("&"):
            parsed = {}
            next_index = _next_content(lines, index + 1)
            if next_index is not None and _indent(lines[next_index]) > indentation:
                _, index = _parse_block(lines, index + 1, _indent(lines[next_index]))
            else:
                index += 1
        elif raw.startswith("!!set"):
            parsed = _OMIT
            next_index = _next_content(lines, index + 1)
            if next_index is not None and _indent(lines[next_index]) > indentation:
                _, index = _parse_block(lines, index + 1, _indent(lines[next_index]))
            else:
                index += 1
        else:
            parsed = _parse_scalar(raw)
            index += 1
        if parsed is not _OMIT:
            assert isinstance(collection, dict)
            collection[key] = parsed
    return collection, index


def _normalize_frontmatter(frontmatter: dict[str, object]) -> None:
    for field in _BOOLEAN_FIELDS:
        value = frontmatter.get(field)
        normalized: bool | None = None
        if isinstance(value, bool):
            normalized = value
        elif isinstance(value, int) and value in {0, 1}:
            normalized = bool(value)
        elif isinstance(value, str):
            lowered = value.lower()
            if lowered in _TRUE_VALUES:
                normalized = True
            elif lowered in _FALSE_VALUES:
                normalized = False
        if normalized is not None:
            frontmatter[field] = normalized
    context = frontmatter.get("context")
    if context is not None:
        normalized_context = context.lower() if isinstance(context, str) else ""
        if normalized_context in {"inline", "fork"}:
            frontmatter["context"] = normalized_context
        else:
            frontmatter.pop("context", None)


def parse_frontmatter(frontmatter_text: str) -> tuple[dict[str, object] | None, str | None]:
    """Parse and normalize Pi's JSON-safe skill-frontmatter subset."""
    try:
        lines = normalize_newlines(frontmatter_text).split("\n")
        parsed, _ = _parse_block(lines, 0, 0)
        if not isinstance(parsed, dict) or not parsed:
            return None, "Frontmatter must be a YAML dictionary"
        _normalize_frontmatter(parsed)
        json.dumps(parsed, allow_nan=False)
        return parsed, None
    except (AssertionError, TypeError, ValueError, json.JSONDecodeError) as error:
        return None, str(error)


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    try:
        frontmatter_text = extract_frontmatter(content)
    except ValueError as error:
        raise ValueError(f"SKILL.md {str(error).lower()}") from error
    frontmatter, parse_error = parse_frontmatter(frontmatter_text)
    if frontmatter is None:
        raise ValueError(parse_error or "invalid SKILL.md frontmatter")
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    return (
        name if isinstance(name, str) else "",
        description if isinstance(description, str) else "",
        content,
    )
