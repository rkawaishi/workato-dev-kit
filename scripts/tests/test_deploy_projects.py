#!/usr/bin/env python3
"""Tests for the Projects-API-based deploy commands in workato-api.py.

Covers:
  - infer_profile_env
  - check_deploy_transition (allow-list, refusal categories)
  - resolve_project_ref (--project-id, --folder-id, .workatoenv, missing)
  - poll_deployment (terminal exit, timeout exit, sleep injection)
  - cmd_deploy_run --yes gate for prod
  - cmd_deploy_run env-guard short-circuits before any API call
  - cmd_deploy_run --wait happy path / non-success exit code
  - cmd_deploy_preview happy path

Run with:
    python3 scripts/tests/test_deploy_projects.py
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


def _capture_stdout(fn):
    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        fn()
        return sys.stdout.getvalue()
    finally:
        sys.stdout = saved


# ---------------------------------------------------------------------------
# infer_profile_env
# ---------------------------------------------------------------------------


def test_infer_env_dev():
    assert wa.infer_profile_env("acme-dev") == "dev"


def test_infer_env_test():
    assert wa.infer_profile_env("acme-test") == "test"


def test_infer_env_prod():
    assert wa.infer_profile_env("acme-prod") == "prod"


def test_infer_env_multi_dash_org():
    assert wa.infer_profile_env("my-corp-dev") == "dev"


def test_infer_env_missing_returns_none():
    assert wa.infer_profile_env("plain") is None


def test_infer_env_just_suffix_returns_none():
    # The suffix alone (empty org prefix) does not count as a match.
    assert wa.infer_profile_env("-dev") is None


# ---------------------------------------------------------------------------
# check_deploy_transition — allow-list and refusals
# ---------------------------------------------------------------------------


def test_transition_allows_dev_to_test():
    wa.check_deploy_transition("dev", "test")  # no exit


def test_transition_allows_test_to_prod():
    wa.check_deploy_transition("test", "prod")


def test_transition_refuses_dev_to_prod_skip_tier():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.check_deploy_transition("dev", "prod")
    )
    assert exited and code == 1
    assert "dev->prod" in err
    assert "not allowed" in err


def test_transition_refuses_test_to_dev_backward():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.check_deploy_transition("test", "dev")
    )
    assert exited and code == 1
    assert "test->dev" in err


def test_transition_refuses_prod_as_source():
    for to_env in ("dev", "test", "prod"):
        exited, code, _ = _capture_stderr_exit(
            lambda te=to_env: wa.check_deploy_transition("prod", te)
        )
        assert exited and code == 1, f"prod->{to_env} should be refused"


def test_transition_refuses_same_env():
    for env in ("dev", "test", "prod"):
        exited, code, err = _capture_stderr_exit(
            lambda e=env: wa.check_deploy_transition(e, e)
        )
        assert exited and code == 1
        assert env in err


def test_transition_refuses_when_source_is_none():
    """Profile name didn't follow `<org>-<env>` → infer returns None → refuse."""
    exited, code, err = _capture_stderr_exit(
        lambda: wa.check_deploy_transition(None, "test")
    )
    assert exited and code == 1
    assert "infer source environment" in err
    assert "<org>-<env>" in err


# ---------------------------------------------------------------------------
# resolve_project_ref
# ---------------------------------------------------------------------------


def test_resolve_project_ref_uses_explicit_project_id():
    assert wa.resolve_project_ref(42, None) == "42"


def test_resolve_project_ref_uses_explicit_folder_id():
    assert wa.resolve_project_ref(None, 88) == "f88"


def test_resolve_project_ref_prefers_project_id_over_folder():
    # When both are given, project_id wins (it is the unambiguous form).
    assert wa.resolve_project_ref(1, 2) == "1"


def test_resolve_project_ref_reads_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            (Path(d) / ".workatoenv").write_text(
                json.dumps({"workspace_id": 1, "folder_id": 777})
            )
            assert wa.resolve_project_ref(None, None) == "f777"
        finally:
            os.chdir(prev)


