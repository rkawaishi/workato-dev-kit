# 共有アセット管理ガイド

ワークスペース構成、命名規則、共有アセットの設計と運用方法。Claude Code / Cursor のどちらでも `/catalog` スキルでカタログを生成・参照できる。

## ワークスペースの構成

### 環境分離

| 環境 | 用途 |
|---|---|
| Dev | 開発・実験 |
| Test | テスト・検証 |
| Prod | 本番運用 |

環境ごとにワークスペースを分離し、SSO で認証を統合する。

### プロジェクトの階層構造

ワークスペース内のプロジェクトは3レベルの共有スコープで整理する:

```
Workspace/
├── Globally Shared Assets/           # 全チーム共通
│   ├── Common - Connections/         # 共通コネクション（Slack, Email 等）
│   ├── Common - Functions/           # 共通 Recipe Function
│   └── Error Handler/                # 共通エラーハンドリング
│
├── <Team> Shared Assets/             # チーム単位の共有
│   ├── <Team> - Connections/
│   ├── <Team> - Common Functions/
│   └── <Team> - <App Name>/         # チームのアプリ
│
└── <Project>/                        # プロジェクト固有
    ├── Connections/
    ├── Recipes/
    └── ...
```

| レベル | スコープ | 含むもの |
|---|---|---|
| **Globally Shared** | 全チーム・全プロジェクト | 共通コネクション、エラーハンドラ、汎用 Function |
| **Team Shared** | チーム内の全プロジェクト | チーム固有のコネクション、業務ロジック |
| **Project** | 単一プロジェクト | プロジェクト固有のレシピ |

## 命名規則

### プロジェクト・アセットの命名

```
<Project> <AssetCode> <Sequence> | <Description>
```

| アセットコード | 対象 |
|---|---|
| `REC` | レシピ |
| `CON` | コネクション |
| `FNC` | Recipe Function |
| `WFA` | Workflow App |
| `GNI` | Genie |
| `MCP` | MCP サーバー |
| `SKL` | Agentic Skill |

**例:**
- `Sales Lead Enrichment REC 001 | Enrich new Salesforce lead`
- `Common FNC 001 | Get line manager from AD`

### コネクションの命名

```
<Environment/Context> | <Provider> [- <Purpose>]
```

**例:**
- `Shared | Slack`
- `Shared | Jira - Engineering`
- `Sales | Salesforce - Production`

## 共有アセットの設計

### いつ共有するか

| 条件 | 判断 |
|---|---|
| 3つ以上のプロジェクトで使う | 共有する |
| チーム内で2つ以上のプロジェクトで使う | チーム共有する |
| 1つのプロジェクトでしか使わない | 共有しない |
| 認証スコープが異なる | 別コネクションにする |

### Recipe Function の設計

共有 Recipe Function は `fnc_<verb>_<noun>` の命名規則に従う:

```
fnc_get_line_manager       # 上長情報を取得
fnc_send_notification      # 通知を送信
fnc_validate_input         # 入力を検証
```

**設計指針:**
- 入出力スキーマを `parameter_schema_json` で明確に定義する
- エラーハンドリングを内部で完結させる
- 副作用を最小限にする（可能なら冪等に）

### コネクションの共有判断

| 観点 | 共有する | 共有しない |
|---|---|---|
| 認証スコープ | 全チーム共通の権限 | プロジェクト固有の権限 |
| 環境 | 全環境で同一 | 環境ごとに異なる |
| リスク | 障害影響が限定的 | 障害時の影響が広範 |

## カタログの運用

### /catalog でカタログを生成

```
/catalog
```

`projects/CATALOG.md` に以下を出力する:

- 全コネクション（名前、プロバイダ）
- 全 Recipe Function（入出力スキーマ付き）
- 全 Workflow App
- 全 MCP サーバー

### スコープ制御

`projects/CATALOG_CONFIG.yaml` で各プロジェクトのスコープを設定:

```yaml
scopes:
  "Globally Shared Assets": global
  "Sales - Common Functions": "team:sales"
  "My Private Project": private
```

| スコープ | カタログ掲載 | 他プロジェクトから参照 |
|---|---|---|
| `global` | される | 全プロジェクト |
| `team:<name>` | される | 同チームのプロジェクト |
| `private` | されない | 不可 |

### カタログの活用

- `/create-recipe` がステップ 2 でカタログを参照し、既存のコネクションや Recipe Function を再利用提案する
- `/design` がアーキテクチャ設計時にカタログから共有アセットの候補を表示する
- 新しいプロジェクトを始める前に `/catalog` を実行し、最新の共有アセット一覧を把握する

## Workato の参照メカニズム

共有アセットをプロジェクト間で参照する際、JSON 内で `zip_name` と `folder` フィールドを使う:

```json
{
  "keyword": "share",
  "provider": "salesforce",
  "zip_name": "Shared | Salesforce",
  "folder": "Globally Shared Assets/Common - Connections"
}
```

`/create-recipe` はカタログの情報を元にこれらの参照を自動生成する。手動で JSON を書く必要はない。
