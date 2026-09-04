# Campaign artifact schemas

These are the machine contracts for an pi-skill-creator benchmark campaign. The objects documented below are strict UTF-8 JSON. Duplicate keys, non-standard numeric constants, malformed fields, missing records, unexpected configurations, and placeholder metadata invalidate aggregation.

## Workspace layout

A campaign is stored below the evaluated project, not inside the distributed skill:

```text
<project-root>/.skill-creator/<skill-name>/campaign-<campaign-id>/
├── campaign.json
├── evals.json
├── trigger/
│   ├── train.json
│   ├── validation.json
│   ├── final-test.json
│   └── results.json
└── iteration-N/
    ├── benchmark.json
    ├── benchmark.md
    ├── feedback.json
    ├── viewer.pid
    └── <eval-name>/
        ├── eval_metadata.json
        ├── with_skill/
        │   └── run-N/
        │       ├── outputs/
        │       ├── transcript.jsonl
        │       ├── transcript-metrics.json
        │       ├── run.json
        │       ├── timing.json
        │       └── grading.json
        └── without_skill/
            └── run-N/
                ├── outputs/
                ├── transcript.jsonl
                ├── transcript-metrics.json
                ├── run.json
                ├── timing.json
                └── grading.json
```

`campaign-id` and `eval-name` match `[a-z0-9][a-z0-9-]{0,63}`. `iteration-N` and `run-N` use positive decimal integers without missing repetitions. The only configuration directories are `with_skill` (treatment) and `without_skill` (control). Benchmark deltas are always treatment minus control.

## `campaign.json` (`pi-skill-creator.campaign/v1`)

`campaign.json` is at the campaign root. Its required aggregation fields are:

```json
{
  "schema_version": "pi-skill-creator.campaign/v1",
  "campaign_id": "fork-smoke-1",
  "created_at": "2026-09-02T12:00:00Z",
  "repository_revision": "1111111111111111111111111111111111111111",
  "pi_revision": "db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee",
  "pi_subagents_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
  "workflow_runtime": "pi-subagents",
  "workflow_runtime_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
  "skill_name": "example-skill",
  "skill_path": "/absolute/path/to/example-skill",
  "evaluation_cwd": "/absolute/path/to/deployment-project",
  "environment_profile": "declared-dependencies",
  "declared_extensions": [
    "/absolute/path/to/pi-subagents/src/index.ts"
  ],
  "treatment": "with_skill",
  "control": "without_skill",
  "repetitions": 3,
  "roles": {
    "executor": {
      "requested_model": "provider/model",
      "requested_thinking": "high"
    }
  },
  "partitions": {
    "seed": 42,
    "train": "trigger/train.json",
    "validation": "trigger/validation.json",
    "final_test": "trigger/final-test.json"
  },
  "notes": [
    "Comparator claude-bridge/claude-opus-5 at high thinking judges blind; for outputs produced by Claude-family executors this comparison is not family-independent."
  ]
}
```

`created_at` is caller supplied in UTC. Revisions are lowercase 40-hex values read from `git rev-parse HEAD`, never typed from memory. `workflow_runtime` is `pi-subagents` or `pi-dynamic-workflows` and names the runtime that executed `workflows/benchmark.js`; `workflow_runtime_revision` is the `HEAD` of that runtime's checkout (under `pi-subagents` it equals `pi_subagents_revision`). Both fields are required: a campaign supports claims only for the runtime it records, and a run under the other runtime is a new campaign. `skill_path`, `evaluation_cwd`, and every declared extension are absolute. `environment_profile` is `in-situ`, `hermetic-core`, or `declared-dependencies`. Role entries not used by a campaign may be omitted, but benchmark aggregation requires the executor role. Requested model and thinking values must be concrete non-empty values. `notes` is an optional array of non-empty strings copied into `benchmark.json`; the setup launcher records the comparator family caveat there.

## `eval_metadata.json`

Each human-readable eval directory contains:

```json
{
  "eval_id": 1,
  "eval_name": "forked-skill-dispatch",
  "prompt": "Use the bundled specialist to inspect the project.",
  "expectations": [
    "The specialist result is reported."
  ]
}
```

`eval_id` is a positive integer, unique within the iteration. `eval_name` matches its directory exactly. `prompt` is non-empty and `expectations` is a non-empty array of non-empty strings.

## `run.json` (`pi-skill-creator.run/v1`)

Every `run-N` directory contains identity and effective runtime metadata:

```json
{
  "schema_version": "pi-skill-creator.run/v1",
  "campaign_id": "fork-smoke-1",
  "eval_id": 1,
  "eval_name": "forked-skill-dispatch",
  "configuration": "with_skill",
  "run_number": 1,
  "environment_profile": "declared-dependencies",
  "status": "completed",
  "role": "executor",
  "requested_model": "provider/model",
  "effective_model": "provider/model-exact",
  "requested_thinking": "high",
  "effective_thinking": "high",
  "transcript_format": "pi-json-events-v3",
  "transcript_path": "transcript.jsonl",
  "metrics_path": "transcript-metrics.json",
  "outputs_dir": "outputs"
}
```

