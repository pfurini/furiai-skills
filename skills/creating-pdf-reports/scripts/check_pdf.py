# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf>=5.0"]
# ///
"""Check a generated PDF for self-containment and baseline accessibility.

Usage:
    uv run check_pdf.py <report.pdf> [--require-tagged]

Checks (FAIL blocks delivery, WARN needs a stated reason to ship):
  - document metadata: title (FAIL), author and subject (WARN)
  - document language set (FAIL: screen readers need it)
  - tagged structure tree (WARN, or FAIL with --require-tagged)
  - every used font embedded (FAIL: unembedded fonts render differently
    on other machines, breaking the "portable" requirement)
  - text layer extractable (FAIL: image-only text is unsearchable and
    inaccessible)
  - bookmarks/outline present for documents of 10+ pages (WARN)

Exit code 0 = no FAIL. This is a baseline gate, not a conformance
certificate: for PDF/A or PDF/UA claims, run veraPDF as well
(references/pdf-standards.md).
"""

from __future__ import annotations

import argparse
import sys

from pypdf import PdfReader

results: list[tuple[str, str]] = []  # (level, message)


def report(level: str, message: str) -> None:
    results.append((level, message))
    print(f"[{level}] {message}")


def font_is_embedded(font) -> bool:
    font = font.get_object()
    if font.get("/Subtype") == "/Type0":
        descendants = font.get("/DescendantFonts")
        if descendants:
            return font_is_embedded(descendants[0])
        return False
    if font.get("/Subtype") == "/Type3":
        return True  # Type3 glyphs are defined inside the PDF itself
    descriptor = font.get("/FontDescriptor")
    if descriptor is None:
        return False
    descriptor = descriptor.get_object()
    return any(k in descriptor for k in ("/FontFile", "/FontFile2", "/FontFile3"))


def check(path: str, require_tagged: bool) -> int:
    reader = PdfReader(path)
    n_pages = len(reader.pages)
    print(f"{path}: {n_pages} page(s)")

    meta = reader.metadata or {}
    if meta.get("/Title"):
        report("PASS", f"title: {meta['/Title']}")
    else:
        report("FAIL", "no document title in metadata")
    for key in ("/Author", "/Subject"):
        if meta.get(key):
            report("PASS", f"{key[1:].lower()}: {meta[key]}")
        else:
            report("WARN", f"no {key[1:].lower()} in metadata")

    root = reader.trailer["/Root"]
    lang = root.get("/Lang")
    if lang:
        report("PASS", f"document language: {lang}")
    else:
        report("FAIL", "no document language (/Lang) set")

    mark_info = root.get("/MarkInfo")
    tagged = bool(mark_info and mark_info.get_object().get("/Marked")) and "/StructTreeRoot" in root
    if tagged:
        report("PASS", "tagged PDF (structure tree present)")
    else:
        report("FAIL" if require_tagged else "WARN", "not a tagged PDF (no structure tree)")

    unembedded: set[str] = set()
    seen: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources")
        if not resources:
            continue
        fonts = resources.get_object().get("/Font")
        if not fonts:
            continue
        for name, font in fonts.get_object().items():
            font_obj = font.get_object()
            base = str(font_obj.get("/BaseFont", name))
            if base in seen:
                continue
            seen.add(base)
            if not font_is_embedded(font_obj):
                unembedded.add(base)
    if not seen:
        report("WARN", "no fonts found (text-free document?)")
    elif unembedded:
        report("FAIL", f"unembedded font(s): {', '.join(sorted(unembedded))}")
    else:
        report("PASS", f"all {len(seen)} font(s) embedded")

    # Sample up to the first 5 pages: enough to detect an image-only PDF
    # without reparsing a large document.
    extracted = any((page.extract_text() or "").strip() for page in reader.pages[:5])
    if extracted:
        report("PASS", "text layer extractable")
    else:
        report("FAIL", "no extractable text on the first pages (image-only PDF?)")

    if n_pages >= 10 and not reader.outline:
        report("WARN", f"{n_pages} pages but no bookmarks/outline")
    elif reader.outline:
        report("PASS", "bookmarks/outline present")

    failures = [m for level, m in results if level == "FAIL"]
    warnings = [m for level, m in results if level == "WARN"]
    print(f"\n{len(failures)} failure(s), {len(warnings)} warning(s)")
    return 1 if failures else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("--require-tagged", action="store_true",
                        help="treat a missing structure tree as FAIL (accessibility required)")
    args = parser.parse_args()
    sys.exit(check(args.pdf, args.require_tagged))


if __name__ == "__main__":
    main()
