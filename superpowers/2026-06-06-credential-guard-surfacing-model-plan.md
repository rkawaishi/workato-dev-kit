# Credential Guard 表出モデル再設計 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** credential guard の Bash スキャンを「プログラム許可リスト（default-deny）」から「内容が stdout/stderr に表出するときだけブロック（default-allow）」へ作り替え、正当な開発コマンドの偽陽性を構造的に解消する。

**Architecture:** Read/Edit/Write/Grep/Glob のパス照合（一次防御・default-deny）は不変。Bash ブランチのみ刷新：セグメント分割 → credential パターンを含むセグメントについて `surfaces(seg)` が真（emitter / 既知プリンタ / インタプリタ -c|-e / `<` 読み込み / git 非safe）のときだけ block。`SAFE_PROGS` 許可リストは廃止。Claude 版（フル）と Codex 版（Bash-only）の2フックに同じロジックを適用（両者は意図的に独立した standalone スクリプトなので共有モジュール化はしない）。

**Tech Stack:** Bash ラッパ + 埋め込み Python3（外部依存なし）。テストは `scripts/tests/test_block_credential_read.py`（subprocess でフックを起動するハーネス）。

---

## File Structure

| ファイル | 責務 | 操作 |
|---|---|---|
| `framework/claude/hooks/block-credential-read.sh` | Claude PreToolUse フック（パス＋Bash） | Modify（Bash 分類部のみ） |
| `framework/codex/hooks/block-credential-read.sh` | Codex PreToolUse フック（Bash-only） | Modify（分類部） |
| `scripts/tests/test_block_credential_read.py` | 両フックのテスト | Modify（ALLOW ケース追加・意味更新） |
| `framework/credential-patterns.txt` | パターン単一ソース＋ヘッダ説明 | Modify（ヘッダに表出モデルを明記） |
| `superpowers/2026-06-06-credential-guard-surfacing-model-design.md` / `.html` | 設計 spec / 可視化 | 既存（branch に commit 済） |
| `superpowers/2026-06-06-credential-guard-surfacing-model-plan.md` | 本実装計画 | 既存（branch に commit 済） |

不変領域（触らない）：両フックの path 分岐（`path_hit`、Grep/Glob 到達性 walk）、`pat_to_bash_re`、fail-open ラッパ、`git_segment_safe`（表出オラクルとして再利用）。

---

## Task 1: ブランチ準備と設計成果物の配置（完了済み）

**Files:**
- Branch: `feature/credential-guard-surfacing-model`（作成済）
- `superpowers/` 配下に spec(.md) / 可視化(.html) / 本計画(.md) を commit 済み

- [ ] **Step 1: ブランチと配置を確認**

Run: `git -C /Users/ryotaro/workspace/workato-dev-kit branch --show-current && ls superpowers/`
Expected: `feature/credential-guard-surfacing-model` と、`superpowers/` に design.md / design.html / plan.md が存在。

---

## Task 2: Claude フックを表出モデルへ刷新（TDD）

**Files:**
- Test: `scripts/tests/test_block_credential_read.py`
- Modify: `framework/claude/hooks/block-credential-read.sh`（埋め込み Python の `SAFE_PROGS` 宣言〜`bash_hit` を置換。`git_segment_safe` は残す）

- [ ] **Step 1: Claude 向け ALLOW / 回帰 BLOCK テストを追加**

`scripts/tests/test_block_credential_read.py` の `test_claude_allows_output_dot_key_false_positive` の直後に追記：

```python
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
```

- [ ] **Step 2: 新規テストを実行して RED を確認**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | grep -E "FAIL|passed"`
Expected: 少なくとも `test_claude_allows_cp_encrypted_settings`・`test_claude_allows_mv_master_key`・`test_claude_allows_custom_script_takes_settings_arg`・`test_claude_allows_curl_client_key`・`test_claude_allows_bundle_exec_workato_exec_with_settings_and_key` が **FAIL**（現行 default-deny がブロックするため）。`env/time/bundle exec cat`・`base64`・redirect 系は現行でも BLOCK され PASS（回帰ガード）。

- [ ] **Step 3: Claude フックの分類部を置換**

`framework/claude/hooks/block-credential-read.sh` の中で、`SAFE_PROGS = {"workato"}` の宣言とその直前コメント（現行 71〜84 行目相当）から `bash_hit` 関数の末尾（現行 148 行目相当）までを、以下で置換する。**`git_segment_safe` 関数（現行 90〜114 行目）はそのまま残し、下記の `# >>> git_segment_safe is defined here, unchanged <<<` の位置に維持すること。**

