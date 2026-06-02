#!/usr/bin/env python3
"""Tests for `sdk pull-project` and `sdk diff-project`.

Both commands shell out to `workato` and `diff`; the tests inject a
runner so they assert command construction and exit-code handling
without invoking real subprocesses.

Run with:
    python3 scripts/tests/test_sdk_project_pull_diff.py
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


def _chdir(target: Path) -> Path:
    prev = Path.cwd()
    os.chdir(target)
    return prev


def _capture_stderr_exit(fn):
    saved = sys.stderr
    sys.stderr = io.StringIO()
    exited = False
    code = 0
    try:
        try:
            fn()
        except SystemExit as e:
            exited = True
            code = int(e.code) if isinstance(e.code, int) else 1
        err = sys.stderr.getvalue()
    finally:
        sys.stderr = saved
    return exited, code, err


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


def _make_project_dir(root: Path) -> Path:
    """Create a minimal project dir with .workatoenv."""
    (root / ".workatoenv").write_text(
        json.dumps({"workspace_id": 1, "folder_id": 42})
    )
    (root / "Recipes").mkdir()
    (root / "Recipes" / "a.recipe.json").write_text('{"name": "local"}')
    return root


# ---------------------------------------------------------------------------
# _invoke_workato_pull — command construction
# ---------------------------------------------------------------------------


def test_invoke_workato_pull_builds_expected_command():
    captured: list = []

    def runner(cmd, cwd):
        captured.append((list(cmd), cwd))
        return 0, "pulled\n", ""

    rc, out, err = wa._invoke_workato_pull(
        "acme-dev", Path("/tmp/proj"), _runner=runner,
    )
    assert rc == 0
    assert out == "pulled\n"
    assert err == ""
    assert captured == [
        (["workato", "--profile", "acme-dev", "pull"], Path("/tmp/proj")),
    ]


def test_invoke_workato_pull_propagates_non_zero():
    def runner(_cmd, _cwd):
        return 3, "", "boom\n"

    rc, _, err = wa._invoke_workato_pull(
        "acme-dev", Path("/tmp/x"), _runner=runner,
    )
    assert rc == 3
    assert err == "boom\n"


# ---------------------------------------------------------------------------
# _validate_project_dir
# ---------------------------------------------------------------------------


def test_validate_project_dir_refuses_nonexistent():
    exited, code, err = _capture_stderr_exit(
        lambda: wa._validate_project_dir(Path("/nonexistent-XYZ-test"))
    )
    assert exited and code == 1
    assert "does not exist" in err


def test_validate_project_dir_refuses_missing_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        exited, code, err = _capture_stderr_exit(
            lambda: wa._validate_project_dir(Path(d))
        )
        assert exited and code == 1
        assert ".workatoenv" in err


def test_validate_project_dir_passes_when_workatoenv_present():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / ".workatoenv").write_text("{}")
        # Should not exit
        wa._validate_project_dir(Path(d))


# ---------------------------------------------------------------------------
# cmd_sdk_pull_project — wraps workato pull
# ---------------------------------------------------------------------------


def _patch_pull(rc=0, stdout="", stderr=""):
    """Patch _invoke_workato_pull. Returns (restore_callable, calls list)."""
    calls: list = []
    saved = wa._invoke_workato_pull

    def fake(profile, cwd, _runner=None):
        calls.append((profile, cwd))
        return rc, stdout, stderr

    wa._invoke_workato_pull = fake
    return (lambda: setattr(wa, "_invoke_workato_pull", saved)), calls


def test_pull_project_invokes_workato_with_resolved_profile():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore, calls = _patch_pull(rc=0, stdout="ok\n", stderr="")
            try:
                args = SimpleNamespace(
                    project_dir=None,
                    _resolved_profile_name="acme-test",
                )
                exited, code, out, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 0
                assert calls == [("acme-test", Path(d).resolve())]
                assert "ok" in out
            finally:
                restore()
        finally:
            os.chdir(prev)


def test_pull_project_uses_explicit_project_dir():
    with tempfile.TemporaryDirectory() as outer:
        proj = Path(outer) / "subproj"
        proj.mkdir()
        _make_project_dir(proj)
        restore, calls = _patch_pull(rc=0)
        try:
            args = SimpleNamespace(
                project_dir=str(proj),
                _resolved_profile_name="acme-dev",
            )
            exited, code, _, _ = _capture_stdout_stderr_exit(
                lambda: wa.cmd_sdk_pull_project(None, args)
            )
            assert exited and code == 0
            assert calls == [("acme-dev", proj.resolve())]
        finally:
            restore()


def test_pull_project_propagates_non_zero_exit():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore, _ = _patch_pull(rc=2, stdout="", stderr="auth failed\n")
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, _out, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 2
                assert "auth failed" in err
            finally:
                restore()
        finally:
            os.chdir(prev)


def test_pull_project_refuses_missing_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        # No .workatoenv created
        prev = _chdir(Path(d))
        try:
            restore, calls = _patch_pull(rc=0)
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, _, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 1
                assert ".workatoenv" in err
                # workato pull must NOT have been invoked
                assert calls == []
            finally:
                restore()
        finally:
            os.chdir(prev)


# ---------------------------------------------------------------------------
# cmd_sdk_diff_project — copy + pull-in-copy + diff
# ---------------------------------------------------------------------------


def _patch_diff(rc=0, stdout="", stderr=""):
    saved = wa._run_diff
    calls: list = []

    def fake(local, pulled, _runner=None):
        calls.append((local, pulled))
        return rc, stdout, stderr

    wa._run_diff = fake
    return (lambda: setattr(wa, "_run_diff", saved)), calls


def test_diff_project_identical_returns_zero():
    """diff -ru exit 0 → diff-project also exits 0."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, calls = _patch_diff(rc=0, stdout="")
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, out, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 0
                assert out == ""
                assert len(calls) == 1
                # local arg is the resolved project dir
                assert calls[0][0] == Path(d).resolve()
            finally:
                restore_diff()
                restore_pull()
        finally:
            os.chdir(prev)


