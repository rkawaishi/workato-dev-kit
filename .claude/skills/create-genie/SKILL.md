---
description: Workato Genie (AIエージェント) + スキル + レシピの構成一式を対話的に生成する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /create-genie

Workato Genie（AIエージェント）の構成ファイル一式を生成するスキル。
Genie 単体、MCP サーバー単体、または両方の組み合わせに対応。

## Genie vs MCP Server — いつどちらを作るか

| | Genie | MCP Server |
|---|---|---|
| **用途** | 会話型AIエージェント | 外部AIへのツール公開 |
| **利用チャネル** | Slack, Teams, Workato GO | Claude Desktop, Cursor, ChatGPT |
| **ファイル** | `.agentic_genie.json` | `.mcp_server.json` |
| **スキル参照方式** | `references` で直接参照 | `tools[]` 配列で順序・説明付き参照 |
| **AI 指示** | `instructions`（システムプロンプト） | `tools[].description`（ツール選択指示） |

- **Genie のみ**: 社内チャットで使う会話型エージェント
- **MCP Server のみ**: 外部 AI エディタ/チャットからツールとして呼ぶ
- **両方**: Genie でも使え、外部 AI からも呼べる（スキル・レシピは共有可能）

## 手順

1. ユーザーに以下を確認:
   - **Genie の目的**: どんなAIエージェントを作るか
   - **対象ユーザー**: 誰が使うか
   - **スキル一覧**: Genie が持つスキル（それぞれの用途）
   - **AI プロバイダー**: `anthropic` / `openai`（デフォルト: `anthropic`）
   - **格納先プロジェクト**: どのプロジェクトディレクトリに作成するか
   - **MCP 公開**: MCP サーバーとしても公開するか（デフォルト: No）
   - **VUA**: Verified User Access が必要か（エンドユーザー認証情報で API 呼出し）

2. リファレンスを読む:
   - `@.claude/rules/workato-agentic-format.md`
   - `@.claude/rules/workato-recipe-format.md`
   - `@.claude/rules/workato-project-structure.md`
   - `@docs/connectors/_index.md` + 該当コネクタのナレッジ
   - `@docs/platform/agent-studio.md`
   - `@docs/platform/mcp.md`

3. 既存の Genie があれば構造を参照

4. Genie 構成ファイルを生成（`@.claude/rules/workato-project-structure.md` に従う）:
   - `<project>/Agents/<name>.agentic_genie.json` — Genie 本体
   - スキルごとに:
     - `<project>/Agents/<skill_name>.agentic_skill.json` — スキル定義
   - MCP 公開する場合: `<project>/Agents/<name>.mcp_server.json` — MCP サーバー定義
   - JSON 内の `zip_name` / `folder` にサブフォルダパスを含める

5. スキル用レシピは **`/create-recipe` に委譲** する:
   - 各スキルに必要なレシピの要件（トリガー: `workato_genie/start_workflow`、パラメータ、外部連携先）を整理
   - `/create-recipe` を呼び出してレシピを生成（ヒアリング含む）
   - Genie スキルレシピ固有の設定（`as` にランダム hex、`parameters_schema_json` 等）は `/create-recipe` のスキルが処理する

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
- `as` にはランダム8文字 hex を使用（Genie スキルレシピ固有の規則）
- `input.parameters_schema_json`: 入力パラメータのスキーマ（JSON文字列）
- `input.result_schema_json`: 出力スキーマ（JSON文字列）
- `input.requires_user_confirmation`: `"false"`（デフォルト）
- `input.description`: スキルの trigger_description と同じ
- パラメータ参照: `path:["parameters","<param_name>"]` — `parameters` 配下にネスト
- 最終ステップ: `workato_genie` / `workflow_return_result` で結果を返す
- `workflow_return_result` の入力: `input.result.<field>` に個別マッピング
  ```json
  "input": {
    "result": {
      "field1": "#{_dp('...')}",
      "field2": "#{_dp('...')}"
    }
  }
  ```
