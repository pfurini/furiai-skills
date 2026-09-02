"""Regression and differential tests for standalone skill validation."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

from conftest import PI_REVISION, SKILL_ROOT, TEST_ROOT

VALIDATOR_FIXTURES = TEST_ROOT / "fixtures/validator"
EXPECTED_LOADABILITY = {
    "empty-description": False,
    "empty-name": False,
    "invalid-boolean": True,
    "invalid-context": True,
    "malformed-yaml": False,
    "unsafe-json-values": True,
    "missing-description": False,
    "missing-name": False,
    "no-frontmatter": False,
    "valid-current-fields": True,
    "valid-disallowed-camel": True,
    "valid-fork": True,
    "valid-inline": True,
    "valid-multiline-bom": True,
    "valid-user-invoked": True,
    "whitespace-description": False,
    "whitespace-name": False,
}


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


UTILS = _load_module("utils", SKILL_ROOT / "scripts/utils.py")
VALIDATOR = _load_module("opin_quick_validate", SKILL_ROOT / "scripts/quick_validate.py")


def _fixture_directories() -> list[Path]:
    return sorted(path for path in VALIDATOR_FIXTURES.iterdir() if (path / "SKILL.md").is_file())


def test_accepts_current_pi_frontmatter_and_rejects_empty_required_fields() -> None:
    cases = {
        "valid-current-fields": True,
        "empty-name": False,
        "empty-description": False,
    }

    actual = {
        name: VALIDATOR.validate_skill(VALIDATOR_FIXTURES / name)[0]
        for name in cases
    }

    assert actual == cases


@pytest.mark.parametrize("fixture_name, expected", sorted(EXPECTED_LOADABILITY.items()))
def test_fixture_corpus_has_expected_standalone_verdict(
    fixture_name: str, expected: bool
) -> None:
    valid, message = VALIDATOR.validate_skill(VALIDATOR_FIXTURES / fixture_name)

    assert valid is expected, message


def test_normalizes_pi_boolean_context_and_json_safe_values() -> None:
    current_text = (VALIDATOR_FIXTURES / "valid-current-fields/SKILL.md").read_text(
        encoding="utf-8"
    )
    current, error = UTILS.parse_frontmatter(UTILS.extract_frontmatter(current_text))
    invalid_boolean_text = (VALIDATOR_FIXTURES / "invalid-boolean/SKILL.md").read_text(
        encoding="utf-8"
    )
    invalid_boolean, invalid_error = UTILS.parse_frontmatter(
        UTILS.extract_frontmatter(invalid_boolean_text)
    )
    invalid_context_text = (VALIDATOR_FIXTURES / "invalid-context/SKILL.md").read_text(
        encoding="utf-8"
    )
    invalid_context, context_error = UTILS.parse_frontmatter(
        UTILS.extract_frontmatter(invalid_context_text)
    )

    assert error is None
    assert current is not None
    assert current["disable-model-invocation"] is True
    assert current["user-invocable"] is False
    assert current["background"] is False
    assert current["context"] == "fork"
    assert current["unknown-map"] == {"nested": True, "count": 2}
    assert current["unknown-list"] == ["one", "two"]
    json.dumps(current)

    unsafe_text = (VALIDATOR_FIXTURES / "unsafe-json-values/SKILL.md").read_text(
        encoding="utf-8"
    )
    unsafe, unsafe_error = UTILS.parse_frontmatter(UTILS.extract_frontmatter(unsafe_text))
    assert unsafe_error is None
    assert unsafe is not None
    assert unsafe["cycle"] == {}
    assert not ({"nan", "positive", "negative", "set", "binary"} & unsafe.keys())
    json.dumps(unsafe, allow_nan=False)

    assert invalid_error is None
    assert invalid_boolean is not None
    assert invalid_boolean["disable-model-invocation"] == "maybe"
    assert invalid_boolean["user-invocable"] == "perhaps"
    assert invalid_boolean["background"] == "later"

    assert context_error is None
    assert invalid_context is not None
    assert "context" not in invalid_context


def test_bom_and_multiline_values_match_pi_shapes() -> None:
    fixture = VALIDATOR_FIXTURES / "valid-multiline-bom"
    content = (fixture / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, error = UTILS.parse_frontmatter(UTILS.extract_frontmatter(content))

    assert error is None
    assert frontmatter is not None
    assert frontmatter["description"] == "First line second line"
    assert frontmatter["when_to_use"] == "First\nSecond"
    assert UTILS.parse_skill_md(fixture)[:2] == (
        "valid-multiline-bom",
        "First line second line",
    )


def test_fixture_manifest_covers_every_fixture() -> None:
    assert {path.name for path in _fixture_directories()} == set(EXPECTED_LOADABILITY)


@pytest.mark.contract
def test_differential_loadability_matches_pinned_pi_loader(pi_checkout: Path) -> None:
    oracle = VALIDATOR_FIXTURES / "pi-loader-oracle.mjs"
    command = [
        "node",
        "--experimental-strip-types",
        str(oracle),
        str(pi_checkout),
        *[str(path) for path in _fixture_directories()],
    ]
    outcome = subprocess.run(command, check=True, capture_output=True, text=True)
    pi_results = json.loads(outcome.stdout)

    print(f"Reconciled Pi revision: {PI_REVISION}")
    assert set(pi_results) == set(EXPECTED_LOADABILITY)
    for fixture_name, expected in EXPECTED_LOADABILITY.items():
        python_loadable = VALIDATOR.validate_skill(
            VALIDATOR_FIXTURES / fixture_name
        )[0]
        pi_loadable = pi_results[fixture_name]["loadable"]
        if fixture_name in {"missing-name", "empty-name", "whitespace-name"}:
            # Pi falls back to the directory name. The frozen standalone contract
            # deliberately requires an authored, non-empty name.
            pi_loadable = False
        assert python_loadable is expected
        assert python_loadable is pi_loadable, pi_results[fixture_name]
