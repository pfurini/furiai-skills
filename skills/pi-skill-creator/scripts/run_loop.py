#!/usr/bin/env python3
"""Run the eval + improve loop until all pass or max iterations reached.

Combines run_eval.py and improve_description.py in a loop, tracking history
and returning the best description found. Supports train/test split to prevent
overfitting.
"""

import argparse
import json
import random
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

from scripts.generate_report import generate_html
from scripts.improve_description import improve_description
from scripts.run_eval import (
    RoleConfigurationError,
    RoleModelConfig,
    add_role_arguments,
    find_project_root,
    role_config_from_args,
    run_eval,
)
from scripts.utils import extract_frontmatter, parse_frontmatter, parse_skill_md


Partition = tuple[list[dict], list[dict], list[dict]]


def partition_eval_set(
    eval_set: list[dict], holdout: float, seed: int = 42
) -> Partition:
    """Create deterministic stratified train, validation, and final-test sets."""
    if holdout == 0:
        return list(eval_set), [], []
    if not 0 < holdout < 1:
        raise ValueError("holdout must be greater than 0 and less than 1")

    classes = {
        True: [item for item in eval_set if item.get("should_trigger") is True],
        False: [item for item in eval_set if item.get("should_trigger") is False],
    }
    if any(len(items) < 3 for items in classes.values()):
        raise ValueError(
            "three-way stratification requires at least 3 examples per class"
        )

    rng = random.Random(seed)
    partitions: dict[str, list[dict]] = {
        "train": [],
        "validation": [],
        "final_test": [],
    }
    for items in classes.values():
        shuffled = list(items)
        rng.shuffle(shuffled)
        held_out = min(len(shuffled) - 1, max(2, int(len(shuffled) * holdout)))
        validation_size = held_out // 2
        final_test_size = held_out - validation_size
        partitions["validation"].extend(shuffled[:validation_size])
        partitions["final_test"].extend(
            shuffled[validation_size : validation_size + final_test_size]
        )
        partitions["train"].extend(shuffled[held_out:])

    return (
        partitions["train"],
        partitions["validation"],
        partitions["final_test"],
    )


