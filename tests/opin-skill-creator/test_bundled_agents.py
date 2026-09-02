"""Contract tests for opin-skill-creator's bundled pi-subagents agents."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest

from conftest import PI_SUBAGENTS_REVISION, verify_checkout_revision


AGENT_NAMES = (
    "grader",
    "comparator",
    "comparison-analyzer",
    "benchmark-analyzer",
)
EXPECTED_CONFIGS = {
    "grader": {
        "model": "openai-codex/gpt-5.6-sol",
        "thinking": "high",
        "maxTurns": 24,
        "runInBackground": True,
        "builtinToolNames": ["read", "write", "find", "grep", "ls"],
    },
    "comparator": {
        "model": "openrouter/~anthropic/claude-opus-latest",
        "thinking": "high",
        "maxTurns": 20,
        "runInBackground": True,
        "builtinToolNames": ["read", "write", "find", "grep", "ls"],
    },
    "comparison-analyzer": {
        "model": "openai-codex/gpt-5.6-sol",
        "thinking": "high",
        "maxTurns": 24,
        "runInBackground": False,
        "builtinToolNames": ["read", "write", "find", "grep", "ls"],
    },
    "benchmark-analyzer": {
        "model": "openai-codex/gpt-5.6-terra",
        "thinking": "medium",
        "maxTurns": 16,
        "runInBackground": False,
        "builtinToolNames": ["read", "write"],
    },
}

_NODE_PROBE = r"""
import { pathToFileURL } from "node:url";

let stdin = "";
for await (const chunk of process.stdin) stdin += chunk;
const input = JSON.parse(stdin);
const moduleUrl = name => pathToFileURL(`${input.checkout}/dist/${name}.js`).href;
const { buildAgentRegistry, setDefaultsDisabled } = await import(moduleUrl("agent-types"));
const { resolveAgentInvocationConfig } = await import(moduleUrl("invocation-config"));
const { resolveModel } = await import(moduleUrl("model-resolver"));
const { buildRewriteMaps, discoverSkillAgents } = await import(moduleUrl("skill-agents"));

setDefaultsDisabled(true);
const skillId = `${input.skillRoot}/SKILL.md`;
const snapshot = {
  revision: 1,
  removed: [],
  skills: [{
    id: skillId,
    name: "opin-skill-creator",
    listingName: "opin-skill-creator",
    baseDir: input.skillRoot,
    source: { path: skillId, source: "local", scope: "project", origin: "top-level" },
    frontmatter: { name: "opin-skill-creator" },
    visibility: { model: "full", user: "yes", userInvokeError: false },
  }],
};
const layer = discoverSkillAgents(snapshot);
const free = buildAgentRegistry(new Map(), { skillAgents: layer });
const userConfig = name => ({
  name,
  description: "Synthetic collision",
  extensions: false,
  skills: false,
  systemPrompt: "Synthetic collision",
  promptMode: "replace",
});
const collisions = new Map(input.agentNames.map(name => [name, userConfig(name)]));
const collided = buildAgentRegistry(collisions, { skillAgents: layer });

const availableModels = input.availableModels;
const registry = {
  find(provider, id) {
    return availableModels.find(model => model.provider === provider && model.id === id);
  },
  getAll() { return availableModels; },
  getAvailable() { return availableModels; },
};
const requireResolved = model => {
  const resolved = resolveModel(model, registry);
  if (typeof resolved === "string") throw new Error(resolved);
  return `${resolved.provider}/${resolved.id}`;
};
let unavailableError;
try {
  requireResolved("extension-only/unavailable-model");
} catch (error) {
  unavailableError = String(error.message ?? error);
}

const summarize = config => ({
  name: config.name,
  description: config.description,
  builtinToolNames: config.builtinToolNames,
  extensions: config.extensions,
  skills: config.skills,
  model: config.model,
  thinking: config.thinking,
  maxTurns: config.maxTurns,
  persistSession: config.persistSession,
  outputTranscript: config.outputTranscript,
  promptMode: config.promptMode,
  inheritContext: config.inheritContext,
  runInBackground: config.runInBackground,
});
const configs = Object.fromEntries(layer.map(entry => [entry.bareName, summarize(entry.config)]));
const effective = Object.fromEntries(layer.map(entry => [entry.bareName, resolveAgentInvocationConfig(
  entry.config,
  {
    model: "parent/inherited-model",
    thinking: "low",
    max_turns: 1,
    inherit_context: true,
    run_in_background: !entry.config.runInBackground,
  },
  { defaultRunInBackground: false },
)]));

