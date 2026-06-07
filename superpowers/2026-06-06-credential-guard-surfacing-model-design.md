# Credential Guard — 表出モデルへの再設計（design）

- 日付: 2026-06-06
- 対象: `framework/claude/hooks/block-credential-read.sh`, `framework/codex/hooks/block-credential-read.sh`, `scripts/tests/test_block_credential_read.py`
- 関連: PR #175（ダンプ限定ブロック化）, PR #176（`bundle exec` 展開 — 本redesignが包含・上書き）

## 背景と問題

credential guard の Bash スキャンは「プログラム許可リスト（`SAFE_PROGS = {"workato"}` ＋ git staging）にないプログラムが credential パターンを含んだら全ブロック」という **default-deny** だった。これは構造的に**偽陽性（正当作業のブロック）を生み続ける**:

- `bundle exec workato exec -s settings.yaml.enc -k master.key`（暗号化設定でのローカルテスト＝標準形） → 先頭が `bundle` 判定でブロック（PR #176 で一旦回避）
- `cp settings.yaml.enc bak` / `./deploy.sh --settings settings.yaml.enc` / `curl --key client.key` — 内容を表出しないのに名前を含むだけでブロック

新しい正当ツールが出るたびに allowlist 追加が必要な「もぐら叩き」になっていた。

## 脅威モデル（確定版）

> 防ぎたいのは **credential の内容が LLM のコンテキストに入ること**。bash 等で直接プログラムに入力・引数として渡す分は許容する。

- エージェントが credential を「取得して低レイヤーで再利用（迂回）」できるのは、まず内容が自分のコンテキストに入った時だけ。**コンテキスト流入を断てば迂回の原資も断てる。**
- これは「サンドボックス」ではなく**事故 / 迂回ガード**。意図的な多段回避（credential を非credential名のファイルへコピーしてから読む、シェル関数再定義、コネクタコードが secret を print する等）は**スコープ外**。
- ネットワーク exfil（`curl -d @cred` 等）も、ユーザーが「プログラムに流すのは OK」と明示的にスコープ外とした。

## 設計判断（採用案 = 案B「表出モデル」default-allow）

検討した3案:

- **案A（default-deny / allowlist 維持）**: セキュア寄りだが偽陽性が残り続ける。脅威モデルが「内容のコンテキスト流入だけ」を問題視するため過剰。
- **案B（採用）: 表出モデル / default-allow**: credential 名を含むセグメントは**内容を stdout/stderr に表出させるときだけブロック**。それ以外は許可。
- **案C（Bash スキャン廃止）**: `cat master.key` 等を素通りさせ脅威モデルに反する。不採用。

案B の偏陰性リスク（default-allow なので未知のプリンタが漏れうる）は、**「表出ブロックリスト＋既知プリンタ明示」で十分**とユーザー判断。根拠: (1) 一次防御の Read/Grep/Glob パスフックは default-deny のまま、(2) Bash はセカンダリ防御、(3) これは事故/迂回ガードでありサンドボックスではない。

## アーキテクチャ

### 不変（一次防御）

`tool_name in {Read, Edit, Write, NotebookEdit, Grep, Glob}` のパス照合は現状維持（default-deny）。Grep/Glob のディレクトリ到達性チェックも維持。これらは内容を LLM に返すツールそのもの。

### 刷新（二次防御 = Bash ブランチ）

`bash_hit(cmd)` を「表出検出」に作り替える。`SAFE_PROGS` 許可リストは**廃止**（`workato` を特別扱いする必要が消える）。

コマンドを既存のセパレータ（`|| && | ; & \n $( ) \``）でセグメント分割し、各セグメントについて:

1. credential パターンを含まないセグメント → スキップ（allow）
2. 含むセグメントが下記「表出条件」のいずれかに該当 → **block**
3. どれにも該当しない → allow（default-allow）

### 表出条件（block するケース）

セグメントの実プログラムを解決する際、既存の**ランナー展開**（`VAR=value` env 代入のスキップ＋ `bundle exec [opts]` / `exec` / `env` / `command` / `time` / `nice` の剥がし）を流用して「実プログラム」を得る。PR #176 の `segment_safe` 内展開ロジックをこの解決器へ転用する。

