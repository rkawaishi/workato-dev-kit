#!/usr/bin/env python3
"""Tests for `scripts/migrate-to-toolkit.sh`.

Builds real local git repositories (an "old" and a "new" kit remote, plus a
workspace that tracks the old one as a submodule), runs the migration script,
and asserts the submodule is re-pointed at the new remote.

Run with:
    python3 scripts/tests/test_migrate_to_toolkit.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SCRIPT = REPO / "scripts" / "migrate-to-toolkit.sh"

OLD_SLUG = "workato-dev-kit"
NEW_SLUG = "workato-toolkit"

# Allow file:// submodules and keep git non-interactive / deterministic.
GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_COUNT": "1",
    "GIT_CONFIG_KEY_0": "protocol.file.allow",
    "GIT_CONFIG_VALUE_0": "always",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


def git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    r = subprocess.run(
        ["git", *args], cwd=str(cwd), env=GIT_ENV,
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"git {' '.join(args)} failed:\n{r.stdout}\n{r.stderr}"
    return r


def make_source_repo(root: Path, slug: str, marker: str) -> Path:
    """Create a working repo that looks like the kit, plus a bare clone to
    serve as its remote. Returns the bare remote path (whose name contains
    the slug, so the URL-slug swap has something to match)."""
    work = root / f"src-{slug}"
    work.mkdir(parents=True)
    git("init", "-b", "main", cwd=work)
    # Ship the real migration script and a setup.sh stub inside the kit.
    scripts_dir = work / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "migrate-to-toolkit.sh").write_text(SCRIPT.read_text())
    (work / "setup.sh").write_text("#!/usr/bin/env bash\necho stub setup\n")
    (work / marker).write_text(slug)
    git("add", "-A", cwd=work)
    git("commit", "-m", f"init {slug}", cwd=work)

    bare = root / "remotes" / f"{slug}.git"
    bare.parent.mkdir(parents=True, exist_ok=True)
    git("clone", "--bare", str(work), str(bare), cwd=root)
    return bare


def make_workspace(root: Path, old_remote: Path) -> Path:
    """Create a workspace repo tracking old_remote as the `kit/` submodule."""
    ws = root / "ws"
    ws.mkdir()
    git("init", "-b", "main", cwd=ws)
    (ws / "README.md").write_text("workspace\n")
    git("add", "-A", cwd=ws)
    git("commit", "-m", "init workspace", cwd=ws)
    git("-c", "protocol.file.allow=always",
        "submodule", "add", f"file://{old_remote}", "kit", cwd=ws)
    # Track main so `submodule update --remote` is deterministic.
    git("config", "-f", ".gitmodules", "submodule.kit.branch", "main", cwd=ws)
    git("add", "-A", cwd=ws)
    git("commit", "-m", "add kit submodule", cwd=ws)
    return ws


def run_migrate(ws: Path, *args: str, input_text: str | None = None
                ) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(ws / "kit" / "scripts" / "migrate-to-toolkit.sh"), *args],
        cwd=str(ws), env=GIT_ENV, capture_output=True, text=True,
        input=input_text,
    )


def submodule_url(ws: Path) -> str:
    return git("config", "-f", ".gitmodules", "submodule.kit.url", cwd=ws).stdout.strip()


def origin_url(ws: Path) -> str:
    return git("remote", "get-url", "origin", cwd=ws / "kit").stdout.strip()


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_migrates_url_and_content_with_yes():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        new = make_source_repo(root, NEW_SLUG, "MARKER_NEW")
        ws = make_workspace(root, old)

        assert OLD_SLUG in submodule_url(ws)
        r = run_migrate(ws, "-y")
        assert r.returncode == 0, r.stdout + r.stderr

        # .gitmodules and the submodule's own origin both point at the new repo.
        assert NEW_SLUG in submodule_url(ws), submodule_url(ws)
        assert OLD_SLUG not in submodule_url(ws)
        assert NEW_SLUG in origin_url(ws), origin_url(ws)

        # The derived URL is exactly the new bare remote.
        assert submodule_url(ws) == f"file://{new}"

        # Working tree now reflects the new remote's content.
        assert (ws / "kit" / "MARKER_NEW").exists()
        assert not (ws / "kit" / "MARKER_OLD").exists()


# ---------------------------------------------------------------------------
# Slug-swap preserves host / protocol / org
# ---------------------------------------------------------------------------

def test_slug_swap_preserves_surrounding_url():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        make_source_repo(root, NEW_SLUG, "MARKER_NEW")
        ws = make_workspace(root, old)

        before = submodule_url(ws)
        run_migrate(ws, "-y")
        after = submodule_url(ws)
        # Only the slug changed.
        assert after == before.replace(OLD_SLUG, NEW_SLUG)


# ---------------------------------------------------------------------------
# Dry run changes nothing
# ---------------------------------------------------------------------------

def test_dry_run_makes_no_changes():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        make_source_repo(root, NEW_SLUG, "MARKER_NEW")
        ws = make_workspace(root, old)

        before = submodule_url(ws)
        r = run_migrate(ws, "--dry-run")
        assert r.returncode == 0, r.stdout + r.stderr
        assert "dry-run" in r.stdout.lower()
        assert submodule_url(ws) == before
        assert OLD_SLUG in origin_url(ws)  # submodule remote untouched


# ---------------------------------------------------------------------------
# Idempotency: a second run is a clean no-op
# ---------------------------------------------------------------------------

def test_second_run_is_noop():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        make_source_repo(root, NEW_SLUG, "MARKER_NEW")
        ws = make_workspace(root, old)

        assert run_migrate(ws, "-y").returncode == 0
        migrated_url = submodule_url(ws)

        r2 = run_migrate(ws, "-y")
        assert r2.returncode == 0, r2.stdout + r2.stderr
        assert "already migrated" in r2.stdout.lower() \
            or "nothing to do" in r2.stdout.lower()
        assert submodule_url(ws) == migrated_url


# ---------------------------------------------------------------------------
# Explicit override URL
# ---------------------------------------------------------------------------

def test_explicit_new_url_override():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        # Give the new remote a name that is NOT the slug-swap of the old one,
        # so only an explicit override could select it.
        new = make_source_repo(root, "custom-fork-name", "MARKER_NEW")
        ws = make_workspace(root, old)

        r = run_migrate(ws, "-y", f"file://{new}")
        assert r.returncode == 0, r.stdout + r.stderr
        assert submodule_url(ws) == f"file://{new}"
        assert (ws / "kit" / "MARKER_NEW").exists()


# ---------------------------------------------------------------------------
# Confirmation prompt: declining aborts
# ---------------------------------------------------------------------------

def test_declining_prompt_aborts():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        old = make_source_repo(root, OLD_SLUG, "MARKER_OLD")
        make_source_repo(root, NEW_SLUG, "MARKER_NEW")
        ws = make_workspace(root, old)

        before = submodule_url(ws)
        # No -y, and /dev/tty is unavailable under capture → read fails → abort.
        r = run_migrate(ws, input_text="n\n")
        assert r.returncode == 1, r.stdout + r.stderr
        assert submodule_url(ws) == before  # unchanged


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_unknown_option_exits_2():
    r = subprocess.run(
        ["bash", str(SCRIPT), "--bogus"],
        env=GIT_ENV, capture_output=True, text=True,
    )
    assert r.returncode == 2, r.returncode


def test_help_exits_0():
    r = subprocess.run(
        ["bash", str(SCRIPT), "--help"],
        env=GIT_ENV, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    assert NEW_SLUG in r.stdout


def test_no_gitmodules_exits_1():
    """Running where the workspace has no .gitmodules (kit not a submodule)."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        ws = root / "plain"
        (ws / "kit" / "scripts").mkdir(parents=True)
        (ws / "kit" / "scripts" / "migrate-to-toolkit.sh").write_text(
            SCRIPT.read_text())
        git("init", "-b", "main", cwd=ws)
        r = run_migrate(ws)
        assert r.returncode == 1, r.stdout + r.stderr
        assert ".gitmodules" in (r.stdout + r.stderr)


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
