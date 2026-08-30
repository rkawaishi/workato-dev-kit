# WordPress.com recipes

Provider value to use in every step: `word_press`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "word_press"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_comment` | New comment | - |
| `new_post` | New post created | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_post` | Create post | - |
| `delete_post` | Delete post | - |
| `likes_for_post` | Get details of likes for post | yes |
| `post_lookup` | Search post | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
