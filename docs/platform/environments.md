# Environments (dev / test / prod)

Official: https://docs.workato.com/en/recipe-development-lifecycle/environments.html

## Overview

Workato separates each tier of the development lifecycle into a **dedicated workspace**.
The standard layout is three tiers — **dev**, **test**, **prod** — and any code, connection, or asset change moves between them only through Workato's **Deploy** feature (UI or Recipe Lifecycle Management API).

Direct push to test or prod is prohibited (see `@.claude/rules/workato-deployment-flow.md`). All push operations target dev; promotion to higher tiers goes through Deploy.

## Environment roles

| Environment | Purpose | Who pushes here | How code arrives |
|---|---|---|---|
| **dev** | Development, experimentation, AI agent work | Developers, `/push-project`, AI agents | `workato push` (CLI / API) |
| **test** | QA verification, UAT | Release manager only | **Deploy** from dev |
| **prod** | Production operations | Release manager only (with approval) | **Deploy** from test |

The flow is one-directional:

```
dev  ──Deploy──▶  test  ──Deploy──▶  prod
 ▲
 │
push / pull (CLI, API, AI agents)
```

A change never skips a tier (dev → prod is not allowed) and never flows backward (prod → dev requires a fresh `workato pull` and re-development in dev).

## The Deploy feature

Deploy packages a project (or a subset of assets) from one workspace and applies it to the next-tier workspace. Each deployment is an immutable **manifest** that records the assets, the source environment, the target environment, and the operator.

### Deploy via the Workato UI

1. In the **source** workspace (e.g. dev), open the project.
2. Click **Deploy** → choose the target environment (e.g. test).
3. Select the manifest contents:
   - Recipes (specific recipes or all)
   - Connections (re-mapping per target)
   - Data Tables, Lookup Tables, Properties, etc.
4. Review the diff and submit. The target workspace receives the manifest.
5. (For prod) The release manager approves the manifest in the target workspace.

### Deploy via the API

Deploy is exposed by the **Recipe Lifecycle Management API** (also called Deploy API). The Platform CLI does not currently provide a high-level wrapper, so use `python3 scripts/workato-api.py` or call the API directly when scripting.

Key endpoints (in the source workspace):

| Action | Endpoint |
|---|---|
| Create a deployment manifest | `POST /api/deployments` |
| List deployments | `GET /api/deployments` |
| Get deployment status | `GET /api/deployments/{id}` |

See https://docs.workato.com/en/recipe-development-lifecycle/recipe-lifecycle-management.html for the full schema. Wrap usage in helper scripts so AI agents do not call the raw API ad-hoc.

### Approvals

The prod target can require explicit approval before the deployment becomes effective. Approval is a workspace setting; check with the workspace admin if your organization requires it. **AI agents must not bypass or auto-approve** deployment approvals.

## Differences between environments

Although the three workspaces share the same schema, each has its own runtime state. Plan around the following per-environment differences.

### Connections

Each workspace has its own connection credentials. The same connection file (e.g. `Connections/example_jira.connection.json`) is deployed across all three environments, but the **credentials** (OAuth tokens, API keys) are entered in each workspace independently.

| Concern | Per-environment behavior |
|---|---|
| Endpoint URL | Often different (e.g. `*-sandbox.example.com` in dev/test, `example.com` in prod) |
| Credentials | Always different; entered in the UI per workspace |
| Connection name | Same (use the same display name across environments) |

If the target service itself has a sandbox (e.g. Salesforce Sandbox vs. Production), keep the connection name identical but configure different credentials per workspace. Do **not** rename the connection per environment (it breaks Deploy).

### Data sources

| Source | Per-environment behavior |
|---|---|
| Data Tables | Schema is deployed; **records are not** (each environment starts empty) |
| Lookup Tables | Schema is deployed; rows must be seeded per environment |
| Environment Properties | Values are workspace-scoped; set them per environment (e.g. dev URL vs. prod URL). See `@docs/platform/environment-properties.md` |
| Custom Connectors | Source code is deployed; the connector must be **released** in each workspace |

### Runtime resources

| Resource | Per-environment behavior |
|---|---|
| Job execution quota | Each workspace has its own concurrency / job-per-minute quota |
| Job history | Workspace-scoped; you cannot replay a prod job in dev |
| Recipe ID | Different per environment (do not hardcode recipe IDs in code that crosses environments) |
| API endpoint base URL | Same Workato region, but the workspace ID in the URL differs |

### Folder / project IDs

`folder_id` and `project_id` are workspace-specific. The `.workatoenv` file therefore differs per environment. `.workatoenv` is git-managed (it holds only IDs, no credentials) and **must point at dev** — that is the binding the whole team shares. Prod-push protection does not depend on hiding this file: it comes from the deployment-flow profile check (the resolved profile must end in `-dev`). See `@.claude/rules/workato-deployment-flow.md` for the safety rule.

## Mapping environments to CLI profiles

Each environment corresponds to one **Platform CLI profile** (stored in `~/.workato/profiles`). The recommended naming is `<org>-<env>`:

| Profile name | Workspace | Allowed CLI operations |
|---|---|---|
| `<org>-dev` | Dev workspace | `workato push`, `workato pull`, `workato init` |
| `<org>-test` | Test workspace | `workato pull` only (push is forbidden by policy) |
| `<org>-prod` | Prod workspace | `workato pull` only (push is forbidden by policy) |

See `@docs/platform/cli-profiles.md` for the full profile selection rules and the push/pull matrix.

## Common mistakes

| Mistake | Consequence | Prevention |
|---|---|---|
| `workato push` against the prod profile | Bypasses Deploy approvals; overwrites prod | Set `<org>-dev` as the default profile in `.workatoenv`; use `<org>-test`/`<org>-prod` only for pull |
| Renaming a connection per environment | Deploy treats it as a new connection | Keep the same display name across environments |
| Hardcoding `folder_id` from dev into a doc / script | Targets the wrong workspace when the doc is reused | Always read `folder_id` from `.workatoenv` at runtime |
| Committing a `.workatoenv` that points at prod | Other developers resolve a prod profile | Commit only a dev-pointing `.workatoenv`; the deployment-flow check refuses any push whose profile is not `-dev` |
| Auto-approving prod deploy via script | Skips release-manager review | Manual approval only; never script `POST /api/deployments/{id}/approve` |

## Related

- `@.claude/rules/workato-deployment-flow.md` — the inviolable rule (dev-only push, Deploy-only promotion)
- `@docs/platform/cli-profiles.md` — profile naming and push/pull matrix
- `@docs/platform/environment-properties.md` — per-environment configuration values
- `@docs/patterns/workspace-management.md` — workspace layout and connection management
- `@docs/patterns/deployment-guide.md` — per-asset deployment procedure