置換後の領域（コメント宣言 → 定数 → git_segment_safe[既存] → resolve_prog_index → surfaces → bash_hit）：

```python
# Surfacing model: a Bash segment is blocked only when it would emit a
# credential file's CONTENT to stdout/stderr — i.e. into the agent/LLM context.
# Passing a credential to a program as an argument or input (workato exec,
# git-staging, cp, a deploy script, curl --key) is allowed: the bytes never
# reach the agent, so it cannot reuse them at a lower layer.
#
# This is an accident / bypass guard, NOT a sandbox. Out of scope: deliberate
# multi-step evasion (copy to a non-credential name, then read it), shell
# function redefinition, connector code that prints a secret, and network
# exfiltration (feeding a credential to a program is explicitly allowed).
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

# Programs that read a named FILE argument and print its content to stdout.
EMITTERS = {
    "cat", "tac", "nl", "head", "tail", "less", "more", "bat", "view",
    "strings", "xxd", "od", "hexdump", "base64", "base32",
    "grep", "egrep", "fgrep", "rg", "ag", "ack",
    "sed", "awk", "gawk", "cut", "sort", "uniq", "column", "jq", "yq",
    "paste", "fold", "rev", "diff", "comm",
}
# Interpreters that surface content only when given inline code (-c / -e) that
# reads the credential. Running a *script* file with a credential argument is a
# consumer, not an emitter.
INTERPRETERS = {"python", "python3", "ruby", "node", "nodejs", "perl", "php"}
# Command-runner prefixes that do not themselves read files; unwrap to find the
# real program. NOTE: value-taking wrapper flags (e.g. `nice -n 5`) are not
# parsed, so a contrived `nice -n 5 cat secret` may slip — acceptable for an
# accident guard (the path-based Read/Grep/Glob hooks are the primary defense).
RUNNERS = {"env", "command", "exec", "nice", "time", "nohup", "stdbuf"}

# >>> git_segment_safe is defined here, unchanged <<<

def resolve_prog_index(toks):
    """Index of the real program token after skipping VAR=value env assignments
    and unwrapping `bundle exec` / RUNNER prefixes. Returns len(toks) if no
    program token remains (e.g. a bare redirect)."""
    i = 0
    while i < len(toks):
        if re.match(r"^\w+=", toks[i]):
            i += 1
            continue
        base = os.path.basename(toks[i])
        if base == "bundle" and i + 1 < len(toks) and toks[i + 1] == "exec":
            i += 2
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        if base in RUNNERS:
            i += 1
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        break
    return i

def surfaces(seg):
    """True if this segment would emit a credential's CONTENT to stdout/stderr.
    The segment is already known to reference a credential pattern."""
    stripped = seg.strip()
    # Bare read-redirect with no consuming program: `$(< master.key)` splits to
    # a `< master.key` segment; bash reads the file straight into the
    # substitution (→ stdout → agent).
    if re.match(r"^<\s*\S", stripped):
        return True
    toks = seg.split()
    pi = resolve_prog_index(toks)
    if pi >= len(toks):
        return False
    prog = os.path.basename(toks[pi])
    args = toks[pi + 1:]
    # git: defer to the vetted oracle — "not git-safe" means it would print
    # file content (show <rev>:<path>, diff, log -p, -c alias=!cat, --no-index).
    if prog == "git":
        return not git_segment_safe(args)
    if prog in EMITTERS:
        return True
    if prog in INTERPRETERS:
        for a in args:
            if a == "-c" or a == "-e" or a.startswith("-c") or a.startswith("-e"):
                return True  # inline code in a segment that names a credential
    if prog == "openssl" and "-in" in args:
        return True
    if prog == "gpg" and any(a in ("-d", "--decrypt") for a in args):
        return True
    # Generic decrypt subcommand: the kit helper `sdk decrypt`, gpg-style, etc.
    if "decrypt" in args:
        return True
    return False

def bash_hit(cmd):
    """Return the first credential pattern whose segment would SURFACE its
    content, else None. Default-allow: naming a credential is fine unless the
    segment emits its content into the agent's tool output."""
    sep = re.compile("|".join([r"\|\|", r"&&", r"[|;&\n]", r"\$\(", r"\)", re.escape(chr(96))]))
    for seg in sep.split(cmd):
        if not seg.strip():
            continue
        hit = None
        for pat in patterns:
            if pat_to_bash_re(pat).search(seg):
                hit = pat
                break
        if not hit:
            continue
        if surfaces(seg):
            return hit
    return None
```