1. **Emitter プログラム**（実プログラムが下記集合）が credential を**読み位置**で参照するとき:
   `cat tac nl head tail less more bat view strings xxd od hexdump base64 base32 grep egrep fgrep rg ag ack sed awk gawk cut sort uniq fold paste column jq yq diff comm dd iconv pr expand unexpand fmt`
   - credential が**出力リダイレクトのシンク**（`> cred` `>> cred` `1> cred` `&> cred`、左端密着形 `1>cred`）や **dd の `of=cred`** の場合は**書き先**であり表出しないので allow（`cat README.md > master.key` は許可、`cat master.key > x` は読み元なのでブロック）。判定は `_emitter_surfaces_cred()`（round-5 Codex レビュー）。
   - 残余の軽微な偽陽性: `>` がトークン中央に密着する `cat README.md>master.key`（スペース無し）は naive な whitespace split では分離できず over-block する。**安全側の過剰ブロック**かつ人間が通常書かない形のため未対応（一般形・スペース形・左端密着形は解消済み）。
   - `tr` `tee` は file 引数を読まず stdin を echo するだけなので emitter ではなく **STDIN_ECHOERS** として扱い、stdin リダイレクト元が credential のとき（`tr ... < cred`、`tee f < cred`）だけブロック。`tee cred`（書き先）・`tr a b cred`（positional）は allow。
2. **既知の平文プリンタ**:
   - `openssl` で `-in <cred>` を伴う呼び出し
   - `gpg` で `-d` / `--decrypt` を伴う呼び出し
   - kit ヘルパー `sdk decrypt`（`workato-api.py ... sdk decrypt ...`）
   - トークン列に `decrypt` を含み credential 名を伴う呼び出し（汎用キャッチ）
3. **シェル構文での吸い出し**:
   - command substitution `$(...)` / `` `...` `` の本体に credential パターンが出現
   - emitter への入力リダイレクト `<emitter> < <cred>` および裸の `< <cred>`
   （注: セグメント分割で `$(` `)` `` ` `` は分割点なので、置換本体は別セグメントとして評価される。本体が emitter を含めば(1)で捕捉。これで `echo $(cat master.key)` は内側 `cat master.key` セグメントが block）
4. **インタプリタの読み出し**:
   実プログラムが `python python3 ruby node perl php` で、引数に `-c` / `-e` があり、その後続に credential パターンが出現 → 保守的に block
5. **git（専用オラクル）**:
   git は内容表出のモードが多彩（`show <rev>:<path>`・`diff`・`log -p`・`-c alias=!cat`・`--no-index`・`-v/--verbose`）。既存の `git_segment_safe()` を**そのまま流用**し、「git-safe でない = 表出する = block」と解釈する。staging 系（add/rm/mv/status/commit/stash/restore/checkout/switch/reset）で危険フラグなしのものだけ allow、それ以外の git は block。

### allow されるケース（表出しない）

`bundle exec workato exec -s settings.yaml.enc -k master.key` / `workato edit settings.yaml.enc` / `git add settings.yaml.enc` / `cp|mv settings.yaml.enc bak` / `./deploy.sh --settings settings.yaml.enc` / `curl --key client.key https://...` / `workato generate schema --output=out.key` / `cat template > master.key`（出力リダイレクト先）/ `dd if=template of=master.key`（dd の書き先）

## コンポーネントとデータフロー

```
INPUT(JSON) ─▶ tool_name 判定
  ├─ Read/Edit/Write/NotebookEdit ─▶ path_hit() ─▶ deny/allow         （不変）
  ├─ Grep/Glob ─▶ path_hit() + 到達性walk ─▶ deny/allow                （不変）
  └─ Bash ─▶ segment 分割 ─▶ 各 seg: contains_cred? ─▶ surfaces(seg)? ─▶ deny/allow （刷新）
                                                         │
                          resolve_program()（ランナー展開）─┤
                          emitter / known-printer / subst / interpreter / git-oracle
```

`surfaces(seg)` が True を返したら最初の該当でブロック理由を添えて exit 2。

## エラーハンドリング / fail-open（ハイブリッド ※round-2 で確定）

- **malformed JSON・パターンファイル欠如**: fail-**open**（allow）。入力が読めない/パターンが無いと判定不能なため。
- **自前の分類ロジックが例外**（`_decide()` 内）: fail-**CLOSED**（exit 2）。バグで credential 読み出しを黙って許可するのを防ぐ。`try/except SystemExit: raise / except Exception: exit(2)` で囲う。
- **Python 自体が起動不能**: bash ラッパが fail-open（ここで閉じると全ツール呼び出しが文鎖するため）。

