#!/usr/bin/env python3
"""Tests for the retrofit of sdk push + oauth-profiles create/update/delete.

Each command now:
  - calls require_dev_profile_for_mutation before doing anything else
  - honors --dry-run by emitting the intended request and skipping the API
  - redacts secrets in dry-run output (oauth-profiles)

Run with:
    python3 scripts/tests/test_retrofit_mutations.py
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
    saved_err = sys.stderr
    sys.stderr = io.StringIO()  # silence informational stderr
    try:
        fn()
        return sys.stdout.getvalue()
    finally:
        sys.stdout = saved
        sys.stderr = saved_err


class _ExplodingAPI:
    base_url = "https://workato.example.com"

    def __getattr__(self, name):
        def boom(*_a, **_kw):
            raise AssertionError(f"_ExplodingAPI.{name} called despite guard")
        return boom


class _RecordingAPI:
    def __init__(self, base_url="https://workato.example.com"):
        self.base_url = base_url
        self.calls: list = []

    def sdk_push(self, **kwargs):
        self.calls.append(("sdk_push", kwargs))
        return {"id": 99, "title": kwargs.get("title", "X")}

    def oauth_profiles_create(self, **kwargs):
        self.calls.append(("create", kwargs))
        return {"id": 1, "name": kwargs.get("name")}

    def oauth_profiles_update(self, **kwargs):
        self.calls.append(("update", kwargs))
        return {"id": kwargs["profile_id"], "name": kwargs.get("name")}

    def oauth_profiles_delete(self, profile_id):
        self.calls.append(("delete", profile_id))
        return {"success": True}


# ---------------------------------------------------------------------------
# _redact_oauth_body
# ---------------------------------------------------------------------------


def test_redact_masks_client_secret():
    body = {"data": {"client_id": "id", "client_secret": "sekret"}}
    out = wa._redact_oauth_body(body)
    assert out["data"]["client_secret"] == "***REDACTED***"
    assert out["data"]["client_id"] == "id"


def test_redact_masks_token():
    body = {"data": {"token": "xoxb-1234"}}
    out = wa._redact_oauth_body(body)
    assert out["data"]["token"] == "***REDACTED***"


def test_redact_leaves_input_untouched():
    """Defense-in-depth: original dict must not be mutated."""
    body = {"data": {"client_secret": "sekret"}}
    wa._redact_oauth_body(body)
    assert body["data"]["client_secret"] == "sekret"


def test_redact_handles_missing_data_key():
    """Body without `data` should be returned without crashing."""
    assert wa._redact_oauth_body({}) == {}


def test_redact_handles_none_token():
    """A token field that is None should not become '***REDACTED***'."""
    body = {"data": {"token": None, "client_secret": "x"}}
    out = wa._redact_oauth_body(body)
    assert out["data"]["token"] is None
    assert out["data"]["client_secret"] == "***REDACTED***"


# ---------------------------------------------------------------------------
# cmd_oauth_profiles_create — guard + --dry-run + happy path
# ---------------------------------------------------------------------------


def test_oauth_create_refuses_non_dev():
    api = _ExplodingAPI()
    args = SimpleNamespace(
        name="x", provider="slack", client_id="id", client_secret="sek",
        token=None, dry_run=False, _resolved_profile_name="acme-prod",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_oauth_profiles_create(api, args)
    )
    assert exited and code == 1
    assert "prod" in err


def test_oauth_create_dry_run_does_not_call_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        name="x", provider="slack", client_id="id", client_secret="sek",
        token="xoxb-tok", dry_run=True, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_oauth_profiles_create(api, args))
    parsed = json.loads(out)
    assert parsed["mode"] == "dry-run"
    assert parsed["would_call"]["method"] == "POST"
    assert parsed["would_call"]["url"].endswith("/api/custom_oauth_profiles")
    body = parsed["would_call"]["body"]
    assert body["data"]["client_secret"] == "***REDACTED***"
    assert body["data"]["token"] == "***REDACTED***"
    assert body["data"]["client_id"] == "id"
    assert api.calls == []


def test_oauth_create_happy_path_invokes_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        name="x", provider="slack", client_id="id", client_secret="sek",
        token=None, dry_run=False, _resolved_profile_name="acme-dev",
    )
    _capture_stdout(lambda: wa.cmd_oauth_profiles_create(api, args))
    assert len(api.calls) == 1
    assert api.calls[0][0] == "create"


# ---------------------------------------------------------------------------
# cmd_oauth_profiles_update — guard + --dry-run + happy path
# ---------------------------------------------------------------------------


def test_oauth_update_refuses_non_dev():
    api = _ExplodingAPI()
    args = SimpleNamespace(
        id=42, name="x", provider="slack",
        client_id="id", client_secret="sek", token=None,
        dry_run=False, _resolved_profile_name="acme-test",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_oauth_profiles_update(api, args)
    )
    assert exited and code == 1
    assert "test" in err


def test_oauth_update_dry_run_redacts_secrets():
    api = _RecordingAPI()
    args = SimpleNamespace(
        id=42, name="x", provider="slack",
        client_id="id", client_secret="sek", token=None,
        dry_run=True, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_oauth_profiles_update(api, args))
    parsed = json.loads(out)
    assert parsed["would_call"]["method"] == "PUT"
    assert parsed["would_call"]["url"].endswith("/api/custom_oauth_profiles/42")
    assert parsed["would_call"]["body"]["data"]["client_secret"] == "***REDACTED***"
    assert api.calls == []


def test_oauth_update_happy_path_invokes_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        id=42, name="x", provider="slack",
        client_id="id", client_secret="sek", token=None,
        dry_run=False, _resolved_profile_name="acme-dev",
    )
    _capture_stdout(lambda: wa.cmd_oauth_profiles_update(api, args))
    assert api.calls[0][0] == "update"
    assert api.calls[0][1]["profile_id"] == 42


# ---------------------------------------------------------------------------
# cmd_oauth_profiles_delete — guard + --dry-run + happy path
# ---------------------------------------------------------------------------


def test_oauth_delete_refuses_non_dev():
    api = _ExplodingAPI()
    args = SimpleNamespace(
        id=99, dry_run=False, _resolved_profile_name="acme-prod",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_oauth_profiles_delete(api, args)
    )
    assert exited and code == 1
    assert "prod" in err


def test_oauth_delete_dry_run_does_not_call_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        id=99, dry_run=True, _resolved_profile_name="acme-dev",
    )
    out = _capture_stdout(lambda: wa.cmd_oauth_profiles_delete(api, args))
    parsed = json.loads(out)
    assert parsed["would_call"]["method"] == "DELETE"
    assert parsed["would_call"]["url"].endswith("/api/custom_oauth_profiles/99")
    assert parsed["would_call"]["body"] is None
    assert api.calls == []


def test_oauth_delete_happy_path_invokes_api():
    api = _RecordingAPI()
    args = SimpleNamespace(
        id=99, dry_run=False, _resolved_profile_name="acme-dev",
    )
    _capture_stdout(lambda: wa.cmd_oauth_profiles_delete(api, args))
    assert api.calls == [("delete", 99)]


# ---------------------------------------------------------------------------
# cmd_sdk_push — guard + --dry-run + happy path
# ---------------------------------------------------------------------------


def _chdir(target: Path) -> Path:
    prev = Path.cwd()
    os.chdir(target)
    return prev


def _make_connector_dir(root: Path, name: str = "foo",
                        with_id: int | None = None) -> Path:
    """Create connectors/<name>/connector.rb and (optionally) the docs file
    with `connector_id: <with_id>` in its frontmatter."""
    cdir = root / "connectors" / name
    cdir.mkdir(parents=True)
    (cdir / "connector.rb").write_text("{ title: 'Foo' }\n")
    if with_id is not None:
        docs = root / "connectors" / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / f"{name}.md").write_text(
            f"---\nconnector_id: {with_id}\n---\n# {name}\n"
        )
    return cdir / "connector.rb"


def test_sdk_push_refuses_non_dev():
    api = _ExplodingAPI()
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            cpath = _make_connector_dir(Path(d), with_id=42)
            args = SimpleNamespace(
                connector=str(cpath), title=None, connector_id=None,
                description=None, notes=None, no_release=False,
                skip_save_id=True, dry_run=False,
                _resolved_profile_name="acme-prod",
            )
            exited, code, err = _capture_stderr_exit(
                lambda: wa.cmd_sdk_push(api, args)
            )
            assert exited and code == 1
            assert "prod" in err
        finally:
            os.chdir(prev)


def test_sdk_push_dry_run_update_path():
    api = _RecordingAPI()
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            cpath = _make_connector_dir(Path(d), with_id=42)
            args = SimpleNamespace(
                connector=str(cpath), title=None, connector_id=None,
                description=None, notes=None, no_release=False,
                skip_save_id=True, dry_run=True,
                _resolved_profile_name="acme-dev",
            )
            out = _capture_stdout(lambda: wa.cmd_sdk_push(api, args))
            parsed = json.loads(out)
            assert parsed["mode"] == "dry-run"
            assert parsed["is_update"] is True
            assert parsed["would_call"]["method"] == "PUT"
            assert parsed["would_call"]["url"].endswith("/api/custom_connectors/42")
            assert parsed["would_call"]["body_summary"]["title"] == "Foo"
            assert parsed["would_call"]["body_summary"]["code_length"] > 0
            assert parsed["would_release"] is True
            assert api.calls == []
        finally:
            os.chdir(prev)


def test_sdk_push_dry_run_create_path():
    """No existing docs frontmatter → would POST to /api/custom_connectors."""
    api = _RecordingAPI()
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            cpath = _make_connector_dir(Path(d), with_id=None)
            args = SimpleNamespace(
                connector=str(cpath), title=None, connector_id=None,
                description=None, notes=None, no_release=False,
                skip_save_id=True, dry_run=True,
                _resolved_profile_name="acme-dev",
            )
            out = _capture_stdout(lambda: wa.cmd_sdk_push(api, args))
            parsed = json.loads(out)
            assert parsed["is_update"] is False
            assert parsed["would_call"]["method"] == "POST"
            assert parsed["would_call"]["url"].endswith("/api/custom_connectors")
            assert api.calls == []
        finally:
            os.chdir(prev)


def test_sdk_push_dry_run_no_release_flag():
    api = _RecordingAPI()
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            cpath = _make_connector_dir(Path(d), with_id=7)
            args = SimpleNamespace(
                connector=str(cpath), title=None, connector_id=None,
                description=None, notes=None, no_release=True,
                skip_save_id=True, dry_run=True,
                _resolved_profile_name="acme-dev",
            )
            out = _capture_stdout(lambda: wa.cmd_sdk_push(api, args))
            parsed = json.loads(out)
            assert parsed["would_release"] is False
        finally:
            os.chdir(prev)


def test_sdk_push_happy_path_invokes_api():
    api = _RecordingAPI()
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            cpath = _make_connector_dir(Path(d), with_id=42)
            args = SimpleNamespace(
                connector=str(cpath), title=None, connector_id=None,
                description=None, notes=None, no_release=False,
                skip_save_id=True, dry_run=False,
                _resolved_profile_name="acme-dev",
            )
            _capture_stdout(lambda: wa.cmd_sdk_push(api, args))
            assert len(api.calls) == 1
            assert api.calls[0][0] == "sdk_push"
            assert api.calls[0][1]["connector_id"] == 42
        finally:
            os.chdir(prev)


def test_sdk_push_guard_runs_before_file_read():
    """A non-dev profile should fail before the connector file is even read."""
    api = _ExplodingAPI()
    args = SimpleNamespace(
        connector="/nonexistent/path/connector.rb",
        title=None, connector_id=None,
        description=None, notes=None, no_release=False,
        skip_save_id=True, dry_run=True,
        _resolved_profile_name="acme-test",
    )
    exited, code, err = _capture_stderr_exit(
        lambda: wa.cmd_sdk_push(api, args)
    )
    assert exited and code == 1
    # The error must be about the profile, not "File not found".
    assert "test" in err
    assert "File not found" not in err


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
