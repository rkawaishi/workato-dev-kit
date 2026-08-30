# workato-kit — a `wk` plugin for the assets `wk` does not model

[`wk`](https://github.com/workato-devs/wk) covers recipes, connections, folders,
tags, jobs, API Platform, MCP servers and agentic skills. Its
[known-limitations](https://github.com/workato-devs/wk/blob/main/docs/known-limitations.md)
map lists what it does not: **Genies, Data Tables, lookup tables, knowledge
bases, test cases, custom OAuth profiles**. Workflow Apps (`lcap_*`) and the
Connector SDK are not modelled either.

This plugin fills that gap. It deliberately does **not** validate
`*.recipe.json` — [`recipe-lint`](https://github.com/workato-devs/recipe-lint)
does that far better, with 66 built-in rules across four tiers.

Not affiliated with or endorsed by Workato.

## Install

```bash
wk plugins install <path-to>/workato-dev-kit/wk-plugin
wk kit version
```

Requires Python 3.8+ on PATH. `wk` spawns the entrypoint as a subprocess and
speaks newline-delimited JSON-RPC 2.0 over its stdin/stdout, so a plugin can be
written in any language ([ADR-004](https://github.com/workato-devs/wk/blob/main/docs/adrs/ADR-004-plugin-repo-structure.md)).

## Use

```bash
wk kit <path>...            # human-readable output (goes through the renderer)
wk kit <path>... --json     # machine-readable
wk kit validate <path>...   # subcommand form; always raw JSON
```

`wk kit` with no path walks the current directory.

## What it checks

| File | Rule | Why |
|---|---|---|
| `*.connection.json` | `KIT_CONNECTION_FILENAME` | The filename must be the snake_case of the display name, workspace prefix included. Otherwise Workato renames the file on push and the next pull reports it as a delete plus an add. |
| `*.connection.json` | `KIT_CONNECTION_REQUIRED` | `name` and `provider` are mandatory. |
| `*.workato_db_table.json` | `KIT_DATATABLE_SYSTEM_COLUMN` | Record ID / Created time / Last modified time are assigned server-side. Declaring them locally makes `pull` return a duplicate column. |
| `*.agentic_genie.json` | `KIT_GENIE_REQUIRED`, `KIT_GENIE_REF_TYPE`, `KIT_GENIE_REF_MISSING` | Skill references must resolve to a file in the project. |
| `*.agentic_skill.json` | `KIT_SKILL_REQUIRED`, `KIT_SKILL_RECIPE_MISSING` | The referenced recipe must exist. |

## The wire contract (as observed, not as documented)

`wk` 1.0.3 sends two different `params` shapes and one undocumented method.
None of this is in the ADR, so it was determined empirically — set
`WK_PLUGIN_DEBUG=<file>` to re-verify after a `wk` upgrade.

| Call | `params` |
|---|---|
| top-level command (`wk kit ...`) | object — declared args and flags |
| subcommand (`wk kit validate ...`) | bare array of positional arguments |
| `renderer` (`kit.render`) | `{"result": <command result>, "context": {"format": "text", "command_path": "wk kit"}}` |
| `shutdown` | none — sent when the command finishes; answer it or `wk` logs an error |

Flags declared under `[[commands.flags]]` attach to the **top-level** command
only; `wk kit validate --strict` is rejected as an unknown flag. Subcommands
have no `renderer` field, so they always print raw JSON.

## Windows

`plugin.toml` declares an extension-less `entrypoint`, and `wk` resolves it
through `PATHEXT` (the same mechanism that lets `recipe-lint`'s `./recipe-lint`
find `recipe-lint.exe`). So this directory ships both launchers:

- `workato-kit` — POSIX shell, `exec python3 workato_kit.py`
- `workato-kit.cmd` — Windows, resolved via `PATHEXT`

## Status

Skeleton. The remaining `wk` gaps — `deploy` (environment promotion),
`sdk push/pull/test` (Connector SDK), lookup tables, custom OAuth profiles —
are still served by `scripts/workato-api.py` and have not been moved behind
this plugin yet.