- [ ] **Step 4: Bash 分岐の deny メッセージを表出モデルに合わせる**

同ファイルの Bash 分岐（現行 189〜193 行目相当）の deny 文言を更新：

```python
elif tool == "Bash":
    hit = bash_hit(ti.get("command", "") or "")
    if hit:
        deny(f"{hit}: command would surface credential content to the agent")
    sys.exit(0)
```

- [ ] **Step 5: フック冒頭コメントを更新**

同ファイル先頭のコメントブロック（現行 71〜83 行目にあった allowlist 説明は Step 3 で消えている）に加え、ファイル冒頭（2〜17 行目付近）の概要に1行追記しておく。下記の一文を 7 行目（"scanning." の行）の直後に挿入：

```bash
# The Bash layer uses a surfacing model: it blocks only commands that would
# emit a credential file's CONTENT into the agent context, not every command
# that merely names one. See framework/credential-patterns.txt for the model.
```

- [ ] **Step 6: 全テストを実行して GREEN を確認**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | tail -3`
Expected: 末尾に `N/N passed`（FAIL 行なし）。Claude の新規 ALLOW テストが通り、既存の Claude BLOCK テスト（cat/grep/openssl/python -c/git show・diff・-p/sdk decrypt/comment-spoof/連鎖）も維持。Codex の新規テストはまだ無いので影響なし。

- [ ] **Step 7: Commit**

```bash
git add framework/claude/hooks/block-credential-read.sh scripts/tests/test_block_credential_read.py
git commit -m "fix(kit): switch Claude credential guard to a surfacing model

Block a Bash command only when it would emit a credential file's content to
stdout/stderr (the agent context), instead of blocking every program that is
not on a small allowlist. Feeding a credential to a program as an argument or
input (bundle exec workato exec -s ..., cp, ./deploy.sh --settings ..., curl
--key) is now allowed; readers/printers (cat, grep, base64, openssl -in, gpg
-d, the sdk decrypt helper, interpreters with -c/-e, git content views) and
bare \`< cred\` redirects stay blocked. SAFE_PROGS is removed."
```

---

## Task 3: Codex フックを表出モデルへ刷新（TDD）

**Files:**
- Test: `scripts/tests/test_block_credential_read.py`
- Modify: `framework/codex/hooks/block-credential-read.sh`（埋め込み Python の `SAFE_PROGS` 宣言〜末尾の判定ループを置換。`git_segment_safe` は残す）

- [ ] **Step 1: Codex 向け ALLOW / 回帰 BLOCK テストを追加**

`scripts/tests/test_block_credential_read.py` の `test_codex_allows_git_add_enc` の直後に追記：

```python
def test_codex_allows_bundle_exec_workato_exec_with_settings_and_key():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "bundle exec workato exec connectors/foo/connector.rb test -s settings.yaml.enc -k master.key"}})
    assert r.returncode == 0, r.stderr


def test_codex_allows_cp_encrypted_settings():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "cp connectors/x/settings.yaml.enc connectors/x/settings.yaml.enc.bak"}})
    assert r.returncode == 0, r.stderr


def test_codex_allows_custom_script_takes_settings_arg():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "./deploy.sh --settings connectors/x/settings.yaml.enc"}})
    assert r.returncode == 0, r.stderr


def test_codex_blocks_env_cat_master_key():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "env cat master.key"}})
    assert r.returncode == 2


def test_codex_blocks_bundle_exec_cat_master_key():
    r = run(CODEX_HOOK, {"tool_name": "Bash",
                         "tool_input": {"command": "bundle exec cat master.key"}})
    assert r.returncode == 2
```

