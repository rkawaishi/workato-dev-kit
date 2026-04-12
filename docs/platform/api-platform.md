# API Platform

公式: https://docs.workato.com/en/api-management.html

## 概要

エンタープライズグレードの API 管理機能。レシピのワークフローを REST エンドポイントとして公開し、API プロキシでレガシーシステムを安全に外部公開できる。

## コアコンポーネント

### API Recipes & Endpoints
レシピの機能を REST エンドポイントとして公開。他のレシピから呼び出したり、パートナーとデータを共有したりできる。

### API Collections
エンドポイント（レシピベース・プロキシベース）をコレクションにグループ化。統一的な管理とアクセス制御を提供。

### API Proxies
クライアントと内部 API の間に立つ仲介者。レガシーや内部システムを直接外部に晒さず安全に公開。

## 認証とセキュリティ

| 方式 | 説明 |
|---|---|
| OAuth 2.0 | 標準的な OAuth フロー |
| JWT tokens | JSON Web Token ベースの認証 |
| OpenID Connect | ID トークンベースの認証 |
| API Token | HTTP ヘッダー `api-token` で認証 |

## アクセス制御

| 概念 | 説明 |
|---|---|
| **Clients** | API コレクションへのアクセスを許可されたユーザー |
| **Access Profiles** | クライアントがアクセスできるコレクションを定義 |
| **Access Policies** | レート制限とクォータ管理をクライアントごとに設定 |

## モニタリング

- レスポンスタイム、エラーレート、トラフィックパターンのリアルタイム可視化
- 同時実行制限の追跡
- 容量超過時のリクエストキューイング

## MCP との関連

API Collections のエンドポイントは MCP サーバーとしても公開可能。
詳細は `@docs/platform/mcp.md` を参照。