def test_resolve_project_ref_errors_when_nothing_resolves():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            exited, code, err = _capture_stderr_exit(
                lambda: wa.resolve_project_ref(None, None)
            )
            assert exited and code == 1
            assert "--project-id" in err and "--folder-id" in err
        finally:
            os.chdir(prev)


# ---------------------------------------------------------------------------
# poll_deployment — injected sleep and clock
# ---------------------------------------------------------------------------


class _PollFakeAPI:
    def __init__(self, states: list[str]):
        self._states = states
        self.calls = 0

    def deployment_get(self, _id):
        s = self._states[min(self.calls, len(self._states) - 1)]
        self.calls += 1
        return {"id": 1, "state": s}


def test_poll_returns_on_first_terminal_state():
    api = _PollFakeAPI(["success"])
    sleeps: list[float] = []
    t = [0.0]

    def sleep(d):
        sleeps.append(d)
        t[0] += d

    def now():
        return t[0]

    result = wa.poll_deployment(
        api, 1, timeout_seconds=10, poll_interval_seconds=2.0,
        _sleep=sleep, _now=now,
    )
    assert result["state"] == "success"
    assert api.calls == 1
    assert sleeps == []  # no sleep needed when first state is terminal


def test_poll_iterates_until_terminal():
    api = _PollFakeAPI(["pending", "pending", "success"])
    sleeps: list[float] = []
    t = [0.0]
    wa.poll_deployment(
        api, 1, timeout_seconds=10, poll_interval_seconds=2.0,
        _sleep=lambda d: (sleeps.append(d), t.__setitem__(0, t[0] + d)),
        _now=lambda: t[0],
    )
    assert api.calls == 3
    assert sleeps == [2.0, 2.0]


def test_poll_exits_on_timeout():
    api = _PollFakeAPI(["pending"])  # never reaches terminal
    t = [0.0]
    exited, code, err = _capture_stderr_exit(
        lambda: wa.poll_deployment(
            api, 1, timeout_seconds=5, poll_interval_seconds=2.0,
            _sleep=lambda d: t.__setitem__(0, t[0] + d),
            _now=lambda: t[0],
        )
    )
    assert exited and code == 1
    assert "did not reach a terminal state" in err
    assert "5s" in err


def test_poll_recognizes_failed_state_as_terminal():
    api = _PollFakeAPI(["failed"])
    result = wa.poll_deployment(
        api, 1, timeout_seconds=10, poll_interval_seconds=2.0,
        _sleep=lambda d: None, _now=lambda: 0.0,
    )
    assert result["state"] == "failed"


# ---------------------------------------------------------------------------
# cmd_deploy_run — env guard short-circuits + --yes prod gate
# ---------------------------------------------------------------------------


def _patch_profile(name: str, region_url: str = "https://example.com"):
    """Patch resolve_profile + get_token + load_profiles to return a single profile.

    Returns a restore callable.
    """
    saved_load = wa.load_profiles
    saved_resolve = wa.resolve_profile
    saved_token = wa.get_token

    pool = {name: {"region_url": region_url, "workspace_id": 1}}

    wa.load_profiles = lambda: {"profiles": pool, "current_profile": name}
    wa.resolve_profile = lambda explicit: (
        (explicit, pool[explicit]) if explicit else (name, pool[name])
    )
    wa.get_token = lambda _n: "fake-token"

    def restore():
        wa.load_profiles = saved_load
        wa.resolve_profile = saved_resolve
        wa.get_token = saved_token

    return restore


def _patch_api(fake_api_cls):
    saved = wa.WorkatoAPI
    wa.WorkatoAPI = fake_api_cls  # type: ignore[assignment]
    return lambda: setattr(wa, "WorkatoAPI", saved)


