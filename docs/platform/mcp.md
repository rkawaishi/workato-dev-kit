# MCP (Model Context Protocol)

公式: https://docs.workato.com/en/mcp.html

## 概要

AI モデルを外部ツールやデータソースに接続するオープンスタンダード。AI エージェントがデータベース、API、ビジネスアプリケーションに共通プロトコルでアクセスできる。

## MCP サーバーの種類

| 種別 | 説明 | ホスティング |
|---|---|---|
| **MCP Servers** | API Collection エンドポイントを認証付き MCP URL で接続 | Workato ホスト |
| **MCP Local Servers** | ローカルのツール、データベース、API にアクセス | ローカルインフラ |
| **Developer API MCP Server** | Claude Desktop, Cursor, ChatGPT 等から Workato ワークスペースにアクセス | Workato ホスト |

## コアコンポーネント

| コンポーネント | 説明 |
|---|---|
| **Servers** | AI エージェントにツール/スキルを公開。認証とアクセス制御を実装 |
| **Skills / Tools** | 個別の機能（検索、作成、更新、分析等）。入出力スキーマと説明を持つ |
| **Dynamic Discovery** | AI エージェントが実行時に利用可能なツールを発見 |
| **Identity-Aware Execution** | 認証されたユーザー/エージェントの権限に基づいてアクション実行 |

## セキュリティ & ガバナンス

### 認証
- OAuth ベースのフローでユーザー認証
- **MCP Verified User Access**: 静的トークンではなくエンドユーザーの認証情報で外部 API を呼出し

### レート制限
- サーバーレベルで設定可能
- サーバー内の全スキル/ツールで共有
- ダウンストリームアプリケーションの保護と公平なリソース配分

### 監査 & コンプライアンス
- MCP サーバー経由の全アクションをログ記録
- 操作ごとのアイデンティティ追跡
- エンタープライズ監査システムとの統合

## API Platform との関係

API Collections のエンドポイントを MCP サーバーとして公開できる:
```
API Collection → MCP Server → AI Agent (Genie, Claude, ChatGPT)
```

詳細: `@docs/platform/api-platform.md`

## Agent Studio との関係

Genie は MCP クライアントとして MCP サーバーを消費できる:
```
Genie → MCP Client → MCP Server → 外部 API / ツール
```

`agentic_genie.json` の `mcp_servers` フィールドで接続先を指定。

## MCP Server Registry

プリビルトの MCP サーバーを検索・設定して LLM プロジェクトにアプリ固有のツールセットを追加。
公式: https://docs.workato.com/en/mcp/mcp-server-registry.html

## MCP Server JSON 構造 (`*.mcp_server.json`)

Workato プロジェクトをエクスポートすると、MCP サーバー定義が `*.mcp_server.json` ファイルとして含まれる。

### トップレベルフィールド

| フィールド | 説明 |
|---|---|
| `name` | サーバー表示名（例: "Gmail"） |
| `description` | AI がサーバーを選択する際に使う説明文 |
| `auth_type` | 認証方式。`"workato_idp"` = Workato Identity Provider |
| `tools_type` | `"project_assets"` = プロジェクト内アセットをツールとして公開 |
| `tools` | ツール定義の配列 |
| `references` | `ref_N` → agentic_skill へのマッピング |

### tools 配列の構造

```json
{
  "tool": "ref_0",
  "description": "Use this tool when... / Do not use this tool when...",
  "vua_required": true
}
```

- `tool`: `references` 内の参照キー
- `description`: AI がツール選択に使う詳細な指示文
- `vua_required`: Verified User Access が必要か（エンドユーザーの認証情報で外部 API を呼出し）

### references マップの構造

```json
{
  "ref_0": {
    "type": "agentic_skill",
    "id": {
      "zip_name": "Gmail/search_threads.agentic_skill.json",
      "name": "search_threads",
      "folder": "Gmail"
    }
  }
}
```

### MCP サーバー → スキル → レシピの関係

```
mcp_server.json
  └── tools[] → references → agentic_skill.json (複数可)
                                └── references.recipe_id → recipe.json
```

MCP サーバーは Genie とは異なる経路でスキルを外部 AI エージェント（Claude Desktop, Cursor, ChatGPT 等）に公開する。Genie が自身の `references` でスキルを直接参照するのに対し、MCP サーバーは `tools[]` 配列で順序付き・説明付きでスキルを公開する。

### スキル名の自動リネーム

MCP サーバーにスキルを紐付けると、Workato がスキルの `zip_name` をレシピ名ベースにリネームすることがある:
- push 時: `submit_pc_loan_request.agentic_skill.json`
- pull 後: `submit_pc_loan_request_via_mcp.agentic_skill.json`（レシピ名に合わせてリネーム）

スキルのファイル名はレシピ名と一致させておくのが安全。

### Gmail MCP Server の実例

Gmail サーバーでは 20 個のツール/スキルが定義されている:
search_threads, search_messages, list_labels, get_thread, get_message, list_attachments, add_labels, remove_labels, unstar_messages, star_messages, unarchive_threads, archive_threads, create_draft, get_draft, update_draft, send_draft, mark_message_read_state, list_drafts, add_attachments, remove_attachments

## 利用可能リージョン

US, EU, AU, JP, SG データセンター（CN は不可）
