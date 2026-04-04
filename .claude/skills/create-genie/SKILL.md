---
description: Workato Genie (AIエージェント) + スキル + レシピの構成一式を対話的に生成する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /create-genie

Workato Genie（AIエージェント）の構成ファイル一式を生成するスキル。

## 手順

1. ユーザーに以下を確認:
   - **Genie の目的**: どんなAIエージェントを作るか
   - **対象ユーザー**: 誰が使うか
   - **スキル一覧**: Genie が持つスキル（それぞれの用途）
   - **AI プロバイダー**: `anthropic` / `openai`（デフォルト: `anthropic`）
   - **格納先プロジェクト**: どのプロジェクトディレクトリに作成するか

2. リファレンスを読む:
   - `@.claude/rules/workato-agentic-format.md`
   - `@.claude/rules/workato-recipe-format.md`
   - `@docs/known-patterns.md`

3. 既存の Genie があれば構造を参照

4. ファイルを生成（1つの Genie につき）:
   - `<name>.agentic_genie.json` — Genie 本体
   - スキルごとに:
     - `<skill_name>.agentic_skill.json` — スキル定義
     - `<skill_name>.recipe.json` — スキル用レシピ
   - 必要なコネクション: `<prefix>_<provider>.connection.json`

## Genie instructions の生成

以下のセクション構成でプロンプトを生成:

```markdown
You are a [Role] Agent

**What's my job?**
[主な責務の説明]

**Who will need my help?**
[対象ユーザーのリスト]

**How do I get things done?**
[行動パターンのリスト]

**What should I avoid?**
[禁止事項のリスト]

**What results do you want me to track?**
[追跡すべき指標]

**How should I talk to people?**
[コミュニケーションスタイル]

**Any extra tips?**
[追加のヒント]
```

## スキル用レシピの生成ルール

- トリガー: `workato_genie` / `start_workflow`
- `as` にはランダム8文字 hex を使用
- `input.parameters_schema_json`: 入力パラメータのスキーマ（JSON文字列）
- `input.result_schema_json`: 出力スキーマ（JSON文字列）
- `input.requires_user_confirmation`: `"false"`（デフォルト）
- `input.description`: スキルの trigger_description と同じ
- 最終ステップ: `workato_genie` / `workflow_return_result` で結果を返す
- 中間ステップ: 実際の業務ロジック（Salesforce 検索、API呼び出し等）

## 出力

生成完了後、以下を表示:
- 生成ファイル一覧
- Genie の構成図（Genie → Skills → Recipes）
- 各スキルの trigger_description サマリー
