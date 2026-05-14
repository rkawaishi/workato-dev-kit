# connector.rb reference

Official: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html

## Top-level structure

```ruby
{
  title: 'Connector name',

  connection: {
    # Authentication / connection config
  },

  test: lambda do |connection|
    # Connection test
  end,

  actions: {
    # Action definitions
  },

  triggers: {
    # Trigger definitions
  },

  object_definitions: {
    # Shared field definitions
  },

  pick_lists: {
    # Dropdown lists
  },

  methods: {
    # Reusable methods
  },

  # Advanced features
  # secure_tunnel:  OPA support
  # webhook_keys:   For static webhook triggers
  # streams:        File streaming
}
```

Not all keys are required. Define only what you need.

## connection block

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

### Authentication types

| type | Description |
|---|---|
| `basic_auth` | Basic auth (username + password) |
| `api_key` | API key authentication |
| `oauth2` | OAuth 2.0 (authorization_code, client_credentials) |
| `custom_auth` | Custom authentication flow |
| `multi` | Choice among multiple authentication methods |

## test block

```ruby
test: lambda do |connection|
  get('/me')  # Call a connection-check API
end
```

## actions block

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

### Required keys

| Key | Description |
|---|---|
| `execute` | Action execution logic (HTTP request, etc.) |
| `input_fields` | Input field definitions |
| `output_fields` | Output field (datapill) definitions |

### Optional keys

| Key | Description |
|---|---|
| `title` / `subtitle` | UI display names |
| `description` / `help` | Description and guidance |
| `config_fields` | Pre-configuration fields (shown before `input_fields`) |
| `sample_output` | Sample output for preview |
| `batch` / `bulk` | Batch/bulk processing flags |
| `retry_on_response` | Retry conditions (e.g. `[500, /error/]`) |
| `max_retries` | Maximum retries (cap of 3) |

## triggers block

### Polling trigger

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

### Required keys for polling triggers

| Key | Description |
|---|---|
| `poll` | Data fetch logic. Returns `events`, `can_poll_more`, `next_poll` |
| `dedup` | Deduplication key (record ID, etc.) |
| `input_fields` | Input fields |
| `output_fields` | Output fields |

### Webhook trigger (dynamic)

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

## object_definitions block

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

Reference from an action or trigger as `object_definitions['record']`. Prevents duplicated field definitions.

## pick_lists block

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

## methods block

```ruby
methods: {
  parse_response: lambda do |response|
    response['data'] || []
  end
}
```

Call from anywhere in the connector via `call('parse_response', response)`.

## Field definition schema

```ruby
{
  name: 'field_name',           # Required
  type: 'string',               # string, integer, number, boolean, date, timestamp, object, array
  control_type: 'text',         # text, password, email, url, select, multiselect, checkbox, subdomain
  label: 'Display name',
  optional: true,               # Default true
  hint: 'Help text',
  pick_list: 'statuses',        # Name from pick_lists
  properties: [...],            # Child fields when type: 'object'
  of: 'object',                 # Element type when type: 'array'
  sticky: true                  # Always show (prevents collapse)
}
```

## HTTP methods

```ruby
get('path')                      # GET
post('path', payload)            # POST
put('path', payload)             # PUT
patch('path', payload)           # PATCH
delete('path')                   # DELETE
```

### `base_uri` and path

Every request joins `connection.base_uri` with the path as if by `URI.join`. **A path that starts with `/` is treated as an absolute path and resets to the host root**, dropping the path prefix on `base_uri`.

```ruby
# Reproduce the behavior in IRB (do not call URI.join inside a connector; this is just to inspect the SDK's behavior).
require 'uri'
URI.join('https://example.com/api/', '/users/me').to_s
# => "https://example.com/users/me"     <- /api/ is dropped
URI.join('https://example.com/api/', 'users/me').to_s
# => "https://example.com/api/users/me"
```

**Convention**: keep `base_uri` with a trailing slash, and pass paths to `get` etc. as relative paths with no leading slash.

### Return type

`get`, `post`, `put`, `patch`, `delete` return a `Workato::Connector::Sdk::Request < SimpleDelegator`. Even for APIs that return an Array or Hash, a direct type check inspects the Delegator itself and returns false.

```ruby
response = get('items')
response.is_a?(Array)   # => false (it inspects the Delegator)
response.class          # => Workato::Connector::Sdk::Request
```

To unwrap the underlying object, first route through `method_missing` to force lazy evaluation, then take `__getobj__` for the value. Always **restrict `rescue` to `NoMethodError`** (a modifier `rescue` swallows all of `StandardError` and would hide network exceptions).

```ruby
begin
  response.length
rescue NoMethodError
  # Pass through when the underlying object has no length (e.g. Hash)
end
body = response.__getobj__   # The underlying value (Array / Hash)
```

### Normalization helper for list APIs

For APIs whose response wrapping varies per endpoint (`[...]` directly / `{ "result": [...] }` / `{ "data": [...], "total": N }` / `{ "items": [...], "cursor": "..." }`, etc.), place a shared helper in the `methods` block and always route through it from `execute`.

```ruby
methods: {
  normalize_list_response: lambda do |response|
    begin
      response.length
    rescue NoMethodError
      # Pass through when the underlying value is a Hash, etc.
    end
    body = begin
      response.__getobj__
    rescue NoMethodError
      response
    end

    items = case body
            when Array then body
            when Hash  then body['result'] || body['data'] || body['items'] || []
            else []
            end
    next_cursor = body.is_a?(Hash) ? (body['next_page'] || body['cursor']) : nil

    { items: items, next_cursor: next_cursor }
  end
}
```

Normalizing the return value to a fixed shape `{ items:, next_cursor: }` makes `closure` design for trigger `poll` straightforward.
