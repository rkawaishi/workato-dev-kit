# スキルリファレンス

全 12 スキルの用途・使い方・オプションをまとめたリファレンス。

## スキルの呼び出し方

| エディタ | 呼び出し方 | スキル定義の場所 |
|---|---|---|
| **Claude Code** | プロンプトで `/skill-name` を入力 | `.claude/skills/` |
| **Cursor** | Agent モードで `/skill-name` を入力 | `.cursor/skills/`（`.claude/skills/` から同期） |

Cursor ではスキルファイルが `.cursor/skills/` にも同期されている。ツールキット側でスキルを更新した場合は `bash scripts/sync-cursor-rules.sh` を実行して反映する。

## 設計フェーズ

### /design — 設計書の作成・更新

プロジェクトの `DESIGN.md` を作成・更新・参照する。

```
/design                    # 既存の DESIGN.md を読み込み、対話開始
/design new                # 新規プロジェクトの設計を開始
/design update             # 実装状況を反映して DESIGN.md を更新
```

**設計書に含まれる内容:**
- ユーザー体験（ユーザーストーリー形式）
- 技術アーキテクチャ（レシピ構成図、コネクション、Data Table）
- 実装チェックリスト（各アセットの完了状況）
- 設計判断の記録
- 未解決事項

**ポイント:**
- `/create-recipe` や `/create-workflow-app` の前に実行し、全体設計を固める
- `projects/CATALOG.md` を参照し、既存の共有アセットの再利用を提案する
- `.workatoignore` に `DESIGN.md` を追加し、`workato pull` で消えないようにする

---

## 構築フェーズ

### /create-recipe — レシピ JSON 生成

対話的にレシピの目的・トリガー・アクションを決め、`.recipe.json` と `.connection.json` を生成する。

```
/create-recipe             # 対話的にレシピを生成
```

**ワークフロー:**
1. レシピの目的・トリガー・アクションを確認
2. 共有アセットカタログ (`CATALOG.md`) から再利用可能なコネクション・Recipe Function を検索
3. コネクタナレッジ (`docs/connectors/`) でフィールド仕様を確認
4. ユーザーインタビューで入力フィールド値を決定
5. パターンカタログ (`docs/patterns/recipe-patterns/`) から適用可能なパターンを提案
6. JSON を生成し、デプロイ手順を案内

**フィールド値の3分類:**
- **自動決定**: ナレッジから確定できる値
- **要確認**: 推測可能だがユーザー確認が必要な値
- **接続依存**: コネクション認証後にしか分からない値（object 定義の `pick_list` 等）

### /create-workflow-app — Workflow App 構築

承認ワークフローなどの Workflow App を JSON で構築する。

```
/create-workflow-app       # 対話的に Workflow App を構築
```

**生成されるアセット:**
- Data Table スキーマ (`.data_table.json`)
- ページ定義 (`.page.json`) — 申請フォーム、レビュー画面、完了画面
- アプリ定義 (`lcap_app.json`) — ステージ遷移とページ紐付け
- 関連レシピ — `/create-recipe` に委譲

**唯一の UI 操作**: Workflow App の有効化（Settings → Workflow Apps）

詳細は [Workflow App 構築ガイド](workflow-apps.md) を参照。

### /create-genie — Genie & MCP 生成

AI エージェント (Genie) とスキル、オプションで MCP サーバーを生成する。

```
/create-genie              # 対話的に Genie 構成を生成
```

**生成されるアセット:**
- `.agentic_genie.json` — Genie 定義（指示文、AI モデル設定）
- `.agentic_skill.json` — スキル定義（パラメータ、トリガー設定）
- `.mcp_server.json` — MCP サーバー定義（オプション）
- スキルレシピ — `/create-recipe` に委譲

詳細は [Genie & MCP 構築ガイド](genie-and-mcp.md) を参照。

### /create-connector — カスタムコネクタ生成

Connector SDK プロジェクトをスキャフォールドし、`connector.rb` を生成する。

```
/create-connector          # 対話的にカスタムコネクタを生成
```

**生成されるファイル:**
- `connector.rb` — メインのコネクタ定義
- `settings.yaml` — 認証情報テンプレート
- `Gemfile` — 依存関係
- `.gitignore` — 機密情報の除外
- `README.md` — セットアップ手順

詳細は [カスタムコネクタ開発ガイド](connector-development.md) を参照。

---

## 検証フェーズ

### /validate-recipe — JSON 構造検証

レシピや Genie の JSON ファイルを検証し、問題を報告する。

```
/validate-recipe <file>            # 特定ファイルを検証
/validate-recipe <project-name>    # プロジェクト全体を検証
```

**検証対象と主なチェック項目:**