> 当初案は「Python 例外も fail-open」だったが、round-2 Codex レビューを受けユーザー合意のもとハイブリッド（自前バグは fail-closed）へ変更。

## テスト方針

`scripts/tests/test_block_credential_read.py` を更新。

**維持（BLOCK のまま）:**
- `cat master.key` / `grep token settings.yaml`（codex）/ `openssl pkey -in id_rsa.key` / `python3 -c "open('master.key').read()"` / `git show HEAD:...settings.yaml` / `git add -p ...` / `git status -v` / `git --no-pager diff --no-index` / `git -c alias.x='!cat ...'` / `sdk decrypt` / comment-spoof / `git status && cat master.key`(連鎖) / `bundle exec cat master.key`

**新規追加（B が許可 = ALLOW）:**
- `bundle exec workato exec connectors/foo/connector.rb test -s settings.yaml.enc -k master.key`
- `cp connectors/x/settings.yaml.enc connectors/x/settings.yaml.enc.bak`
- `mv master.key connectors/x/master.key`
- `./deploy.sh --settings connectors/x/settings.yaml.enc`
- `curl --key connectors/x/client.key https://example.test`
- `env cat master.key` → BLOCK（env 展開後 emitter）/ `time cat master.key` → BLOCK（回帰ガード）

**意味更新:** allowlist 前提だった `test_*_allows_workato_edit_enc` 等は「emitter でないので自然に allow」へ。

## 移行 / PR 運用

- 本redesignは PR #176（`bundle exec` 展開）を**包含・上書き**する（`SAFE_PROGS` 自体が消えるため）。**#176 はクローズ**し、案B を単一の新PR（feature ブランチ → PR → レビュー）に集約する。
- フック冒頭コメント・`credential-patterns.txt` ヘッダ・関連 rules（`workato-cli.md` 等で言及があれば）に「表出モデル」と脅威モデルを明記。
- `python3 scripts/sync_agents.py` は hooks 非対象だが drift 確認のため実行。

## スコープ外（明示）

- 意図的多段回避（非credential名へコピー後に読む、シェル関数再定義、コネクタコードが secret を print）
- ネットワーク exfil（プログラムへ流す行為は許容）
- 一次防御（Read/Grep/Glob パスフック）の挙動変更
- **値付きフラグによる回避**（意図的構築）: 実プログラム/スクリプトの手前に値を取るフラグを挟む形。
  - runner: `nice -n 5 cat master.key`（`resolve_prog_index` は `-n` の値 `5` を実プログラムと誤認）
  - interpreter: `python3 -W ignore master.key`（第1 positional 判定が `-W` の値 `ignore` をスクリプトと誤認）
  - 対応するにはツールごとのフラグ引数アリティ表が必要で、複雑化＋新たな偽陽性リスクを生むため不採用（Codex round-3 #1/#7）。
- **コマンド間接化**（意図的構築）: `find . -name master.key -exec cat {} \;` や `… | xargs cat` のように別コマンドへ委譲して読む形。埋め込みコマンドの再帰解析は arts-race かつ `find -name <cred> -exec rm` 等の正当操作を巻き込む偽陽性リスクがあるため不採用（Codex round-3 #3）。
- **インタプリタ `-c`/`-e` が credential を argv 経由で読む形**（意図的構築）: `python3 -c "import sys;print(open(sys.argv[1]).read())" master.key`。credential をコードに直書きする形（`python3 -c "open('master.key')…"`）は**ブロック済み**。argv 間接化はそれを回避する意図的構築で、データ引数の正当形（`python3 -c "print('ok')" master.key`）と**コード意味解析なしには静的に区別不能**。保守的に「`-c`＋cred 引数」を一律ブロックすると正当形まで巻き込むため不採用（Codex round-4 #1）。

> いずれも「うっかり読む」一般形（`cat`/`python -c open(...)` 等）ではなく**意図的に異常なコマンドを構築する**ケース。本ガードは事故/迂回ガードでありサンドボックスではないため対象外とする。一次防御の Read/Grep/Glob パスフックはこれらに影響されない。
