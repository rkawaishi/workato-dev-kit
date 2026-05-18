#!/usr/bin/env python3
"""Tests for `scripts/ensure-workatoignore.sh`.

Run with:
    python3 scripts/tests/test_ensure_workatoignore.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SCRIPT = REPO / "scripts" / "ensure-workatoignore.sh"
TEMPLATE = REPO / "templates" / "workatoignore.template"


def run(project_dir: str) -> subprocess.CompletedProcess:
    """Invoke the helper against project_dir."""
    return subprocess.run(
        ["bash", str(SCRIPT), project_dir],
        capture_output=True, text=True,
    )


def lines(path: Path) -> list[str]:
    return path.read_text().splitlines()


# ---------------------------------------------------------------------------
# Create from template
# ---------------------------------------------------------------------------

def test_creates_when_absent():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "myproj"
        proj.mkdir()
        r = run(str(proj))
        assert r.returncode == 0, r.stderr
        woi = proj / ".workatoignore"
        assert woi.exists()
        body = lines(woi)
        # Core + opt-out content is all present on a fresh create.
        for entry in ("specs/", "DESIGN.md", "DESIGN.md.legacy.*",
                      "CATALOG.md", ".workatoignore",
                      "*.custom_adapter.rb", "*.custom_adapter.json"):
            assert entry in body, f"missing {entry!r}"
        assert any(">>> opt-out" in ln for ln in body)


def test_created_file_matches_template_exactly():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        run(str(proj))
        assert (proj / ".workatoignore").read_text() == TEMPLATE.read_text()


# ---------------------------------------------------------------------------
# Top up an existing file
# ---------------------------------------------------------------------------

def test_tops_up_old_file_without_optout_block():
    """A pre-this-PR .workatoignore (no opt-out block) must receive both the
    missing core entries AND the connector opt-out block."""
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        (proj / ".workatoignore").write_text("specs/\n")
        r = run(str(proj))
        assert r.returncode == 0, r.stderr
        body = lines(proj / ".workatoignore")
        assert "DESIGN.md" in body            # core topped up
        assert "*.custom_adapter.rb" in body  # opt-out block added
        assert "*.custom_adapter.json" in body
        assert any(">>> opt-out" in ln for ln in body)
        assert body.count("specs/") == 1      # no duplication


def test_preserves_user_lines():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        (proj / ".workatoignore").write_text("specs/\nmy-private-notes.txt\n")
        run(str(proj))
        body = lines(proj / ".workatoignore")
        assert "my-private-notes.txt" in body


# ---------------------------------------------------------------------------
# Connector opt-out is sticky
# ---------------------------------------------------------------------------

def test_optout_respected_when_block_present():
    """If the opt-out block markers are present but the connector lines were
    deleted (the user manages a connector as code), the helper must NOT
    re-add them."""
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        # Created file, then connector lines removed but markers kept.
        run(str(proj))
        woi = proj / ".workatoignore"
        kept = [ln for ln in lines(woi) if "custom_adapter" not in ln]
        woi.write_text("\n".join(kept) + "\n")
        assert any(">>> opt-out" in ln for ln in kept)  # markers still there

        r = run(str(proj))
        assert r.returncode == 0, r.stderr
        body = lines(woi)
        assert not any("custom_adapter" in ln for ln in body), \
            "opt-out broken: connector lines were re-added"
        assert sum(">>> opt-out" in ln for ln in body) == 1  # no duplicate block


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------

def test_idempotent_on_created_file():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        run(str(proj))
        first = (proj / ".workatoignore").read_text()
        run(str(proj))
        run(str(proj))
        assert (proj / ".workatoignore").read_text() == first


def test_idempotent_after_topup():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "p"
        proj.mkdir()
        (proj / ".workatoignore").write_text("specs/\n")
        run(str(proj))
        after_first = (proj / ".workatoignore").read_text()
        run(str(proj))
        assert (proj / ".workatoignore").read_text() == after_first


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_missing_argument_exits_2():
    r = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode == 2, r.returncode


def test_missing_project_dir_exits_1():
    with tempfile.TemporaryDirectory() as d:
        r = run(str(Path(d) / "does-not-exist"))
        assert r.returncode == 1, r.returncode


def main() -> int:
    tests = [(name, obj) for name, obj in sorted(globals().items())
             if name.startswith("test_") and callable(obj)]
    failures: list[tuple[str, str]] = []
    for name, fn in tests:
        try:
            fn()
            print(f"  ok  {name}")
        except Exception:
            failures.append((name, traceback.format_exc()))
            print(f"  FAIL {name}")

    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
