# connector.rb リファレンス

公式: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html

ハマりどころ: `@docs/connector-sdk/pitfalls.md`

## トップレベル構造

```ruby
{
  title: 'コネクタ名',

  connection: {
    # 認証・接続設定
  },

  test: lambda do |connection|
    # 接続テスト
  end,

  actions: {
    # アクション定義
  },

  triggers: {
    # トリガー定義
  },

  object_definitions: {
    # 共通フィールド定義
  },

  pick_lists: {
    # ドロップダウンリスト
  },

  methods: {
    # 再利用可能なメソッド
  },

  # 上級機能
  # secure_tunnel:  OPA 対応
  # webhook_keys:   静的 Webhook トリガー用
  # streams:        ファイルストリーミング
}
```

全てのキーが必須ではない。必要なものだけ定義すればよい。

## connection ブロック

```ruby
connection: {
  fields: [
    { name: 'api_key', control_type: 'password', optional: false },
    { name: 'domain', control_type: 'subdomain', url: 'example.com' }
  ],

  authorization: {
    type: 'api_key',  # basic_auth, api_key, oauth2, custom_auth, multi
    apply: lambda do |connection|
      headers('Authorization': "Bearer #{connection['api_key']}")
    end
  },

  base_uri: lambda do |connection|
    "https://#{connection['domain']}.example.com/api/v1/"
  end
}
```

### 認証タイプ

| type | 説明 |
|---|---|
| `basic_auth` | Basic 認証（username + password） |
| `api_key` | API キー認証 |
| `oauth2` | OAuth 2.0（authorization_code, client_credentials） |
| `custom_auth` | カスタム認証フロー |
| `multi` | 複数認証方式の選択 |

## test ブロック

```ruby
test: lambda do |connection|
  get('/me')  # 接続確認 API を呼出し
end
```

## actions ブロック

```ruby
actions: {
  create_record: {
    title: 'Create record',
    subtitle: 'Creates a new record',
    description: lambda do |_input, pick_lists|
      "Create a <span class='provider'>record</span>"
    end,

    input_fields: lambda do |object_definitions|
      object_definitions['record']
    end,

    execute: lambda do |connection, input|
      post('/records', input)
    end,

    output_fields: lambda do |object_definitions|
      object_definitions['record']
    end,

    sample_output: lambda do |_connection, _input|
      { id: '123', name: 'Sample' }
    end
  }
}
```

### 必須キー

| キー | 説明 |
|---|---|
| `execute` | アクションの実行ロジック（HTTP リクエスト等） |
| `input_fields` | 入力フィールド定義 |
| `output_fields` | 出力フィールド（datapill）定義 |

### オプションキー

| キー | 説明 |
|---|---|
| `title` / `subtitle` | UI 表示名 |
| `description` / `help` | 説明・ガイダンス |
| `config_fields` | 事前設定フィールド（input_fields の前に表示） |
| `sample_output` | プレビュー用サンプル出力 |
| `batch` / `bulk` | バッチ/バルク処理フラグ |
| `retry_on_response` | リトライ条件（例: `[500, /error/]`） |
| `max_retries` | 最大リトライ回数（上限 3） |

## triggers ブロック

### ポーリングトリガー

```ruby
triggers: {
  new_record: {
    title: 'New record',

    input_fields: lambda do
      [{ name: 'since', type: 'timestamp' }]
    end,

    poll: lambda do |connection, input, closure|
      records = get('/records', updated_since: closure || input['since'])
      {
        events: records,
        can_poll_more: records.size >= 100,
        next_poll: records.last&.dig('updated_at') || closure
      }
    end,

    dedup: lambda do |record|
      record['id']
    end,

    output_fields: lambda do |object_definitions|
      object_definitions['record']
    end
  }
}
```

### ポーリングトリガーの必須キー

| キー | 説明 |
|---|---|
| `poll` | データ取得ロジック。`events`, `can_poll_more`, `next_poll` を返す |
| `dedup` | 重複排除キー（レコード ID 等） |
| `input_fields` | 入力フィールド |
| `output_fields` | 出力フィールド |

### Webhook トリガー（動的）

```ruby
triggers: {
  new_event: {
    webhook_subscribe: lambda do |webhook_url, connection, input|
      post('/webhooks', url: webhook_url, events: ['created'])
    end,

    webhook_unsubscribe: lambda do |webhook, connection|
      delete("/webhooks/#{webhook['id']}")
    end,

    webhook_notification: lambda do |_input, payload|
      payload
    end,

    output_fields: lambda do
      [{ name: 'id' }, { name: 'type' }]
    end
  }
}
```

## object_definitions ブロック

```ruby
object_definitions: {
  record: {
    fields: lambda do |connection, config_fields|
      [
        { name: 'id', type: 'string' },
        { name: 'name', type: 'string', optional: false },
        { name: 'email', type: 'string', control_type: 'email' },
        { name: 'created_at', type: 'timestamp' }
      ]
    end
  }
}
```

アクション/トリガーから `object_definitions['record']` で参照。フィールド定義の重複を防ぐ。

## pick_lists ブロック

```ruby
pick_lists: {
  statuses: lambda do |connection|
    [
      ['Active', 'active'],
      ['Inactive', 'inactive']
    ]
  end
}
```

## methods ブロック

```ruby
methods: {
  parse_response: lambda do |response|
    response['data'] || []
  end
}
```

コネクタ全体から `call('parse_response', response)` で呼び出し。

## フィールド定義スキーマ

```ruby
{
  name: 'field_name',           # 必須
  type: 'string',               # string, integer, number, boolean, date, timestamp, object, array
  control_type: 'text',         # text, password, email, url, select, multiselect, checkbox, subdomain
  label: '表示名',
  optional: true,               # デフォルト true
  hint: 'ヘルプテキスト',
  pick_list: 'statuses',        # pick_lists 内の名前
  properties: [...],            # type: 'object' の場合の子フィールド
  of: 'object',                 # type: 'array' の場合の要素型
  sticky: true                  # 常に表示（折りたたみ防止）
}
```

## HTTP メソッド

```ruby
get('/path')                     # GET
post('/path', payload)           # POST
put('/path', payload)            # PUT
patch('/path', payload)          # PATCH
delete('/path')                  # DELETE
```

全リクエストに `connection.base_uri` が自動付与される。

戻り値は `Workato::Connector::Sdk::Request < SimpleDelegator` でラップされているため、型判定・包装パターン・path 先頭スラッシュの扱いに注意。詳細は `@docs/connector-sdk/pitfalls.md`。
