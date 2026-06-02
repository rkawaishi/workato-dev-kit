#!/usr/bin/env python3
"""Tests for `deploy preview` helpers in `scripts/workato-api.py`.

Run with:
    python3 scripts/tests/test_deploy_preview.py
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
# Small helpers
# ---------------------------------------------------------------------------


def _chdir(target: Path) -> Path:
    prev = Path.cwd()
    os.chdir(target)
    return prev


def _capture_stderr_exit(fn):
    """Run fn() with stderr captured; return (exited:bool, code:int, err:str)."""
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
# check_deploy_transition
# ---------------------------------------------------------------------------


def test_transition_allows_dev_to_test():
    # Should not raise / exit
    wa.check_deploy_transition("dev", "test")


def test_transition_allows_test_to_prod():
    wa.check_deploy_transition("test", "prod")


def test_transition_refuses_skip_tier_dev_to_prod():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.check_deploy_transition("dev", "prod")
    )
    assert exited and code == 1
    assert "dev->prod" in err
    assert "not allowed" in err


def test_transition_refuses_backward_test_to_dev():
    exited, code, err = _capture_stderr_exit(
        lambda: wa.check_deploy_transition("test", "dev")
    )
    assert exited and code == 1
    assert "test->dev" in err


def test_transition_refuses_prod_as_source():
    for to_env in ("dev", "test", "prod"):
        exited, code, err = _capture_stderr_exit(
            lambda te=to_env: wa.check_deploy_transition("prod", te)
        )
        assert exited and code == 1, f"prod->{to_env} should be refused"


def test_transition_refuses_same_env():
    for env in ("dev", "test", "prod"):
        exited, code, err = _capture_stderr_exit(
            lambda e=env: wa.check_deploy_transition(e, e)
        )
        assert exited and code == 1
        assert "both" in err and env in err


# ---------------------------------------------------------------------------
# _strip_env_suffix / derive_sibling_profile
# ---------------------------------------------------------------------------


def test_strip_env_suffix_dev():
    assert wa._strip_env_suffix("acme-dev") == "acme"


def test_strip_env_suffix_test():
    assert wa._strip_env_suffix("acme-test") == "acme"


def test_strip_env_suffix_prod():
    assert wa._strip_env_suffix("acme-prod") == "acme"


def test_strip_env_suffix_missing_returns_none():
    assert wa._strip_env_suffix("randomname") is None


def test_strip_env_suffix_just_suffix_returns_none():
    # The suffix alone shouldn't count as an org match (empty prefix).
    assert wa._strip_env_suffix("-dev") is None


def test_strip_env_suffix_multi_dash_org():
    # Multi-dash org names like "my-corp" should still strip correctly.
    assert wa._strip_env_suffix("my-corp-dev") == "my-corp"


def test_derive_sibling_dev_to_test():
    assert wa.derive_sibling_profile("acme-dev", "test") == "acme-test"


def test_derive_sibling_test_to_prod():
    assert wa.derive_sibling_profile("acme-test", "prod") == "acme-prod"


def test_derive_sibling_unparseable_returns_none():
    assert wa.derive_sibling_profile("plain-name", "test") is None


# ---------------------------------------------------------------------------
# resolve_deploy_folder_id
# ---------------------------------------------------------------------------


def test_resolve_folder_id_uses_explicit():
    assert wa.resolve_deploy_folder_id(42) == 42


def test_resolve_folder_id_reads_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            (Path(d) / ".workatoenv").write_text(
                json.dumps({"workspace_id": 1, "folder_id": 777})
            )
            assert wa.resolve_deploy_folder_id(None) == 777
        finally:
            os.chdir(prev)


def test_resolve_folder_id_errors_when_no_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            exited, code, err = _capture_stderr_exit(
                lambda: wa.resolve_deploy_folder_id(None)
            )
            assert exited and code == 1
            assert ".workatoenv" in err
        finally:
            os.chdir(prev)


def test_resolve_folder_id_errors_when_non_int_in_workatoenv():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            (Path(d) / ".workatoenv").write_text(
                json.dumps({"workspace_id": 1, "folder_id": "not-an-int"})
            )
            exited, code, err = _capture_stderr_exit(
                lambda: wa.resolve_deploy_folder_id(None)
            )
            assert exited and code == 1
            assert "folder_id" in err
        finally:
            os.chdir(prev)


# ---------------------------------------------------------------------------
# resolve_deploy_profiles — uses monkey-patched load_profiles / resolve_profile
# ---------------------------------------------------------------------------


def _with_profile_pool(profiles: dict, current_resolution: tuple[str, dict] | None):
    """Return restore callable; patches load_profiles + resolve_profile."""
    saved_load = wa.load_profiles
    saved_resolve = wa.resolve_profile

    def fake_load():
        return {"profiles": profiles, "current_profile": None}

    def fake_resolve(explicit):
        if explicit is not None:
            return explicit, profiles[explicit]
        if current_resolution is None:
            print(
                "Error: fake resolve_profile called with no default set",
                file=sys.stderr,
            )
            sys.exit(1)
        return current_resolution

    wa.load_profiles = fake_load
    wa.resolve_profile = fake_resolve

    def restore():
        wa.load_profiles = saved_load
        wa.resolve_profile = saved_resolve

    return restore


def test_resolve_profiles_derives_target_from_source():
    pool = {
        "acme-dev": {"region_url": "https://dev.example"},
        "acme-test": {"region_url": "https://test.example"},
    }
    restore = _with_profile_pool(pool, ("acme-dev", pool["acme-dev"]))
    try:
        (sn, sp), (tn, tp) = wa.resolve_deploy_profiles(
            "dev", "test",
            explicit_from=None, explicit_to=None, explicit_default=None,
        )
        assert sn == "acme-dev"
        assert tn == "acme-test"
        assert sp["region_url"].endswith("dev.example")
        assert tp["region_url"].endswith("test.example")
    finally:
        restore()


def test_resolve_profiles_explicit_overrides_both():
    pool = {
        "acme-dev": {"region_url": "u1"},
        "acme-test": {"region_url": "u2"},
        "foo-test": {"region_url": "u3"},
    }
    restore = _with_profile_pool(pool, ("acme-dev", pool["acme-dev"]))
    try:
        (sn, _), (tn, _) = wa.resolve_deploy_profiles(
            "dev", "test",
            explicit_from="acme-dev", explicit_to="foo-test",
            explicit_default=None,
        )
        assert sn == "acme-dev"
        assert tn == "foo-test"
    finally:
        restore()


def test_resolve_profiles_errors_when_source_not_in_pool():
    pool = {"acme-dev": {"region_url": "u1"}}
    restore = _with_profile_pool(pool, ("acme-dev", pool["acme-dev"]))
    try:
        exited, code, err = _capture_stderr_exit(
            lambda: wa.resolve_deploy_profiles(
                "dev", "test",
                explicit_from="missing-dev", explicit_to=None,
                explicit_default=None,
            )
        )
        assert exited and code == 1
        assert "source profile" in err
        assert "missing-dev" in err
    finally:
        restore()


def test_resolve_profiles_errors_when_target_cannot_be_derived():
    # Current profile doesn't follow <org>-<env>, so target cannot be derived
    # and there's no --to-profile override.
    pool = {"plainname": {"region_url": "u1"}}
    restore = _with_profile_pool(pool, ("plainname", pool["plainname"]))
    try:
        exited, code, err = _capture_stderr_exit(
            lambda: wa.resolve_deploy_profiles(
                "dev", "test",
                explicit_from=None, explicit_to=None,
                explicit_default=None,
            )
        )
        assert exited and code == 1
        assert "cannot derive" in err
        assert "--to-profile" in err
    finally:
        restore()


def test_resolve_profiles_errors_when_derived_target_not_in_pool():
    # Source resolves, derivation works, but `<org>-test` isn't configured.
    pool = {"acme-dev": {"region_url": "u1"}}
    restore = _with_profile_pool(pool, ("acme-dev", pool["acme-dev"]))
    try:
        exited, code, err = _capture_stderr_exit(
            lambda: wa.resolve_deploy_profiles(
                "dev", "test",
                explicit_from=None, explicit_to=None,
                explicit_default=None,
            )
        )
        assert exited and code == 1
        assert "target profile 'acme-test'" in err
    finally:
        restore()


# ---------------------------------------------------------------------------
# _summarize_assets
# ---------------------------------------------------------------------------


def test_summarize_assets_groups_by_type():
    assets = [
        {"id": 1, "type": "recipe", "name": "A"},
        {"id": 2, "type": "recipe", "name": "B"},
        {"id": 3, "type": "connection", "name": "C"},
    ]
    assert wa._summarize_assets(assets) == {"recipe": 2, "connection": 1}


def test_summarize_assets_handles_asset_type_alias():
    assert wa._summarize_assets([{"asset_type": "lookup_table"}]) == {
        "lookup_table": 1
    }


def test_summarize_assets_unknown_for_typeless():
    assert wa._summarize_assets([{"id": 1}]) == {"unknown": 1}


def test_summarize_assets_skips_non_dict():
    assert wa._summarize_assets(["not a dict", None]) == {}  # type: ignore[list-item]


# ---------------------------------------------------------------------------
# cmd_deploy_preview — guard runs BEFORE any API/profile work
# ---------------------------------------------------------------------------


class _ExplodingAPI:
    """If any method is called, the test fails — used to prove guards short-circuit."""

    def __getattr__(self, name):
        def boom(*_a, **_kw):
            raise AssertionError(
                f"_ExplodingAPI.{name} called — guard did not short-circuit"
            )
        return boom


def test_cmd_deploy_preview_guard_short_circuits_dev_to_prod():
    """Skip-tier transition must be refused before profile/token resolution."""
    # Patch load_profiles + get_token + WorkatoAPI to blow up if reached
    saved_load = wa.load_profiles
    saved_token = wa.get_token
    saved_api = wa.WorkatoAPI

    def boom_load():
        raise AssertionError("load_profiles called despite refused transition")

    def boom_token(_n):
        raise AssertionError("get_token called despite refused transition")

    class BoomAPI:
        def __init__(self, *a, **kw):
            raise AssertionError("WorkatoAPI() constructed despite refused transition")

    wa.load_profiles = boom_load
    wa.get_token = boom_token
    wa.WorkatoAPI = BoomAPI  # type: ignore[assignment]
    try:
        args = SimpleNamespace(
            from_env="dev", to_env="prod",
            folder_id=42, from_profile=None, to_profile=None,
            profile=None,
        )
        exited, code, err = _capture_stderr_exit(
            lambda: wa.cmd_deploy_preview(None, args)
        )
        assert exited and code == 1
        assert "dev->prod" in err
    finally:
        wa.load_profiles = saved_load
        wa.get_token = saved_token
        wa.WorkatoAPI = saved_api  # type: ignore[assignment]


def test_cmd_deploy_preview_end_to_end_dev_to_test():
    """Happy path: dev->test renders the expected preview JSON shape."""
    pool = {
        "acme-dev": {"region_url": "https://dev.example.com"},
        "acme-test": {"region_url": "https://test.example.com"},
    }
    saved_load = wa.load_profiles
    saved_resolve = wa.resolve_profile
    saved_token = wa.get_token
    saved_api = wa.WorkatoAPI

    def fake_load():
        return {"profiles": pool, "current_profile": None}

    def fake_resolve(explicit):
        if explicit is not None:
            return explicit, pool[explicit]
        return "acme-dev", pool["acme-dev"]

    def fake_token(name):
        assert name == "acme-dev", f"expected source token only, got {name}"
        return "fake-token"

    class FakeAPI:
        def __init__(self, base_url, token):
            self.base_url = base_url
            self.token = token
            self._calls: list[tuple[int, ...]] = []

        def deploy_folder_assets(self, folder_id):
            self._calls.append(("folder_assets", folder_id))
            return [
                {"id": 1, "type": "recipe", "name": "R1"},
                {"id": 2, "type": "connection", "name": "C1"},
            ]

    wa.load_profiles = fake_load
    wa.resolve_profile = fake_resolve
    wa.get_token = fake_token
    wa.WorkatoAPI = FakeAPI  # type: ignore[assignment]
    try:
        args = SimpleNamespace(
            from_env="dev", to_env="test",
            folder_id=42, from_profile=None, to_profile=None,
            profile=None,
        )
        out = _capture_stdout(lambda: wa.cmd_deploy_preview(None, args))
        parsed = json.loads(out)
        assert parsed["mode"] == "preview"
        assert parsed["source"]["profile"] == "acme-dev"
        assert parsed["source"]["env"] == "dev"
        assert parsed["source"]["workspace_url"].endswith("dev.example.com")
        assert parsed["target"]["profile"] == "acme-test"
        assert parsed["target"]["env"] == "test"
        assert parsed["target"]["workspace_url"].endswith("test.example.com")
        assert parsed["folder_id"] == 42
        assert parsed["asset_summary"] == {"recipe": 1, "connection": 1}
        assert len(parsed["assets"]) == 2
        assert any("No API writes" in n for n in parsed["notes"])
    finally:
        wa.load_profiles = saved_load
        wa.resolve_profile = saved_resolve
        wa.get_token = saved_token
        wa.WorkatoAPI = saved_api  # type: ignore[assignment]


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