| ファイル種別 | チェック項目 |
|---|---|
| `.recipe.json` | 必須フィールド、ステップ番号の連続性、UUID 形式、datapill 参照の解決、フィルタ条件 |
| `.agentic_genie.json` | 必須フィールド、スキル参照の整合性、指示文の存在 |
| `.agentic_skill.json` | 必須フィールド、レシピ参照、トリガータイプ |
| `.connection.json` | 必須フィールド |

**出力形式:** ✅ OK / ⚠️ Warning / ❌ Error

---

## 同期フェーズ

### /wpull — Workato からプルする

Workato リモートからプロジェクトのアセットをローカルに取得する。

```
/wpull                     # カレントプロジェクトをプル
/wpull --all               # 全リモートプロジェクトをプル
/wpull --list              # リモートプロジェクトの一覧表示
```

**プル後のアクション:**
- 変更されたファイルを報告
- 新しいパターンが見つかった場合、`/learn-recipe` の実行を提案

### /wpush — Workato にプッシュする

ローカルの変更を Workato リモートにプッシュする。プッシュ前にバリデーションを実行。

```
/wpush                     # バリデーション → プッシュ
/wpush --start             # プッシュ後にレシピを起動
/wpush --test              # プッシュ後にテスト実行・ジョブ確認
/wpush --restart-recipes   # 既存の稼働中レシピを再起動
/wpush --delete            # リモートから削除されたアセットを削除
```

**プッシュフロー:**
1. JSON 構文チェック（全アセット）
2. `extended_output_schema` の存在チェック
3. 新規コネクションの検出 → **2段階プッシュ**
   - 第1段階: コネクションのみプッシュ → UI で認証
   - 第2段階: 残りのアセットをプッシュ
4. プッシュ実行
5. アセット種別に応じた後続手順の案内

**2段階プッシュの理由:** コネクションが未認証だと、レシピの `pick_list` フィールドが解決できず、プッシュ時にエラーになる。

詳細は [デプロイ手順ガイド](deployment.md) を参照。

---

## 学習フェーズ

### /learn-recipe — レシピからナレッジを学習

プルしたレシピ JSON を解析し、発見した知見をナレッジベースに直接追記する。

```
/learn-recipe <file>       # 特定レシピを学習
/learn-recipe <project>    # プロジェクト全体を学習
```

**学習対象と反映先:**

| 発見内容 | 反映先 |
|---|---|
| フィールド情報（extended_output_schema 等） | `docs/connectors/<provider>.md` |
| 新しいプロバイダ/アクション | `docs/connectors/` または `docs/platform/` |
| JSON 構造の新発見 | `.claude/rules/` |
| datapill パターン | `docs/logic/data-pills.md` |
| デプロイ関連の知見 | `docs/patterns/deployment-guide.md` |

### /learn-pattern — 構築パターンを記録

エキスパートの知見をパターンカタログに記録する。

```
/learn-pattern             # 対話的にパターンを記録
```

**パターンの構成:**
- 利用条件（いつこのパターンを使うか）
- レシピ構造図
- ステップ構成の詳細
- 設計判断のポイント
- 既知の落とし穴

**保存先:**
- 汎用パターン → `docs/patterns/recipe-patterns/`
- 組織ドメインパターン → `projects/docs/patterns/`

詳細は [ナレッジ管理ガイド](knowledge-management.md) を参照。

### /sync-connectors — コネクタ情報を同期

Pre-built コネクタとカスタムコネクタの情報を収集し、ドキュメントを更新する。

```
/sync-connectors <provider>        # 特定のコネクタを同期
/sync-connectors --custom          # カスタムコネクタのみ同期
/sync-connectors --all             # 全コネクタを同期
```

**Pre-built コネクタ:**
- Workato API でトリガー/アクションのメタデータを取得
- `docs/connectors/<provider>.md` を作成・更新

**カスタムコネクタ:**
- `connectors/*/connector.rb` を Ruby DSL パースで解析
- `connectors/docs/<name>.md` を作成・更新

---

## 整理フェーズ

### /catalog — 共有アセットのカタログ化

組織の共有プロジェクトをスキャンし、再利用可能なアセットをカタログ化する。

```
/catalog                   # 共有アセットをスキャン・カタログ生成
```

**スキャン対象:**
- コネクション（名前、プロバイダ）
- Recipe Function（入出力スキーマ付き）
- Workflow App
- MCP サーバー

**出力:** `projects/CATALOG.md` — `/create-recipe` や `/design` が参照し、既存アセットの再利用を提案する。

**スコープ制御:** `projects/CATALOG_CONFIG.yaml` で `global` / `team:<name>` / `private` を設定。`private` なプロジェクトはカタログに含まれない。
