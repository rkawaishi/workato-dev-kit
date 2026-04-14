# デプロイメントガイド

レシピや Workflow App を作成してから Workato 上で動作させるまでの手順。
JSON 生成後にユーザーが UI で行うべき操作を段階的にガイドする。

## レシピのデプロイフロー

### Step 1: コネクション先行 push（新規コネクションがある場合のみ）

新しい `.connection.json` を作成した場合は、コネクションだけを先に push して認証を済ませる。

```
ユーザーへの案内:
---
新しいコネクションを作成しました:
- <connection_name> (<provider>)

Workato にコネクションを push します。push 後に UI で認証を設定してください:
1. Workato UI でプロジェクトを開く
2. コネクション <connection_name> を開く
3. 認証情報を入力して「Connect」をクリック
4. 接続成功を確認

認証が完了したら教えてください。レシピを push します。
---
```

**なぜ先にコネクション認証が必要か:**
- 未認証コネクションでレシピを push すると、UI でフィールド候補が表示されない
- `extended_output_schema` が展開されない
- テスト実行でエラーになる

### Step 2: レシピを push

コネクション認証が完了した後（または既存コネクションを使う場合）、レシピを push する。

```bash
workato push
```

### Step 3: UI でのレシピ確認・調整

push 後、Workato UI でレシピを開いて以下を確認するようユーザーに案内する。

```
ユーザーへの案内:
---
レシピを push しました。Workato UI で以下を確認してください:

1. **レシピ構造**: 各ステップが正しく表示されるか
2. **コネクション選択**: 各ステップで正しいコネクションが選ばれているか
3. **フィールドマッピング**: input フィールドの datapill 参照が正しいか
   - ⚠️ フィールドが空になっている場合は UI で再設定してください
4. **トリガー設定**: トリガー固有の設定（テーブル選択、イベントタイプ等）

調整が必要な場合は、UI で編集後に教えてください。pull して学習します。
---
```

### Step 4: pull → 学習

UI で調整を行った場合:
```bash
echo "y" | workato pull
```

pull 後に `/learn-recipe` でフィールド情報を抽出・蓄積する。

### Step 5: テスト実行

```
ユーザーへの案内:
---
レシピをテスト実行してください:
1. Workato UI でレシピの「Test」ボタンをクリック
2. テストデータを入力して実行
3. ジョブの結果を確認

エラーが出た場合は教えてください。エラー内容を分析して修正します。
---
```

CLI でテスト結果を確認する場合:
```bash
workato recipes start --id <recipe-id>
python3 scripts/workato-api.py jobs list --recipe-id <recipe-id> --status failed
python3 scripts/workato-api.py jobs get --recipe-id <recipe-id> --job-id <job-id>
```

## Workflow App のデプロイフロー

### Step 1: Workflow App の有効化（UI、1回のみ）

```
ユーザーへの案内:
---
Workato UI で以下を実行してください:
1. プロジェクト内で Workflow App を有効化

完了したら教えてください。Data Table、ステージ、ページ、レシピを push します。
---
```

### Step 2: 全アセットを push

Data Table、lcap_app、ページ、レシピを一括 push。
新規コネクションがある場合はレシピのデプロイフロー Step 1 と同様にコネクション先行 push。

### Step 3: UI 確認

```
ユーザーへの案内:
---
push 完了。Workato UI で以下を確認してください:
1. Workflow App にステージ・ページが反映されているか
2. 送信フォームのフィールドが正しく表示されるか
3. レビューページで承認/却下ができるか
4. コネクション認証（外部サービスを使う場合）
5. レシピの各ステップのフィールドマッピング

テスト: 送信フォームからリクエストを送信して、承認フロー全体を通してテストしてください。
---
```

## MCP サーバーのデプロイフロー

### Step 1: push

MCP サーバー + スキル + スキルレシピを push。

### Step 2: MCP サーバーの有効化

```
ユーザーへの案内:
---
push 完了。Workato UI で MCP サーバーを確認してください:
1. MCP サーバーの設定画面を開く
2. ツール一覧にスキルが表示されているか確認
3. 各ツールの説明が適切か確認
4. MCP サーバーの URL をコピーして AI クライアント（Claude Desktop 等）に設定

テスト: AI クライアントからツールを呼び出してテストしてください。
---
```

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|---|---|---|
| `expired_access_token` | コネクション未認証 | UI でコネクション認証を設定 |
| フィールドが空 | コネクション未認証のため UI がスキーマを取得できない | コネクション認証後に UI でフィールドを再設定 |
| `Unresolved reference` | 参照先ファイルが存在しない | 参照先を先に push するか、参照を null にする |
| ページエディタが無限ロード | コンポーネント type の誤り（date 型に input を使った等） | `type: "date"` に修正 |
| `parameters` が空にリセット | push 時にコネクション未設定のフィールドがリセットされた | コネクション認証 → UI で再設定 → pull |
| datapill がリロードまで認識されない | `return_result` に `extended_output_schema` / `extended_input_schema` がない | `result_schema_json` と同じフィールド定義を extended スキーマに展開する |
| トリガーのフィールドがリフレッシュまで認識されない | トリガーに `extended_output_schema` がない | トリガー出力のフィールド定義を `extended_output_schema` に展開する。特に Workflow App の `new_requests_realtime` は Data Table のフィールドをスキーマに含める |
| `PG::UniqueViolation` (agentic_skill) | スキルが既に存在する状態で再 push | CLI の `--delete` では MCP サーバー・スキルは削除できない（`Skipped` になる）。UI で手動削除してから再 push |
