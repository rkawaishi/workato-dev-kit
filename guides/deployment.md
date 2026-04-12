# デプロイ手順ガイド

ローカルで作成したアセットを Workato にデプロイする手順とトラブルシューティング。

## 基本フロー

すべてのデプロイは `/wpush` スキルを通じて行う。手動で `workato push` を実行する必要はない。

```
/wpush                     # 標準プッシュ（バリデーション付き）
/wpush --start             # プッシュ後にレシピを自動起動
/wpush --test              # プッシュ後にテスト実行・結果確認
/wpush --delete            # リモートの不要アセットも削除
```

## レシピのデプロイ

### 新規レシピ（コネクションも新規の場合）

新しいコネクションを含む場合、**2段階プッシュ** が必要になる。

```
ステップ 1: /wpush
  → コネクションのみ先行プッシュ
  → "Workato UI でコネクションを認証してください" と案内される

ステップ 2: UI でコネクションを認証
  → 認証情報を入力し、接続テストを実行

ステップ 3: /wpush --start
  → 残りのアセット（レシピ等）をプッシュ
  → レシピを起動
```

**なぜ2段階か:** コネクションが未認証だと、レシピ内の `pick_list` フィールド（動的選択肢）が解決できず、プッシュがエラーになる。

### 既存レシピの更新

```
/wpush --restart-recipes
```

稼働中のレシピを更新する場合、`--restart-recipes` で自動的に停止→更新→再起動される。

### テスト実行

```
/wpush --test
```

プッシュ後にレシピをテスト実行し、ジョブの成功/失敗を確認する。失敗時はジョブ詳細を取得してエラー分析を行う。

## Workflow App のデプロイ

Workflow App は UI での有効化が必要な唯一のケース。

```
ステップ 1: Workato UI → Settings → Workflow Apps → 有効化

ステップ 2: /wpush
  → Data Table、アプリ定義、ページ、レシピをまとめてプッシュ

ステップ 3: UI で確認
  → ページの表示、ステージ遷移、データ登録をテスト
```

**デプロイ順序:** Data Table → lcap_app.json → Pages → Recipes の順でプッシュされる。依存関係は `/wpush` が自動的に解決する。

## Genie / MCP サーバーのデプロイ

```
ステップ 1: /wpush
  → Genie 定義、スキル定義、MCP サーバー定義、スキルレシピをプッシュ

ステップ 2: UI で確認
  → Agent Studio でスキルが認識されているか確認
  → MCP サーバーの場合、ツールが discoverable か確認

ステップ 3: テスト
  → Genie チャットでスキルを呼び出し、期待通りに動作するか確認
```

**注意:** `/wpush --delete` は `agentic_skill` と `mcp_server` を削除できない（CLI の制限）。これらの削除は UI から手動で行う。

## カスタムコネクタのデプロイ

カスタムコネクタは Connector SDK CLI で直接プッシュする。

```bash
# 本家 gem CLI の場合
workato push connectors/<name>

# テスト実行
workato exec connectors/<name>/connector.rb test
```

## プッシュ前バリデーション

`/wpush` は以下のチェックを自動実行する:

| チェック | 対象 | 内容 |
|---|---|---|
| JSON 構文 | 全 `.json` ファイル | パース可能かどうか |
| 必須フィールド | `.recipe.json` | `name`, `code`, `config` の存在 |
| extended_output_schema | アクションステップ | 後続ステップが参照するフィールド定義の存在 |
| ページコンポーネント | `.page.json` | `dataSource` 定義の整合性 |
| UUID 形式 | レシピステップ | `uuid` フィールドの形式チェック |

バリデーションのみ実行したい場合は `/validate-recipe` を使う。

## トラブルシューティング

| エラー | 原因 | 対処 |
|---|---|---|
| `Connection not found` | コネクションが未プッシュまたは未認証 | 2段階プッシュで先にコネクションを認証 |
| `Token expired` | API トークンの期限切れ | `workato init` で再認証 |
| `Unresolved reference` | 参照先アセットが存在しない | 依存先を先にプッシュする |
| `Schema validation error` | JSON 構造が仕様と不一致 | `/validate-recipe` で詳細を確認 |
| `Recipe is running` | 稼働中レシピの更新 | `--restart-recipes` オプションを使用 |
| `pick_list resolution failed` | コネクション未認証で動的選択肢が取得不可 | UI でコネクションを認証してから再プッシュ |
| `Skipped: agentic_skill` | CLI が skill/MCP の削除に未対応 | UI から手動削除 |

## デプロイ後の学習サイクル

デプロイ後に UI で調整した場合は、必ず pull → learn のサイクルを回す:

```
/wpull                     # UI での変更をローカルに取得
/learn-recipe <project>    # 変更から新しい知見を学習
```

これにより、UI でしか設定できないフィールド値や、ドキュメント化されていない構造がナレッジベースに蓄積される。
