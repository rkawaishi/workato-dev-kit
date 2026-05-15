#!/usr/bin/env python3
"""Tests for `sdk pull` helpers in `scripts/workato-api.py`.

Run with:
    python3 scripts/tests/test_sdk_pull.py
"""

from __future__ import annotations

import importlib.util
import io
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
# _extract_connector_source
# ---------------------------------------------------------------------------


def test_extract_source_top_level_code():
    assert wa._extract_connector_source({"code": "{ title: 'X' }"}) == "{ title: 'X' }"


def test_extract_source_source_code_alias():
    assert wa._extract_connector_source({"source_code": "X"}) == "X"


def test_extract_source_latest_released_version():
    rec = {"latest_released_version": {"code": "Y"}}
    assert wa._extract_connector_source(rec) == "Y"


def test_extract_source_released_versions_picks_newest():
    rec = {
        "released_versions": [
            {"version": 1, "code": "v1"},
            {"version": 3, "code": "v3"},
            {"version": 2, "code": "v2"},
        ]
    }
    assert wa._extract_connector_source(rec) == "v3"


def test_extract_source_released_versions_non_int_version():
    rec = {
        "released_versions": [
            {"version": "abc", "code": "vA"},
            {"version": 1, "code": "v1"},
        ]
    }
    assert wa._extract_connector_source(rec) == "v1"


def test_extract_source_missing():
    assert wa._extract_connector_source({}) is None
    assert wa._extract_connector_source({"name": "foo"}) is None


def test_extract_source_non_dict():
    assert wa._extract_connector_source([]) is None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# _connector_slug
# ---------------------------------------------------------------------------


def test_connector_slug_uses_name():
    assert wa._connector_slug({"name": "my_conn", "title": "Whatever"}) == "my_conn"


def test_connector_slug_falls_back_to_title():
    assert wa._connector_slug({"title": "My Cool Connector"}) == "my_cool_connector"


def test_connector_slug_falls_back_to_arg():
    assert wa._connector_slug({}, fallback="cli-arg") == "cli_arg"


def test_connector_slug_falls_back_to_id_when_empty():
    assert wa._connector_slug({"id": 42}, fallback=None) == "42"


# ---------------------------------------------------------------------------
# cmd_sdk_pull
# ---------------------------------------------------------------------------


class _FakeAPI:
    """Stub WorkatoAPI for cmd_sdk_pull tests."""

    def __init__(self, *, list_response=None, get_response=None):
        self._list = list_response or []
        self._get = get_response or {}
        self.get_calls: list[int] = []
        self.list_calls = 0

    def connectors_list_custom(self):
        self.list_calls += 1
        return self._list

    def connectors_get_custom(self, connector_id: int):
        self.get_calls.append(connector_id)
        return self._get


def _chdir(path: Path):
    """Tiny context-manager-like helper to change cwd for the duration of a test."""
    import os
    prev = Path.cwd()
    os.chdir(path)
    return prev


def test_sdk_pull_requires_id_or_name():
    api = _FakeAPI()
    args = SimpleNamespace(
        connector_id=None, name=None, output_dir=None,
        force=False, skip_save_id=False,
    )
    saved = sys.stderr
    sys.stderr = io.StringIO()
    try:
        try:
            wa.cmd_sdk_pull(api, args)
        except SystemExit as e:
            assert e.code == 1
        err = sys.stderr.getvalue()
    finally:
        sys.stderr = saved
    assert "--connector-id" in err


