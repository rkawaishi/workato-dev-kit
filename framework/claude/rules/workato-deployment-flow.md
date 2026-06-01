---
paths:
  - "projects/**"
  - ".workatoenv"
---

# Workato deployment flow (inviolable)

## The rule

**Push always targets dev.** Promotion to test or prod must go through Workato's **Deploy** feature (UI or Recipe Lifecycle Management API).

> Never run `workato push` against a `<org>-test` or `<org>-prod` profile.
> Never script around deployment approvals.
> If unsure which environment a profile points at, **default to dev**.

This rule applies to AI agents and human developers alike. It exists because:

- A direct push to test or prod skips release-manager review.
- A direct push leaves no manifest, so the deployment cannot be audited or rolled back.
- A direct push silently overwrites whatever is currently running in that environment.

## Pre-flight checks before every push

Run these in order. **Abort the push if any check fails.**

1. **Read `.workatoenv`** and extract `workspace_id`.
2. **Resolve the profile** via `python3 scripts/workato-api.py profile show`.
3. **Confirm the profile name ends with `-dev`.** If it ends with `-test` or `-prod`, abort and tell the user:

   ```
   Refusing to push: the resolved profile is <profile-name>, which targets a non-dev environment.
   Push must target dev. To promote to test/prod, use the Deploy feature in the Workato UI.
   ```

4. **Confirm `workspace_id` matches a dev workspace.** If your organization tags workspaces (e.g. in a comment field), verify the tag says dev.

## When the user asks "push to prod"

Do not do it. Reply with:

```
Direct push to prod is not allowed. To release to prod:

1. Push to dev (workato push, with the <org>-dev profile).
2. Verify in the dev workspace.
3. In the Workato UI, open the project and click Deploy → test. Get QA sign-off.
4. From test, click Deploy → prod. Get release-manager approval.

See @docs/platform/environments.md for the full Deploy flow.
```

## When you must read from test or prod

Reading (pull, list) is allowed against any profile because it does not mutate the remote. Use it sparingly — for example, to diff dev against prod when investigating a release issue:

```bash
# Allowed
workato pull --profile <org>-prod   # into a scratch directory

# Forbidden
workato push --profile <org>-prod
```

## CLI/API operations the rule covers

| Operation | Against `<org>-dev` | Against `<org>-test` | Against `<org>-prod` |
|---|---|---|---|
| `workato push` | ✅ | ❌ refuse | ❌ refuse |
| `workato push --delete` | ✅ (with care) | ❌ refuse | ❌ refuse |
| `workato push --restart-recipes` | ✅ | ❌ refuse | ❌ refuse |
| `workato pull` | ✅ | ✅ | ✅ |
| `workato recipes start --all` | ✅ | ❌ refuse | ❌ refuse |
| `python3 scripts/workato-api.py sdk push` | ✅ | ❌ refuse | ❌ refuse |
| `POST /api/deployments/{id}/approve` | n/a | ❌ never script | ❌ never script |

## Related

- `@docs/platform/environments.md` — environment roles and the Deploy feature
- `@docs/platform/cli-profiles.md` — profile naming and push/pull matrix
- `@.claude/rules/workato-cli.md` — Platform CLI commands
- `@.claude/rules/workato-cli-autonomy.md` — when the CLI is the right answer
