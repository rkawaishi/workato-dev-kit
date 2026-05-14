# Custom connector development guide

Development flow for custom connectors using the Workato Connector SDK. Both Claude Code and Cursor can develop with the same steps via the `/create-connector` skill.

## When to build a custom connector

- You want to connect to a service that has no pre-built Workato connector
- You need actions/triggers that the pre-built connector lacks
- You want to connect to internal APIs or on-premises systems

## Project structure

```
connectors/
├── docs/                        # Custom connector knowledge (auto-generated)
│   └── <name>.md
└── <name>/
    ├── connector.rb             # Connector definition (main)
    ├── settings.yaml            # Credential template
    ├── Gemfile                  # Dependencies
    ├── .gitignore               # Exclude secrets
    └── README.md                # Setup instructions
```

## Build steps

### 1. Scaffold

```
/create-connector
```

Interactively decide the following and generate files:

- Target API (URL, documentation)
- Authentication method (API Key, OAuth2, Basic Auth, etc.)
- Required actions (CRUD operations, etc.)
- Required triggers (Polling, Webhook)

When you specify the API documentation URL, WebFetch retrieves the spec and the actions/triggers are designed automatically.

### 2. Structure of connector.rb

`connector.rb` is a connector definition written in a Ruby DSL:

```ruby
{
  title: "My Connector",

  connection: {
    # Auth settings
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
    # Reusable schema definitions
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
        # Polling logic
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

For the detailed DSL reference, see `docs/connector-sdk/connector-rb.md`. Format rules are defined in `.claude/rules/workato-connector-sdk.md` (Cursor: `.cursor/rules/workato-connector-sdk.mdc`).

### 3. Local testing

```bash
# Install the Connector SDK gem (first time only)
gem install workato-connector-sdk

cd connectors/<name>
bundle install

# Connection test
bundle exec workato exec connector.rb test

# Action execution test
bundle exec workato exec connector.rb actions.get_user

# Trigger execution test
bundle exec workato exec connector.rb triggers.new_user
```

> **Note**: `bundle exec workato` is used because the Platform CLI and the `workato` command name conflict.

Configure credentials in `settings.yaml` before testing. This file must be included in `.gitignore`.

### 4. Deploy

Push via the API helper (authenticates with the Platform CLI profile; Ruby not required):

```bash
# Create new
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --title "<Title>"

# Update an existing connector
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --connector-id <id>
```

After pushing, create a Connection in the Workato UI and run the authentication test.

### 5. Knowledge capture

```
/sync-connectors --custom
```

Parses `connector.rb` and auto-generates a list of actions/triggers/fields into `connectors/docs/<name>.md`. This lets `/create-recipe` reference field information for custom connectors (works the same in Claude Code and Cursor).

## Authentication methods

| Method | Use case | Configuration |
|---|---|---|
| API Key | Simple APIs | Pass in header or query parameter |
| Basic Auth | Username/password | `type: "basic_auth"` |
| OAuth 2.0 (Auth Code) | APIs requiring user authorization | `type: "oauth2"`, `authorization_url`, `token_url` |
| OAuth 2.0 (Client Credentials) | Server-to-server communication | `type: "oauth2"`, `client_credentials` grant |
| Custom | Custom authentication | `type: "custom_auth"`, implement in `acquire` block |

## Trigger types

| Type | Use case | Implementation |
|---|---|---|
| `paging_desc` | Poll new records in descending order | `poll` + `dedup` for deduplication |
| `paging_asc` | Poll new records in ascending order | Timestamp-based cursor management |
| Webhook | Real-time notifications | `webhook_subscribe` + `webhook_notification` |

## Design points

### Leverage object_definitions

When input/output fields are shared across multiple actions/triggers, define them in `object_definitions` for reuse:

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

### Error handling

Convert API errors into Workato's error format:

```ruby
execute: lambda do |connection, input|
  response = get("/api/users/#{input['id']}")
  if response["error"]
    error(response["error"]["message"])
  end
  response
end
```

### Pagination

Implement pagination for retrieving large amounts of data:

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

## Development environment requirements

- Ruby 2.7.x to 3.1.x (for local testing)
- `gem install workato-connector-sdk` (for local testing)
- Configure credentials in `settings.yaml` (do not commit to git)
- Pushing to Workato is possible via `python3 scripts/workato-api.py sdk push` (Ruby not required)