Identity fields must match the campaign, eval metadata, and directory path. Only `completed` executor runs aggregate. Requested values must match the campaign executor role. Effective values must be observed values, not copies or placeholders. The three artifact paths are exactly the shown run-relative names. `transcript_format` is `pi-json-events-v3` or `pi-subagents-output-v1`.

## `transcript-metrics.json` (`pi-skill-creator.transcript-metrics/v1`)

This file is produced by `scripts.transcript_metrics` from the execution transcript:

```json
{
  "schema_version": "pi-skill-creator.transcript-metrics/v1",
  "source_format": "pi-json-events-v3",
  "tool_calls": {
    "bash": 2,
    "read": 3
  },
  "total_tool_calls": 5,
  "assistant_turns": 2,
  "tool_errors": 1,
  "usage": {
    "input": 100,
    "output": 20,
    "cache_read": 50,
    "cache_write": 0,
    "reasoning": 5,
    "total_tokens": 175,
    "cost_usd": 0.0123
  },
  "effective_models": [
    "provider/model-exact"
  ],
  "transcript_chars": 12345
}
```

Tool names are lowercase registered Pi names and counts are non-negative integers. `total_tool_calls` equals the tool histogram. `assistant_turns` is positive. `tool_errors` cannot exceed total calls. Provider token counts and cost live only under `usage`; character counts use names ending in `_chars`. Characters are never substituted for provider tokens. The source format and sole effective model must match `run.json` for an ordinary benchmark campaign.

## `timing.json`

Every completed run supplies the wall-clock value aggregated by the benchmark:

```json
{
  "total_duration_seconds": 23.3
}
```

`total_duration_seconds` is a finite non-negative number.

## `grading.json` (`pi-skill-creator.grading/v1`)

The grader writes one verdict for every expectation:

```json
{
  "schema_version": "pi-skill-creator.grading/v1",
  "expectations": [
    {
      "text": "The output includes the requested result.",
      "passed": true,
      "evidence": "The result appears in outputs/result.txt."
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  },
  "claims": [],
  "user_notes_summary": {
    "uncertainties": [],
    "needs_review": [],
    "workarounds": []
  }
}
```

`expectations` is required and non-empty. Every item requires non-empty `text` and `evidence` plus a boolean `passed`. Summary counts must exactly agree with the items; `pass_rate` may use ordinary decimal rounding. `claims` is an optional array retained in benchmark run details. `user_notes_summary` is optional; when present, its three fields are arrays of non-empty strings.

## `benchmark.json` (`pi-skill-creator.benchmark/v1`)

`scripts.aggregate_benchmark` writes this file only after the complete iteration validates. Its location is `campaign-<campaign-id>/iteration-N/benchmark.json`; `benchmark.md` is generated from the same in-memory summary.

