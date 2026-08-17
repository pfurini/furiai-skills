# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib>=3.8", "PyYAML>=6.0"]
# ///
"""Render a chart deterministically from a figure-spec YAML file.

Usage:
    uv run make_chart.py <spec.yaml> [-o OUTPUT_DIR]

Reads the figure spec (schema: references/figure-specs.md), validates it,
and writes <id>.svg next to the spec (or into OUTPUT_DIR). All validation
errors are collected and reported together with the exact field name, so a
broken spec can be fixed in one pass. Exit code 0 only when the chart was
rendered; warnings go to stderr but do not block rendering.

The output is reproducible: same spec + same data = byte-identical SVG
(fixed hash salt, no timestamps).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib
import yaml

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402

CHART_TYPES = ("line", "bar", "barh", "scatter", "area")

# Okabe-Ito palette: colorblind-safe, distinguishable in grayscale.
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]
ROLE_COLORS = {"focus": "#0072B2", "accent": "#D55E00", "neutral": "#ABABAB"}

INK = "#1a1a1a"
MUTED = "#555555"
FAINT = "#8a8a8a"
GRID = "#d9d9d9"

# Above 4 series a line/bar chart becomes hard to read (ONS guidance);
# warn so the author considers small multiples instead.
MAX_SERIES = 4


def fail(errors: list[str]) -> None:
    print("Spec validation failed:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)


def load_rows(spec: dict, spec_dir: Path, errors: list[str]) -> list[dict]:
    data = spec.get("data")
    if not isinstance(data, dict):
        errors.append("data: required mapping with either 'csv' or 'rows'")
        return []
    if "csv" in data:
        csv_path = (spec_dir / data["csv"]).resolve()
        if not csv_path.exists():
            errors.append(f"data.csv: file not found: {csv_path}")
            return []
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))
    if "rows" in data:
        rows = data["rows"]
        if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
            errors.append("data.rows: must be a list of mappings")
            return []
        return rows
    errors.append("data: needs 'csv' (path relative to the spec) or 'rows' (inline records)")
    return []


def validate(spec: dict, rows: list[dict], errors: list[str]) -> None:
    for field in ("id", "question", "takeaway", "subtitle", "chart_type", "source_note", "alt_text"):
        if not str(spec.get(field, "") or "").strip():
            errors.append(f"{field}: required (see references/figure-specs.md)")
    if spec.get("chart_type") and spec["chart_type"] not in CHART_TYPES:
        errors.append(f"chart_type: '{spec['chart_type']}' not one of {CHART_TYPES}")

    enc = spec.get("encodings")
    if not isinstance(enc, dict) or "x" not in enc or "y" not in enc:
        errors.append("encodings: required mapping with 'x' and 'y' (and optional 'series')")
        return
    if rows:
        missing = [k for k in (enc["x"], enc["y"], enc.get("series")) if k and k not in rows[0]]
        if missing:
            errors.append(f"encodings: field(s) {missing} not in data. Available: {sorted(rows[0])}")
            return
        for i, r in enumerate(rows):
            try:
                float(r[enc["y"]])
            except (TypeError, ValueError):
                errors.append(f"data row {i}: y value '{r[enc['y']]}' is not numeric")
                break

    # Bar lengths encode magnitude, so a truncated axis misstates the data.
    # Truncation is allowed only when declared and explained in the spec.
    if spec.get("chart_type") in ("bar", "barh", "area") and not spec.get("y_zero", True):
        if not str(spec.get("truncation_note", "") or "").strip():
            errors.append("y_zero: false on a bar/area chart requires 'truncation_note' explaining the truncation")


def coerce_x(values: list) -> list:
    try:
        return [float(v) for v in values]
    except (TypeError, ValueError):
        return [str(v) for v in values]


def split_series(rows: list[dict], enc: dict) -> dict[str, tuple[list, list]]:
    """Return {series_name: (x_values, y_values)}, preserving row order."""
    series_field = enc.get("series")
    out: dict[str, tuple[list, list]] = {}
    for r in rows:
        name = str(r[series_field]) if series_field else "_single"
        xs, ys = out.setdefault(name, ([], []))
        xs.append(r[enc["x"]])
        ys.append(float(r[enc["y"]]))
    return {name: (coerce_x(xs), ys) for name, (xs, ys) in out.items()}


def series_color(name: str, index: int, roles: dict) -> str:
    role = roles.get(name)
    if role in ROLE_COLORS:
        return ROLE_COLORS[role]
    # When any series is marked focus, undeclared series recede to neutral
    # so the focus actually stands out.
    if any(v == "focus" for v in roles.values()):
        return ROLE_COLORS["neutral"]
    return OKABE_ITO[index % len(OKABE_ITO)]


def render(spec: dict, rows: list[dict], out_path: Path) -> None:
    enc = spec["encodings"]
    roles = spec.get("color_roles") or {}
    chart = spec["chart_type"]
    data = split_series(rows, enc)

    if len(data) > MAX_SERIES:
        print(
            f"warning: {len(data)} series (> {MAX_SERIES}). Consider small multiples "
            "or marking one series 'focus' and the rest 'neutral'.",
            file=sys.stderr,
        )

    plt.rcParams.update({
        "svg.hashsalt": spec["id"],  # deterministic element ids
        "font.family": "DejaVu Sans",  # bundled with matplotlib: no external font dependency
        "text.color": INK,
        "axes.edgecolor": FAINT,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.titlelocation": "left",
    })

    fig, ax = plt.subplots(figsize=(8, 4.5))

    if chart in ("line", "scatter", "area"):
        for i, (name, (xs, ys)) in enumerate(data.items()):
            color = series_color(name, i, roles)
            if chart == "line":
                ax.plot(xs, ys, color=color, linewidth=2.2)
            elif chart == "scatter":
                ax.scatter(xs, ys, color=color, s=28)
            else:
                ax.fill_between(xs, ys, color=color, alpha=0.35, linewidth=0)
                ax.plot(xs, ys, color=color, linewidth=1.6)
            if enc.get("series"):
                # Direct label at the line end instead of a legend the
                # reader must decode.
                ax.annotate(
                    f" {name}", (xs[-1], ys[-1]), color=color if chart != "area" else INK,
                    fontsize=10, fontweight="bold", va="center",
                )
        if enc.get("series"):
            ax.margins(x=0.02)
            fig.subplots_adjust(right=0.86)
        # Integer x values (years, quarters): tick exactly on the data
        # points so the axis never shows fractional years like 2022.5.
        all_x = sorted({v for xs, _ in data.values() for v in xs})
        if all_x and all(isinstance(v, float) for v in all_x) and all(v == int(v) for v in all_x) and len(all_x) <= 10:
            ax.set_xticks(all_x, labels=[str(int(v)) for v in all_x])
    else:  # bar, barh
        name, (xs, ys) = next(iter(data.items()))
        if len(data) > 1:
            print("warning: bar/barh renders only the first series; use 'line' or small multiples for grouped comparisons", file=sys.stderr)
        order = list(range(len(xs)))
        sort = spec.get("sort", "none")
        if sort in ("y_desc", "y_asc"):
            order.sort(key=lambda i: ys[i], reverse=(sort == "y_desc"))
        xs = [str(xs[i]) for i in order]
        ys = [ys[i] for i in order]
        colors = [series_color(x, i, roles) if roles else OKABE_ITO[0] for i, x in enumerate(xs)]
        if chart == "bar":
            ax.bar(xs, ys, color=colors, width=0.65)
        else:
            xs.reverse(); ys.reverse(); colors.reverse()
            ax.barh(xs, ys, color=colors, height=0.65)
        if len(xs) <= 12:
            fmt = "{:,.0f}" if all(abs(v) >= 10 or v == int(v) for v in ys) else "{:,.2f}"
            for container in ax.containers:
                ax.bar_label(container, fmt=fmt.format, fontsize=9, color=MUTED, padding=3)

    if spec.get("y_zero", chart in ("bar", "barh", "area")):
        if chart == "barh":
            ax.set_xlim(left=min(0, ax.get_xlim()[0]))
        else:
            ax.set_ylim(bottom=min(0, ax.get_ylim()[0]))

    value_axis = "x" if chart == "barh" else "y"
    ax.grid(axis=value_axis, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if chart == "barh":
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", length=0)
    else:
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x" if chart != "barh" else "y", rotation=0)

    for ann in spec.get("annotations") or []:
        ax.annotate(
            ann["text"], (ann["x"], ann.get("y", ax.get_ylim()[1] * 0.95)),
            fontsize=9, color=MUTED, style="italic", ha="center",
        )

    fig.suptitle(spec["takeaway"], x=0.01, y=0.99, ha="left", fontsize=13, fontweight="bold", color=INK)
    ax.set_title(spec["subtitle"], fontsize=10, color=MUTED, pad=12)
    fig.text(0.01, 0.01, spec["source_note"], fontsize=8, color=FAINT, ha="left")
    fig.subplots_adjust(top=0.82, bottom=0.16)

    fig.savefig(
        out_path,
        format="svg",
        metadata={
            "Title": spec["takeaway"],
            "Description": spec["alt_text"],
            "Creator": "make_chart.py",
            "Date": None,  # suppress timestamp for reproducible output
        },
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="figure-spec YAML file")
    parser.add_argument("-o", "--output-dir", type=Path, default=None)
    args = parser.parse_args()

    if not args.spec.exists():
        fail([f"spec file not found: {args.spec}"])
    try:
        with open(args.spec, encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail([f"spec is not valid YAML: {e}"])
    if not isinstance(spec, dict):
        fail(["spec: top level must be a mapping"])

    errors: list[str] = []
    rows = load_rows(spec, args.spec.parent, errors)
    validate(spec, rows, errors)
    if errors:
        fail(errors)

    out_dir = args.output_dir or args.spec.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{spec['id']}.svg"
    render(spec, rows, out_path)
    print(out_path)


if __name__ == "__main__":
    main()
