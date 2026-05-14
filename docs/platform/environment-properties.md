# Environment Properties

Official: https://docs.workato.com/en/features/account-properties.html

## Overview

Recipe configuration parameters (name-value pairs) usable across the entire workspace. Also called environment variables or configuration variables. Centralizes shared configuration values across multiple recipes.

## Limits

| Item | Limit |
|---|---|
| Properties per environment | 1,000 |
| Property name | 100 characters |
| Property value | 1,024 characters |

## Configuration

Create name-value pairs from Tools > Environment properties.

## Use in recipes

Automatically appears in every recipe's **Properties** data tree. Values are retrieved dynamically at recipe runtime.

## Important behavior

> **Property value changes during a running job are not reflected.**
> Values are frozen at job start. Use Lookup Tables when dynamic value detection is required.

## Example use cases

- Centralized management of notification email addresses
- API endpoint URLs per environment
- Flag-based feature enable / disable
- Tenant IDs for external services

## Management via the Platform CLI

```bash
workato properties list
workato properties set <name> <value>
```