- [ ] **Step 2: 新規テストを実行して RED を確認**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | grep -E "FAIL|passed"`
Expected: `test_codex_allows_cp_encrypted_settings`・`test_codex_allows_custom_script_takes_settings_arg`・`test_codex_allows_bundle_exec_workato_exec_with_settings_and_key` が **FAIL**（現行 codex フックがブロック）。`env/bundle exec cat` は現行でも BLOCK で PASS。

- [ ] **Step 3: Codex フックの分類部を置換**

`framework/codex/hooks/block-credential-read.sh` の埋め込み Python のうち、`SAFE_PROGS = {"workato"}` の宣言とその直前コメント（現行 57〜67 行目相当）から、末尾の判定ループ（現行 107〜121 行目の `# Block only when ...` から `deny(hit)` まで）を、以下で置換する。**`pat_re`（現行 69〜71 行）と `git_segment_safe`（現行 73〜93 行）はそのまま残す。**

定数ブロック（`SAFE_PROGS` の代わり）：

```python
# Surfacing model: block a Bash command only when it would emit a credential
# file's CONTENT to stdout/stderr (the agent context). Passing a credential to
# a program as an argument/input (workato exec, git-staging, cp, deploy script,
# curl --key) is allowed. Accident/bypass guard, not a sandbox: deliberate
# multi-step evasion, shell-function redefinition, and network exfil are out of
# scope.
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}
EMITTERS = {
    "cat", "tac", "nl", "head", "tail", "less", "more", "bat", "view",
    "strings", "xxd", "od", "hexdump", "base64", "base32",
    "grep", "egrep", "fgrep", "rg", "ag", "ack",
    "sed", "awk", "gawk", "cut", "sort", "uniq", "column", "jq", "yq",
    "paste", "fold", "rev", "diff", "comm",
}
INTERPRETERS = {"python", "python3", "ruby", "node", "nodejs", "perl", "php"}
RUNNERS = {"env", "command", "exec", "nice", "time", "nohup", "stdbuf"}
```

`pat_re` と `git_segment_safe` の後に、ヘルパーと判定ループを追加（`segment_safe` は削除する）：

```python
def resolve_prog_index(toks):
    i = 0
    while i < len(toks):
        if re.match(r"^\w+=", toks[i]):
            i += 1
            continue
        base = os.path.basename(toks[i])
        if base == "bundle" and i + 1 < len(toks) and toks[i + 1] == "exec":
            i += 2
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        if base in RUNNERS:
            i += 1
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        break
    return i

def surfaces(seg):
    stripped = seg.strip()
    if re.match(r"^<\s*\S", stripped):
        return True
    toks = seg.split()
    pi = resolve_prog_index(toks)
    if pi >= len(toks):
        return False
    prog = os.path.basename(toks[pi])
    args = toks[pi + 1:]
    if prog == "git":
        return not git_segment_safe(args)
    if prog in EMITTERS:
        return True
    if prog in INTERPRETERS:
        for a in args:
            if a == "-c" or a == "-e" or a.startswith("-c") or a.startswith("-e"):
                return True
    if prog == "openssl" and "-in" in args:
        return True
    if prog == "gpg" and any(a in ("-d", "--decrypt") for a in args):
        return True
    if "decrypt" in args:
        return True
    return False

# Block only when a segment would surface credential content to the agent.
sep = re.compile("|".join([r"\|\|", r"&&", r"[|;&\n]", r"\$\(", r"\)", re.escape(chr(96))]))
for seg in sep.split(cmd):
    if not seg.strip():
        continue
    hit = None
    for pat in patterns:
        if pat_re(pat).search(seg):
            hit = pat
            break
    if not hit:
        continue
    if surfaces(seg):
        deny(hit)

sys.exit(0)
```

> 注: codex の `pat_re` は Claude の `pat_to_bash_re` と同等。`surfaces` 内で参照する正規表現名は各フックの既存名に合わせること（codex=`pat_re`、claude=`pat_to_bash_re`。ただし `surfaces` 自体は `pat_*` を呼ばないので差異なし）。

- [ ] **Step 4: フック冒頭コメントに表出モデルを1行追記**

`framework/codex/hooks/block-credential-read.sh` 冒頭（7 行目 "grep token settings.yaml`)." の直後）に挿入：

```bash
# The Bash scan uses a surfacing model: it blocks only commands that would emit
# a credential file's CONTENT into the agent context, not every command that
# merely names one.
```

- [ ] **Step 5: 全テストを実行して GREEN を確認**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | tail -3`
Expected: `N/N passed`（FAIL なし）。Codex の新規 ALLOW テストが通り、既存 Codex BLOCK テスト（grep master.key / sdk decrypt / git add -p）も維持。

- [ ] **Step 6: Commit**

```bash
git add framework/codex/hooks/block-credential-read.sh scripts/tests/test_block_credential_read.py
git commit -m "fix(kit): switch Codex credential guard to the surfacing model

