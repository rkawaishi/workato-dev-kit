# Agent Studio

公式: https://docs.workato.com/en/agentic/agent-studio.html

## 概要

ノーコードで AI エージェント（Genie）を構築・管理するプラットフォーム。Genie はコンテキストを理解し、事前定義されたスキルを動的に実行する対話型 AI エージェント。

## Genie の4つのコンポーネント

### 1. AI Model & Job Description
- 使用する言語モデル（`anthropic`, `openai` 等）
- ペルソナ、制約、トーン、フォーマットの指示（`instructions` フィールド）

### 2. Chat Interface
- ユーザーとの対話インターフェース
- 対応プラットフォーム: Slack, Microsoft Teams, Workato GO

### 3. Knowledge Base
- FAQ、ポリシー、企業データなどの情報ソース
- 構造化データ、ドキュメント、記事、テキストリソース
- ファイル対応: PDF, CSV, Markdown, TXT（最大 25MB）、画像（最大 5MB）

### 4. Skills
- Workato ワークフロー/レシピを介したアクション実行
- データ取得、メッセージ送信、外部 API 呼出し

## 主な特徴

| 特徴 | 説明 |
|---|---|
| ドメイン専門性 | 既存システムと統合、ユーザーインタラクションから学習 |
| 推論能力 | 自然言語理解、マルチステップタスクの処理 |
| 責任ある行動 | 承認ワークフローで管理者がコントロール |
| 継続的学習 | フィードバックループとナレッジベース更新 |
| MCP クライアント | MCP サーバーを消費して外部 API やツールにアクセス |

## セキュリティ

- **RBAC**: Genie とナレッジベースの表示/編集/作成/削除権限を管理
- **Verified User Access**: ユーザーごとの認証情報でアクション実行（個人の権限に基づく）
- **監査証跡**: コンプライアンス用のログ記録

## JSON 構造

### agentic_genie.json
```json
{
  "name": "Genie名",
  "description": "短い説明",
  "instructions": "システムプロンプト",
  "ai_provider": "anthropic",
  "ai_model": null,
  "mcp_servers": [],
  "references": { "ref_0": { "type": "agentic_skill", "id": {...} } }
}
```

### agentic_skill.json
```json
{
  "name": "スキル名",
  "trigger_description": "スキルの実行条件",
  "references": { "recipe_id": { "type": "recipe", "id": {...} } }
}
```

詳細なフォーマット: `@.claude/rules/workato-agentic-format.md`

## レシピからの呼び出し

`workato_genie/assign_task_to_genie` アクションでレシピから Genie を呼び出し可能。
詳細: `@docs/learned-patterns.md`

## 利用可能リージョン

US, EU, AU, SG, JP データセンター（CN は不可）
