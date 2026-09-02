#!/usr/bin/env python3
"""Generate and serve a review page for eval results.

Reads the workspace directory, discovers runs (directories with outputs/),
embeds all output data into a self-contained HTML page, and serves it via
a tiny HTTP server. Feedback auto-saves to feedback.json in the workspace.

Usage:
    python generate_review.py <workspace-path> [--port PORT] [--skill-name NAME]
    python generate_review.py <workspace-path> --previous-feedback /path/to/old/feedback.json

No dependencies beyond the Python stdlib are required.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import tempfile
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Files to exclude from output listings
METADATA_FILES = {"transcript.md", "user_notes.md", "metrics.json"}

# Extensions we render as inline text
TEXT_EXTENSIONS = {
    ".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".yaml", ".yml", ".xml", ".html", ".css", ".sh", ".rb", ".go", ".rs",
    ".java", ".c", ".cpp", ".h", ".hpp", ".sql", ".r", ".toml",
}

# Raster formats are safe to display as inert image data. Active or document
# formats (including SVG, PDF, and spreadsheets) remain download-only.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
CONFIGURATIONS = ("with_skill", "without_skill")
MAX_FEEDBACK_BYTES = 1024 * 1024
MAX_REVIEWS = 1000
MAX_RUN_ID_CHARS = 512
MAX_FEEDBACK_CHARS = 100_000
MAX_TIMESTAMP_CHARS = 64

# MIME type overrides for common types
MIME_OVERRIDES = {
    ".svg": "image/svg+xml",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def get_mime_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in MIME_OVERRIDES:
        return MIME_OVERRIDES[ext]
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def _read_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def find_runs(workspace: Path) -> list[dict]:
    """Discover only runs in the frozen iteration workspace layout."""
    runs: list[dict] = []
    for eval_dir in sorted(workspace.iterdir()):
        if not eval_dir.is_dir():
            continue
        metadata = _read_object(eval_dir / "eval_metadata.json")
        for configuration in CONFIGURATIONS:
            configuration_dir = eval_dir / configuration
            if not configuration_dir.is_dir():
                continue
            for run_dir in sorted(configuration_dir.iterdir()):
                if not run_dir.is_dir() or re.fullmatch(r"run-[1-9][0-9]*", run_dir.name) is None:
                    continue
                if not (run_dir / "outputs").is_dir():
                    continue
                runs.append(build_run(workspace, run_dir, metadata, configuration))

    def sort_key(run: dict) -> tuple[int, int, str, int, int]:
        eval_id = run.get("eval_id")
        numbered = isinstance(eval_id, int) and not isinstance(eval_id, bool)
        return (
            0 if numbered else 1,
            eval_id if numbered else 0,
            str(run["eval_name"]),
            CONFIGURATIONS.index(run["configuration"]),
            int(run["run_number"]),
        )

    runs.sort(key=sort_key)
    return runs


def build_run(
    root: Path,
    run_dir: Path,
    metadata: dict | None = None,
    configuration: str | None = None,
) -> dict:
    """Build one run record from its contract-defined directory."""
    metadata = metadata or _read_object(run_dir.parent.parent / "eval_metadata.json")
    configuration = configuration or run_dir.parent.name
    prompt = metadata.get("prompt") if isinstance(metadata.get("prompt"), str) else ""
    eval_id = metadata.get("eval_id")
    if not isinstance(eval_id, int) or isinstance(eval_id, bool):
        eval_id = None

    if not prompt:
        for candidate in (run_dir / "transcript.md", run_dir / "outputs/transcript.md"):
            if not candidate.is_file():
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except OSError:
                continue
            match = re.search(r"## Eval Prompt\n\n([\s\S]*?)(?=\n##|$)", text)
            if match:
                prompt = match.group(1).strip()
                break
    if not prompt:
        prompt = "(No prompt found)"

    outputs_dir = run_dir / "outputs"
    output_files = [
        embed_file(path)
        for path in sorted(outputs_dir.iterdir())
        if path.is_file() and path.name not in METADATA_FILES
    ]
    grading = _read_object(run_dir / "grading.json") or None
    eval_name = metadata.get("eval_name")
    if not isinstance(eval_name, str) or not eval_name:
        eval_name = run_dir.parent.parent.name

    return {
        "id": os.fspath(run_dir.relative_to(root)).replace(os.sep, "-"),
        "prompt": prompt,
        "eval_id": eval_id,
        "eval_name": eval_name,
        "configuration": configuration,
        "run_number": int(run_dir.name.removeprefix("run-")),
        "outputs": output_files,
        "grading": grading,
    }


def embed_file(path: Path) -> dict:
    """Read a file and return an embedded representation."""
    ext = path.suffix.lower()
    mime = get_mime_type(path)

    if ext in TEXT_EXTENSIONS:
        try:
            content = path.read_text(errors="replace")
        except OSError:
            content = "(Error reading file)"
        return {
            "name": path.name,
            "type": "text",
            "content": content,
        }
    elif ext in IMAGE_EXTENSIONS:
        try:
            raw = path.read_bytes()
            b64 = base64.b64encode(raw).decode("ascii")
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        return {
            "name": path.name,
            "type": "image",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }
    else:
        # Active/document formats and unknown binaries are download-only.
        try:
            raw = path.read_bytes()
            b64 = base64.b64encode(raw).decode("ascii")
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        embedded = {
            "name": path.name,
            "type": "binary",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }
        if ext == ".xlsx":
            embedded["notice"] = "Spreadsheet preview unavailable offline. Download the file to review it safely."
        elif ext in {".pdf", ".svg"}:
            embedded["notice"] = "Preview disabled for safety. Download the file to review it."
        return embedded


def load_previous_iteration(workspace: Path) -> dict[str, dict]:
    """Load previous iteration's feedback and outputs.

    Returns a map of run_id -> {"feedback": str, "outputs": list[dict]}.
    """
    result: dict[str, dict] = {}

    # Load feedback
    feedback_map: dict[str, str] = {}
    feedback_path = workspace / "feedback.json"
    if feedback_path.exists():
        try:
            data = json.loads(feedback_path.read_text())
            feedback_map = {
                r["run_id"]: r["feedback"]
                for r in data.get("reviews", [])
                if r.get("feedback", "").strip()
            }
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    # Load runs (to get outputs)
    prev_runs = find_runs(workspace)
    for run in prev_runs:
        result[run["id"]] = {
            "feedback": feedback_map.get(run["id"], ""),
            "outputs": run.get("outputs", []),
        }

    # Also add feedback for run_ids that had feedback but no matching run
    for run_id, fb in feedback_map.items():
        if run_id not in result:
            result[run_id] = {"feedback": fb, "outputs": []}

    return result


def generate_html(
    runs: list[dict],
    skill_name: str,
    previous: dict[str, dict] | None = None,
    benchmark: dict | None = None,
) -> str:
    """Generate the complete standalone HTML page with embedded data."""
    template_path = Path(__file__).parent / "viewer.html"
    template = template_path.read_text()

    # Build previous_feedback and previous_outputs maps for the template
    previous_feedback: dict[str, str] = {}
    previous_outputs: dict[str, list[dict]] = {}
    if previous:
        for run_id, data in previous.items():
            if data.get("feedback"):
                previous_feedback[run_id] = data["feedback"]
            if data.get("outputs"):
                previous_outputs[run_id] = data["outputs"]

    embedded = {
        "skill_name": skill_name,
        "runs": runs,
        "previous_feedback": previous_feedback,
        "previous_outputs": previous_outputs,
    }
    if benchmark:
        embedded["benchmark"] = benchmark

    data_json = json.dumps(embedded, ensure_ascii=True)
    # HTML parses a script end tag before JavaScript parses its string. Escaping
    # markup characters keeps executor-controlled values inside the data object.
    data_json = data_json.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")

    return template.replace("/*__EMBEDDED_DATA__*/", f"const EMBEDDED_DATA = {data_json};")


# ---------------------------------------------------------------------------
# HTTP server (stdlib only, zero dependencies)
# ---------------------------------------------------------------------------

def _write_text_atomically(path: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary_path, path)
    except BaseException:
        try:
            temporary_path.unlink()
        except OSError:
            pass
        raise


def validate_feedback(data: object) -> dict:
    """Return validated feedback or raise ValueError without touching disk."""
    if not isinstance(data, dict) or set(data) != {"reviews", "status"}:
        raise ValueError("feedback must contain only 'reviews' and 'status'")
    reviews = data["reviews"]
    status = data["status"]
    if status not in {"in_progress", "complete"}:
        raise ValueError("feedback status must be 'in_progress' or 'complete'")
    if not isinstance(reviews, list) or len(reviews) > MAX_REVIEWS:
        raise ValueError(f"reviews must be an array of at most {MAX_REVIEWS} items")

    seen: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict) or set(review) != {"run_id", "feedback", "timestamp"}:
            raise ValueError("each review must contain only run_id, feedback, and timestamp")
        run_id = review["run_id"]
        feedback = review["feedback"]
        timestamp = review["timestamp"]
        if not isinstance(run_id, str) or not run_id or len(run_id) > MAX_RUN_ID_CHARS:
            raise ValueError("review run_id must be a bounded non-empty string")
        if run_id in seen:
            raise ValueError("review run_id values must be unique")
        seen.add(run_id)
        if not isinstance(feedback, str) or len(feedback) > MAX_FEEDBACK_CHARS:
            raise ValueError("review feedback must be a bounded string")
        if not isinstance(timestamp, str) or not timestamp or len(timestamp) > MAX_TIMESTAMP_CHARS:
            raise ValueError("review timestamp must be a bounded non-empty string")
    return data


class ReviewHandler(BaseHTTPRequestHandler):
    """Serves the review HTML and handles feedback saves.

    Regenerates the HTML on each page load so that refreshing the browser
    picks up new eval outputs without restarting the server.
    """

    def __init__(
        self,
        workspace: Path,
        skill_name: str,
        feedback_path: Path,
        previous: dict[str, dict],
        benchmark_path: Path | None,
        *args,
        **kwargs,
    ):
        self.workspace = workspace
        self.skill_name = skill_name
        self.feedback_path = feedback_path
        self.previous = previous
        self.benchmark_path = benchmark_path
        super().__init__(*args, **kwargs)

    def _send(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, status: int, value: dict) -> None:
        self._send(status, json.dumps(value, separators=(",", ":")).encode("utf-8"), "application/json")

    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            runs = find_runs(self.workspace)
            benchmark = None
            if self.benchmark_path and self.benchmark_path.exists():
                benchmark = _read_object(self.benchmark_path) or None
            content = generate_html(runs, self.skill_name, self.previous, benchmark).encode("utf-8")
            self._send(200, content, "text/html; charset=utf-8")
        elif self.path == "/api/feedback":
            try:
                if self.feedback_path.is_symlink():
                    raise OSError("feedback path must not be a symlink")
                content = self.feedback_path.read_bytes() if self.feedback_path.exists() else b"{}"
            except OSError:
                self._send_json(500, {"error": "unable to read feedback.json"})
                return
            self._send(200, content, "application/json")
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/feedback":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._send_json(400, {"error": "invalid Content-Length"})
            return
        if length < 0:
            self._send_json(400, {"error": "invalid Content-Length"})
            return
        if length > MAX_FEEDBACK_BYTES:
            self._send_json(413, {"error": "feedback payload is too large"})
            return

        body = self.rfile.read(length)
        try:
            data = validate_feedback(json.loads(body))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            self._send_json(400, {"error": str(error)})
            return
        try:
            _write_text_atomically(
                self.feedback_path,
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            )
        except OSError:
            self._send_json(500, {"error": "unable to write feedback.json"})
            return
        self._send_json(200, {"ok": True})

    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and serve eval review")
    parser.add_argument("workspace", type=Path, help="Path to workspace directory")
    parser.add_argument("--port", "-p", type=int, default=3117, help="Server port (default: 3117)")
    parser.add_argument("--skill-name", "-n", type=str, default=None, help="Skill name for header")
    parser.add_argument(
        "--previous-workspace", type=Path, default=None,
        help="Path to previous iteration's workspace (shows old outputs and feedback as context)",
    )
    parser.add_argument(
        "--benchmark", type=Path, default=None,
        help="Path to benchmark.json to show in the Benchmark tab",
    )
    parser.add_argument(
        "--static", "-s", type=Path, default=None,
        help="Write standalone HTML to this path instead of starting a server",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"Error: {workspace} is not a directory", file=sys.stderr)
        sys.exit(1)

    runs = find_runs(workspace)
    if not runs:
        print(f"No runs found in {workspace}", file=sys.stderr)
        sys.exit(1)

    skill_name = args.skill_name or workspace.name.replace("-workspace", "")
    feedback_path = workspace / "feedback.json"

    previous: dict[str, dict] = {}
    if args.previous_workspace:
        previous = load_previous_iteration(args.previous_workspace.resolve())

    benchmark_path = args.benchmark.resolve() if args.benchmark else None
    benchmark = _read_object(benchmark_path) if benchmark_path and benchmark_path.exists() else None

    if args.static:
        html = generate_html(runs, skill_name, previous, benchmark)
        args.static.parent.mkdir(parents=True, exist_ok=True)
        args.static.write_text(html, encoding="utf-8")
        print(json.dumps({
            "event": "opin.viewer.static_written",
            "path": os.fspath(args.static.resolve()),
            "feedback_filename": "feedback.json",
        }), flush=True)
        sys.exit(0)

    if not 0 <= args.port <= 65535:
        print("Error: port must be between 0 and 65535", file=sys.stderr)
        sys.exit(2)

    handler = partial(ReviewHandler, workspace, skill_name, feedback_path, previous, benchmark_path)
    try:
        server = HTTPServer(("127.0.0.1", args.port), handler)
    except OSError:
        if args.port == 0:
            raise
        server = HTTPServer(("127.0.0.1", 0), handler)
    port = int(server.server_address[1])
    pid_path = workspace / "viewer.pid"
    try:
        _write_text_atomically(pid_path, f"{os.getpid()}\n")
    except OSError as error:
        server.server_close()
        print(f"Error: unable to write {pid_path}: {error}", file=sys.stderr)
        sys.exit(1)

    startup = {
        "event": "opin.viewer.started",
        "host": "127.0.0.1",
        "port": port,
        "requested_port": args.port,
        "url": f"http://127.0.0.1:{port}",
        "pid": os.getpid(),
        "pid_path": os.fspath(pid_path),
        "workspace": os.fspath(workspace),
        "feedback_path": os.fspath(feedback_path),
        "message": "Open the URL, review in Pi, and submit feedback to feedback.json.",
    }
    print(json.dumps(startup, sort_keys=True), flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