def test_diff_project_differs_returns_one_and_prints_diff():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, _ = _patch_diff(
                rc=1,
                stdout="diff -ru ./Recipes/a.recipe.json ./pulled/...",
            )
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, out, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 1
                assert "Recipes/a.recipe.json" in out
            finally:
                restore_diff()
                restore_pull()
        finally:
            os.chdir(prev)


def test_diff_project_pull_failure_returns_two():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pull, _ = _patch_pull(rc=3, stderr="auth boom\n")
            restore_diff, calls = _patch_diff(rc=0)
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, _out, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 2
                assert "workato pull" in err
                assert "auth boom" in err
                # diff must NOT have been called
                assert calls == []
            finally:
                restore_diff()
                restore_pull()
        finally:
            os.chdir(prev)


def test_diff_project_diff_failure_returns_two():
    """diff exit 2 (e.g. permission error) bubbles up as 2."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, _ = _patch_diff(rc=2, stderr="cannot read\n")
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                exited, code, _, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 2
                assert "diff" in err
            finally:
                restore_diff()
                restore_pull()
        finally:
            os.chdir(prev)


def test_diff_project_does_not_modify_original_dir():
    """The local project files must be unchanged after diff-project runs."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        original_file = Path(d) / "Recipes" / "a.recipe.json"
        original_text = original_file.read_text()

        prev = _chdir(Path(d))
        try:
            # Patch pull to *modify* the temp copy (simulating a real pull
            # overwriting a file). This proves the helper isolates that
            # mutation to the temp dir.
            def writing_pull(profile, cwd, _runner=None):
                target = Path(cwd) / "Recipes" / "a.recipe.json"
                if target.exists():
                    target.write_text('{"name": "REMOTE"}')
                return 0, "", ""

            saved_pull = wa._invoke_workato_pull
            wa._invoke_workato_pull = writing_pull
            restore_diff, _ = _patch_diff(rc=0, stdout="")
            try:
                args = SimpleNamespace(
                    project_dir=None, _resolved_profile_name="acme-dev",
                )
                _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                # The original must be untouched.
                assert original_file.read_text() == original_text
            finally:
                restore_diff()
                wa._invoke_workato_pull = saved_pull
        finally:
            os.chdir(prev)


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
