---
name: create-connector
description: Workato カスタムコネクタ (Connector SDK) のプロジェクトをスキャフォールドし connector.rb を生成する。
---

# /create-connector

Workato Connector SDK のカスタムコネクタプロジェクトを対話的に生成するスキル。

## 使い方

- `/create-connector` — 対話的に新しいカスタムコネクタを作成
- `/create-connector <api-name>` — 指定 API 用のコネクタを作成

## 手順

1. ユーザーに以下を確認:
   - **接続先 API**: どのサービスに接続するか
   - **API ドキュメント URL**: API の仕様書
   - **認証方式**: API キー / OAuth 2.0 / Basic 認証 / カスタム
   - **必要なアクション**: どんな操作が必要か（CRUD、検索等）
   - **必要なトリガー**: どんなイベントを検知するか（ポーリング / Webhook）

2. リファレンスを読む:
   - `docs/connector-sdk/overview.md` — SDK の概要
   - `docs/connector-sdk/connector-rb.md` — connector.rb リファレンス
   - `.cursor/rules/workato-connector-sdk.md` — フォーマットルール

3. API ドキュメントが提供された場合:
   - WebFetch で API の認証方法、エンドポイント、リクエスト/レスポンスを取得
   - OpenAPI 仕様がある場合はそれを優先参照

4. `connectors/<name>/` にファイルを生成:

### 生成ファイル

```
connectors/<name>/
├── connector.rb          # コネクタ本体
├── settings.yaml         # 認証情報テンプレート
├── Gemfile               # Ruby 依存関係
├── .gitignore            # master.key 等を除外
└── README.md             # 接続設定手順
```

## connector.rb の生成ルール

### connection ブロック
- API の認証方式に合わせて `authorization.type` を設定
- `base_uri` に API のベース URL を設定
- `fields` にユーザーが入力する認証情報（api_key, domain 等）を定義

### test ブロック
- API の「自分の情報を取得」エンドポイント（`/me`, `/user`, `/account` 等）を呼出し

### actions ブロック
- 各アクションに `execute`, `input_fields`, `output_fields` を必ず定義
- `object_definitions` で共通フィールドを定義し、アクション間で再利用
- API ドキュメントのリクエスト/レスポンスを正確に反映

### triggers ブロック
- **ポーリング**: `poll`, `dedup`, `input_fields`, `output_fields` を定義
  - `poll` は `{ events:, can_poll_more:, next_poll: }` を返す
  - `dedup` はレコードの一意キーを返す
- **Webhook**: `webhook_subscribe`, `webhook_unsubscribe`, `webhook_notification` を定義

### object_definitions ブロック
- API のレスポンスオブジェクトをスキーマとして定義
- アクション/トリガー間でフィールド定義を共有

## settings.yaml テンプレート

```yaml
# 認証情報（実際の値に置き換えてください）
api_key: YOUR_API_KEY
# domain: YOUR_DOMAIN
```

## Gemfile テンプレート

```ruby
source 'https://rubygems.org'
gem 'workato-connector-sdk'
gem 'rspec'
gem 'vcr'
gem 'webmock'
```

## .gitignore テンプレート

```
master.key
settings.yaml
settings.yaml.enc
*.gem
.bundle/
```

## 出力

生成完了後、以下を表示:
- 生成したファイル一覧
- コネクタの構成サマリー（認証方式、アクション数、トリガー数）
- 次のステップ（本家 CLI の場合）:
  1. `settings.yaml` に認証情報を設定
  2. `workato exec connectors/<name>/connector.rb test` でテスト
  3. `workato push connectors/<name>` でアップロード
- 次のステップ（フォーク版 CLI の場合）:
  1. `settings.yaml` に認証情報を設定
  2. `workato sdk exec connectors/<name>/connector.rb test` でテスト
  3. `workato sdk push connectors/<name>` でアップロード