def test_run_short_circuits_on_bad_transition_dev_to_prod():
    """Dev profile + --to prod must be refused before any API call."""
    restore_p = _patch_profile("acme-dev")

    class BoomAPI:
        def __init__(self, *_a, **_kw):
            raise AssertionError("WorkatoAPI was constructed despite refused transition")

    # WorkatoAPI IS constructed in _deploy_resolve_profile_and_api before the
    # guard runs (we need the client to make API calls if the guard passes).
    # Re-architecting to defer construction would require larger changes; the
    # important guarantee is that no HTTP call is made. So we patch the actual
    # API methods to explode instead of the constructor.
    class ExplodingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, *_a, **_kw):
            raise AssertionError(
                "project_deploy was called despite refused transition"
            )

        def deployment_get(self, *_a, **_kw):
            raise AssertionError(
                "deployment_get was called despite refused transition"
            )

    restore_api = _patch_api(ExplodingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="prod",
            project_id=42, folder_id=None,
            description=None, yes=True, wait=False, timeout=30,
        )
        exited, code, err = _capture_stderr_exit(
            lambda: wa.cmd_deploy_run(None, args)
        )
        assert exited and code == 1
        assert "dev->prod" in err
    finally:
        restore_api()
        restore_p()


def test_run_refuses_prod_without_yes():
    """Test->prod is an allowed transition, but --yes is required."""
    restore_p = _patch_profile("acme-test")

    class ExplodingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, *_a, **_kw):
            raise AssertionError("project_deploy called without --yes")

    restore_api = _patch_api(ExplodingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="prod",
            project_id=42, folder_id=None,
            description=None, yes=False, wait=False, timeout=30,
        )
        exited, code, err = _capture_stderr_exit(
            lambda: wa.cmd_deploy_run(None, args)
        )
        assert exited and code == 1
        assert "--yes" in err
    finally:
        restore_api()
        restore_p()


def test_run_allows_test_to_prod_with_yes_no_wait():
    restore_p = _patch_profile("acme-test")
    calls: list[tuple] = []

    class RecordingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, project_ref, environment_type, description):
            calls.append(("project_deploy", project_ref, environment_type, description))
            return {"id": 999, "state": "pending"}

    restore_api = _patch_api(RecordingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="prod",
            project_id=42, folder_id=None,
            description="Release X", yes=True, wait=False, timeout=30,
        )
        out = _capture_stdout(lambda: wa.cmd_deploy_run(None, args))
        parsed = json.loads(out)
        assert parsed["id"] == 999
        assert parsed["state"] == "pending"
        assert calls == [("project_deploy", "42", "prod", "Release X")]
    finally:
        restore_api()
        restore_p()


def test_run_dev_to_test_with_folder_id_becomes_f_prefix():
    restore_p = _patch_profile("acme-dev")
    seen: list[str] = []

    class RecordingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, project_ref, environment_type, description):
            seen.append(project_ref)
            return {"id": 1, "state": "pending"}

    restore_api = _patch_api(RecordingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="test",
            project_id=None, folder_id=12345,
            description=None, yes=False, wait=False, timeout=30,
        )
        _capture_stdout(lambda: wa.cmd_deploy_run(None, args))
        assert seen == ["f12345"]
    finally:
        restore_api()
        restore_p()


def test_run_wait_exits_nonzero_when_state_failed():
    restore_p = _patch_profile("acme-dev")

    class RecordingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, project_ref, environment_type, description):
            return {"id": 777, "state": "pending"}

        def deployment_get(self, _id):
            return {"id": 777, "state": "failed", "error": "boom"}

    restore_api = _patch_api(RecordingAPI)
    saved_poll = wa.poll_deployment

    # Inject sleep/now so the test does not actually wait.
    def fast_poll(api, did, timeout_seconds, poll_interval_seconds=2.0, _sleep=None, _now=None):
        return saved_poll(
            api, did, timeout_seconds, poll_interval_seconds,
            _sleep=lambda d: None, _now=lambda: 0.0,
        )

    wa.poll_deployment = fast_poll
    try:
        args = SimpleNamespace(
            profile=None, to_env="test",
            project_id=42, folder_id=None,
            description=None, yes=False, wait=True, timeout=30,
        )
        saved_out = sys.stdout
        sys.stdout = io.StringIO()
        exited = False
        code = 0
        try:
            try:
                wa.cmd_deploy_run(None, args)
            except SystemExit as e:
                exited = True
                code = int(e.code) if isinstance(e.code, int) else 1
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = saved_out
        assert exited and code == 1
        parsed = json.loads(out)
        assert parsed["state"] == "failed"
    finally:
        wa.poll_deployment = saved_poll
        restore_api()
        restore_p()


