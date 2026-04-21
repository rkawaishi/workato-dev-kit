---
name: wpush
description: ローカルのプロジェクト変更を Workato リモートに push する。バリデーション、コネクション先行 push、デプロイガイダンスまで一貫して実行。
disable-model-invocation: true
---

# /wpush

ローカルの変更を Workato リモートに push し、レシピの動作確認まで行う。

## 使い方

- `/wpush` — 現在のプロジェクトを push
- `/wpush <project-name>` — 指定プロジェクトに切り替えて push
- `/wpush --start` — push 後にレシピを起動
- `/wpush --test` — push 後にレシピを起動し、ジョブの成否を確認
- `/wpush --restart-recipes` — push 後に稼働中レシピを自動再起動（既存レシピ更新時）
- `/wpush --delete` — リモートにあるがローカルにないアセットを削除
- `/wpush --validate-only` — バリデーションのみ実行（push しない）

## 実行手順

### 1. プロジェクトのバリデーション

push 前にプロジェクト内の JSON ファイルを検証する。`--validate-only` 指定時はここで終了。

#### 1a. JSON 構文チェック

プロジェクトディレクトリ内の全 JSON ファイルに対して構文チェックを行う:

```bash
# 対象: *.recipe.json, *.connection.json, *.agentic_genie.json,
#        *.agentic_skill.json, *.mcp_server.json, *.lcap_app.json,
#        *.lcap_page.json, *.workato_db_table.json
for f in projects/<project-name>/*.json; do
  python3 -c "import json; json.load(open('$f'))" 2>&1 || echo "INVALID: $f"
done
```

エラーがあれば修正してから続行する。

#### 1b. extended_output_schema チェック

以下のアクション/トリガーに `extended_output_schema` が定義されているか確認する:

- **add_record / update_record / search_records**: Data Table 操作のフィールド定義
- **return_result**: Recipe Function の戻り値スキーマ（datapill が後続ステップで認識されるために必須）
- **トリガー全般**: 特に `new_requests_realtime` は Data Table フィールドをスキーマに含める

```
# チェック方法: レシピ JSON を読み込み、該当ブロックに extended_output_schema があるか確認
# 欠落している場合は警告を表示:
WARNING: <recipe>.recipe.json のステップ <keyword> に extended_output_schema がありません。
  datapill が後続ステップで認識されない可能性があります。
```

#### 1c. Workflow App ページコンポーネントチェック

`*.lcap_page.json` がある場合、ドロップダウンコンポーネントの `dataSource` を確認:

```
# dataSource: null の場合は警告:
WARNING: <page>.lcap_page.json のドロップダウン "<label>" の dataSource が null です。
  push しても選択肢の値が保存されません。UI で設定するか、JSON で dataSource を定義してください。
```

#### 1d. Workato CLI recipes validate（ブロッキング）

`.claude/hooks/validate-before-push.sh` が `workato push` 検知時に自動実行する。全 `*.recipe.json` に対して `workato recipes validate --path <file>` を流し、フォーマット不備を push 前に検出する。

- **実行時間**: 約 2 秒/ファイル（直列実行）。大規模プロジェクトでは push 前の待ち時間になる点に留意
- **失敗時**: エラー詳細を表示して push を中断（exit 2）
- **ワークスペース制約（警告扱い）**: workspace に未リリースのカスタムコネクタがあると CLI 側の pre-check が先に失敗し、レシピ本体の検証まで到達できない。この場合は「CLI validate skipped for N recipe(s): ... Release with 'workato sdk push' to enable deeper validation.」という警告が出るのみで push は通す。deeper validation を有効にするには `workato sdk push` で連携対象のカスタムコネクタを release する

### 2. 新規コネクションの検出

push 前にプロジェクト内の `.connection.json` ファイルを確認し、Workato リモートにまだ存在しない新規コネクションがあるか検出する。

検出方法:
- ローカルの `*.connection.json` ファイルを一覧
- `workato pull` 時に取得済みのコネクション（既に Workato 上に存在）と比較
- 新規に作成されたコネクションファイルを特定

### 3. push（2段階 or 通常）

**新規コネクションがある場合 — 2段階 push:**

1. **まずコネクションファイルのみを push**: レシピ等を一時的に `.workato-ignore` に追加するか、コネクションファイルだけのディレクトリで push する。ただし **`--delete` オプションは絶対に使わない**（既存リモートアセットが削除される）
2. ユーザーに認証設定を依頼:

```
新しいコネクションを Workato にプッシュしました:
- <connection_name> (<provider>)

Workato UI で認証を設定してください:
1. プロジェクト「<project>」を開く
2. 各コネクションの認証情報を入力して接続

認証が完了したら教えてください。残りのアセットを push します。
```

3. 認証完了後、全アセットを push

**新規コネクションがない場合 — 通常 push:**

```bash
workato projects use "<project-name>"
workato push
```

**`--restart-recipes` 指定時:**

