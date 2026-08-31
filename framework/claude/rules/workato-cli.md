---
paths:
  - ".workatoenv"
  - "projects/**"
  - "connectors/**"
---

# Workato CLI Tools

Four tools, in priority order. **Reach for `wk` first** — it is the official
Workato Labs CLI and it owns credentials, so the others borrow its token.

## 1. `wk` (Workato Labs CLI) — the default

Install: `brew install workato-devs/tap/wk` (macOS/Linux) or
`scoop bucket add workato-devs https://github.com/workato-devs/scoop-bucket && scoop install wk` (Windows).

```bash
wk auth login --environment dev --region us   # once, per environment
wk auth status                                # which workspace am I on?
```

Use it for:

| Task | Command |
|---|---|
| Sync a project | `wk pull` / `wk push` / `wk status` / `wk diff` |
| List recipes | `wk recipes list [--folder N] [--status running\|stopped]` |
| Read jobs | `wk recipes jobs <recipe-id> [--status failed] [--limit N]` |
| One job's step traces | `wk recipes jobs get <recipe-id> <job-id>` |
| Retry jobs | `wk recipes jobs retry ...` |
| Connections | `wk connections list/get/create/update/delete` |
| Custom SDK connectors | `wk connectors list` |
| Folders, projects, tags | `wk folders ...` / `wk tags ...` |
| API Platform | `wk api collections/endpoints/clients ...` |
| MCP servers | `wk mcp servers ...` |
| Lint a recipe | `wk lint <file> --skills-path kit/skills` |

Add `--json` to any command for machine-readable output.

> **`wk` has no environment guard.** `wk recipes start 123` will start a recipe
> in production without complaint. For anything that mutates state outside
> `wk push`, prefer the kit wrappers below, which refuse against non-dev.

## 2. API helper (only what `wk` does not do)

```bash
python3 scripts/workato-api.py <command>
```

It resolves the profile and token from `wk` (`wk auth status --json` +
`wk auth token`), falling back to the Platform CLI profile store when `wk` is
not set up. Nothing has to be authenticated twice.

| Command | Why it is not `wk` |
|---|---|
| `connectors list-platform [--provider <name>]` | `wk connectors list` returns only **custom SDK** connectors; this is pre-built connector metadata, and it is what `/sync-connectors` feeds into `docs/connectors/` and `skills/` |
| `jobs tail --recipe-id <id>` | `wk recipes jobs` is a single fetch; this follows |
| `recipes start <id>... [--folder N]` | delegates to `wk recipes start`, but **refuses unless the profile targets dev** |
| `recipes stop <id>... [--folder N]` | same guard, delegates to `wk recipes stop` |
| `deploy preview/run/status/list` | environment promotion via the Projects API — no `wk` command |
| `sdk push/pull/test/...` | Connector SDK — no `wk` command |
| `oauth-profiles list/get/create/update/delete` | custom OAuth profiles — listed as unsupported in `wk`'s known-limitations |
| `profile show` | shows the resolved profile **and its environment**, which is what the deploy guards read |

**Removed — use `wk` instead.** These fail with the replacement printed:

| Was | Now |
|---|---|
| `workato-api.py jobs list` | `wk recipes jobs <recipe-id>` |
| `workato-api.py jobs get` | `wk recipes jobs get <recipe-id> <job-id>` |
| `workato-api.py recipes list` | `wk recipes list` |
| `workato-api.py connectors list-custom` | `wk connectors list` |

## 2b. Platform CLI (legacy; still used by `pull-project` / `push-project`)

Install: `pipx install workato-platform-cli`

The kit's project pull/push still goes through this because the local layout is
`.workatoenv` + `projects/<name>/`, not `wk`'s `.wk/wk.toml` + `[[sync]]`.

- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "projects/<name>"`
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push` (`--restart-recipes`, `--delete`)

## 3. Connector SDK CLI (custom connector development & local testing)

