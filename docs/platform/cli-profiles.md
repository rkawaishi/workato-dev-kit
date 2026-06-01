# Platform CLI profiles (dev / test / prod)

## Overview

A **CLI profile** is a named credential set in `~/.workato/profiles` that tells the Workato Platform CLI which workspace to talk to. Each workspace (dev, test, prod) gets its own profile.

> **Not to be confused with "Custom OAuth profiles"** (`workato oauth-profiles ...`), which is a workspace feature for storing OAuth client credentials for custom OAuth-based connectors. That feature has nothing to do with environment selection. This document is about CLI profiles only.

## Naming convention

```
<org>-<env>
```

| Profile name | Workspace | Example |
|---|---|---|
| `<org>-dev` | Dev workspace | `acme-dev` |
| `<org>-test` | Test workspace | `acme-test` |
| `<org>-prod` | Prod workspace | `acme-prod` |

The `<org>` prefix lets one developer hold profiles for multiple Workato tenants on the same machine (e.g. `acme-dev`, `beta-dev`).

## Push / pull matrix

This is the rule for AI agents and human developers alike. **Push is dev-only.** Promotion to test/prod must go through the Deploy feature (see `@docs/platform/environments.md`).

| Profile | `workato pull` | `workato push` | `workato init` | Notes |
|---|---|---|---|---|
| `<org>-dev` | ✅ | ✅ | ✅ | Default for daily work |
| `<org>-test` | ✅ | ❌ forbidden | ❌ | Pull only — e.g. to inspect what test currently has |
| `<org>-prod` | ✅ | ❌ forbidden | ❌ | Pull only — e.g. to verify a deploy succeeded |

"Forbidden" means the policy disallows it even though the CLI itself does not enforce it. Treat any `workato push` against `<org>-test` or `<org>-prod` as a bug.

## Profile selection rules

When you (or an AI agent) need to choose a profile, follow this order:

1. **If `.workatoenv` has `workspace_id`**: let `scripts/workato-api.py` auto-resolve. The `workspace_id` in `.workatoenv` is matched against the `workspace_id` field in each profile.
2. **If `.workatoenv` is missing**: explicitly pass `--profile <org>-dev`. **Never default to `-test` or `-prod`.**
3. **When in doubt**: default to `<org>-dev`. The cost of a misfire against prod is far higher than the cost of a misfire against dev.

The AI-agent shortcut: **if you cannot tell which profile to use, choose dev.**

## How AI agents should reason about profiles

- The `/push-project` skill operates on the project named in `.workatoenv` and the profile auto-resolved from `workspace_id`. If `workspace_id` points at prod, the agent **must refuse** and ask the user to switch to dev.
- `/pull-project` is safe against any profile — pull does not mutate the remote.
- When `--profile` is passed on the command line and it ends with `-test` or `-prod`, refuse `push` and only allow `pull` / read commands.

## Setting up profiles

```bash
# First-time setup for a workspace
workato init --non-interactive --profile <org>-dev --project-id <id> --folder-name "projects/<name>"

# Verify the profile maps to the right workspace
python3 scripts/workato-api.py profile show
```

Switch the **current profile** (used when no `.workatoenv` is present):

```bash
workato profiles use <org>-dev
```

List all profiles:

```bash
workato profiles list
```

## Where the credentials live

| File | Contents |
|---|---|
| `~/.workato/profiles` | Profile metadata (workspace_id, region, current_profile) — **not** the API tokens |
| OS keyring (macOS Keychain / Linux Secret Service) | API token per profile, managed by `workato init` |
| `.workatoenv` (per project) | `workspace_id` + `folder_id`; no credentials. Auto-generated; gitignored |

Never commit `.workatoenv` or anything from `~/.workato/`.

## Common mistakes

| Mistake | Consequence | Prevention |
|---|---|---|
| Naming a profile `dev` (no org prefix) | Collides across tenants; agent cannot disambiguate | Use `<org>-dev` |
| Setting `current_profile` to `<org>-prod` | Any CLI command without `--profile` hits prod | Keep `current_profile` on dev; pass `--profile <org>-prod` explicitly when needed |
| `workato push --profile <org>-prod` | Bypasses Deploy; overwrites prod | Push is dev-only; promote via Deploy |
| Sharing one profile across teammates | Audit log shows the wrong actor | Each developer runs `workato init` for their own profile |

## Related

- `@docs/platform/environments.md` — the three-tier environment model and Deploy feature
- `@.claude/rules/workato-deployment-flow.md` — the inviolable push-target rule
- `@.claude/rules/workato-cli.md` — Platform CLI reference
- `@.claude/rules/workato-cli-autonomy.md` — when to use the CLI vs. ask the user