Mirror the Claude hook: block a Bash command only when it would emit a
credential file's content to stdout/stderr. SAFE_PROGS removed; emitters,
known printers, interpreters with -c/-e, bare \`< cred\` redirects, and
content-printing git forms stay blocked."
```

---

## Task 4: パターンファイルのヘッダに表出モデルを明記

**Files:**
- Modify: `framework/credential-patterns.txt`

- [ ] **Step 1: ヘッダの consumer 説明を表出モデルの説明に更新**

`framework/credential-patterns.txt` の冒頭コメント、`# Consumed by:` ブロックの直後（現行 11 行目あたり、`# Gitignore-style globs ...` の前）に以下を挿入：

```text
#
# Bash enforcement model (both hooks): SURFACING. A shell command is blocked
# only when it would emit a credential file's CONTENT to stdout/stderr — i.e.
# into the agent/LLM context (cat, grep, base64, openssl -in, gpg -d, the
# `sdk decrypt` helper, interpreters run with -c/-e, content-printing git
# forms, and bare `< cred` redirects). Feeding a credential to a program as an
# argument or input (workato exec, git add, cp, a deploy script, curl --key) is
# allowed. This is an accident/bypass guard, not a sandbox; deliberate
# multi-step evasion and network exfiltration are out of scope. The path-based
# Read/Edit/Write/Grep/Glob checks remain default-deny and are the primary
# defense.
```

- [ ] **Step 2: 念のためテスト実行（パターン行に影響がないこと）**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | tail -1`
Expected: `N/N passed`（コメント追加のみなのでパターン解析に影響なし）。

- [ ] **Step 3: Commit**

```bash
git add framework/credential-patterns.txt
git commit -m "docs(kit): document the surfacing model in credential-patterns.txt"
```

---

## Task 5: sync drift チェックと最終検証

**Files:**
- Read-only verification

- [ ] **Step 1: sync_agents.py を実行して drift がないこと**

Run: `python3 scripts/sync_agents.py >/dev/null 2>&1 && git status --short`
Expected: 変更ファイルは `connectors/`・`projects/`（既存の untracked テストデータ）のみで、`framework/{cursor,codex,gemini}/` や `AGENTS.md` に差分が出ないこと（hooks は sync 非対象）。差分が出た場合はその生成物も commit する。

- [ ] **Step 2: 表出モデルの before/after を実コマンドで再現確認**

Run:
```bash
HOOK=framework/claude/hooks/block-credential-read.sh
chk(){ echo "$2" | python3 -c 'import json,sys;print(json.dumps({"tool_name":"Bash","tool_input":{"command":sys.stdin.read().strip()}}))' | bash "$HOOK" >/dev/null 2>&1; [ $? -eq 2 ] && echo "BLOCK $1" || echo "allow $1"; }
chk "bundle-exec-workato-exec" "bundle exec workato exec connectors/foo/connector.rb test -s settings.yaml.enc -k master.key"
chk "cp-enc"                   "cp connectors/x/settings.yaml.enc bak"
chk "deploy-script"            "./deploy.sh --settings connectors/x/settings.yaml.enc"
chk "curl-key"                 "curl --key connectors/x/client.key https://example.test"
chk "cat-master-key"           "cat connectors/x/master.key"
chk "grep-settings"            "grep token connectors/x/settings.yaml"
chk "sdk-decrypt"              "python3 scripts/workato-api.py sdk decrypt settings.yaml.enc --key master.key"
chk "bundle-exec-cat"          "bundle exec cat master.key"
chk "git-show-secret"          "git show HEAD:connectors/x/settings.yaml"
```
Expected:
```
allow bundle-exec-workato-exec
allow cp-enc
allow deploy-script
allow curl-key
BLOCK cat-master-key
BLOCK grep-settings
BLOCK sdk-decrypt
BLOCK bundle-exec-cat
BLOCK git-show-secret
```

- [ ] **Step 3: 全テスト最終実行**

Run: `python3 scripts/tests/test_block_credential_read.py 2>&1 | tail -1`
Expected: `N/N passed`。

---

## Task 6: PR 運用（#176 クローズ → 新 PR）

**Files:**
- GitHub 操作のみ

- [ ] **Step 1: ブランチを push**

```bash
git push -u origin feature/credential-guard-surfacing-model
```

- [ ] **Step 2: PR #176 をクローズ（本redesignが包含・上書き）**

```bash
gh pr close 176 --comment "Superseded by the surfacing-model redesign (feature/credential-guard-surfacing-model). The \`bundle exec\` unwrap folds into the new program resolver and SAFE_PROGS is removed entirely."
```

- [ ] **Step 3: 新 PR を作成**

```bash
gh pr create --base main --head feature/credential-guard-surfacing-model \
  --title "fix(kit): credential guard — switch Bash scan to a surfacing model" \
  --body "$(cat <<'BODY'
