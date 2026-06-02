#!/usr/bin/env python3
"""Tests for `sdk test` (local connector lint).

Covers:
  - _ruby_syntax_check: rc passthrough, missing binary → 127
  - _inspect_connector_structure: detects top-level keys, ignores
    comments, ignores deeply-indented keys
  - cmd_sdk_test: file missing → 1, syntax OK → 0, syntax error → 1,
    missing ruby → 127, warning when title/connection absent

Run with:
    python3 scripts/tests/test_sdk_test.py
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "workato-api.py"

spec = importlib.util.spec_from_file_location("workato_api", SCRIPT)
wa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wa)


def _capture_stdout_stderr_exit(fn):
    saved_out, saved_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
    exited = False
    code = 0
    try:
        try:
            fn()
        except SystemExit as e:
            exited = True
            code = int(e.code) if isinstance(e.code, int) else 1
        return exited, code, sys.stdout.getvalue(), sys.stderr.getvalue()
    finally:
        sys.stdout, sys.stderr = saved_out, saved_err


def _patch_subprocess_run_to_raise():
    import subprocess as _sp
    saved = _sp.run

    def boom(*_a, **_kw):
        raise FileNotFoundError("no ruby")

    _sp.run = boom
    return lambda: setattr(_sp, "run", saved)


# ---------------------------------------------------------------------------
# _ruby_syntax_check
# ---------------------------------------------------------------------------


def test_ruby_check_returns_127_when_ruby_missing():
    restore = _patch_subprocess_run_to_raise()
    try:
        rc, _out, err = wa._ruby_syntax_check(Path("/tmp/x.rb"))
        assert rc == 127
        assert "ruby" in err
        assert "PATH" in err
    finally:
        restore()


def test_ruby_check_runner_injection_passes_argv():
    captured: list = []

    def runner(argv, _cwd):
        captured.append(list(argv))
        return 0, "", ""

    rc, _, _ = wa._ruby_syntax_check(Path("/path/foo.rb"), _runner=runner)
    assert rc == 0
    assert captured == [["ruby", "-c", "/path/foo.rb"]]


# ---------------------------------------------------------------------------
# _inspect_connector_structure
# ---------------------------------------------------------------------------


def test_structure_detects_top_level_keys():
    src = """{
  title: 'Foo',
  connection: {
    fields: [],
  },
  actions: {
    create_thing: {
      ...
    }
  },
  triggers: {},
  methods: {},
}
"""
    s = wa._inspect_connector_structure(src)
    assert "title" in s["found"]
    assert "connection" in s["found"]
    assert "actions" in s["found"]
    assert "triggers" in s["found"]
    assert "methods" in s["found"]
    assert "object_definitions" in s["missing"]
    assert "pick_lists" in s["missing"]


def test_structure_ignores_comments():
    """A `# connection: ...` comment must NOT count as a found key."""
    src = """{
  title: 'X',
  # connection: would-be commented-out
  # actions: not-real-actions
}
"""
    s = wa._inspect_connector_structure(src)
    assert "title" in s["found"]
    assert "connection" in s["missing"]
    assert "actions" in s["missing"]


def test_structure_ignores_deeply_indented_keys():
    """A nested `actions:` inside connection should NOT register as
    a top-level actions block."""
    src = """{
  title: 'X',
  connection: {
    fields: [],
    authorization: {
      type: 'custom_auth',
        actions: 'fake-nested',
    },
  },
}
"""
    s = wa._inspect_connector_structure(src)
    assert "title" in s["found"]
    assert "connection" in s["found"]
    assert "actions" in s["missing"]


def test_structure_recognises_quoted_keys():
    """Workato examples occasionally use string keys: 'title': 'X'."""
    src = """{
  'title': 'X',
  "connection": {},
}
"""
    s = wa._inspect_connector_structure(src)
    assert "title" in s["found"]
    assert "connection" in s["found"]


def test_structure_empty_source_returns_all_missing():
    s = wa._inspect_connector_structure("")
    assert s["found"] == []
    assert set(s["missing"]) == set(wa.CONNECTOR_TOP_LEVEL_KEYS)


# ---------------------------------------------------------------------------
# cmd_sdk_test
# ---------------------------------------------------------------------------


def _patch_ruby_check(rc=0, stdout="", stderr=""):
    saved = wa._ruby_syntax_check

    def fake(_path, _runner=None):
        return rc, stdout, stderr

    wa._ruby_syntax_check = fake
    return lambda: setattr(wa, "_ruby_syntax_check", saved)


def test_sdk_test_file_not_found_exits_1():
    args = SimpleNamespace(path="/nonexistent/connector.rb")
    exited, code, _, err = _capture_stdout_stderr_exit(
        lambda: wa.cmd_sdk_test(None, args)
    )
    assert exited and code == 1
    assert "not found" in err


def test_sdk_test_path_is_directory_exits_1():
    with tempfile.TemporaryDirectory() as d:
        args = SimpleNamespace(path=d)
        exited, code, _, err = _capture_stdout_stderr_exit(
            lambda: wa.cmd_sdk_test(None, args)
        )
        assert exited and code == 1
        assert "not a file" in err


def test_sdk_test_happy_path_exits_0_with_structure():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "connector.rb"
        # Multi-line connector — the conventional Workato format.
        path.write_text(
            "{\n"
            "  title: 'X',\n"
            "  connection: { fields: [] },\n"
            "  actions: {},\n"
            "}\n"
        )
        restore = _patch_ruby_check(rc=0)
        try:
            args = SimpleNamespace(path=str(path))
            exited, code, out, _ = _capture_stdout_stderr_exit(
                lambda: wa.cmd_sdk_test(None, args)
            )
            # Success means either returns cleanly (exited=False) OR exits 0.
            assert (not exited) or code == 0
            parsed = json.loads(out)
            assert parsed["syntax_ok"] is True
            assert parsed["ruby_exit_code"] == 0
            assert "title" in parsed["structure"]["found"]
            assert "connection" in parsed["structure"]["found"]
            assert "warnings" not in parsed
        finally:
            restore()


def test_sdk_test_syntax_error_exits_1_and_includes_stderr():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "connector.rb"
        path.write_text("{ title: 'X', invalid ruby syntax here\n")
        restore = _patch_ruby_check(rc=1, stderr="parse error: unexpected ...\n")
        try:
            args = SimpleNamespace(path=str(path))
            exited, code, out, _ = _capture_stdout_stderr_exit(
                lambda: wa.cmd_sdk_test(None, args)
            )
            assert exited and code == 1
            parsed = json.loads(out)
            assert parsed["syntax_ok"] is False
            assert "parse error" in parsed["ruby_stderr"]
        finally:
            restore()


def test_sdk_test_warns_when_title_missing():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "connector.rb"
        path.write_text("{ actions: {} }\n")
        restore = _patch_ruby_check(rc=0)
        try:
            args = SimpleNamespace(path=str(path))
            exited, code, out, _ = _capture_stdout_stderr_exit(
                lambda: wa.cmd_sdk_test(None, args)
            )
            # Warning, not failure — success-style exit.
            assert (not exited) or code == 0
            parsed = json.loads(out)
            assert "warnings" in parsed
            assert any("title" in w or "connection" in w for w in parsed["warnings"])
        finally:
            restore()


def test_sdk_test_exits_127_when_ruby_missing():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "connector.rb"
        path.write_text("{ title: 'X', connection: {} }\n")
        restore = _patch_ruby_check(rc=127, stderr="ruby not found\n")
        try:
            args = SimpleNamespace(path=str(path))
            exited, code, out, _ = _capture_stdout_stderr_exit(
                lambda: wa.cmd_sdk_test(None, args)
            )
            assert exited and code == 127
            parsed = json.loads(out)
            assert parsed["ruby_exit_code"] == 127
        finally:
            restore()


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
