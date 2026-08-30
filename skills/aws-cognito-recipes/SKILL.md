# Amazon Cognito recipes

Provider value to use in every step: `aws_cognito`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "aws_cognito"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `admin_initiate_auth_admin_no_srp_auth` | Authenticate user | - |
| `admin_initiate_auth_refresh_token_auth` | Refresh auth token | - |
| `get_credentials_for_identity` | Generate AWS secutity tokens using Cognito token | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