## 背景
credential guard の Bash スキャンはプログラム許可リスト（default-deny）で、新しい正当ツールが出るたび allowlist 追加が必要な「もぐら叩き」だった（#175→#176）。`bundle exec workato exec -s settings.yaml.enc`・`cp`・`./deploy.sh --settings`・`curl --key` などが偽陽性でブロックされていた。

## 脅威モデル（確定版）
防ぎたいのは **credential 内容が LLM コンテキストに入ること**。プログラムへ入力・引数として渡す分は許容。事故/迂回ガードでありサンドボックスではない（意図的多段回避・ネットワーク exfil はスコープ外）。

## 変更
Bash ブランチを **表出モデル（default-allow）** へ。credential 名を含むセグメントは、内容を stdout/stderr に表出させるとき（emitter / 既知プリンタ `sdk decrypt`・`openssl -in`・`gpg -d` / インタプリタ `-c|-e` / `< cred` リダイレクト / 内容表示系 git）だけブロック。`SAFE_PROGS` 廃止。`bundle exec` 等のランナー展開は新しいプログラム解決器へ転用。Claude/Codex 両フックに適用。一次防御の Read/Grep/Glob パスフックは default-deny のまま不変。

設計詳細: `superpowers/2026-06-06-credential-guard-surfacing-model-design.md`（`.html` に可視化）。

## テスト
`scripts/tests/test_block_credential_read.py` 全パス。新規 ALLOW ケース（bundle exec workato exec / cp / deploy script / curl --key）と回帰 BLOCK ガード（env・bundle exec 経由の emitter、`$(< cred)`、base64）を追加。

Supersedes #176.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
BODY
)"
```

- [ ] **Step 4: PR URL を確認してユーザーに報告**

Run: `gh pr view --json url -q .url`
Expected: 新 PR の URL。bugbot / Codex レビュー待ちフェーズへ。

---

## Self-Review

**Spec coverage（spec の各節 → 実装タスク）:**
- 脅威モデル確定版 → Task 2/3 のコメント＋Task 4 のヘッダに明文化 ✓
- 採用案B（表出モデル / default-allow） → Task 2 Step 3・Task 3 Step 3 ✓
- 表出判定ルール ①emitter ②既知プリンタ ③シェル構文 ④インタプリタ ⑤git オラクル → `surfaces()` に全反映（①EMITTERS ②openssl/gpg/decrypt ③`< ` redirect＋セグメント分割 ④INTERPRETERS+-c/-e ⑤`git_segment_safe` 再利用）✓
- SAFE_PROGS 廃止 → Task 2/3 で削除 ✓
- ランナー展開（#176 転用） → `resolve_prog_index` ✓
- 一次防御不変 → path 分岐は未変更（File Structure の不変領域に明記）✓
- テスト方針（維持 BLOCK＋新規 ALLOW） → Task 2 Step 1・Task 3 Step 1 ✓
- PR #176 クローズ→新 PR 集約 → Task 6 ✓
- ドキュメント明記（フックコメント・credential-patterns.txt） → Task 2 Step5・Task 3 Step4・Task 4 ✓
- sync drift 確認 → Task 5 Step1 ✓
- スコープ外明記 → Task 2 Step3 コメント・Task 4 ヘッダ ✓

**Placeholder scan:** TBD/TODO・「適切に処理」等なし。各コード変更ステップに完全なコードを記載 ✓

**Type/identifier consistency:** `resolve_prog_index` / `surfaces` / `bash_hit` / `EMITTERS` / `INTERPRETERS` / `RUNNERS` / `SAFE_GIT_SUBCMDS` / `git_segment_safe` を Task 2・3 で同一シグネチャ・同一名で使用。Claude=`pat_to_bash_re` / Codex=`pat_re` の差は Step3 の注記で明示（`surfaces` は両者を呼ばないため非依存）✓
