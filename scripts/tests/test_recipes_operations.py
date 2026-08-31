#!/usr/bin/env python3
"""Tests for recipes start / stop in workato-api.py.

`recipes list` is gone -- `wk recipes list` covers it. start/stop delegate the
API call to `wk recipes start|stop` but keep the dev-only guard, which wk does
not have, so these tests assert the guard fires before wk is ever spawned.

Covers:
  - require_dev_profile_for_mutation (refuses test/prod/None)
  - resolve_env prefers a wk profile's `environment` over name inference
  - cmd_recipes_start / cmd_recipes_stop guard + --dry-run + wk argv

Run with:
    python3 scripts/tests/test_recipes_operations.py
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "workato-api.py"

spec = importlib.util.spec_from_file_location("workato_api", SCRIPT)
wa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wa)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


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


def _capture_stdout(fn):
    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        fn()
        return sys.stdout.getvalue()
    finally:
        sys.stdout = saved


# ---------------------------------------------------------------------------
# require_dev_profile_for_mutation
# ---------------------------------------------------------------------------


def test_require_dev_allows_dev_profile():
    # Should not raise / exit
    wa.require_dev_profile_for_mutation("acme-dev", "start recipe 1")


def test_require_dev_refuses_test_profile():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.require_dev_profile_for_mutation("acme-test", "start recipe 1")
    )
    assert exited and code == 1
    assert "test" in err
    assert "deploy run" in err


def test_require_dev_refuses_prod_profile():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.require_dev_profile_for_mutation("acme-prod", "stop recipe 99")
    )
    assert exited and code == 1
    assert "prod" in err


def test_require_dev_refuses_unparseable_profile():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.require_dev_profile_for_mutation("plain", "start recipe 1")
    )
    assert exited and code == 1
    assert "<org>-dev" in err
    assert "cannot prove" in err


def test_require_dev_error_includes_operation_label():
    """The operation label flows through so the user can tell what was refused."""
    exited, code, err = _capture_stderr_exit(
        lambda: wa.require_dev_profile_for_mutation("acme-prod", "start recipe 777")
    )
    assert exited and code == 1
    assert "start recipe 777" in err


# ---------------------------------------------------------------------------
# resolve_env
# ---------------------------------------------------------------------------


def test_resolve_env_prefers_wk_environment_field():
    """A wk profile states its environment; naming must not override it."""
    profile = {"environment": "prod", "_source": "wk"}
    assert wa.resolve_env("anything-dev", profile) == "prod"


def test_resolve_env_falls_back_to_name_when_no_field():
    assert wa.resolve_env("acme-dev", {"region_url": "https://x"}) == "dev"


def test_resolve_env_normalises_case_and_whitespace():
    assert wa.resolve_env("x", {"environment": " DEV "}) == "dev"


def test_guard_refuses_wk_prod_profile_despite_dev_name():
    """The regression this guard exists for: a dev-looking name on prod."""
    exited, code, err = _capture_stderr_exit(
        lambda: wa.require_dev_profile_for_mutation(
            "acme-dev", "start recipe 1", {"environment": "prod"},
        )
    )
    assert exited and code == 1
    assert "prod" in err


# ---------------------------------------------------------------------------
# cmd_recipes_start / cmd_recipes_stop — guard + --dry-run + wk delegation
# ---------------------------------------------------------------------------


class _RecordingRunner:
    """Stands in for subprocess.run so no wk process is spawned."""

    def __init__(self, returncode=0, stdout="{}", stderr=""):
        self.calls: list = []
        self._rc, self._out, self._err = returncode, stdout, stderr

    def __call__(self, argv, **_kw):
        self.calls.append(argv)
        return SimpleNamespace(
            args=argv, returncode=self._rc, stdout=self._out, stderr=self._err,
        )


def _explode(*_a, **_kw):
    raise AssertionError("wk invoked despite guard refusal")


def _args(**kw):
    base = dict(
        recipe_id=[1], folder=None, no_wait=False, dry_run=False,
        _resolved_profile_name="acme-dev", _resolved_profile=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


def test_start_refuses_when_profile_is_test():
    exited, code, err = _capture_stderr_exit(
        lambda: wa._recipes_mutate_via_wk(
            "start", _args(_resolved_profile_name="acme-test"), _runner=_explode,
        )
    )
    assert exited and code == 1
    assert "test" in err


def test_stop_refuses_when_profile_is_prod():
    exited, code, err = _capture_stderr_exit(
        lambda: wa._recipes_mutate_via_wk(
            "stop", _args(_resolved_profile_name="acme-prod"), _runner=_explode,
        )
    )
    assert exited and code == 1
    assert "prod" in err


def test_guard_runs_before_wk_is_spawned():
    runner = _RecordingRunner()
    _capture_stderr_exit(
        lambda: wa._recipes_mutate_via_wk(
            "start", _args(_resolved_profile_name="acme-prod"), _runner=runner,
        )
    )
    assert runner.calls == []


def test_start_dry_run_does_not_invoke_wk():
    runner = _RecordingRunner()
    out = _capture_stdout(
        lambda: wa._recipes_mutate_via_wk(
            "start", _args(recipe_id=[42], dry_run=True), _runner=runner,
        )
    )
    parsed = json.loads(out)
    assert parsed["mode"] == "dry-run"
    assert parsed["would_run"][1:4] == ["recipes", "start", "42"]
    assert parsed["profile"] == "acme-dev"
    assert runner.calls == []


def test_stop_dry_run_does_not_invoke_wk():
    runner = _RecordingRunner()
    out = _capture_stdout(
        lambda: wa._recipes_mutate_via_wk(
            "stop", _args(recipe_id=[7], dry_run=True), _runner=runner,
        )
    )
    parsed = json.loads(out)
    assert parsed["would_run"][1:4] == ["recipes", "stop", "7"]
    assert runner.calls == []


def test_start_happy_path_invokes_wk_with_profile_and_json():
    runner = _RecordingRunner(stdout='{"ok":true}')
    out = _capture_stdout(
        lambda: wa._recipes_mutate_via_wk(
            "start", _args(recipe_id=[100, 200]), _runner=runner,
        )
    )
    assert out == '{"ok":true}'
    argv = runner.calls[0]
    assert argv[1:4] == ["recipes", "start", "100"]
    assert "200" in argv
    # The guard resolved a profile; wk must act on that same one, not on
    # whatever its own active profile happens to be.
    assert argv[argv.index("--profile") + 1] == "acme-dev"
    assert argv[-1] == "--json"


def test_folder_scope_is_forwarded():
    runner = _RecordingRunner()
    wa._recipes_mutate_via_wk(
        "stop", _args(recipe_id=[], folder=678), _runner=runner,
    )
    argv = runner.calls[0]
    assert argv[argv.index("--folder") + 1] == "678"


def test_no_wait_only_applies_to_start():
    runner = _RecordingRunner()
    wa._recipes_mutate_via_wk("start", _args(no_wait=True), _runner=runner)
    assert "--no-wait" in runner.calls[0]
    runner2 = _RecordingRunner()
    wa._recipes_mutate_via_wk("stop", _args(no_wait=True), _runner=runner2)
    assert "--no-wait" not in runner2.calls[0]


def test_wk_failure_exit_code_propagates():
    runner = _RecordingRunner(returncode=3, stdout="", stderr="boom")
    exited, code, err = _capture_stderr_exit(
        lambda: wa._recipes_mutate_via_wk("start", _args(), _runner=runner)
    )
    assert exited and code == 3
    assert "boom" in err


# ---------------------------------------------------------------------------
# CLI argparse
# ---------------------------------------------------------------------------


def test_cli_argparse_refuses_non_int_recipe_id():
    import subprocess
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "recipes", "start", "not-an-int",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 2


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