- `extended_output_schema` / `extended_input_schema` には `result` オブジェクト配下に result_schema_json のフィールドが展開される
- 中間ステップ: 実際の業務ロジック（Salesforce 検索、API呼び出し等）

## MCP サーバーファイルの生成

MCP 公開する場合、`<project>/Agents/<name>.mcp_server.json` を生成:

```json
{
  "name": "サーバー名",
  "description": "MCP サーバーの説明（AI がサーバー選択に使用）",
  "auth_type": "workato_idp",
  "tools_type": "project_assets",
  "tools": [
    {
      "tool": "ref_0",
      "description": "Use this tool when... / Do not use this tool when...",
      "vua_required": true
    }
  ],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "Agents/skill_name.agentic_skill.json",
        "name": "skill_name",
        "folder": "Agents"
      }
    }
  }
}
```

### MCP ツール description のガイドライン

- AI がツール選択に使う指示文。Genie の `trigger_description` より詳細に書く
- 「Use this tool when...」「Do not use this tool when...」形式が推奨
- 各ツールの使い分けが明確になるように記述する

### スキル名の注意

MCP サーバーにスキルを紐付けると、Workato がスキルの `zip_name` をレシピ名ベースにリネームすることがある。スキルのファイル名はレシピ名と一致させておくのが安全。

### MCP サーバーのデプロイ注意事項

- **初回 push**: MCP サーバー、スキル、スキルレシピが一括で作成される
- **更新時の `PG::UniqueViolation` エラー**: スキルが既に存在する状態で再 push するとこのエラーが発生する。CLI の `--delete` では `agentic_skill` と `mcp_server` は削除できない（`Skipped` になる）。**ユーザーに UI で手動削除してもらってから再 push** する必要がある
- **スキルレシピの `extended_output_schema`**: `add_record` 等のアクションに `extended_output_schema` がないと、後続ステップで datapill が認識されず起動エラーになる。全アクションに設定すること

### MCP のみの場合（Genie なし）

Genie を作らず MCP サーバーだけを作る場合:
1. スキル用レシピ（`workato_genie/start_workflow` トリガー）を生成
2. スキル定義（`.agentic_skill.json`）を生成
3. MCP サーバー定義（`.mcp_server.json`）を生成
4. Genie 本体（`.agentic_genie.json`）は不要

```
MCP Server → Skills → Recipes（Genie なし）
```

## レシピから Genie を呼び出す: `assign_task_to_genie`

レシピ内から Genie にタスクを委譲するアクション:

```json
{
  "provider": "workato_genie",
  "name": "assign_task_to_genie",
  "keyword": "action",
  "dynamicPickListSelection": { "genie_handle": "Genie名" },
  "toggleCfg": { "genie_handle": true },
  "input": {
    "genie_handle": {
      "zip_name": "Agents/genie.agentic_genie.json",
      "name": "Genie名",
      "folder": "Agents"
    },
    "task_instructions": "タスク指示文（datapill 可）"
  }
}
```

- `genie_handle`: 呼び出し先の Genie を参照（zip_name で指定）
- `task_instructions`: Genie に渡すタスク指示（datapill でコンテキストを注入可能）
- 用途: 承認フロー内で Genie に分析を依頼、イベント駆動で Genie にタスクを振る等

## 出力とデプロイガイド

生成完了後、以下を表示:
- 生成ファイル一覧
- 構成図:
  - Genie のみ: `Genie → Skills → Recipes`
  - MCP 付き: `Genie → Skills → Recipes ← MCP Server`
- 各スキルの trigger_description サマリー
- MCP 公開の場合: MCP サーバーの tools[] サマリー

`@docs/patterns/deployment-guide.md` に従い、デプロイを段階的に案内する:
1. コネクション先行 push → UI 認証（新規コネクションがある場合）
2. 全アセット push
3. UI でスキルレシピのフィールドマッピング確認を案内
4. MCP の場合: サーバー有効化と AI クライアント設定を案内
5. テスト実行を案内