```json
{
  "schema_version": "pi-skill-creator.benchmark/v1",
  "metadata": {
    "campaign_id": "fork-smoke-1",
    "created_at": "2026-09-02T12:00:00Z",
    "repository_revision": "1111111111111111111111111111111111111111",
    "pi_revision": "db6bee3d6ccb79f5bc7884962ea4d98ca21e60ee",
    "pi_subagents_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
    "workflow_runtime": "pi-subagents",
    "workflow_runtime_revision": "7f569969445bf8bc6fbd7757f18db80b35de0ba9",
    "skill_name": "example-skill",
    "skill_path": "/absolute/path/to/example-skill",
    "evaluation_cwd": "/absolute/path/to/deployment-project",
    "environment_profile": "declared-dependencies",
    "treatment": "with_skill",
    "control": "without_skill",
    "executor_model": "provider/model-exact",
    "executor_thinking": "high",
    "requested_executor_model": "provider/model",
    "requested_executor_thinking": "high",
    "timestamp": "2026-09-02T12:00:00Z",
    "evals_run": [1],
    "runs_per_configuration": 1
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "forked-skill-dispatch",
      "configuration": "with_skill",
      "run_number": 1,
      "environment_profile": "declared-dependencies",
      "requested_model": "provider/model",
      "effective_model": "provider/model-exact",
      "requested_thinking": "high",
      "effective_thinking": "high",
      "result": {
        "pass_rate": 1.0,
        "passed": 1,
        "failed": 0,
        "total": 1,
        "time_seconds": 23.3,
        "tool_calls": {
          "read": 3
        },
        "total_tool_calls": 3,
        "tool_errors": 0,
        "usage": {
          "input": 100,
          "output": 20,
          "cache_read": 50,
          "cache_write": 0,
          "reasoning": 5,
          "total_tokens": 175,
          "cost_usd": 0.0123
        },
        "transcript_chars": 12345
      },
      "expectations": [
        {
          "text": "The output includes the requested result.",
          "passed": true,
          "evidence": "The result appears in outputs/result.txt."
        }
      ],
      "claims": [],
      "notes": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {
        "mean": 1.0,
        "stddev": 0.0,
        "min": 1.0,
        "max": 1.0
      },
      "time_seconds": {
        "mean": 23.3,
        "stddev": 0.0,
        "min": 23.3,
        "max": 23.3
      },
      "total_tool_calls": {
        "mean": 3.0,
        "stddev": 0.0,
        "min": 3.0,
        "max": 3.0
      },
      "tool_errors": {
        "mean": 0.0,
        "stddev": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "transcript_chars": {
        "mean": 12345.0,
        "stddev": 0.0,
        "min": 12345.0,
        "max": 12345.0
      },
      "usage": {
        "input": {
          "mean": 100.0,
          "stddev": 0.0,
          "min": 100.0,
          "max": 100.0
        },
        "output": {
          "mean": 20.0,
          "stddev": 0.0,
          "min": 20.0,
          "max": 20.0
        },
        "cache_read": {
          "mean": 50.0,
          "stddev": 0.0,
          "min": 50.0,
          "max": 50.0
        },
        "cache_write": {
          "mean": 0.0,
          "stddev": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "reasoning": {
          "mean": 5.0,
          "stddev": 0.0,
          "min": 5.0,
          "max": 5.0
        },
        "total_tokens": {
          "mean": 175.0,
          "stddev": 0.0,
          "min": 175.0,
          "max": 175.0
        },
        "cost_usd": {
          "mean": 0.0123,
          "stddev": 0.0,
          "min": 0.0123,
          "max": 0.0123
        }
      }
    },
    "without_skill": {
      "pass_rate": {
        "mean": 0.25,
        "stddev": 0.0,
        "min": 0.25,
        "max": 0.25
      },
      "time_seconds": {
        "mean": 23.3,
        "stddev": 0.0,
        "min": 23.3,
        "max": 23.3
      },
      "total_tool_calls": {
        "mean": 3.0,
        "stddev": 0.0,
        "min": 3.0,
        "max": 3.0
      },
      "tool_errors": {
        "mean": 0.0,
        "stddev": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "transcript_chars": {
        "mean": 12345.0,
        "stddev": 0.0,
        "min": 12345.0,
        "max": 12345.0
      },
      "usage": {
        "input": {
          "mean": 100.0,
          "stddev": 0.0,
          "min": 100.0,
          "max": 100.0
        },
        "output": {
          "mean": 20.0,
          "stddev": 0.0,
          "min": 20.0,
          "max": 20.0
        },
        "cache_read": {
          "mean": 50.0,
          "stddev": 0.0,
          "min": 50.0,
          "max": 50.0
        },
        "cache_write": {
          "mean": 0.0,
          "stddev": 0.0,
          "min": 0.0,
          "max": 0.0
        },
        "reasoning": {
          "mean": 5.0,
          "stddev": 0.0,
          "min": 5.0,
          "max": 5.0
        },
        "total_tokens": {
          "mean": 175.0,
          "stddev": 0.0,
          "min": 175.0,
          "max": 175.0
        },
        "cost_usd": {
          "mean": 0.0123,
          "stddev": 0.0,
          "min": 0.0123,
          "max": 0.0123
        }
      }
    },
    "delta": {
      "pass_rate": "+0.75",
      "time_seconds": "+0.0",
      "total_tool_calls": "+0.0",
      "tool_errors": "+0.0",
      "transcript_chars": "+0",
      "usage": {
        "input": "+0.0",
        "output": "+0.0",
        "cache_read": "+0.0",
        "cache_write": "+0.0",
        "reasoning": "+0.0",
        "total_tokens": "+0.0",
        "cost_usd": "+0.0000"
      }
    }
  },
  "notes": []
}
```

Each arm has the same complete statistic set. Each statistic has finite `mean`, sample `stddev`, `min`, and `max`. `evals_run` and `runs_per_configuration` are derived from validated records. `workflow_runtime` and `workflow_runtime_revision` are copied from `campaign.json`, so every numeric claim names the runtime that produced it; `notes` carries the campaign notes. All runs in one benchmark share the campaign profile and one observed effective executor model and thinking level. Mixed values require a separate pre-registered comparison campaign and are not accepted by this aggregator.

`python -m scripts.aggregate_benchmark <iteration-dir> --validate-only` runs the same validation over the whole iteration tree and writes nothing: exit 0 when everything validates, exit 2 with one bounded error on a contract failure, exit 1 on a filesystem error. The runtime workflow runs it after grading and before aggregation.
