# Genie & MCP 構築ガイド

Workato の AI エージェント (Genie) と MCP サーバーを構築・デプロイする手順。Claude Code / Cursor のどちらでも同じスキル・同じ手順で構築できる。

## 概要

### Genie (Agent Studio)

Genie は Workato の AI エージェント基盤。Slack や Teams から自然言語で業務を実行できる。

**4つの柱:**
1. **AI モデル & ジョブ記述** — エージェントの役割と振る舞いを定義
2. **チャットインターフェース** — Slack, Teams, Workato GO から利用
3. **ナレッジベース** — PDF, CSV, Markdown 等のドキュメント参照
4. **スキル** — Workato レシピを「ツール」として呼び出す

### MCP サーバー

Model Context Protocol (MCP) に準拠したサーバー。外部の AI モデル（Claude Desktop 等）から Workato のスキルをツールとして呼び出せる。

**3つのタイプ:**
- **Workato-hosted** — Workato が提供する MCP サーバー
- **Local** — ローカル環境で動作する MCP サーバー
- **Developer API** — API 経由でアクセスする MCP サーバー

## 構成要素

```
<project>/Agents/
├── <genie>.agentic_genie.json     # Genie 定義
├── <skill>.agentic_skill.json     # スキル定義（複数可）
├── <mcp>.mcp_server.json          # MCP サーバー定義（オプション）
└── ...

<project>/Recipes/
├── <skill-recipe>.recipe.json     # スキルが呼び出すレシピ
└── ...
```

### Genie 定義 (`.agentic_genie.json`)

- **instructions**: エージェントへの指示文（役割、制約、応答スタイル）
- **skills**: 紐付けるスキルの参照
- **ai_model**: 使用する AI モデル設定

### スキル定義 (`.agentic_skill.json`)

- **parameters**: ユーザー入力を受け取るパラメータ定義
- **recipe_reference**: 実行するレシピへの参照
- **trigger_type**: スキルのトリガータイプ

### MCP サーバー定義 (`.mcp_server.json`)

- **tools[]**: 公開するツール一覧（説明文、VUA 要件）
- **references**: スキル定義への参照マッピング

JSON のフォーマットルールは `.claude/rules/workato-agentic-format.md`（Cursor: `.cursor/rules/workato-agentic-format.mdc`）を参照。

## 構築手順

### 1. 設計

`/design` でエージェントの全体像を固める:

- **ペルソナ**: 誰向けのエージェントか（営業チーム、IT ヘルプデスクなど）
- **スキル一覧**: どんな操作ができるか
- **コネクション**: どのシステムに接続するか
- **MCP 公開**: 外部 AI からも使えるようにするか

### 2. アセット生成

```
/create-genie
```

対話的に以下を決定し、生成する:

1. Genie の目的とターゲットユーザー
2. 必要なスキル（操作の単位）
3. 各スキルのパラメータ
4. AI プロバイダ（デフォルト: Workato 提供モデル）
5. MCP サーバーとして公開するか
6. Genie の指示文（自動生成）

スキルレシピは `/create-recipe` に委譲して生成される。

### 3. デプロイ

```
/wpush
```

プッシュ後の確認:

```
ステップ 1: Agent Studio で Genie を確認
  → スキルが認識されているか
  → 指示文が正しく設定されているか

ステップ 2: テスト
  → チャットインターフェースでスキルを呼び出す
  → パラメータが正しく渡されるか確認

ステップ 3: (MCP の場合) ツール公開を確認
  → MCP サーバーのエンドポイントを確認
  → 外部 AI クライアントから接続テスト
```

## 設計のポイント

### Genie 指示文の設計

指示文はエージェントの品質を決定する最重要要素:

- **役割を明確に**: 「あなたは IT ヘルプデスクのアシスタントです」
- **制約を設ける**: 「人事情報には直接アクセスせず、必ず承認フローを通してください」
- **応答スタイル**: 「簡潔に回答し、技術用語は避けてください」
- **スキル使用の条件**: 「ユーザーが明確に依頼した場合のみスキルを実行してください」

### スキル粒度の設計

- **1スキル = 1操作** が基本（「Jira チケットを作成する」「Slack に通知する」）
- 複合操作は Genie の指示文で組み合わせを定義する
- パラメータは必要最小限に。AI が推論できる値はパラメータにしない

### MCP 公開の判断

| MCP 公開する場合 | MCP 公開しない場合 |
|---|---|
| 外部 AI (Claude Desktop 等) から使いたい | Slack/Teams の Genie チャットで十分 |
| 複数の AI クライアントから共通で使いたい | 社内の Workato ユーザーのみが対象 |
| API として外部に公開したい | セキュリティ上、外部公開は不可 |

### セキュリティ

- **Verified User Access (VUA)**: スキル実行時にユーザー認証を要求できる
- **RBAC**: Genie やスキルへのアクセスをロールで制御
- **監査ログ**: 全スキル実行がログに記録される
- **OAuth 認証**: MCP サーバーへの接続は OAuth で保護

## レシピから Genie を呼び出す

レシピ内から Genie にタスクを割り当てることも可能:

- コネクタ: `workato_genie`
- アクション: `assign_task_to_genie`
- 用途: 判断が必要なステップを AI に委譲する（例: メールの分類、データの要約）

## 既知の制限

- `/wpush --delete` では `agentic_skill` と `mcp_server` を削除できない。UI から手動削除が必要
- MCP サーバーにスキルを紐付けると、スキル名が自動リネームされる場合がある
- ナレッジベースのファイルアップロードは UI からのみ可能
