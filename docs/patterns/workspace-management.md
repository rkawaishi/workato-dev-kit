# ワークスペース管理のベストプラクティス

ワークスペース構成、命名規則、コネクション管理のガイドライン。

## ワークスペースの構成

### 環境の分離

| 環境 | 用途 |
|---|---|
| Dev | 開発・実験 |
| Test | テスト・検証 |
| Prod | 本番運用 |

SSO で認証を統合し、環境ごとにワークスペースを分離する。

### プロジェクトの階層構造

```
Workspace/
├── Globally Shared Assets/           # 全チーム共通
│   ├── Common - Connections/         # 共通コネクション（Slack, Email 等）
│   ├── Common - Functions/           # 共通 Recipe Function
│   └── Error Handler/                # 共通エラーハンドリング
│
├── Team Shared Assets/               # チーム単位の共有
│   ├── Sales - Connections/
│   ├── Sales - Common Functions/
│   ├── Sales - Lead Enrichment/
│   ├── Sales - Sales Bell/
│   ├── Finance - Connections/
│   ├── Finance - Common Functions/
│   ├── Finance - Invoice Creator/
│   ├── Finance - Month End/
│   └── Finance - Cost Center Sync/
│
└── Project Shared Assets/            # プロジェクト固有
    ├── Connections/
    ├── Recipes/
    └── Workbot/
```

### 共有の3レベル

| レベル | スコープ | 例 |
|---|---|---|
| **Globally Shared** | 全チーム・全プロジェクト | 共通コネクション、エラーハンドラ、汎用 Function |
| **Team Shared** | チーム内の全プロジェクト | チーム固有のコネクション、業務ロジック |
| **Project** | 単一プロジェクト | プロジェクト固有のレシピ・コネクション |

## アセット命名規則

### 共通ボキャブラリーを使う理由

- アセット数が増えると検索・識別が困難になる
- 統一された命名で管理・監査が容易になる
- チーム間で一貫性を保てる

### 命名の構造

```
<Project> <Asset Code> <Sequence> | <Description>
```

| 要素 | 説明 | 例 |
|---|---|---|
| **Project** | プロジェクト略称 | `CBI`, `FIN`, `HR` |
| **Asset Code** | アセット種別コード | `REC` (Recipe), `CON` (Connection), `FNC` (Function) |
| **Sequence** | 連番 | `D01`, `D02` |
| **Description** | 説明（自然言語） | `Customer 360 Data Hub` |

**例**: `CBI REC D01 | Customer 360 Data Hub`

### アセット種別コード

| コード | 種別 |
|---|---|
| `REC` | Recipe |
| `CON` | Connection |
| `FNC` | Recipe Function |
| `WFA` | Workflow App |
| `GNI` | Genie |
| `MCP` | MCP Server |
| `SKL` | Agentic Skill |

### 本ツールキットでの適用

workato-dev-kit では以下の命名規則を使用している:

| アセット | 命名パターン | 例 |
|---|---|---|
| レシピ | `<説明的な名前>` | `IT onboarding: manager approval, Jira ticket, Slack notification` |
| Recipe Function | `fnc: <説明>` / `fnc_<snake_case>` | `fnc: Get manager from Google Sheets` |
| コネクション | `<Project> \| <Provider>` | `IT Onboarding \| Jira` |
| Workflow App | `<App名>` | `IT Onboarding` |
| スキルレシピ | `Skill: <説明>` | `Skill: Submit IT onboarding request` |

公式の `<Project> <Code> <Seq> | <Description>` 形式を採用する場合は、プロジェクト内で統一すること。

## コネクションの管理

### 命名規則

```
<環境/コンテキスト> | <Provider> [- <用途>]
```

**例**:
- `Shared | Slack` — 全社共通
- `IT Onboarding | Jira` — プロジェクト固有
- `Finance | Salesforce - Sandbox` — チーム固有 + 環境指定

### コネクション共有の判断

| 判断基準 | 共有 | 個別 |
|---|---|---|
| 認証スコープ | 全社共通の権限で十分 | プロジェクト固有の権限が必要 |
| 環境 | 同じ本番環境を参照 | Sandbox / テスト環境を使用 |
| リスク | 変更の影響範囲を許容 | 他プロジェクトへの影響を避けたい |

### 環境ごとのコネクション

開発環境と本番環境でコネクションを分離する:

```
Dev: IT Onboarding | Jira - Dev
Test: IT Onboarding | Jira - Test
Prod: IT Onboarding | Jira
```

## エラーハンドリング

Globally Shared に共通のエラーハンドラを配置し、全プロジェクトから参照する:

- **Error Handler** プロジェクト内に共通エラー通知レシピを配置
- 各レシピの Monitor/Error ブロックからエラーハンドラを呼び出す
- エラー通知先（Slack チャンネル、メール）を一元管理
