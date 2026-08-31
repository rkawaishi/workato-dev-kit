#!/usr/bin/env python3
"""Tests for the wk credential/profile backend in workato-api.py.

`wk` owns the credential store, so this helper reads the profile from
`wk auth status --json` and the token from `wk auth token`. The Platform CLI
path stays as a fallback for workspaces that have not migrated, and every
"wk cannot answer" case must fall through to it rather than fail.

Covers:
  - wk_auth_status: JSON shapes, nesting, non-zero exit, missing binary
  - wk_auth_token: success, failure, empty output
  - normalise_wk_profile: base_url vs region fallback
  - resolve_profile prefers wk and never touches ~/.workato/profiles
  - get_token routes to wk only for wk-sourced profiles
  - the delegated-command table stays in sync with the argparse stubs

Run with:
    python3 -m pytest scripts/tests/test_wk_delegation.py
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
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


def _runner(stdout="", returncode=0, stderr="", record=None):
    def run(argv, **_kw):
        if record is not None:
            record.append(argv)
        return SimpleNamespace(
            args=argv, returncode=returncode, stdout=stdout, stderr=stderr,
        )
    return run


def _missing_binary(*_a, **_kw):
    raise FileNotFoundError("wk")


def _capture_stderr_exit(fn):
    saved = sys.stderr
    sys.stderr = io.StringIO()
    exited, code = False, 0
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


PROFILE = {
    "name": "us-acme-dev",
    "workspace": "acme",
    "workspace_id": 2100000735,
    "environment": "dev",
    "region": "us",
    "base_url": "https://www.workato.com",
}


# ---------------------------------------------------------------------------
# wk_auth_status
# ---------------------------------------------------------------------------


def test_auth_status_parses_a_flat_profile():
    got = wa.wk_auth_status(_runner=_runner(json.dumps(PROFILE)))
    assert got["name"] == "us-acme-dev"


def test_auth_status_unwraps_a_nested_profile():
    """`auth status` also reports connectivity, so the profile may be nested."""
    payload = json.dumps({"profile": PROFILE, "reachable": True})
    got = wa.wk_auth_status(_runner=_runner(payload))
    assert got["name"] == "us-acme-dev"


def test_auth_status_forwards_explicit_profile():
    calls: list = []
    wa.wk_auth_status("other-dev", _runner=_runner(json.dumps(PROFILE), record=calls))
    assert calls[0][-2:] == ["--profile", "other-dev"]


def test_auth_status_returns_none_when_wk_exits_nonzero():
    assert wa.wk_auth_status(_runner=_runner("", returncode=1)) is None


def test_auth_status_returns_none_on_empty_output():
    assert wa.wk_auth_status(_runner=_runner("   ")) is None


def test_auth_status_returns_none_on_non_json():
    """An older wk without --json must fall through, not crash."""
    assert wa.wk_auth_status(_runner=_runner("Active profile: dev")) is None


def test_auth_status_returns_none_without_a_name():
    assert wa.wk_auth_status(_runner=_runner('{"reachable": true}')) is None


def test_auth_status_returns_none_when_wk_is_not_installed():
    assert wa.wk_auth_status(_runner=_missing_binary) is None


# ---------------------------------------------------------------------------
# wk_auth_token
# ---------------------------------------------------------------------------


def test_auth_token_strips_trailing_newline():
    assert wa.wk_auth_token(_runner=_runner("wrk_abc123\n")) == "wrk_abc123"


def test_auth_token_returns_none_on_failure():
    assert wa.wk_auth_token(_runner=_runner("", returncode=1)) is None


def test_auth_token_returns_none_on_empty_output():
    assert wa.wk_auth_token(_runner=_runner("\n")) is None


def test_auth_token_returns_none_when_wk_is_not_installed():
    assert wa.wk_auth_token(_runner=_missing_binary) is None


# ---------------------------------------------------------------------------
# normalise_wk_profile
# ---------------------------------------------------------------------------


def test_normalise_uses_base_url_when_present():
    got = wa.normalise_wk_profile(PROFILE)
    assert got["region_url"] == "https://www.workato.com"
    assert got["workspace_id"] == 2100000735
    assert got["environment"] == "dev"
    assert got["_source"] == "wk"


def test_normalise_strips_trailing_slash_from_base_url():
    got = wa.normalise_wk_profile({**PROFILE, "base_url": "https://www.workato.com/"})
    assert got["region_url"] == "https://www.workato.com"


def test_normalise_falls_back_to_region_table():
    got = wa.normalise_wk_profile({**PROFILE, "base_url": "", "region": "eu"})
    assert got["region_url"] == wa.WK_REGION_URLS["eu"]


def test_normalise_keeps_the_wk_profile_name_for_token_lookup():
    assert wa.normalise_wk_profile(PROFILE)["_wk_profile"] == "us-acme-dev"


# ---------------------------------------------------------------------------
# resolve_profile / get_token wiring
# ---------------------------------------------------------------------------


def _patch(**attrs):
    saved = {k: getattr(wa, k) for k in attrs}
    for k, v in attrs.items():
        setattr(wa, k, v)

    def restore():
        for k, v in saved.items():
            setattr(wa, k, v)
    return restore


def test_resolve_profile_prefers_wk_and_skips_platform_cli():
    def _boom():
        raise AssertionError("load_profiles called even though wk answered")

    restore = _patch(
        wk_auth_status=lambda *_a, **_kw: PROFILE,
        load_profiles=_boom,
    )
    try:
        name, profile = wa.resolve_profile(None)
    finally:
        restore()
    assert name == "us-acme-dev"
    assert profile["_source"] == "wk"


def test_resolve_profile_falls_back_when_wk_has_no_profile():
    pool = {"acme-dev": {"region_url": "https://x", "workspace_id": 1}}
    restore = _patch(
        wk_auth_status=lambda *_a, **_kw: None,
        load_profiles=lambda: {"profiles": pool, "current_profile": "acme-dev"},
        find_workatoenv=lambda *_a, **_kw: None,
    )
    try:
        name, profile = wa.resolve_profile(None)
    finally:
        restore()
    assert name == "acme-dev"
    assert profile.get("_source") is None


def test_get_token_uses_wk_for_a_wk_sourced_profile():
    restore = _patch(wk_auth_token=lambda name: f"token-for-{name}")
    saved_env = wa.os.environ.pop("WORKATO_API_TOKEN", None)
    try:
        token = wa.get_token("us-acme-dev", wa.normalise_wk_profile(PROFILE))
    finally:
        restore()
        if saved_env is not None:
            wa.os.environ["WORKATO_API_TOKEN"] = saved_env
    assert token == "token-for-us-acme-dev"


def test_get_token_fails_loudly_when_wk_store_is_empty():
    """Silently falling through to the Platform CLI keyring would resolve a
    credential for a different workspace."""
    restore = _patch(wk_auth_token=lambda _n: None)
    saved_env = wa.os.environ.pop("WORKATO_API_TOKEN", None)
    try:
        exited, code, err = _capture_stderr_exit(
            lambda: wa.get_token("us-acme-dev", wa.normalise_wk_profile(PROFILE))
        )
    finally:
        restore()
        if saved_env is not None:
            wa.os.environ["WORKATO_API_TOKEN"] = saved_env
    assert exited and code == 1
    assert "wk auth token" in err


def test_env_var_still_wins_over_wk():
    restore = _patch(wk_auth_token=lambda _n: "from-wk")
    wa.os.environ["WORKATO_API_TOKEN"] = "from-env"
    try:
        token = wa.get_token("us-acme-dev", wa.normalise_wk_profile(PROFILE))
    finally:
        restore()
        wa.os.environ.pop("WORKATO_API_TOKEN", None)
    assert token == "from-env"


# ---------------------------------------------------------------------------
# delegated command table
# ---------------------------------------------------------------------------


def test_every_delegated_entry_names_a_wk_command():
    for (group, sub), replacement in wa.DELEGATED_TO_WK.items():
        assert replacement.startswith("wk "), (group, sub, replacement)


def test_delegated_exit_reports_the_replacement():
    exited, code, err = _capture_stderr_exit(
        lambda: wa._delegated_exit("jobs", "list")
    )
    assert exited and code == 2
    assert "wk recipes jobs" in err


def test_delegated_subcommands_are_still_registered_in_argparse():
    """Removing the parser outright would say "invalid choice" instead of
    pointing at the replacement."""
    saved = sys.argv
    for group, sub in wa.DELEGATED_TO_WK:
        sys.argv = ["workato-api.py", group, sub]
        try:
            exited, code, err = _capture_stderr_exit(wa.main)
        finally:
            sys.argv = saved
        assert exited and code == 2, (group, sub)
        assert "has been removed" in err, (group, sub)
