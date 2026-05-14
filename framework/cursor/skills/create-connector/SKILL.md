---
name: create-connector
description: Scaffold a Workato custom connector (Connector SDK) project and generate its connector.rb. Japanese prompts are also supported.
---

# /create-connector

Interactively generate a Workato Connector SDK custom-connector project.

## Usage

- `/create-connector <api-name>` — create a connector for the given API (**preferred**; how `/implement` invokes it)
- `/create-connector` — create a new custom connector interactively (fallback)

> **Note**: connectors live under `connectors/<name>/` and are not tied to a single project (they're shared assets reused across projects). That's why this skill does not take a `<project>/<NNN>-<slug>` argument. When `/implement` dispatches a `[connector]` task, pass the **API documentation URL and the auth-method hints** from the calling project's `plan.md` `## New Components` `### Connections` section as arguments, or confirm them interactively.

## Procedure

1. Interview the user:
   - **Target API**: which service to connect to.
   - **API documentation URL**: the API spec.
   - **Auth method**: API key / OAuth 2.0 / Basic auth / custom.
   - **Required actions**: what operations are needed (CRUD, search, ...).
   - **Required triggers**: what events to detect (polling / webhook).

2. Read the references:
   - `docs/connector-sdk/overview.md` — SDK overview and setup pitfalls.
   - `docs/connector-sdk/connector-rb.md` — connector.rb reference (HTTP method return types, `base_uri` conventions, normalization helper templates).
   - `.cursor/rules/workato-connector-sdk.mdc` — format rules.

3. If the API docs are provided:
   - Use WebFetch to learn the auth method, endpoints, and request/response shapes.
   - If an OpenAPI spec exists, prefer it.

4. Generate files under `connectors/<name>/`:

### Files generated

```
connectors/
├── .gitignore            # shared (copy from templates/gitignore/connectors.gitignore on first run only)
└── <name>/
    ├── connector.rb      # the connector itself
    ├── settings.yaml     # credentials template
    ├── Gemfile           # Ruby dependencies
    └── README.md         # connection setup instructions
```

## Rules for generating connector.rb

### `connection` block
- Set `authorization.type` to match the API's auth method.
- Set `base_uri` to the API's base URL.
- Define the credentials the user has to enter (api_key, domain, etc.) under `fields`.

### `test` block
- Call a "get my info" endpoint (`/me`, `/user`, `/account`, etc.).

### `actions` block
- Always define `execute`, `input_fields`, and `output_fields` on every action.
- Define common fields under `object_definitions` and reuse across actions.
- Mirror the API docs' requests / responses faithfully.

### `triggers` block
- **Polling**: define `poll`, `dedup`, `input_fields`, `output_fields`.
  - `poll` returns `{ events:, can_poll_more:, next_poll: }`.
  - `dedup` returns the record's unique key.
- **Webhook**: define `webhook_subscribe`, `webhook_unsubscribe`, `webhook_notification`.

### `object_definitions` block
- Define the API's response objects as schemas.
- Share the field definitions across actions / triggers.

## settings.yaml template

```yaml
# Credentials (replace with real values)
api_key: YOUR_API_KEY
# domain: YOUR_DOMAIN
```

## Gemfile template

```ruby
source 'https://rubygems.org'

gem 'workato-connector-sdk'

# Stdlib gems that were removed from default gems in Ruby 3.4+.
# Declare them explicitly to avoid `LoadError: cannot load such file -- csv` etc.
# See docs/connector-sdk/overview.md "Default gems removed in Ruby 4.0".
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

## .gitignore template

Copy `templates/gitignore/connectors.gitignore` directly into the org's `connectors/` repository root as `.gitignore` (single source):

```bash
cp templates/gitignore/connectors.gitignore connectors/.gitignore
```

If a per-connector directory (`connectors/<name>/`) needs additional excludes, add a separate `.gitignore` in that subdirectory.

## Output

After generation, display:
- The list of generated files.
- A summary of the connector (auth method, action count, trigger count).
- Next steps:
  1. Set credentials in `settings.yaml` (for local testing).
  2. Test (Ruby gem CLI, optional):
     ```bash
     cd connectors/<name>
     bundle install                              # first run only
     bundle exec workato exec connector.rb test  # test (needs real credentials in settings.yaml)
     ```
     > **Note**: use `bundle exec workato` because the Connector SDK's `workato` command collides with the Platform CLI.
  3. Upload to Workato (API helper — no Ruby required; auths via the Platform CLI's profile):
     ```bash
     # The same command works for both the first push and subsequent updates.
     # On the first push it creates a new connector and saves the returned connector_id
     # to the YAML frontmatter in connectors/docs/<name>.md.
     # Subsequent pushes read the connector_id from the frontmatter and auto-update.
     python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb
     ```
     - To explicitly create a new connector, add `--title "<Title>"` (only when frontmatter has no ID).
     - To explicitly update a specific ID, add `--connector-id <id>` (overrides frontmatter).
  4. Populate the docs (triggers / actions / fields):
     ```
     /sync-connectors --custom <name>
     ```
     After the first push, `connectors/docs/<name>.md` is just frontmatter + a stub.
     `/sync-connectors` parses `connector.rb` and fills in the body (the frontmatter is preserved).

## Git management

Generated files (`connector.rb`, `Gemfile`, `settings.yaml`, `README.md`) live under `connectors/<name>/`. Commit them in the workspace repository:

```bash
git add connectors/<name>/
git commit -m "Add connector: <name>"
git push origin
```

`settings.yaml` is already excluded in the workspace `.gitignore` (it contains credentials). `sdk push` is the deploy to the Workato API, separate from git.