Install: `gem install workato-connector-sdk`

**Note:** this gem ships a `workato` command that collides with Platform CLI. Always scope it with `bundle exec`.

```bash
cd connectors/<name>
bundle exec workato new <PATH>           # create
bundle exec workato exec <PATH> test     # local test
```

### Pushing a custom connector

**Use the API helper (recommended).** No Ruby needed; authenticates via Platform CLI's profile.

```bash
# First push
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --title "<Title>"
# Update an existing connector
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --connector-id <id>
```

> `bundle exec workato push` and `workato sdk push` also work, but the API helper is preferred for its profile auto-resolution and release automation.

### Pulling a custom connector

Mirror of `sdk push`: download a connector that already exists in the Workato workspace into the local repo.

```bash
# By connector ID
python3 scripts/workato-api.py sdk pull --connector-id <id>
# Or by connector name / title (resolved through list-custom)
python3 scripts/workato-api.py sdk pull --name <name>
```

Writes to `connectors/<name>/connector.rb` and stores `connector_id` in `connectors/docs/<name>.md` frontmatter so subsequent `sdk push` runs auto-update in place. Use `--force` to overwrite an existing `connector.rb`.

`--output-dir` overrides the destination, but it bypasses the canonical `connectors/` layout, so `connector_id` is **not** saved to docs frontmatter in that case — pass `--connector-id <id>` explicitly on the matching `sdk push`.

## Connector taxonomy

- **Pre-built**: Workato's official standard connectors (1,000+).
- **Universal**: HTTP, OpenAPI, GraphQL, SOAP — for APIs that don't have a standard connector.
- **Community**: connectors shared by other users.
- **Custom**: built with Connector SDK → lives in `connectors/`.
- **Custom Action**: in-connector `__adhoc_http_action` calls to hit an API directly.

## Pull / Push pitfalls

`workato pull` / `workato push` treats the Workato remote as the source of truth. If local naming or file structure doesn't match the remote's conventions, you can silently get renames / overwrites / duplicates. Always check the following.

### File naming and structure (before push)

- [ ] **Connection file name = snake_case of the display name (with the workspace name prefix)**
  - Example: display name `Key Broker | Workato Developer API` (workspace name = `Key Broker`) → file name `Connections/key_broker_workato_developer_api.connection.json`.
  - **If the display name does not start with the workspace name, Workato auto-prefixes it on push and renames the file.** The next `pull` then looks like "old file deleted, new file added", which causes confusion.
  - Workaround: decide on the display name as `<Workspace> | <Purpose>` first, then use its snake_case as the file name.
- [ ] **Data Table JSON: business columns only**
  - Do not write system columns (Record ID / Created time / Last modified time) locally. If you assign your own UUID, the remote assigns a different one and you get duplicates on pull.
  - System columns are fetched automatically by `workato pull`.
- [ ] **No credentials in `*.connection.json`** (Workato strips them automatically).

### Pre-pull checks

- [ ] Check for uncommitted changes with `git status`.
  - Pull overwrites (silently) and deletes (with a y/N prompt) local files.
  - Commit or stash any uncommitted edits before pulling.
- [ ] Ensure the project has a `.workatoignore`. The kit ships a base template at `templates/workatoignore.template` (covers catalog files and `*.custom_adapter.{rb,json}`); `/pull-project` places it automatically. Add any further project-specific exclusions to that file.

### Running `workato init` against an existing directory

- `workato init` refuses non-empty directories with `DIRECTORY_NOT_EMPTY` (there is no `--force`-style option).
- If you only need `.workatoenv` in a directory that already holds files:

```bash
# Init into a temporary directory
workato init --non-interactive --profile <profile> --project-id <id> \
  --folder-name "projects/_tmp_init_$$"

# Move only .workatoenv into the real directory
mv "projects/_tmp_init_$$/.workatoenv" "projects/<name>/"
rm -rf "projects/_tmp_init_$$"
```
