#!/usr/bin/env python3
"""Tests for recipes start / stop / list --status in workato-api.py.

Covers:
  - require_dev_profile_for_mutation (refuses test/prod/None)
  - cmd_recipes_start / cmd_recipes_stop env guard + --dry-run + happy path
  - cmd_recipes_list --status running|stopped filter

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
# cmd_recipes_start — guard + --dry-run + real PUT
# ---------------------------------------------------------------------------


class _RecordingAPI:
    def __init__(self, base_url="https://workato.example.com"):
        self.base_url = base_url
        self.calls: list = []

    def recipe_start(self, recipe_id):
        self.calls.append(("start", recipe_id))
        return {"id": recipe_id, "running": True}

    def recipe_stop(self, recipe_id):
        self.calls.append(("stop", recipe_id))
        return {"id": recipe_id, "running": False}


class _ExplodingAPI:
    base_url = "https://workato.example.com"

    def recipe_start(self, *_a, **_kw):
        raise AssertionError("recipe_start called despite guard refusal")

    def recipe_stop(self, *_a, **_kw):
        raise AssertionError("recipe_stop called despite guard refusal")


def test_start_refuses_when_profile_is_test():
    api = _ExplodingAPI()
    args = SimpleNamespace(
        recipe_id=1, dry_run=False, _resolved_profile_name="acme-test",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_recipes_start(api, args)
    )
    assert exited and code == 1
    assert "test" in err


def test_stop_refuses_when_profile_is_prod():
    api = _ExplodingAPI()
    args = SimpleNamespace(
        recipe_id=1, dry_run=False, _resolved_profile_name="acme-prod",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_recipes_stop(api, args)
    )
    assert exited and code == 1
    assert "prod" in err


def test_start_dry_run_does_not_call_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        recipe_id=42, dry_run=True, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_recipes_start(api, args))
    parsed = json.loads(out)
    assert parsed["mode"] == "dry-run"
    assert parsed["would_call"]["method"] == "PUT"
    assert parsed["would_call"]["url"].endswith("/api/recipes/42/start")
    assert parsed["profile"] == "acme-dev"
    assert api.calls == []


def test_stop_dry_run_does_not_call_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        recipe_id=7, dry_run=True, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_recipes_stop(api, args))
    parsed = json.loads(out)
    assert parsed["mode"] == "dry-run"
    assert parsed["would_call"]["url"].endswith("/api/recipes/7/stop")
    assert api.calls == []


def test_start_happy_path_invokes_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        recipe_id=100, dry_run=False, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_recipes_start(api, args))
    parsed = json.loads(out)
    assert parsed == {"id": 100, "running": True}
    assert api.calls == [("start", 100)]


def test_stop_happy_path_invokes_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        recipe_id=200, dry_run=False, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_recipes_stop(api, args))
    parsed = json.loads(out)
    assert parsed == {"id": 200, "running": False}
    assert api.calls == [("stop", 200)]


# ---------------------------------------------------------------------------
# cmd_recipes_list --status
# ---------------------------------------------------------------------------


class _ListAPI:
    def __init__(self, recipes):
        self._recipes = recipes

    def recipes_list(self, _folder_id):
        return self._recipes


def test_list_no_status_returns_all():
    api = _ListAPI([
        {"id": 1, "running": True},
        {"id": 2, "running": False},
    ])
    args = SimpleNamespace(folder_id=None, status=None)
    out = _capture_stdout(lambda: wa.cmd_recipes_list(api, args))
    parsed = json.loads(out)
    assert len(parsed) == 2


def test_list_status_running_filters_to_running():
    api = _ListAPI([
        {"id": 1, "running": True, "name": "A"},
        {"id": 2, "running": False, "name": "B"},
        {"id": 3, "running": True, "name": "C"},
    ])
    args = SimpleNamespace(folder_id=None, status="running")
    out = _capture_stdout(lambda: wa.cmd_recipes_list(api, args))
    parsed = json.loads(out)
    assert [r["id"] for r in parsed] == [1, 3]


def test_list_status_stopped_filters_to_stopped():
    api = _ListAPI([
        {"id": 1, "running": True},
        {"id": 2, "running": False},
        {"id": 3, "running": False},
    ])
    args = SimpleNamespace(folder_id=None, status="stopped")
    out = _capture_stdout(lambda: wa.cmd_recipes_list(api, args))
    parsed = json.loads(out)
    assert [r["id"] for r in parsed] == [2, 3]


def test_list_status_treats_missing_running_field_as_stopped():
    """Recipes without a `running` field should be treated as not-running."""
    api = _ListAPI([
        {"id": 1, "running": True},
        {"id": 2},  # no `running` field
    ])
    args_running = SimpleNamespace(folder_id=None, status="running")
    out_running = _capture_stdout(lambda: wa.cmd_recipes_list(api, args_running))
    assert [r["id"] for r in json.loads(out_running)] == [1]

    args_stopped = SimpleNamespace(folder_id=None, status="stopped")
    out_stopped = _capture_stdout(lambda: wa.cmd_recipes_list(api, args_stopped))
    assert [r["id"] for r in json.loads(out_stopped)] == [2]


def test_list_status_skips_non_dict_entries():
    """Defensive: a malformed list entry must not break the filter."""
    api = _ListAPI([
        {"id": 1, "running": True},
        "not a dict",
        None,
    ])
    args = SimpleNamespace(folder_id=None, status="running")
    out = _capture_stdout(lambda: wa.cmd_recipes_list(api, args))
    assert [r["id"] for r in json.loads(out)] == [1]


# ---------------------------------------------------------------------------
# CLI argparse — --status choices, recipe_id type
# ---------------------------------------------------------------------------


def test_cli_argparse_refuses_invalid_status():
    import subprocess
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "recipes", "list",
            "--status", "paused",  # not in {running, stopped}
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "invalid choice" in result.stderr


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
