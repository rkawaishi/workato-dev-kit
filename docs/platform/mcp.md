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

## 利用可能リージョン

US, EU, AU, JP, SG データセンター（CN は不可）