def test_run_wait_zero_exit_on_success():
    restore_p = _patch_profile("acme-dev")

    class RecordingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def project_deploy(self, *_a, **_kw):
            return {"id": 100, "state": "pending"}

        def deployment_get(self, _id):
            return {"id": 100, "state": "success"}

    restore_api = _patch_api(RecordingAPI)
    saved_poll = wa.poll_deployment

    def fast_poll(api, did, ts, pi=2.0, _sleep=None, _now=None):
        return saved_poll(
            api, did, ts, pi, _sleep=lambda d: None, _now=lambda: 0.0,
        )

    wa.poll_deployment = fast_poll
    try:
        args = SimpleNamespace(
            profile=None, to_env="test",
            project_id=42, folder_id=None,
            description=None, yes=False, wait=True, timeout=30,
        )
        # Should NOT raise SystemExit on success.
        out = _capture_stdout(lambda: wa.cmd_deploy_run(None, args))
        parsed = json.loads(out)
        assert parsed["state"] == "success"
    finally:
        wa.poll_deployment = saved_poll
        restore_api()
        restore_p()


# ---------------------------------------------------------------------------
# cmd_deploy_preview happy path
# ---------------------------------------------------------------------------


def test_preview_dev_to_test_emits_expected_shape():
    restore_p = _patch_profile("acme-dev", region_url="https://dev.example.com")

    class RecordingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def recipes_list(self, _folder_id):
            return [{"id": 5, "name": "R1", "running": False}]

        def project_deploy(self, *_a, **_kw):
            raise AssertionError("project_deploy must not be called in preview")

    restore_api = _patch_api(RecordingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="test",
            project_id=None, folder_id=42,
            description="planned",
        )
        out = _capture_stdout(lambda: wa.cmd_deploy_preview(None, args))
        parsed = json.loads(out)
        assert parsed["mode"] == "preview"
        assert parsed["profile"] == "acme-dev"
        assert parsed["source_env"] == "dev"
        assert parsed["target_env"] == "test"
        assert parsed["project_ref"] == "f42"
        assert parsed["would_call"]["method"] == "POST"
        assert "environment_type=test" in parsed["would_call"]["url"]
        assert parsed["would_call"]["url"].startswith(
            "https://dev.example.com/api/projects/f42/deploy"
        )
        assert parsed["would_call"]["body"] == {"description": "planned"}
        assert parsed["recipes_in_folder"] == [
            {"id": 5, "name": "R1", "running": False}
        ]
        assert any("No API writes" in n for n in parsed["notes"])
    finally:
        restore_api()
        restore_p()


def test_preview_short_circuits_on_bad_transition():
    restore_p = _patch_profile("acme-dev")

    class ExplodingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def recipes_list(self, *_a, **_kw):
            raise AssertionError("recipes_list called despite refused transition")

    restore_api = _patch_api(ExplodingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="prod",   # dev->prod skip-tier
            project_id=42, folder_id=None,
            description=None,
        )
        exited, code, err = _capture_stderr_exit(
            lambda: wa.cmd_deploy_preview(None, args)
        )
        assert exited and code == 1
        assert "dev->prod" in err
    finally:
        restore_api()
        restore_p()


def test_preview_refuses_when_profile_name_unparseable():
    restore_p = _patch_profile("plainname")

    class ExplodingAPI:
        def __init__(self, *_a, **_kw):
            pass

        def recipes_list(self, *_a, **_kw):
            raise AssertionError("recipes_list called despite refused transition")

    restore_api = _patch_api(ExplodingAPI)
    try:
        args = SimpleNamespace(
            profile=None, to_env="test",
            project_id=42, folder_id=None,
            description=None,
        )
        exited, code, err = _capture_stderr_exit(
            lambda: wa.cmd_deploy_preview(None, args)
        )
        assert exited and code == 1
        assert "infer source environment" in err
    finally:
        restore_api()
        restore_p()


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
