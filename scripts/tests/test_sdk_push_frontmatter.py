#!/usr/bin/env python3
"""Regression tests for the connector-docs frontmatter helpers in
`scripts/workato-api.py` that back `sdk push` auto-detect/persist.

Run with:
    python3 scripts/tests/test_sdk_push_frontmatter.py

Intentionally stdlib-only and importlib-based so CI doesn't need a test
runner or the script on sys.path.
"""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "workato-api.py"

spec = importlib.util.spec_from_file_location("workato_api", SCRIPT)
wa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wa)


def _tmp_connector_rb(tmp: Path, name: str = "foo") -> Path:
    """Create `<tmp>/connectors/<name>/connector.rb` and return its path."""
    rb = tmp / "connectors" / name / "connector.rb"
    rb.parent.mkdir(parents=True)
    rb.write_text("{ title: 'Foo' }\n")
    return rb


def test_read_frontmatter_missing_file():
    with tempfile.TemporaryDirectory() as d:
        fm, body = wa._read_frontmatter(Path(d) / "nope.md")
        assert fm == {} and body == ""


def test_read_frontmatter_no_fm():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.md"
        p.write_text("# Hello\n\nbody\n")
        fm, body = wa._read_frontmatter(p)
        assert fm == {}
        assert "# Hello" in body


def test_read_frontmatter_parses_flat_kv():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.md"
        p.write_text("---\nconnector_id: 42\ntitle: Foo\n---\n\n# Hello\n")
        fm, body = wa._read_frontmatter(p)
        assert fm == {"connector_id": "42", "title": "Foo"}
        assert "# Hello" in body


def test_write_frontmatter_creates_stub_when_missing():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "docs" / "my_conn.md"
        wa._write_frontmatter(p, {"connector_id": "99"}, connector_name="my_conn")
        text = p.read_text()
        assert text.startswith("---\nconnector_id: 99\n---\n")
        assert "my_conn コネクタ" in text


def test_write_frontmatter_preserves_body_on_update():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.md"
        p.write_text("---\nconnector_id: 1\n---\n\n# Body\nStuff\n")
        fm, _ = wa._read_frontmatter(p)
        fm["connector_id"] = "2"
        wa._write_frontmatter(p, fm)
        text = p.read_text()
        assert "connector_id: 2" in text
        assert "# Body" in text
        assert "Stuff" in text


def test_write_frontmatter_does_not_duplicate_when_body_empty():
    # Regression: a file containing only frontmatter (no body) previously
    # re-read raw text as the body, producing two `---` blocks.
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.md"
        p.write_text("---\nconnector_id: 123\n---\n")
        fm, _ = wa._read_frontmatter(p)
        fm["connector_id"] = "456"
        wa._write_frontmatter(p, fm)
        text = p.read_text()
        assert text.count("---\n") == 2, f"expected 2 `---` lines, got:\n{text}"
        assert "connector_id: 456" in text
        assert "connector_id: 123" not in text


def test_connector_docs_path_layout():
    with tempfile.TemporaryDirectory() as d:
        rb = _tmp_connector_rb(Path(d), "my_conn")
        expected = (Path(d) / "connectors" / "docs" / "my_conn.md").resolve()
        assert wa._connector_docs_path(rb) == expected


def test_resolve_connector_id_no_docs_returns_none():
    with tempfile.TemporaryDirectory() as d:
        rb = _tmp_connector_rb(Path(d))
        rid, dp = wa._resolve_connector_id(rb, None)
        assert rid is None
        assert dp == (Path(d) / "connectors" / "docs" / "foo.md").resolve()


def test_resolve_connector_id_reads_frontmatter():
    with tempfile.TemporaryDirectory() as d:
        rb = _tmp_connector_rb(Path(d))
        docs = Path(d) / "connectors" / "docs"
        docs.mkdir()
        (docs / "foo.md").write_text("---\nconnector_id: 123\n---\n# Foo\n")
        rid, _ = wa._resolve_connector_id(rb, None)
        assert rid == 123


def test_resolve_connector_id_explicit_wins():
    with tempfile.TemporaryDirectory() as d:
        rb = _tmp_connector_rb(Path(d))
        docs = Path(d) / "connectors" / "docs"
        docs.mkdir()
        (docs / "foo.md").write_text("---\nconnector_id: 123\n---\n")
        rid, _ = wa._resolve_connector_id(rb, 999)
        assert rid == 999


def test_resolve_connector_id_non_integer_warns_and_degrades():
    with tempfile.TemporaryDirectory() as d:
        rb = _tmp_connector_rb(Path(d))
        docs = Path(d) / "connectors" / "docs"
        docs.mkdir()
        (docs / "foo.md").write_text("---\nconnector_id: abc\n---\n")
        saved = sys.stderr
        sys.stderr = io.StringIO()
        try:
            rid, _ = wa._resolve_connector_id(rb, None)
            err = sys.stderr.getvalue()
        finally:
            sys.stderr = saved
        assert rid is None
        assert "not an integer" in err


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
