# SurveyMonkey recipes

Provider value to use in every step: `surveymonkey`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "surveymonkey"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_survey_response` | Completed survey response | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `lookup_survey` | Search surveys | - |
| `send_flow` | Send survey invite via email | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_survey_respondent` | New survey respondent(deprecated) | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