既存レシピの更新で、稼働中レシピの自動再起動が必要な場合に使う:

```bash
workato push --restart-recipes
```

これにより、push 後に running 状態だったレシピが自動的に再起動される。
レシピのロジック変更、datapill 修正、フィールド追加など、稼働中レシピへの変更反映に使う。
新規レシピのみの push では不要。

**`--delete` 指定時:**

ローカルで削除したアセットをリモートからも削除する:

```bash
workato push --delete
```

**既知の制限事項: CLI の `--delete` は `agentic_skill` と `mcp_server` を削除できない**（`Skipped` になる）。
これらを削除する必要がある場合は、ユーザーに以下を案内する:

```
CLI の --delete では MCP サーバーとスキルの削除ができません（Skipped になります）。
以下を Workato UI で手動削除してください:
- <削除対象の skill/mcp_server 名>

削除完了後に再度 push してください。
```

### 4. Post-push デプロイガイダンス

push 成功後、プロジェクト内のアセット構成に基づいて該当するガイダンスを自動表示する。

#### 常に表示: レシピ起動リスト

```
push 完了。以下のレシピを起動してください:
- <recipe_name_1>
- <recipe_name_2>

Workato UI で各レシピを開き「Start recipe」をクリック、
または --start / --test フラグ付きで /wpush を実行してください。
```

#### 新規コネクションがある場合

```
以下のコネクションの認証を確認してください:
- <connection_name> (<provider>)

Workato UI > プロジェクト > コネクション から認証情報を入力してください。
```

#### MCP サーバーがある場合 (`*.mcp_server.json`)

```
MCP サーバーのセットアップ:
1. Workato UI で MCP サーバーの設定画面を開く
2. ツール一覧にスキルが表示されているか確認
3. 各ツールの説明が適切か確認
4. MCP サーバーの URL をコピーして AI クライアント（Claude Desktop 等）に設定
5. AI クライアントからツールを呼び出してテスト
```

#### Workflow App がある場合 (`*.lcap_app.json`, `*.lcap_page.json`)

```
Workflow App の UI 確認チェックリスト:
1. Workflow App にステージ・ページが反映されているか
2. 送信フォームのフィールドが正しく表示されるか
3. ドロップダウンの選択肢が設定されているか
4. レビューページで承認/却下ができるか
5. テスト: 送信フォームからリクエストを送信して承認フロー全体を通す
```

### 5. レシピ起動（--start / --test 指定時）

```bash
# プロジェクト内のレシピ一覧を取得（folder_id は .workatoenv から取得）
python3 scripts/workato-api.py recipes list --folder-id <folder_id>

# 個別レシピを起動
workato recipes start --id <recipe-id>

# 全レシピを起動
workato recipes start --all
```

### 6. ジョブ確認（--test 指定時）

```bash
# レシピのジョブ一覧を取得（失敗のみ）
python3 scripts/workato-api.py jobs list --recipe-id <recipe-id> --status failed

# ジョブの詳細（エラー内容）を取得
python3 scripts/workato-api.py jobs get --recipe-id <recipe-id> --job-id <job-id>
```

### 7. エラー修正サイクル

ジョブが失敗した場合:

1. `python3 scripts/workato-api.py jobs get` でエラー内容を確認
2. エラー原因を分析:
   - **datapill 参照エラー**: path の指定ミス → レシピ JSON を修正
   - **コネクション未設定**: UI でコネクション認証を設定するよう案内
   - **フィールドマッピングエラー**: input のフィールド名/UUID を修正
   - **外部 API エラー**: 接続先の設定確認を案内
3. 修正を適用して再 push
4. レシピを再起動してジョブを再確認
5. 成功するまで繰り返す

### 8. 結果報告

- push 結果
- バリデーション警告（あれば）
- レシピの起動状態
- ジョブの成否（--test 時）
- エラーがあった場合はエラー内容と修正提案

## 注意

- push は Workato リモートの内容を上書きする操作
- **新規コネクションは必ず先に push して認証を済ませる** — 未認証コネクションでレシピを push するとエラーになる
- Workflow App のトリガー（new_requests_realtime 等）はフォーム送信でテスト
- **`--delete` の制限**: `agentic_skill` と `mcp_server` は CLI で削除できない。UI で手動削除が必要
- **`--restart-recipes`**: 稼働中レシピへの変更を反映するために必要。新規レシピのみなら不要

## Git 管理

**`/wpush` は Workato API へのデプロイであり、git への影響はゼロ。** ローカルの変更を git リモートにも残したい場合は、別途内側リポジトリ `projects/` で git 操作が必要:

```bash
(cd projects/<project-name> && git status)
(cd projects/<project-name> && git add . && git commit -m "<msg>")
(cd projects/<project-name> && git push origin)
```

「`/wpush` したから履歴は残っている」と誤認しない。詳細は `.cursor/rules/workato-multi-repo-git.mdc` 参照。
