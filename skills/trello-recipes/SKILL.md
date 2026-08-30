# Trello recipes

Provider value to use in every step: `trello`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "trello"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_card` | New card | - |
| `new_or_updated_card` | New or updated card | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_color` | Add color to card | - |
| `create_board` | Create board | - |
| `create_card` | Create card | - |
| `create_comment` | Add comment to card | - |
| `create_list` | Create list | - |
| `move_card` | Move card between boards | - |
| `move_card_within_board` | Move card within a board | - |
| `search_boards` | Search boards | yes |
| `search_cards` | Search cards | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
