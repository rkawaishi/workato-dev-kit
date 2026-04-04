---
paths:
  - "**/*.agentic_genie.json"
  - "**/*.agentic_skill.json"
  - "**/*.mcp_server.json"
---

# Workato Agentic JSON Format

## Genie（AIエージェント）: *.agentic_genie.json

```json
{
  "name": "Genie名",
  "logo_file_name": "logo.png",
  "logo_content_type": "image/png",
  "description": "Genieの短い説明",
  "instructions": "システムプロンプト（マークダウン）",
  "ai_provider": "anthropic",
  "ai_model": null,
  "matrix": false,
  "mcp_servers": [],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "skill_name.agentic_skill.json",
        "name": "スキル表示名",
        "folder": ""
      }
    }
  }
}
```

### フィールド詳細

| フィールド | 説明 |
|---|---|
| `instructions` | Genie のシステムプロンプト。役割、対象ユーザー、行動指針、禁止事項などを記述 |
| `ai_provider` | `"anthropic"` / `"openai"` 等 |
| `ai_model` | null でデフォルト、または具体的モデル名 |
| `matrix` | マトリクスモード（複数スキル並行実行） |
| `mcp_servers` | 接続する MCP サーバー一覧 |
| `references` | `ref_0`, `ref_1`... で使用するスキルを参照 |

### instructions のベストプラクティス

Genie のプロンプトは以下のセクションで構成:
- **What's my job?** — 主な責務
- **Who will need my help?** — 対象ユーザー
- **How do I get things done?** — 行動パターン
- **What should I avoid?** — 禁止事項
- **What results do you want me to track?** — 追跡すべき指標
- **How should I talk to people?** — コミュニケーションスタイル
- **Any extra tips?** — その他のヒント

## Agentic Skill: *.agentic_skill.json

```json
{
  "name": "スキル名",
  "trigger_description": "このスキルをいつ使うかの説明\n\n具体的な実行条件",
  "references": {
    "recipe_id": {
      "type": "recipe",
      "id": {
        "zip_name": "skill_recipe.recipe.json",
        "name": "レシピ名",
        "folder": ""
      }
    }
  }
}
```

### スキルとレシピの関係

```
agentic_genie.json
  └── references → agentic_skill.json (複数可)
                      └── references.recipe_id → recipe.json
```

- Genie は複数のスキルを持てる
- 各スキルは1つのレシピに紐づく
- スキル用レシピは `workato_genie` プロバイダーの `start_workflow` トリガーを使用
- スキル用レシピの最終ステップは `workflow_return_result` で結果を Genie に返す

## Connection: *.connection.json

```json
{
  "name": "接続名（例: Sample1 | Gmail）",
  "provider": "プロバイダー名",
  "root_folder": false
}
```

認証情報は含まれない。名前とプロバイダーのみ。

## ファイル命名規則

- レシピ: `<snake_case_name>.recipe.json`
- コネクション: `<prefix>_<provider>.connection.json`
- Genie: `<snake_case_name>.agentic_genie.json`
- スキル: `<snake_case_name>.agentic_skill.json`
- ロゴ: `<genie_name>.agentic_genie.png`
- MCP サーバー: `<name>.mcp_server.json`

## MCP Server: *.mcp_server.json

```json
{
  "name": "サーバー名",
  "description": "MCP サーバーの説明（AI がサーバー選択に使用）",
  "auth_type": "workato_idp",
  "tools_type": "project_assets",
  "tools": [
    {
      "tool": "ref_0",
      "description": "ツールの使用条件と指示（Use this tool when... / Do not use this tool when...）",
      "vua_required": true
    }
  ],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "Folder/skill_name.agentic_skill.json",
        "name": "skill_name",
        "folder": "Folder"
      }
    }
  }
}
```

### フィールド詳細

| フィールド | 説明 |
|---|---|
| `name` | MCP サーバーの表示名 |
| `description` | サーバー全体の説明。AI がどのサーバーを使うか判断する際に参照 |
| `auth_type` | 認証方式。確認済み: `"workato_idp"`（Workato Identity Provider） |
| `tools_type` | ツール種別。確認済み: `"project_assets"`（プロジェクト内アセット） |
| `tools[].tool` | `references` 内の参照キー（`ref_0`, `ref_1`, ...） |
| `tools[].description` | AI がツール選択に使う詳細指示 |
| `tools[].vua_required` | Verified User Access が必要か。`true` = エンドユーザーの認証情報で API 呼出し |
| `references` | `ref_N` → agentic_skill へのマッピング |

### 構造の関係

```
mcp_server.json
  └── tools[] → references → agentic_skill.json (複数可)
                                └── references.recipe_id → recipe.json
```

- MCP サーバーは Genie とは別の経路でスキルを公開する仕組み
- Genie が `references` でスキルを直接参照するのに対し、MCP サーバーは `tools[]` 配列で順序・説明付きで参照
- 各ツールの `description` は Genie スキルの `trigger_description` に相当するが、より詳細な AI 向け指示を含む
