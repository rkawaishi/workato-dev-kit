# AI by Workato recipes

Provider value to use in every step: `open_ai_utility`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "open_ai_utility"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `analyse_document` | Analyze text | - |
| `analyse_image` | Analyze image | - |
| `categorise_text` | Categorize text | - |
| `draft_email` | Draft email | - |
| `parse_text_v2` | Parse text | - |
| `summarize_text` | Summarize text | - |
| `translate_text` | Translate text | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `parse_text` | Parse text | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

### analyse_document (Action)

Recipe: Update Contract in Salesforce
Provider: `open_ai_utility`

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| _settings_version | string | - | Configuration version |
| text | string | Yes | Text/URL to analyze (can reference a document via datapill) |
| question | string | Yes | Prompt instruction for the analysis |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
