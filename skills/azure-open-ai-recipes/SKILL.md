# Azure OpenAI recipes

Provider value to use in every step: `azure_open_ai`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "azure_open_ai"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `analyse_document` | Analyse text | - |
| `analyse_image` | Analyse image | - |
| `categorize_text` | Categorize text | - |
| `chat_completion` | Send messages to ChatGPT | - |
| `completion` | Complete prompts | - |
| `draft_email` | Draft email | - |
| `embedding` | Generate text embedding | - |
| `parse_text` | Parse text | - |
| `summarize_text` | Summarize text | - |
| `translate_text` | Translate text | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `images` | Generate images | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
