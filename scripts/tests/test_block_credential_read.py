#!/usr/bin/env python3
"""Tests for the credential-block PreToolUse hooks.

Covers framework/claude/hooks/block-credential-read.sh (every read-ish
tool plus Bash) and framework/codex/hooks/block-credential-read.sh
(Bash-only — the rest do not fire PreToolUse in Codex).

Run with:
    python3 scripts/tests/test_block_credential_read.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CLAUDE_HOOK = REPO / "framework" / "claude" / "hooks" / "block-credential-read.sh"
CODEX_HOOK = REPO / "framework" / "codex" / "hooks" / "block-credential-read.sh"


def run(hook: Path, payload: dict | str) -> subprocess.CompletedProcess:
    body = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        ["bash", str(hook)],
        input=body, capture_output=True, text=True,
    )


# ---------------------------------------------------------------------------
# Claude hook — paths
# ---------------------------------------------------------------------------

def test_claude_allows_read_workatoenv():
    # .workatoenv is git-managed metadata (no credentials); skills must read it.
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": "projects/foo/.workatoenv"}})
    assert r.returncode == 0, r.stderr


def test_claude_blocks_read_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": "/abs/connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_read_settings_yaml_enc():
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": "connectors/y/settings.yaml.enc"}})
    assert r.returncode == 2


def test_claude_blocks_read_glob_dot_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": "secrets/id_rsa.key"}})
    assert r.returncode == 2


def test_claude_blocks_read_dot_env_variant():
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": ".env.production"}})
    assert r.returncode == 2


def test_claude_allows_normal_recipe_read():
    r = run(CLAUDE_HOOK, {"tool_name": "Read",
                          "tool_input": {"file_path": "projects/foo/Recipes/a.recipe.json"}})
    assert r.returncode == 0, r.stderr


def test_claude_blocks_edit_credential():
    r = run(CLAUDE_HOOK, {"tool_name": "Edit",
                          "tool_input": {"file_path": "master.key"}})
    assert r.returncode == 2


def test_claude_blocks_write_credential():
    r = run(CLAUDE_HOOK, {"tool_name": "Write",
                          "tool_input": {"file_path": "settings.yaml"}})
    assert r.returncode == 2


def test_claude_blocks_grep_inside_credential_dir():
    r = run(CLAUDE_HOOK, {"tool_name": "Grep",
                          "tool_input": {"path": "connectors/foo/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_grep_on_dir_containing_credential(tmp_path=None):
    """Codex P1 regression: Grep(path=<dir>) must block if the directory
    contains a credential file, even when the path itself is innocent."""
    import os, tempfile
    with tempfile.TemporaryDirectory() as d:
        cred_dir = Path(d) / "connectors" / "x"
        cred_dir.mkdir(parents=True)
        (cred_dir / "master.key").write_text("secret")
        (cred_dir / "connector.rb").write_text("# code")
        r = run(CLAUDE_HOOK, {"tool_name": "Grep",
                              "tool_input": {"path": str(Path(d) / "connectors")}})
        assert r.returncode == 2, r.stderr
        assert "master.key" in r.stderr


def test_claude_blocks_glob_on_dir_containing_credential():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "settings.yaml.enc").write_text("ciphertext")
        r = run(CLAUDE_HOOK, {"tool_name": "Glob",
                              "tool_input": {"path": str(d), "pattern": "**/*.rb"}})
        assert r.returncode == 2, r.stderr


def test_claude_allows_grep_on_clean_dir():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "a.recipe.json").write_text("{}")
        (Path(d) / "b.recipe.json").write_text("{}")
        r = run(CLAUDE_HOOK, {"tool_name": "Grep",
                              "tool_input": {"path": str(d)}})
        assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------------------
# Claude hook — Bash
# ---------------------------------------------------------------------------

def test_claude_allows_bash_cat_workatoenv():
    # .workatoenv is git-managed metadata (no credentials); reading it is fine.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "cat projects/foo/.workatoenv | head"}})
    assert r.returncode == 0, r.stderr


def test_claude_blocks_bash_glob_token():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "openssl pkey -in id_rsa.key -text"}})
    assert r.returncode == 2


def test_claude_allows_bash_ls_projects():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "ls projects/"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_bash_no_creds():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git status"}})
    assert r.returncode == 0, r.stderr


# Legitimate tools (workato CLI / git / kit helper) operate ON credential
# files without dumping their contents, so they must not be blocked even when
# a credential filename appears as an argument.

def test_claude_allows_workato_edit_enc():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "workato edit settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_git_add_enc():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git add connectors/foo/settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_helper_script_normal_command():
    # The helper's normal commands name no credential file, so they pass.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "python3 scripts/workato-api.py profile show"}})
    assert r.returncode == 0, r.stderr


def test_claude_blocks_helper_sdk_decrypt():
    # `sdk decrypt` prints plaintext to stdout — the helper is NOT allowlisted.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "python3 scripts/workato-api.py sdk decrypt settings.yaml.enc --key master.key"}})
    assert r.returncode == 2


def test_claude_blocks_git_add_patch():
    # `git add -p <file>` prints hunks of file contents.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git add -p connectors/x/settings.yaml"}})
    assert r.returncode == 2


def test_claude_blocks_git_stash_show_patch_named():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git stash show -p connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_git_status_verbose():
    # `git status -v` prints the staged diff (content) to stdout.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git status -v -- connectors/x/settings.yaml"}})
    assert r.returncode == 2


def test_claude_blocks_git_status_bundled_verbose_short_flag():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git status -vv connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_git_verbose_abbreviation():
    # git accepts `--ver` as an abbreviation of --verbose.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git status --ver -- connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_git_patch_abbreviation():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git add --patc connectors/x/settings.yaml"}})
    assert r.returncode == 2


def test_claude_allows_git_add_with_pathspec_separator():
    # `--` is the pathspec separator, not a content-printing option.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git add -- connectors/x/settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_output_dot_key_false_positive():
    # `*.key` must not block a non-credential output file passed to a safe tool.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "workato generate schema --output=out.key"}})
    assert r.returncode == 0, r.stderr


# --- Surfacing model: feeding a credential to a program is allowed ----------

def test_claude_allows_bundle_exec_workato_exec_with_settings_and_key():
    # Standard local-test form names both the encrypted settings and the key as
    # -s / -k args to a non-printing tool → content never reaches the agent.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "bundle exec workato exec connectors/foo/connector.rb test -s settings.yaml.enc -k master.key"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_cp_encrypted_settings():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "cp connectors/x/settings.yaml.enc connectors/x/settings.yaml.enc.bak"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_mv_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "mv master.key connectors/x/master.key"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_custom_script_takes_settings_arg():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "./deploy.sh --settings connectors/x/settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_claude_allows_curl_client_key():
    # `*.key` matches client.key, but curl uses it for TLS, never printing it.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "curl --key connectors/x/client.key https://example.test"}})
    assert r.returncode == 0, r.stderr


# --- Surfacing model: emitters behind a runner wrapper still block -----------

def test_claude_blocks_env_cat_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "env cat master.key"}})
    assert r.returncode == 2


def test_claude_blocks_time_cat_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "time cat master.key"}})
    assert r.returncode == 2


def test_claude_blocks_bundle_exec_cat_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "bundle exec cat master.key"}})
    assert r.returncode == 2


def test_claude_blocks_redirect_read_in_substitution():
    # `$(< master.key)` splits to a bare `< master.key` segment that reads the
    # file straight into the command substitution (→ stdout → agent).
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "echo \"$(< master.key)\""}})
    assert r.returncode == 2


def test_claude_blocks_base64_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "base64 connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_bash_cat_master_key():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "cat connectors/x/master.key"}})
    assert r.returncode == 2


def test_claude_blocks_dump_in_chained_command():
    # A safe leading segment must not shield a later dump segment.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git status && cat master.key"}})
    assert r.returncode == 2


# The allowlist must not be defeatable by cheap tricks (Codex review).

def test_claude_blocks_comment_spoof_helper_marker():
    # A trailing comment naming the helper script must not allowlist a dump.
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "cat master.key # workato-api.py"}})
    assert r.returncode == 2


def test_claude_blocks_git_diff_no_index():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git --no-pager diff --no-index /dev/null master.key"}})
    assert r.returncode == 2


def test_claude_blocks_git_dash_c_alias():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git -c alias.x='!cat master.key' x"}})
    assert r.returncode == 2


def test_claude_blocks_git_show_secret():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "git show HEAD:connectors/x/settings.yaml"}})
    assert r.returncode == 2


def test_claude_blocks_python_dash_c_dump():
    r = run(CLAUDE_HOOK, {"tool_name": "Bash",
                          "tool_input": {"command": "python3 -c \"print(open('master.key').read())\""}})
    assert r.returncode == 2


# ---------------------------------------------------------------------------
# Claude hook — fail-open on malformed input
# ---------------------------------------------------------------------------

def test_claude_allows_malformed_json():
    r = run(CLAUDE_HOOK, "not-json{")
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------------------
# Codex hook (Bash-only)
# ---------------------------------------------------------------------------

def test_codex_blocks_bash_grep_master_key():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "grep token connectors/x/master.key"}})
    assert r.returncode == 2


def test_codex_allows_bash_cat_workatoenv():
    # .workatoenv is git-managed metadata (no credentials); reading it is fine.
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "cat .workatoenv"}})
    assert r.returncode == 0, r.stderr


def test_codex_allows_non_bash_read():
    # Codex PreToolUse only fires for Bash; if a non-Bash payload somehow
    # arrives, the hook must not block (it has no signal to act on).
    r = run(CODEX_HOOK, {"tool_name": "Read",
                         "tool_input": {"file_path": ".workatoenv"}})
    assert r.returncode == 0


def test_codex_allows_bash_no_creds():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "git status"}})
    assert r.returncode == 0


def test_codex_allows_workato_edit_enc():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "workato edit settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_codex_allows_git_add_enc():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "git add connectors/foo/settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_codex_blocks_helper_sdk_decrypt():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "python3 scripts/workato-api.py sdk decrypt settings.yaml.enc --key master.key"}})
    assert r.returncode == 2


def test_codex_blocks_git_add_patch():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "git add -p connectors/x/settings.yaml"}})
    assert r.returncode == 2


def test_codex_allows_malformed_json():
    r = run(CODEX_HOOK, "{broken")
    assert r.returncode == 0


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
