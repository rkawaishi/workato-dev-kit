---
description: Workato カスタムコネクタ (Connector SDK) のプロジェクトをスキャフォールドし connector.rb を生成する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
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
   - `@docs/connector-sdk/overview.md` — SDK の概要と環境構築の落とし穴
   - `@docs/connector-sdk/connector-rb.md` — connector.rb リファレンス（HTTP メソッドの戻り値型・base_uri 規約・正規化ヘルパーのテンプレ含む）
   - `@.claude/rules/workato-connector-sdk.md` — フォーマットルール

3. API ドキュメントが提供された場合:
   - WebFetch で API の認証方法、エンドポイント、リクエスト/レスポンスを取得
   - OpenAPI 仕様がある場合はそれを優先参照

4. `connectors/<name>/` にファイルを生成:

### 生成ファイル

```
connectors/
├── .gitignore            # 共有（templates/gitignore/connectors.gitignore をコピー、初回のみ）
└── <name>/
    ├── connector.rb      # コネクタ本体
    ├── settings.yaml     # 認証情報テンプレート
    ├── Gemfile           # Ruby 依存関係
    └── README.md         # 接続設定手順
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

# Ruby 3.4+ で default gems から外れた stdlib。
# `LoadError: cannot load such file -- csv` 等を避けるため明示する。
# 詳細: docs/connector-sdk/overview.md「Ruby 4.0 では default gems が外れている」
gem 'csv'
gem 'base64'
gem 'bigdecimal'
gem 'logger'
gem 'drb'
gem 'ostruct'
gem 'mutex_m'

group :test do
  gem 'rspec'
  gem 'vcr'
  gem 'webmock'
end
```

## .gitignore テンプレート

`templates/gitignore/connectors.gitignore` を組織の `connectors/` リポジトリ直下に `.gitignore` としてコピーする（単一ソース）。

```bash
cp templates/gitignore/connectors.gitignore connectors/.gitignore
```

個別コネクタディレクトリ（`connectors/<name>/`）固有の追加除外が必要な場合のみ、サブディレクトリに `.gitignore` を別途作成する。

## 出力

生成完了後、以下を表示:
- 生成したファイル一覧
- コネクタの構成サマリー（認証方式、アクション数、トリガー数）
- 次のステップ:
  1. `settings.yaml` に認証情報を設定（ローカルテスト用）
  2. テスト（Ruby gem CLI, 任意）:
     ```bash
     cd connectors/<name>
     bundle install                              # 初回のみ
     bundle exec workato exec connector.rb test  # テスト（settings.yaml に実認証情報が必要）
     ```
     > **Note**: `bundle exec workato` を使うのは、Platform CLI と `workato` コマンド名が競合するため
  3. Workato へアップロード（API ヘルパー — Ruby 不要、Platform CLI のプロファイルで認証）:
     ```bash
     # 初回も更新も同じコマンドで OK。
     # 初回は新規作成し、返ってきた connector_id を
     # connectors/docs/<name>.md の YAML フロントマターに保存する。
     # 2 回目以降は frontmatter の connector_id を読んで自動で更新 push する。
     python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb
     ```
     - 明示的に新規作成したい場合は `--title "<Title>"` を付ける（frontmatter に ID が無い場合のみ）
     - 明示的に特定 ID を更新したい場合は `--connector-id <id>` を付ける（frontmatter より優先）
  4. docs の本体（トリガー/アクション/フィールド）を埋める:
     ```
     /sync-connectors --custom <name>
     ```
     初回 push 後、`connectors/docs/<name>.md` はフロントマター + スタブだけの状態になる。
     `/sync-connectors` が `connector.rb` をパースして本文を埋める（フロントマターは保持される）。