def split_eval_set(
    eval_set: list[dict], holdout: float, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    """Compatibility wrapper returning train and combined held-out data."""
    train, validation, final_test = partition_eval_set(eval_set, holdout, seed)
    return train, validation + final_test


def select_best_candidate(history: list[dict]) -> dict:
    """Select by validation, then train, then the earliest iteration."""
    if not history:
        raise ValueError("candidate history must not be empty")
    return max(
        history,
        key=lambda item: (
            item.get("validation_passed")
            if item.get("validation_passed") is not None
            else item.get("train_passed", 0),
            item.get("train_passed", 0),
            -item.get("iteration", 0),
        ),
    )


def _human_readability_validation(description: str) -> dict:
    checks = {
        "non_empty": bool(description.strip()),
        "single_line": "\n" not in description and "\r" not in description,
        "within_character_limit": len(description) <= 1024,
        "no_angle_brackets": "<" not in description and ">" not in description,
    }
    return {
        "kind": "human_readability",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
    }


def _partition_results(all_results: dict, partition: list[dict]) -> dict:
    queries = {item["query"] for item in partition}
    results = [item for item in all_results["results"] if item["query"] in queries]
    passed = sum(1 for item in results if item["pass"])
    return {
        "results": results,
        "summary": {
            "passed": passed,
            "failed": len(results) - passed,
            "total": len(results),
        },
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def run_loop(
    eval_set: list[dict],
    skill_path: Path,
    description_override: str | None,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    runs_per_query: int,
    trigger_threshold: float,
    holdout: float,
    trigger_config: RoleModelConfig,
    optimizer_config: RoleModelConfig,
    verbose: bool,
    live_report_path: Path | None = None,
    log_dir: Path | None = None,
    results_dir: Path | None = None,
) -> dict:
    """Run deterministic train/validation selection and one final test."""
    if trigger_config.role != "trigger_consumer":
        raise RoleConfigurationError(
            "run_loop requires trigger_consumer role configuration"
        )
    if optimizer_config.role != "optimizer":
        raise RoleConfigurationError(
            "run_loop requires optimizer role configuration"
        )
    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")

    name, original_description, content = parse_skill_md(skill_path)
    current_description = description_override or original_description
    frontmatter, _ = parse_frontmatter(extract_frontmatter(content))
    model_invocation_disabled = bool(
        frontmatter and frontmatter.get("disable-model-invocation") is True
    )

    if model_invocation_disabled:
        validation = _human_readability_validation(current_description)
        output = {
            "exit_reason": "model_invocation_disabled",
            "optimization_skipped": True,
            "validation": validation,
            "original_description": original_description,
            "roles": {
                "trigger_consumer": trigger_config.as_metadata(),
                "optimizer": optimizer_config.as_metadata(),
            },
            "best_description": current_description,
            "best_score": None,
            "best_train_score": None,
            "best_validation_score": None,
            "final_test_score": None,
            "final_description": current_description,
            "iterations_run": 0,
            "holdout": holdout,
            "partition_counts": {
                "train": 0,
                "validation": 0,
                "final_test": 0,
            },
            "train_size": 0,
            "validation_size": 0,
            "final_test_size": 0,
            "final_test_call_count": 0,
            "final_test_results": None,
            "optimizer_transcripts": [],
            "history": [],
        }
        if results_dir:
            _write_json(results_dir / "trigger/results.json", output)
        return output

    project_root = find_project_root()
    train_set, validation_set, final_test_set = partition_eval_set(
        eval_set, holdout
    )
    partition_counts = {
        "train": len(train_set),
        "validation": len(validation_set),
        "final_test": len(final_test_set),
    }
    if results_dir:
        _write_json(results_dir / "trigger/train.json", train_set)
        _write_json(results_dir / "trigger/validation.json", validation_set)
        _write_json(results_dir / "trigger/final-test.json", final_test_set)

    if verbose:
        print(
            "Split: "
            f"{len(train_set)} train, "
            f"{len(validation_set)} validation, "
            f"{len(final_test_set)} final-test (holdout={holdout})",
            file=sys.stderr,
        )

    history: list[dict] = []
    optimizer_transcripts: list[dict] = []
    exit_reason = "unknown"

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"Iteration {iteration}/{max_iterations}", file=sys.stderr)
            print(f"Description: {current_description}", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)

        candidate_queries = train_set + validation_set
        started_at = time.time()
        candidate_results = run_eval(
            eval_set=candidate_queries,
            skill_name=name,
            description=current_description,
            num_workers=num_workers,
            timeout=timeout,
            project_root=project_root,
            role_config=trigger_config,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
        )
        eval_elapsed = time.time() - started_at
        train_results = _partition_results(candidate_results, train_set)
        validation_results = _partition_results(
            candidate_results, validation_set
        )
        train_summary = train_results["summary"]
        validation_summary = validation_results["summary"]

        history.append(
            {
                "iteration": iteration,
                "description": current_description,
                "train_passed": train_summary["passed"],
                "train_failed": train_summary["failed"],
                "train_total": train_summary["total"],
                "train_results": train_results["results"],
                "validation_passed": (
                    validation_summary["passed"] if validation_set else None
                ),
                "validation_failed": (
                    validation_summary["failed"] if validation_set else None
                ),
                "validation_total": (
                    validation_summary["total"] if validation_set else None
                ),
                "validation_results": (
                    validation_results["results"] if validation_set else None
                ),
                "passed": train_summary["passed"],
                "failed": train_summary["failed"],
                "total": train_summary["total"],
                "results": train_results["results"],
            }
        )

        if live_report_path:
            partial_output = {
                "original_description": original_description,
                "best_description": select_best_candidate(history)["description"],
                "best_score": "in progress",
                "iterations_run": len(history),
                "partition_counts": partition_counts,
                "train_size": len(train_set),
                "validation_size": len(validation_set),
                "final_test_size": len(final_test_set),
                "history": history,
            }
            live_report_path.write_text(
                generate_html(
                    partial_output, auto_refresh=True, skill_name=name
                ),
                encoding="utf-8",
            )

        if verbose:
            def print_eval_stats(
                label: str, results: list[dict], elapsed: float
            ) -> None:
                positive = [item for item in results if item["should_trigger"]]
                negative = [item for item in results if not item["should_trigger"]]
                true_positive = sum(item["triggers"] for item in positive)
                positive_runs = sum(item["runs"] for item in positive)
                false_negative = positive_runs - true_positive
                false_positive = sum(item["triggers"] for item in negative)
                negative_runs = sum(item["runs"] for item in negative)
                true_negative = negative_runs - false_positive
                total = (
                    true_positive
                    + true_negative
                    + false_positive
                    + false_negative
                )
                precision = (
                    true_positive / (true_positive + false_positive)
                    if true_positive + false_positive > 0
                    else 1.0
                )
                recall = (
                    true_positive / (true_positive + false_negative)
                    if true_positive + false_negative > 0
                    else 1.0
                )
                accuracy = (
                    (true_positive + true_negative) / total
                    if total > 0
                    else 0.0
                )
                print(
                    f"{label}: {true_positive + true_negative}/{total} correct, "
                    f"precision={precision:.0%} recall={recall:.0%} "
                    f"accuracy={accuracy:.0%} ({elapsed:.1f}s)",
                    file=sys.stderr,
                )
                for result in results:
                    status = "PASS" if result["pass"] else "FAIL"
                    print(
                        f"  [{status}] rate={result['triggers']}/{result['runs']} "
                        f"expected={result['should_trigger']}: "
                        f"{result['query'][:60]}",
                        file=sys.stderr,
                    )

            print_eval_stats("Train", train_results["results"], eval_elapsed)
            if validation_set:
                print_eval_stats(
                    "Validation", validation_results["results"], 0
                )

        if train_summary["failed"] == 0:
            exit_reason = f"all_passed (iteration {iteration})"
            if verbose:
                print(
                    f"\nAll train queries passed on iteration {iteration}!",
                    file=sys.stderr,
                )
            break

        if iteration == max_iterations:
            exit_reason = f"max_iterations ({max_iterations})"
            if verbose:
                print(
                    f"\nMax iterations reached ({max_iterations}).",
                    file=sys.stderr,
                )
            break

        if verbose:
            print("\nImproving description...", file=sys.stderr)

        started_at = time.time()
        blinded_history = [
            {
                key: value
                for key, value in item.items()
                if not key.startswith(("validation_", "test_", "final_test_"))
            }
            for item in history
        ]
        current_description = improve_description(
            skill_name=name,
            skill_content=content,
            current_description=current_description,
            eval_results=train_results,
            history=blinded_history,
            role_config=optimizer_config,
            log_dir=log_dir,
            iteration=iteration,
            transcript_history=optimizer_transcripts,
        )
        if verbose:
            print(
                f"Proposed ({time.time() - started_at:.1f}s): "
                f"{current_description}",
                file=sys.stderr,
            )

    best = select_best_candidate(history)
    if validation_set:
        best_score = (
            f"{best['validation_passed']}/{best['validation_total']}"
        )
    else:
        best_score = f"{best['train_passed']}/{best['train_total']}"

    final_test_results = None
    final_test_call_count = 0
    if final_test_set:
        final_test_results = run_eval(
            eval_set=final_test_set,
            skill_name=name,
            description=best["description"],
            num_workers=num_workers,
            timeout=timeout,
            project_root=project_root,
            role_config=trigger_config,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
        )
        final_test_call_count = 1

    final_test_score = None
    if final_test_results:
        summary = final_test_results["summary"]
        final_test_score = f"{summary['passed']}/{summary['total']}"

    if verbose:
        print(f"\nExit reason: {exit_reason}", file=sys.stderr)
        print(
            f"Best selection score: {best_score} "
            f"(iteration {best['iteration']})",
            file=sys.stderr,
        )

    output = {
        "exit_reason": exit_reason,
        "optimization_skipped": False,
        "validation": None,
        "original_description": original_description,
        "roles": {
            "trigger_consumer": trigger_config.as_metadata(),
            "optimizer": optimizer_config.as_metadata(),
        },
        "best_description": best["description"],
        "best_score": best_score,
        "best_train_score": f"{best['train_passed']}/{best['train_total']}",
        "best_validation_score": (
            f"{best['validation_passed']}/{best['validation_total']}"
            if validation_set
            else None
        ),
        "final_test_score": final_test_score,
        "final_description": current_description,
        "iterations_run": len(history),
        "holdout": holdout,
        "partition_counts": partition_counts,
        "train_size": len(train_set),
        "validation_size": len(validation_set),
        "final_test_size": len(final_test_set),
        "final_test_call_count": final_test_call_count,
        "final_test_results": final_test_results,
        "optimizer_transcripts": optimizer_transcripts,
        "history": history,
    }
    if results_dir:
        _write_json(results_dir / "trigger/results.json", output)
    return output


def main():
    parser = argparse.ArgumentParser(description="Run eval + improve loop")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override starting description")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max improvement iterations")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument(
        "--holdout",
        type=float,
        default=0.4,
        help="Fraction split evenly between validation and final-test (0 disables both)",
    )
    add_role_arguments(parser, "trigger_consumer")
    add_role_arguments(parser, "optimizer")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    parser.add_argument(
        "--report",
        default="none",
        help="Generate HTML at a path, use 'auto' for a temporary live report, or 'none'",
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Persist partitions, results, and optimizer transcripts in this campaign path",
    )
    args = parser.parse_args()
    try:
        trigger_config = role_config_from_args(args, "trigger_consumer")
        optimizer_config = role_config_from_args(args, "optimizer")
    except RoleConfigurationError as error:
        parser.error(str(error))

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, _, _ = parse_skill_md(skill_path)

    # Set up live report path
    if args.report != "none":
        if args.report == "auto":
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            live_report_path = Path(tempfile.gettempdir()) / f"skill_description_report_{skill_path.name}_{timestamp}.html"
        else:
            live_report_path = Path(args.report)
        # Open the report immediately so the user can watch
        live_report_path.write_text("<html><body><h1>Starting optimization loop...</h1><meta http-equiv='refresh' content='5'></body></html>")
        webbrowser.open(str(live_report_path))
    else:
        live_report_path = None

    # The caller supplies the exact campaign path; never add a time-derived layer.
    results_dir = Path(args.results_dir) if args.results_dir else None
    if results_dir:
        results_dir.mkdir(parents=True, exist_ok=True)
    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        description_override=args.description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        max_iterations=args.max_iterations,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        holdout=args.holdout,
        trigger_config=trigger_config,
        optimizer_config=optimizer_config,
        verbose=args.verbose,
        live_report_path=live_report_path,
        results_dir=results_dir,
    )

    json_output = json.dumps(output, indent=2, sort_keys=True)
    print(json_output)
    if results_dir:
        _write_json(results_dir / "trigger/results.json", output)

    if live_report_path:
        live_report_path.write_text(
            generate_html(output, auto_refresh=False, skill_name=name),
            encoding="utf-8",
        )
        print(f"\nReport: {live_report_path}", file=sys.stderr)

    if results_dir:
        print(f"Results saved to: {results_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
