"""Offline regression tests for the local Pi evaluation review viewer."""

from __future__ import annotations

import http.client
import importlib.util
import json
import os
import select
import signal
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from conftest import SKILL_ROOT, TEST_ROOT

VIEWER_ROOT = SKILL_ROOT / "eval-viewer"
VIEWER_SCRIPT = VIEWER_ROOT / "generate_review.py"
VIEWER_FIXTURES = TEST_ROOT / "fixtures/viewer"
MAX_STARTUP_SECONDS = 10


def _load_viewer_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("opin_generate_review", VIEWER_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_run(
    workspace: Path,
    eval_name: str,
    configuration: str,
    *,
    eval_id: int | None,
    output_names: tuple[str, ...] = ("result.txt",),
) -> Path:
    eval_root = workspace / eval_name
    run_root = eval_root / configuration / "run-1"
    outputs = run_root / "outputs"
    outputs.mkdir(parents=True)
    if eval_id is not None:
        metadata = {"eval_id": eval_id, "eval_name": eval_name, "prompt": f"Prompt for {eval_name}"}
        encoded = json.dumps(metadata) + "\n"
        (eval_root / "eval_metadata.json").write_text(encoded, encoding="utf-8")
        # The pre-hardening viewer only checks this legacy location. Keeping it here
        # makes the focused regression exercise its mixed-id sorting defect.
        (run_root.parent / "eval_metadata.json").write_text(encoded, encoding="utf-8")
    for name in output_names:
        source = VIEWER_FIXTURES / name
        destination = outputs / name
        if source.exists():
            destination.write_bytes(source.read_bytes())
        else:
            destination.write_text(f"Output for {eval_name}\n", encoding="utf-8")
    return run_root


@contextmanager
def _occupied_port() -> Iterator[tuple[int, subprocess.Popen[str]]]:
    code = """
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 0))
s.listen()
print(s.getsockname()[1], flush=True)
while True:
    conn, _ = s.accept()
    conn.close()
"""
    process = subprocess.Popen(
        [sys.executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    port = int(process.stdout.readline().strip())
    try:
        yield port, process
    finally:
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=5)


def _read_startup(process: subprocess.Popen[str]) -> dict[str, Any]:
    assert process.stdout is not None
    ready, _, _ = select.select([process.stdout], [], [], MAX_STARTUP_SECONDS)
    assert ready, "viewer did not emit startup metadata"
    line = process.stdout.readline()
    assert line, f"viewer exited before startup: {process.stderr.read() if process.stderr else ''}"
    return json.loads(line)


def _launch_viewer(workspace: Path, port: int) -> tuple[subprocess.Popen[str], dict[str, Any]]:
    process = subprocess.Popen(
        [
            sys.executable,
            os.fspath(VIEWER_SCRIPT),
            os.fspath(workspace),
            "--port",
            str(port),
            "--skill-name",
            "Pi fixture </script><script>globalThis.bad=true</script>",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )
    try:
        return process, _read_startup(process)
    except BaseException:
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=5)
        raise


def _stop_viewer(process: subprocess.Popen[str]) -> None:
    if process.poll() is None:
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)


def test_occupied_port_untrusted_script_and_missing_eval_id_are_safe(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign-safe/iteration-2"
    _make_run(
        workspace,
        "numbered-eval",
        "with_skill",
        eval_id=1,
        output_names=("untrusted-output.txt",),
    )
    _make_run(workspace, "unnumbered-eval", "without_skill", eval_id=None)

    with _occupied_port() as (requested_port, existing_listener):
        viewer, startup = _launch_viewer(workspace, requested_port)
        try:
            assert existing_listener.poll() is None
            assert startup["event"] == "opin.viewer.started"
            assert startup["host"] == "127.0.0.1"
            assert startup["requested_port"] == requested_port
            assert startup["port"] != requested_port
            assert startup["feedback_path"] == os.fspath(workspace / "feedback.json")
            assert startup["pid_path"] == os.fspath(workspace / "viewer.pid")
            assert (workspace / "viewer.pid").read_text(encoding="utf-8") == f"{viewer.pid}\n"

            connection = http.client.HTTPConnection("127.0.0.1", startup["port"], timeout=5)
            connection.request("GET", "/")
            response = connection.getresponse()
            html = response.read().decode("utf-8")
            connection.close()

            assert response.status == 200
            assert "</script><script>globalThis.viewerCompromised" not in html
            assert "</script><script>globalThis.bad" not in html
            assert "\\u003c/script\\u003e" in html
            assert html.index("numbered-eval") < html.index("unnumbered-eval")
            assert "https://" not in html
            assert "http://" not in html
        finally:
            _stop_viewer(viewer)


def test_discovery_uses_only_campaign_run_layout_and_configuration_badges(tmp_path: Path) -> None:
    viewer = _load_viewer_module()
    workspace = tmp_path / "iteration-1"
    _make_run(workspace, "second", "without_skill", eval_id=2)
    _make_run(workspace, "first", "with_skill", eval_id=1)
    _make_run(workspace, "missing", "without_skill", eval_id=None)
    _make_run(workspace, "ignored", "old_skill", eval_id=0)
    (workspace / "loose/outputs").mkdir(parents=True)

    runs = viewer.find_runs(workspace)

    assert [(run["eval_id"], run["configuration"]) for run in runs] == [
        (1, "with_skill"),
        (2, "without_skill"),
        (None, "without_skill"),
    ]
    html = viewer.generate_html(runs, "Pi fixture")
    assert "new_skill|old_skill" not in html
    assert "run.configuration" in html


def test_artifacts_render_as_text_or_inert_downloads_without_remote_assets(tmp_path: Path) -> None:
    viewer = _load_viewer_module()
    workspace = tmp_path / "iteration-1"
    run_root = _make_run(
        workspace,
        "artifact-safety",
        "with_skill",
        eval_id=1,
        output_names=("untrusted-output.txt", "sample.xlsx"),
    )
    svg = run_root / "outputs/vector.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>\n')
    pdf = run_root / "outputs/document.pdf"
    pdf.write_bytes(b"%PDF-1.4 fixture")

    runs = viewer.find_runs(workspace)
    types = {item["name"]: item["type"] for item in runs[0]["outputs"]}
    html = viewer.generate_html(runs, "Pi fixture")

    assert types == {
        "document.pdf": "binary",
        "sample.xlsx": "binary",
        "untrusted-output.txt": "text",
        "vector.svg": "binary",
    }
    assert "XLSX.read" not in html
    assert "Spreadsheet preview unavailable offline" in html
    assert "iframe.src" not in html
    assert "fonts.googleapis.com" not in html
    assert "cdn.sheetjs.com" not in html
    assert "pre.textContent = file.content" in html


def test_feedback_endpoint_validates_shape_size_and_fixed_destination(tmp_path: Path) -> None:
    workspace = tmp_path / "iteration-1"
    _make_run(workspace, "feedback-eval", "with_skill", eval_id=1)
    viewer, startup = _launch_viewer(workspace, 0)
    feedback_path = workspace / "feedback.json"
    outside_path = tmp_path / "outside.json"

    def post(path: str, payload: bytes) -> tuple[int, bytes]:
        connection = http.client.HTTPConnection("127.0.0.1", startup["port"], timeout=5)
        connection.request(
            "POST",
            path,
            body=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
        )
        response = connection.getresponse()
        body = response.read()
        connection.close()
        return response.status, body

    try:
        valid = {
            "reviews": [
                {
                    "run_id": "feedback-eval-with_skill-run-1",
                    "feedback": "Looks correct.",
                    "timestamp": "2026-09-02T12:00:00.000Z",
                }
            ],
            "status": "complete",
        }
        status, body = post("/api/feedback", json.dumps(valid).encode("utf-8"))
        assert status == 200
        assert json.loads(body) == {"ok": True}
        assert json.loads(feedback_path.read_text(encoding="utf-8")) == valid

        original = feedback_path.read_bytes()
        bad_payloads = (
            b"[]",
            b'{"reviews":"wrong","status":"complete"}',
            b'{"reviews":[{"run_id":"x","feedback":1,"timestamp":"now"}],"status":"complete"}',
            b'{"reviews":[],"status":"unknown"}',
            b'{"reviews":[],"status":"complete","path":"../../outside.json"}',
        )
        for payload in bad_payloads:
            status, _ = post("/api/feedback", payload)
            assert status == 400
            assert feedback_path.read_bytes() == original

        status, _ = post("/api/feedback?path=" + os.fspath(outside_path), b"{}")
        assert status == 404
        assert not outside_path.exists()

        connection = http.client.HTTPConnection("127.0.0.1", startup["port"], timeout=5)
        connection.putrequest("POST", "/api/feedback")
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Length", str(1024 * 1024 + 1))
        connection.endheaders()
        response = connection.getresponse()
        response.read()
        connection.close()
        assert response.status == 413
        assert feedback_path.read_bytes() == original
    finally:
        _stop_viewer(viewer)


def test_atomic_feedback_write_preserves_existing_file_on_filesystem_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    viewer = _load_viewer_module()
    feedback_path = tmp_path / "feedback.json"
    feedback_path.write_text('{"original":true}\n', encoding="utf-8")

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError(f"cannot replace {source} with {destination}")

    monkeypatch.setattr(viewer.os, "replace", fail_replace)
    with pytest.raises(OSError, match="cannot replace"):
        viewer._write_text_atomically(feedback_path, '{"replacement":true}\n')

    assert feedback_path.read_text(encoding="utf-8") == '{"original":true}\n'
    assert list(tmp_path.iterdir()) == [feedback_path]


def test_viewer_assets_are_offline_and_name_pi_feedback_flow() -> None:
    viewer_template = (VIEWER_ROOT / "viewer.html").read_text(encoding="utf-8")
    eval_template = (SKILL_ROOT / "assets/eval_review.html").read_text(encoding="utf-8")

    for template in (viewer_template, eval_template):
        assert "https://" not in template
        assert "http://" not in template
    assert "Claude Code" not in viewer_template
    assert "Pi session" in viewer_template
    assert "feedback.json" in viewer_template
