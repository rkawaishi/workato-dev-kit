---
paths:
  - "connectors/**/*.rb"
  - "connectors/**/connector.rb"
---

# Workato Connector SDK (connector.rb)

## File structure

```
connectors/<name>/
├── connector.rb          # main connector definition
├── settings.yaml         # credentials (development)
├── settings.yaml.enc     # credentials (encrypted)
├── master.key            # encryption key (must be in .gitignore)
├── Gemfile
└── spec/
    ├── connector_spec.rb
    └── cassettes/
```

## Top-level structure of connector.rb

```ruby
{
  title: 'Connector name',
  connection: { fields: [...], authorization: {...}, base_uri: lambda { } },
  test: lambda { |connection| },
  actions: { action_name: { execute: lambda { }, input_fields: lambda { }, output_fields: lambda { } } },
  triggers: { trigger_name: { poll: lambda { }, dedup: lambda { }, input_fields: lambda { }, output_fields: lambda { } } },
  object_definitions: { obj_name: { fields: lambda { } } },
  pick_lists: { list_name: lambda { } },
  methods: { method_name: lambda { } }
}
```

## Authorization types

`connection.authorization.type`:
- `basic_auth` — Basic auth
- `api_key` — API key
- `oauth2` — OAuth 2.0
- `custom_auth` — custom auth
- `multi` — multiple auth options

## Required keys for an action

- `execute` — execution logic (HTTP requests, etc.)
- `input_fields` — input field definitions
- `output_fields` — output field definitions

## Required keys for a polling trigger

- `poll` — data fetch. Returns `{ events:, can_poll_more:, next_poll: }`.
- `dedup` — deduplication key
- `input_fields` / `output_fields`

## Required keys for a webhook trigger

- `webhook_subscribe` / `webhook_unsubscribe` — dynamic webhooks
- `webhook_notification` — webhook payload handler
- `output_fields`

## Field definitions

```ruby
{ name: 'field', type: 'string', control_type: 'text', label: 'Display name', optional: true, hint: 'help text' }
```

Types: `string`, `integer`, `number`, `boolean`, `date`, `timestamp`, `object`, `array`.

## HTTP methods

`get`, `post`, `put`, `patch`, `delete` — `base_uri` is automatically prefixed.

## Knowledge management

Custom connector trigger / action / field info lives at `connectors/docs/<name>.md`.
`/sync-connectors --custom` parses `connector.rb` and generates it.
Same format as pre-built connectors (`docs/connectors/`).

## Auto-updating docs after `sdk push`

After `python3 scripts/workato-api.py sdk push` completes, update `connectors/docs/<name>.md` for the connector you pushed.

Steps:
1. Read `connectors/<name>/connector.rb`.
2. Generate or update `connectors/docs/<name>.md` following the custom-connector format used by the `/sync-connectors` skill.
3. Preserve any data accumulated under `## Field details` by `/learn-recipe`.

## Notes

- Only methods on the SDK's allow-list are available in connector.rb.
- Never commit `master.key`.
- If `settings.yaml` contains real credentials, add it to `.gitignore`.
- `connectors/` lives in the organization's workspace repository.

Details: `@docs/connector-sdk/connector-rb.md`.