process.stdout.write(JSON.stringify({
  names: layer.map(entry => entry.bareName).sort(),
  qualified: layer.map(entry => entry.qualified).sort(),
  configs,
  freeAliases: Object.fromEntries(input.agentNames.map(name => [name, free.registry.has(name)])),
  qualifiedDispatch: Object.fromEntries(input.agentNames.map(name => [
    name,
    collided.registry.has(`opin-skill-creator:${name}`),
  ])),
  qualifiedSkillIds: Object.fromEntries(input.agentNames.map(name => [
    name,
    collided.registry.get(`opin-skill-creator:${name}`).skillId,
  ])),
  freeRewriteMaps: buildRewriteMaps(free.aliases),
  collidedRewriteMaps: buildRewriteMaps(collided.aliases),
  collisionPrompts: Object.fromEntries(input.agentNames.map(name => [name, collided.registry.get(name).systemPrompt])),
  selectedProfile: input.selectedProfile,
  effective,
  resolvedModels: Object.fromEntries(layer.map(entry => [
    entry.bareName,
    typeof entry.config.model === "string" ? requireResolved(entry.config.model) : null,
  ])),
  unavailableError,
}));
"""


def _pi_subagents_checkout() -> Path:
    value = os.environ.get("PI_SUBAGENTS_CHECKOUT")
    if not value:
        pytest.skip("bundled-agent loader tests require PI_SUBAGENTS_CHECKOUT")
    try:
        return verify_checkout_revision(
            Path(value), PI_SUBAGENTS_REVISION, "pi-subagents checkout"
        )
    except ValueError as error:
        pytest.fail(str(error), pytrace=False)


def _probe_agents(skill_root: Path) -> dict[str, Any]:
    checkout = _pi_subagents_checkout()
    result = subprocess.run(
        ["node", "--input-type=module", "-e", _NODE_PROBE],
        input=json.dumps(
            {
                "checkout": os.fspath(checkout),
                "skillRoot": os.fspath(skill_root),
                "agentNames": AGENT_NAMES,
                "selectedProfile": "declared-dependencies",
                "availableModels": [
                    {
                        "provider": "openai-codex",
                        "id": "gpt-5.6-sol",
                        "name": "GPT 5.6 Sol",
                    },
                    {
                        "provider": "openai-codex",
                        "id": "gpt-5.6-terra",
                        "name": "GPT 5.6 Terra",
                    },
                    {
                        "provider": "openrouter",
                        "id": "~anthropic/claude-opus-latest",
                        "name": "Claude Opus Latest",
                    },
                ],
            }
        ),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_four_agents_register_with_locked_effective_frontmatter(skill_root: Path) -> None:
    probe = _probe_agents(skill_root)

    assert probe["names"] == sorted(AGENT_NAMES)
    assert probe["qualified"] == sorted(
        f"opin-skill-creator:{name}" for name in AGENT_NAMES
    )
    for name, role_config in EXPECTED_CONFIGS.items():
        config = probe["configs"][name]
        assert config == {
            "name": name,
            "description": config["description"],
            "builtinToolNames": role_config["builtinToolNames"],
            "extensions": False,
            "skills": False,
            "model": role_config["model"],
            "thinking": role_config["thinking"],
            "maxTurns": role_config["maxTurns"],
            "persistSession": False,
            "outputTranscript": True,
            "promptMode": "replace",
            "inheritContext": False,
            "runInBackground": role_config["runInBackground"],
        }
        assert config["description"]

        effective = probe["effective"][name]
        assert effective["modelInput"] == role_config["model"]
        assert effective["thinking"] == role_config["thinking"]
        assert effective["maxTurns"] == role_config["maxTurns"]
        assert effective["inheritContext"] is False
        assert effective["runInBackground"] is role_config["runInBackground"]


def test_bare_qualified_and_collision_dispatch_maps(skill_root: Path) -> None:
    probe = _probe_agents(skill_root)
    skill_id = os.fspath(skill_root / "SKILL.md")

    assert probe["freeAliases"] == {name: True for name in AGENT_NAMES}
    assert probe["qualifiedDispatch"] == {name: True for name in AGENT_NAMES}
    assert probe["qualifiedSkillIds"] == {
        name: skill_id for name in AGENT_NAMES
    }
    assert probe["collisionPrompts"] == {
        name: "Synthetic collision" for name in AGENT_NAMES
    }
    for name in AGENT_NAMES:
        free_entry = probe["freeRewriteMaps"][skill_id][name]
        collided_entry = probe["collidedRewriteMaps"][skill_id][name]
        qualified = f"opin-skill-creator:{name}"
        assert free_entry == {"qualified": qualified, "collided": False}
        assert collided_entry == {"qualified": qualified, "collided": True}


def test_model_preflight_resolves_every_pin_and_rejects_unavailable_pin(
    skill_root: Path,
) -> None:
    probe = _probe_agents(skill_root)

    assert probe["selectedProfile"] == "declared-dependencies"
    assert probe["resolvedModels"] == {
        name: config["model"] for name, config in EXPECTED_CONFIGS.items()
    }
    assert 'Model not found: "extension-only/unavailable-model"' in probe[
        "unavailableError"
    ]
    assert "parent/inherited-model" not in probe["resolvedModels"].values()


def test_comparator_is_blind_and_analyzer_roles_do_not_bleed(skill_root: Path) -> None:
    agents_root = skill_root / "agents"
    comparator = (agents_root / "comparator.md").read_text(encoding="utf-8").lower()
    comparison = (agents_root / "comparison-analyzer.md").read_text(
        encoding="utf-8"
    ).lower()
    benchmark = (agents_root / "benchmark-analyzer.md").read_text(
        encoding="utf-8"
    ).lower()

    for identity in ("with_skill", "without_skill", "treatment", "control"):
        assert identity not in comparator
    assert "winner_skill_path" in comparison
    assert "improvement" in comparison
    assert "benchmark_data_path" not in comparison
    assert "benchmark_data_path" in benchmark
    assert "do not suggest skill improvements" in benchmark
    assert "winner_skill_path" not in benchmark
    assert not (agents_root / "analyzer.md").exists()


def test_grader_uses_jsonl_metrics_contract_and_lowercase_pi_tools(
    skill_root: Path,
) -> None:
    grader = (skill_root / "agents/grader.md").read_text(encoding="utf-8")
    lowered = grader.lower()

    assert "pi-json-events-v3" in grader
    assert "pi-subagents-output-v1" in grader
    assert "opin.transcript-metrics/v1" in grader
    assert "transcript_metrics_path" in grader
    assert "metrics.json" not in lowered
    assert "user_notes.md" not in lowered
    assert "assertion" not in lowered
    for tool_name in ("bash", "edit", "find", "grep", "ls", "read", "write"):
        assert f'"{tool_name}"' in grader
    for non_pi_name in ("Glob", '"Read"', '"Write"', '"Bash"'):
        assert non_pi_name not in grader
