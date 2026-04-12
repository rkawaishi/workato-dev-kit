# カスタムコネクタ開発ガイド

Workato Connector SDK を使ったカスタムコネクタの開発フロー。Claude Code / Cursor のどちらでも `/create-connector` スキルで同じ手順で開発できる。

## いつカスタムコネクタを作るか

- Workato の Pre-built コネクタが存在しないサービスに接続したい
- Pre-built コネクタでは足りないアクション/トリガーが必要
- 社内 API やオンプレミスシステムに接続したい

## プロジェクト構造

```
connectors/
├── docs/                        # カスタムコネクタのナレッジ（自動生成）
│   └── <name>.md
└── <name>/
    ├── connector.rb             # コネクタ定義（メイン）
    ├── settings.yaml            # 認証情報テンプレート
    ├── Gemfile                  # 依存関係
    ├── .gitignore               # 機密情報の除外
    └── README.md                # セットアップ手順
```

## 構築手順

### 1. スキャフォールド

```
/create-connector
```

対話的に以下を決定し、ファイルを生成する:

- ターゲット API（URL、ドキュメント）
- 認証方式（API Key, OAuth2, Basic Auth 等）
- 必要なアクション（CRUD 操作等）
- 必要なトリガー（Polling, Webhook）

API ドキュメントの URL を指定すると、WebFetch で仕様を取得し、自動的にアクション/トリガーを設計する。

### 2. connector.rb の構造

`connector.rb` は Ruby DSL で書かれたコネクタ定義:

```ruby
{
  title: "My Connector",

  connection: {
    # 認証設定
    fields: [
      { name: "api_key", label: "API Key", control_type: "password" }
    ],
    authorization: {
      type: "api_key",
      apply: lambda do |connection|
        headers("Authorization" => "Bearer #{connection['api_key']}")
      end
    }
  },

  test: lambda do |connection|
    get("/api/me")
  end,

  object_definitions: {
    # 再利用可能なスキーマ定義
    user: {
      fields: lambda do
        [
          { name: "id", type: "integer" },
          { name: "name", type: "string" },
          { name: "email", type: "string" }
        ]
      end
    }
  },

  actions: {
    get_user: {
      title: "Get user",
      input_fields: lambda do
        [{ name: "id", type: "integer", optional: false }]
      end,
      execute: lambda do |connection, input|
        get("/api/users/#{input['id']}")
      end,
      output_fields: lambda do
        object_definitions["user"]
      end
    }
  },

  triggers: {
    new_user: {
      title: "New user",
      type: :paging_desc,
      poll: lambda do |connection, input, closure|
        # ポーリングロジック
      end,
      dedup: lambda do |record|
        record["id"]
      end,
      output_fields: lambda do
        object_definitions["user"]
      end
    }
  }
}
```

詳細な DSL リファレンスは `docs/connector-sdk/connector-rb.md` を参照。フォーマットルールは `.claude/rules/workato-connector-sdk.md`（Cursor: `.cursor/rules/workato-connector-sdk.mdc`）に定義されている。

### 3. ローカルテスト

```bash
# Connector SDK gem のインストール（初回のみ）
gem install workato-connector-sdk

# 接続テスト
workato exec connectors/<name>/connector.rb test

# アクション実行テスト
workato exec connectors/<name>/connector.rb actions.get_user

# トリガー実行テスト
workato exec connectors/<name>/connector.rb triggers.new_user
```

`settings.yaml` に認証情報を設定してからテストする。このファイルは `.gitignore` に含めること。

### 4. デプロイ

```bash
workato push connectors/<name>
```

プッシュ後、Workato UI でコネクションを作成し、認証テストを実行する。

### 5. ナレッジ化

```
/sync-connectors --custom
```

`connector.rb` をパースし、`connectors/docs/<name>.md` にアクション/トリガー/フィールドの一覧を自動生成する。これにより `/create-recipe` がカスタムコネクタのフィールド情報を参照できるようになる（Claude Code / Cursor 共通）。

## 認証方式

| 方式 | 用途 | 設定 |
|---|---|---|
| API Key | シンプルな API | ヘッダーまたはクエリパラメータに付与 |
| Basic Auth | ユーザー名/パスワード | `type: "basic_auth"` |
| OAuth 2.0 (Auth Code) | ユーザー認可が必要な API | `type: "oauth2"`, `authorization_url`, `token_url` |
| OAuth 2.0 (Client Credentials) | サーバー間通信 | `type: "oauth2"`, `client_credentials` grant |
| Custom | 独自認証 | `type: "custom_auth"`, `acquire` ブロックで実装 |

## トリガーの種類

| 種類 | 用途 | 実装 |
|---|---|---|
| `paging_desc` | 新規レコードを降順ポーリング | `poll` + `dedup` で重複排除 |
| `paging_asc` | 新規レコードを昇順ポーリング | タイムスタンプベースのカーソル管理 |
| Webhook | リアルタイム通知 | `webhook_subscribe` + `webhook_notification` |

## 設計のポイント

### object_definitions を活用する

入出力フィールドが複数のアクション/トリガーで共通する場合、`object_definitions` に定義して再利用する:

```ruby
object_definitions: {
  user: {
    fields: lambda do
      [
        { name: "id", type: "integer" },
        { name: "name", type: "string" }
      ]
    end
  }
},
actions: {
  get_user: {
    output_fields: lambda do
      object_definitions["user"]
    end
  },
  list_users: {
    output_fields: lambda do
      [{ name: "users", type: "array", of: "object",
         properties: object_definitions["user"] }]
    end
  }
}
```

### エラーハンドリング

API エラーを Workato のエラー形式に変換する:

```ruby
execute: lambda do |connection, input|
  response = get("/api/users/#{input['id']}")
  if response["error"]
    error(response["error"]["message"])
  end
  response
end
```

### ページネーション

大量データの取得にはページネーションを実装する:

```ruby
execute: lambda do |connection, input, extended_input_schema, extended_output_schema, continue|
  page = continue || 1
  response = get("/api/users", page: page, per_page: 100)
  {
    events: response["data"],
    next_poll: response["has_more"] ? page + 1 : nil
  }
end
```

## 開発環境の要件

- Ruby 2.7.x 〜 3.1.x
- `gem install workato-connector-sdk`
- `settings.yaml` に認証情報を設定（git にコミットしない）
