# X recipes

Provider value to use in every step: `twitter`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "twitter"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_search_mention` | New search mention | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `post_status` | Post status | - |
| `search_tweets` | Search tweets | yes |
| `search_users` | Search users | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
