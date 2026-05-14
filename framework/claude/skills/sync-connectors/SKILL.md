---
description: Collect connector metadata and update the docs. Pre-built connectors are fetched via the API and written to `docs/connectors/`; custom connectors are parsed from `connector.rb` and written to `connectors/docs/`. Japanese prompts are also supported.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /sync-connectors

Collect connector metadata and update the documentation.

- **Pre-built connectors**: fetched from the Workato API → updates `docs/connectors/`.
- **Custom connectors**: parsed from `connector.rb` → updates `connectors/docs/`.

## Usage

- `/sync-connectors <provider-name>` — fetch and update info for one pre-built connector
- `/sync-connectors <name1> <name2> ...` — batch-update several pre-built connectors
- `/sync-connectors --all` — update every pre-built + custom connector
- `/sync-connectors --check` — diff existing docs against the API
- `/sync-connectors --custom` — scan and update every custom connector under `connectors/`
- `/sync-connectors --custom <name>` — scan and update only the specified custom connector

## Data sources

### Pre-built connectors

#### Primary source: the Workato API (via CLI)

```bash
# Triggers / actions for a specific connector (JSON)
python3 scripts/workato-api.py connectors list-platform --provider <name>

# List of custom connectors
python3 scripts/workato-api.py connectors list-custom
```

What the API gives you:
- Connector name (`name`), display title (`title`).
- Category, OAuth support, deprecated flag.
- **Trigger list**: `name`, `title`, `deprecated`, `bulk`, `batch`.
- **Action list**: `name`, `title`, `deprecated`, `bulk`, `batch`.

What the API does **not** give you:
- Input / output field definitions (only available after the connection is configured).
- Field types and required/optional flags.

### Custom connectors

#### Source: `connector.rb` (local parse)

Read the Ruby DSL in `connectors/<name>/connector.rb` directly. No API call. Claude reads the DSL and extracts:

- `title:` — connector display name.
- `actions:` block — action names (hash keys), `title`, `batch`/`bulk` flags.
- `triggers:` block — trigger names (hash keys), `title`, and trigger type:
  - `poll` + `dedup` → Polling
  - `webhook_subscribe` → Webhook
- `object_definitions:` — shared field definitions (the array inside the `fields` lambda).
- `input_fields` / `output_fields` — field definitions:
  - For `object_definitions['name']` references, resolve to the corresponding definition.
  - For inline arrays, extract directly.
  - From each field, take `name`, `type`, `label`, `optional`, `hint`.

#### When `connector.rb` is missing

For a custom connector that lives only in the UI (no source under `connectors/<name>/`):
- Suggest running `workato sdk pull`.
- After the pull, run `/sync-connectors --custom` again.

### Supplementary source for pre-built

#### Secondary source: official docs (WebFetch)

Use this to fill in descriptions and notes that the API doesn't expose.
URL pattern: `https://docs.workato.com/en/connectors/<name>.html`

### Tertiary source: pulled recipes

Extract field info from `extended_output_schema` / `extended_input_schema`.
That's `/learn-recipe`'s job.

## Procedure

### Updating custom connectors (`--custom`)

1. Scan under `connectors/` and list directories that have a `connector.rb`:
```bash
ls connectors/*/connector.rb 2>/dev/null
```

2. Read each `connector.rb` and parse the Ruby DSL:
   - Take the connector display name from `title:`.
   - From the `actions:` block, extract each action's name (key), `title`, `batch`/`bulk` flags.
   - From the `triggers:` block, extract each trigger's name (key), `title`, and type (Polling/Webhook).
   - From `object_definitions:`, extract field definitions.
   - Resolve `input_fields` / `output_fields` for each action / trigger:
     - For `object_definitions['name']` references, expand the matching object_definition's fields.
     - For inline arrays, extract directly.

3. Create or update `connectors/docs/<name>.md`:

   **Frontmatter preservation rule**: if the file starts with a `---`-delimited YAML frontmatter (e.g. `connector_id:`), **always preserve it**.
   Do not modify or remove information written by `sdk push` (such as `connector_id`).

```markdown
---
connector_id: <id>   # managed automatically by sdk push
---

# <Title> connector

Provider: `<name>`
Source: Custom (Connector SDK)

## Triggers

| Name | Internal name | Type | Description |
|---|---|---|---|
| <title> | `<name>` | Polling/Webhook | |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## Field details

### <action/trigger name>

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| <name> | <type> | Yes/- | <label or hint> |

#### Output fields
| Field | Type | Description |
|---|---|---|
| <name> | <type> | <label or hint> |
```

4. Create the `connectors/docs/` directory if it doesn't exist.

5. With `--custom <name>`, process only the specified connector.

### Updating one pre-built connector

1. Fetch connector info via the CLI:
```bash
python3 scripts/workato-api.py connectors list-platform --provider <name>
```

2. Parse the JSON and extract triggers/actions.

3. Create or update `docs/connectors/<name>.md`:

```markdown
# <Title> connector

Provider: `<name>`

## Triggers
| Name | Internal name | Batch | Description |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## Actions
| Name | Internal name | Batch | Description |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## Field details

(accumulated by /learn-recipe)
```

### Diff-update rules

- **New file**: create when the file doesn't exist.
- **Existing file**:
  - Compare triggers/actions retrieved from the API with what's in the file.
  - Add anything new.
  - **Always preserve the frontmatter (the `---`-delimited YAML block).** Items like `connector_id` are managed by `sdk push` — never rewrite them.
  - Preserve sections after `## Field details` (info accumulated by `/learn-recipe`).
  - Annotate triggers / actions that flipped to deprecated.
- **Canonical provider name**: the API's `name` field is the canonical provider name.

### Running `--all`

#### Pre-built connectors
```bash
# Fetch every pre-built connector
python3 scripts/workato-api.py connectors list-platform
```
Fetch the JSON for every connector and generate / update `docs/connectors/<name>.md` for each.

#### Custom connectors
Scan every `connector.rb` under `connectors/` and generate / update `connectors/docs/<name>.md` (following the "Updating custom connectors" procedure).

### `--check` behavior

1. Fetch every connector's triggers / actions from the API.
2. Compare with existing files in `docs/connectors/`.
3. Report the diff:
   - ✅ Match
   - ⚠️ API has it, docs don't (new trigger / action)
   - ❌ Docs have it, API doesn't (removed or renamed)
   - 📄 Connector with no docs file at all

## Updating `docs/connectors/_index.md` (pre-built only)

During `--all`, also update `_index.md`:
- Refresh the pre-built connector list precisely from the API data.
- Use the `name` field as the provider name.
- Do not include custom connectors here (those are managed in `connectors/docs/` because they are org-specific).

## Output

After update, report:

### Pre-built connectors
- The list of created / updated files (`docs/connectors/`).
- The number of triggers / actions added.
- Triggers / actions newly flagged deprecated.

### Custom connectors
- The list of created / updated files (`connectors/docs/`).
- The number of triggers / actions / fields extracted.
- Directories whose `connector.rb` was missing (a pull is needed).

## Git management

This skill writes to **two locations**:

- `docs/connectors/*.md` → the knowledge base inside the kit (submodule) → PR back to workato-dev-kit.
- `connectors/docs/*.md` → the workspace repository's custom-connector knowledge.

Commit after running:

```bash
# Workspace side (custom connector updates)
git add connectors/docs/
git commit -m "docs: update custom connector info"

# Kit side (pre-built connector updates) → PR to workato-dev-kit
cd kit
git add docs/connectors/
git commit -m "docs: update pre-built connector info"
```

Committing and pushing only one side leaves your knowledge inconsistent.
