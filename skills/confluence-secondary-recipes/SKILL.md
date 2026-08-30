# Confluence secondary recipes

Provider value to use in every step: `confluence_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "confluence_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_page_v2` | Create page (API v2) | - |
| `get_ancestors_for_page` | Get ancestors for page | yes |
| `get_attachments_for_page` | Get attachments for page | yes |
| `get_children_for_page` | Get children for page | yes |
| `get_page_by_id` | Get page by ID | - |
| `search_labels` | Search labels | yes |
| `search_pages` | Search pages | yes |
| `search_spaces` | Search spaces | yes |
| `update_page` | Update page | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_page` | Create page | - |
| `create_task` | Create task | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
