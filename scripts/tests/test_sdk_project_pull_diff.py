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


def _make_project_dir(root: Path, workspace_id: int = 1) -> Path:
    """Create a minimal project dir with .workatoenv."""
    (root / ".workatoenv").write_text(
        json.dumps({"workspace_id": workspace_id, "folder_id": 42})
    )
    (root / "Recipes").mkdir()
    (root / "Recipes" / "a.recipe.json").write_text('{"name": "local"}')
    return root


def _patch_profile_pool(pool: dict):
    """Patch load_profiles to return a controlled set; returns restore callable."""
    saved = wa.load_profiles
    wa.load_profiles = lambda: {"profiles": pool, "current_profile": None}
    return lambda: setattr(wa, "load_profiles", saved)


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


def test_pull_project_resolves_profile_from_project_workatoenv():
    """workspace_id in the project's .workatoenv selects the right profile."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d), workspace_id=42)
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool({
                "acme-dev": {"workspace_id": 1, "region_url": "u"},
                "acme-test": {"workspace_id": 42, "region_url": "u"},
            })
            restore_pull, calls = _patch_pull(rc=0, stdout="ok\n", stderr="")
            try:
                args = SimpleNamespace(
                    project_dir=None, profile=None,
                )
                exited, code, out, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 0
                assert calls == [("acme-test", Path(d).resolve())]
                assert "ok" in out
            finally:
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_pull_project_dir_resolves_against_target_workatoenv_not_cwd():
    """P1 regression: --project-dir picks the profile from the *target* project,
    not from cwd's .workatoenv. Run with cwd's .workatoenv pointing at one
    workspace and --project-dir at another; the call must use the latter."""
    with tempfile.TemporaryDirectory() as outer:
        cwd_proj = Path(outer) / "cwd_proj"
        target_proj = Path(outer) / "target_proj"
        cwd_proj.mkdir()
        target_proj.mkdir()
        _make_project_dir(cwd_proj, workspace_id=1)
        _make_project_dir(target_proj, workspace_id=42)
        prev = _chdir(cwd_proj)
        try:
            restore_pool = _patch_profile_pool({
                "acme-dev": {"workspace_id": 1, "region_url": "u"},
                "acme-test": {"workspace_id": 42, "region_url": "u"},
            })
            restore_pull, calls = _patch_pull(rc=0)
            try:
                args = SimpleNamespace(
                    project_dir=str(target_proj), profile=None,
                )
                exited, code, _, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 0
                # Must use the target's profile (acme-test), NOT cwd's (acme-dev).
                assert calls == [("acme-test", target_proj.resolve())]
            finally:
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_pull_project_explicit_profile_wins_over_workatoenv():
    """--profile overrides workspace_id resolution from .workatoenv."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d), workspace_id=42)
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool({
                "acme-dev": {"workspace_id": 1, "region_url": "u"},
                "acme-test": {"workspace_id": 42, "region_url": "u"},
            })
            restore_pull, calls = _patch_pull(rc=0)
            try:
                args = SimpleNamespace(
                    project_dir=None, profile="acme-dev",
                )
                exited, code, _, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 0
                assert calls == [("acme-dev", Path(d).resolve())]
            finally:
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_pull_project_propagates_non_zero_exit():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d), workspace_id=1)
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool({
                "acme-dev": {"workspace_id": 1, "region_url": "u"},
            })
            restore_pull, _ = _patch_pull(rc=2, stdout="", stderr="auth failed\n")
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, _out, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 2
                assert "auth failed" in err
            finally:
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_pull_project_refuses_missing_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool({
                "acme-dev": {"workspace_id": 1, "region_url": "u"},
            })
            restore_pull, calls = _patch_pull(rc=0)
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, _, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_pull_project(None, args)
                )
                assert exited and code == 1
                assert ".workatoenv" in err
                assert calls == []
            finally:
                restore_pull()
                restore_pool()
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


_DEFAULT_POOL = {"acme-dev": {"workspace_id": 1, "region_url": "u"}}


def test_diff_project_identical_returns_zero():
    """diff -ru exit 0 → diff-project also exits 0."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool(_DEFAULT_POOL)
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, calls = _patch_diff(rc=0, stdout="")
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, out, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 0
                assert out == ""
                assert len(calls) == 1
                assert calls[0][0] == Path(d).resolve()
            finally:
                restore_diff()
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_diff_project_differs_returns_one_and_prints_diff():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool(_DEFAULT_POOL)
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, _ = _patch_diff(
                rc=1,
                stdout="diff -ru ./Recipes/a.recipe.json ./pulled/...",
            )
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, out, _ = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 1
                assert "Recipes/a.recipe.json" in out
            finally:
                restore_diff()
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_diff_project_pull_failure_returns_two():
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool(_DEFAULT_POOL)
            restore_pull, _ = _patch_pull(rc=3, stderr="auth boom\n")
            restore_diff, calls = _patch_diff(rc=0)
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, _out, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 2
                assert "workato pull" in err
                assert "auth boom" in err
                assert calls == []
            finally:
                restore_diff()
                restore_pull()
                restore_pool()
        finally:
            os.chdir(prev)


def test_diff_project_diff_failure_returns_two():
    """diff exit 2 (e.g. permission error) bubbles up as 2."""
    with tempfile.TemporaryDirectory() as d:
        _make_project_dir(Path(d))
        prev = _chdir(Path(d))
        try:
            restore_pool = _patch_profile_pool(_DEFAULT_POOL)
            restore_pull, _ = _patch_pull(rc=0)
            restore_diff, _ = _patch_diff(rc=2, stderr="cannot read\n")
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                exited, code, _, err = _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert exited and code == 2
                assert "diff" in err
            finally:
                restore_diff()
                restore_pull()
                restore_pool()
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
            restore_pool = _patch_profile_pool(_DEFAULT_POOL)

            def writing_pull(profile, cwd, _runner=None):
                target = Path(cwd) / "Recipes" / "a.recipe.json"
                if target.exists():
                    target.write_text('{"name": "REMOTE"}')
                return 0, "", ""

            saved_pull = wa._invoke_workato_pull
            wa._invoke_workato_pull = writing_pull
            restore_diff, _ = _patch_diff(rc=0, stdout="")
            try:
                args = SimpleNamespace(project_dir=None, profile=None)
                _capture_stdout_stderr_exit(
                    lambda: wa.cmd_sdk_diff_project(None, args)
                )
                assert original_file.read_text() == original_text
            finally:
                restore_diff()
                wa._invoke_workato_pull = saved_pull
                restore_pool()
        finally:
            os.chdir(prev)


# ---------------------------------------------------------------------------
# Exclusion-set consistency (P2 fix from the Codex review)
# ---------------------------------------------------------------------------


def test_diff_argv_excludes_match_project_exclude_patterns():
    """diff -ru must exclude the same patterns copytree's ignore drops.

    Otherwise a local-only `.venv` / `node_modules` would always show
    as "only in local" and diff-project would exit 1 even when the
    Workato-managed assets are identical.
    """
    argv = wa._diff_argv(Path("/a"), Path("/b"))
    excludes = [
        argv[i + 1] for i, tok in enumerate(argv) if tok == "--exclude"
    ]
    for pattern in wa.PROJECT_EXCLUDE_PATTERNS:
        assert pattern in excludes, f"missing --exclude {pattern}"


def test_diff_argv_minimal_shape():
    argv = wa._diff_argv(Path("/x"), Path("/y"))
    assert argv[0] == "diff"
    assert "-ru" in argv
    assert argv[-2:] == ["/x", "/y"]


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