def test_sdk_pull_writes_file_and_frontmatter():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(get_response={
                "id": 42,
                "name": "my_conn",
                "title": "My Connector",
                "code": "{ title: 'My' }\n",
            })
            args = SimpleNamespace(
                connector_id=42, name=None, output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            try:
                wa.cmd_sdk_pull(api, args)
            finally:
                sys.stderr = saved

            rb = Path(d) / "connectors" / "my_conn" / "connector.rb"
            assert rb.exists()
            assert rb.read_text() == "{ title: 'My' }\n"

            docs = Path(d) / "connectors" / "docs" / "my_conn.md"
            assert docs.exists()
            assert "connector_id: 42" in docs.read_text()
            assert api.get_calls == [42]
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_refuses_overwrite_without_force():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            rb_dir = Path(d) / "connectors" / "my_conn"
            rb_dir.mkdir(parents=True)
            (rb_dir / "connector.rb").write_text("ORIGINAL\n")

            api = _FakeAPI(get_response={
                "id": 42, "name": "my_conn", "code": "NEW\n",
            })
            args = SimpleNamespace(
                connector_id=42, name=None, output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            exited = False
            try:
                try:
                    wa.cmd_sdk_pull(api, args)
                except SystemExit as e:
                    exited = (e.code == 1)
                err = sys.stderr.getvalue()
            finally:
                sys.stderr = saved
            assert exited, "expected SystemExit(1) for refused overwrite"
            assert "already exists" in err
            assert (rb_dir / "connector.rb").read_text() == "ORIGINAL\n"
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_force_overwrites():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            rb_dir = Path(d) / "connectors" / "my_conn"
            rb_dir.mkdir(parents=True)
            (rb_dir / "connector.rb").write_text("ORIGINAL\n")

            api = _FakeAPI(get_response={
                "id": 42, "name": "my_conn", "code": "NEW\n",
            })
            args = SimpleNamespace(
                connector_id=42, name=None, output_dir=None,
                force=True, skip_save_id=True,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            try:
                wa.cmd_sdk_pull(api, args)
            finally:
                sys.stderr = saved
            assert (rb_dir / "connector.rb").read_text() == "NEW\n"
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_resolves_name_via_list():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(
                list_response=[
                    {"id": 11, "name": "other", "title": "Other"},
                    {"id": 42, "name": "my_conn", "title": "My", "code": "Z\n"},
                ],
            )
            args = SimpleNamespace(
                connector_id=None, name="my_conn", output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            try:
                wa.cmd_sdk_pull(api, args)
            finally:
                sys.stderr = saved

            rb = Path(d) / "connectors" / "my_conn" / "connector.rb"
            assert rb.read_text() == "Z\n"
            # list response carried code, so no per-id fetch was needed
            assert api.get_calls == []
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_name_not_found():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(list_response=[{"id": 1, "name": "other"}])
            args = SimpleNamespace(
                connector_id=None, name="missing", output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            exited = False
            try:
                try:
                    wa.cmd_sdk_pull(api, args)
                except SystemExit as e:
                    exited = (e.code == 1)
                err = sys.stderr.getvalue()
            finally:
                sys.stderr = saved
            assert exited
            assert "no custom connector" in err
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_ambiguous_name():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(list_response=[
                {"id": 1, "name": "foo", "title": "X"},
                {"id": 2, "name": "bar", "title": "foo"},
            ])
            args = SimpleNamespace(
                connector_id=None, name="foo", output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            exited = False
            try:
                try:
                    wa.cmd_sdk_pull(api, args)
                except SystemExit as e:
                    exited = (e.code == 1)
                err = sys.stderr.getvalue()
            finally:
                sys.stderr = saved
            assert exited
            assert "ambiguous" in err
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_no_source_in_response():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(get_response={"id": 9, "name": "noc"})
            args = SimpleNamespace(
                connector_id=9, name=None, output_dir=None,
                force=False, skip_save_id=False,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            exited = False
            try:
                try:
                    wa.cmd_sdk_pull(api, args)
                except SystemExit as e:
                    exited = (e.code == 1)
                err = sys.stderr.getvalue()
            finally:
                sys.stderr = saved
            assert exited
            assert "no source code" in err
        finally:
            import os
            os.chdir(prev)


def test_sdk_pull_output_dir_override():
    with tempfile.TemporaryDirectory() as d:
        prev = _chdir(Path(d))
        try:
            api = _FakeAPI(get_response={
                "id": 7, "name": "abc", "code": "OK\n",
            })
            args = SimpleNamespace(
                connector_id=7, name=None,
                output_dir=str(Path(d) / "custom_loc"),
                force=False, skip_save_id=True,
            )
            saved = sys.stderr
            sys.stderr = io.StringIO()
            try:
                wa.cmd_sdk_pull(api, args)
            finally:
                sys.stderr = saved
            assert (Path(d) / "custom_loc" / "connector.rb").read_text() == "OK\n"
        finally:
            import os
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
