# Workato Dev Kit

[![tests](https://github.com/rkawaishi/workato-dev-kit/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/rkawaishi/workato-dev-kit/actions/workflows/tests.yml)
[![sync-check](https://github.com/rkawaishi/workato-dev-kit/actions/workflows/sync-check.yml/badge.svg?branch=main)](https://github.com/rkawaishi/workato-dev-kit/actions/workflows/sync-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![editors](https://img.shields.io/badge/editors-Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20CLI%20%7C%20Gemini%20CLI-orange.svg)](#features)

A toolkit for developing on Workato (enterprise iPaaS) with AI coding agents.
Supports [Claude Code](https://claude.com/claude-code), [Cursor](https://cursor.com), [Codex CLI](https://github.com/openai/codex), and [Gemini CLI](https://github.com/google-gemini/gemini-cli).

Covers recipe development, Workflow App construction, AI agent creation (Genie / MCP), and custom connector development.

> The documentation is in English. The toolkit still works for Japanese-speaking users — Claude, Cursor, and the other agents respond in whatever language you write your prompts in, so you can keep working in Japanese while the underlying docs stay English.

## Features

- **Recipe JSON generation** — build a Workato Recipe interactively, then deploy it with `workato push`
- **Workflow App construction** — Data Tables, pages, and approval flows expressed as JSON
- **MCP server construction** — expose tools to AI agents over the MCP protocol
- **Genie (AI agents)** — generate AI agent configurations with attached skills
- **Custom connectors** — assistance for Connector SDK (Ruby DSL) development
- **Knowledge base** — docs for 316 connectors, 7 logic patterns, and 13 platform features
- **Learning cycle** — pull → analyze → accumulate patterns → feed back into the next generation
- **Lint pack for `wk lint`** — a generated connector skill pack (`skills/`, 302 connectors) that makes the official [recipe-lint](https://github.com/workato-devs/recipe-lint) reject actions and triggers a connector does not actually have

## Prerequisites

- A [Workato](https://www.workato.com/) account and API token
- [Workato Platform CLI](https://github.com/workato-devs/workato-platform-cli) (`pipx install workato-platform-cli`)
- One of the supported editors: [Claude Code](https://claude.com/claude-code), [Cursor](https://cursor.com), [Codex CLI](https://github.com/openai/codex), or [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## Setup

> For the full walkthrough, see **[Quick Start (Claude Code)](guides/quickstart-claude-code.md)** or **[Quick Start (Cursor)](guides/quickstart-cursor.md)**.

Add workato-dev-kit as a submodule of your organization's workspace repository. You can update the framework later with `git submodule update`.

```bash
# Create your organization's workspace repository
mkdir my-org-workato && cd my-org-workato
git init

# Add workato-dev-kit as a submodule
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# Run the setup script (creates symlinks/copies and config files)
bash kit/setup.sh

# Initialize the Platform CLI
workato init

# Initial commit
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

Resulting directory layout:

```
my-org-workato/                 ← your organization's repository (the working root)
├── .claude/                    ← for Claude Code
│   ├── CLAUDE.md               # auto-generated (customizable)
│   ├── rules/                  # kit rules (symlinks) + your own rules
│   ├── skills/                 # kit skills (symlinks) + your own skills
│   ├── hooks/                  # kit hooks (symlinks)
│   └── settings.json           # auto-generated (customizable)
├── .cursor/                    ← for Cursor (copies, because Cursor does not reliably follow symlinks)
│   ├── rules/, skills/, hooks.json
│   └── .kit-manifest           # tracks kit-managed files
├── .agents/skills/             ← for Codex CLI (symlinks)
├── .gemini/skills/             ← for Gemini CLI (symlinks)
├── AGENTS.md → kit/...         ← agent-neutral conventions for Codex / Aider / etc.
├── GEMINI.md → kit/...         ← same file as AGENTS.md (different name)
├── docs/ → kit/docs/           ← knowledge base (symlink)
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule (read-only)
├── projects/                   ← your organization's recipes
└── connectors/                 ← your organization's custom connectors
```

**Updating the framework:**

```bash
git submodule update --remote kit
bash kit/setup.sh    # add symlinks for new skills/rules, prune retired ones, re-copy .cursor/
git add kit .cursor && git commit -m "Update workato-dev-kit"
```

> **Cursor users must re-run setup**: `.cursor/` ships as real file copies (not symlinks), so re-run `bash kit/setup.sh` after every kit update. Cursor IDE cannot reliably resolve symlinks ([details](guides/architecture.md#supported-editors)).

**Adding your own skills or rules:** drop them into `.claude/rules/` or `.claude/skills/` as regular files; they coexist with the kit's content. (`setup.sh` does not overwrite real files, only refreshes symlinks.) For Cursor, `.cursor/.kit-manifest` tracks kit-managed files, and any real file not in the manifest is preserved as a user file.

## Workspace structure

Place your organization's recipes and connectors under `projects/` and `connectors/`.

### Recipe projects (projects/)

```bash
# Pull a project from Workato
workato projects use "<project-name>"
workato pull

# Develop, then commit
git add projects/<project-name> && git commit -m "Add IT Onboarding workflow"
```

### Linting recipes (`skills/`)

`scripts/gen_lint_rules.py` turns `docs/connectors/*.md` into a connector skill
pack that the official [`recipe-lint`](https://github.com/workato-devs/recipe-lint)
plugin consumes, so a hallucinated action name fails before it reaches Workato:

```bash
wk plugins install recipe-lint     # once
wk lint projects/<project>/Recipes/*.recipe.json --skills-path kit/skills
```

```
/code/block/0/name [ERROR] ACTION_NAME_VALID: Action name "post_message" is not
valid for provider "slack"; expected one of [__adhoc_http_action ...
post_message_to_channel ...]
```

The `skills/` tree is generated — regenerate it after `/sync-connectors` or
`/auto-learn` updates a connector doc:

```bash
python3 scripts/gen_lint_rules.py            # all connectors
python3 scripts/gen_lint_rules.py --only slack
```

Pass `--exclude-official` to skip the seven connectors
[workato-devs/recipe-skills](https://github.com/workato-devs/recipe-skills)
already ships, if you point `--skills-path` at a directory that merges both.

## Skills

| Skill | Description |
|---|---|
| `/create-recipe` | Generate a recipe JSON interactively |
| `/create-workflow-app` | Build a Workflow App in stages (Data Table, pages, recipes) |
| `/create-genie` | Generate a Genie / MCP server + skills configuration |
| `/create-connector` | Scaffold a custom connector |
| `/catalog` | Scan and catalog shared assets |
| `/validate-recipe` | Validate Genie / Workflow App / connection JSON (recipes go through `wk lint`) |
| `/pull-project` | Pull a project from Workato |
| `/push-project` | Push local changes (with validation and recipe start) |
| `/learn-recipe` | Learn field info from pulled recipes into `org/docs/` |
| `/learn-pattern` | Record or update recipe construction patterns in the catalog |
| `/sync-connectors` | Collect and update connector info (pre-built: API; custom: parse `connector.rb`) |
| `/auto-learn` | Autonomously collect all operations for one connector via Claude in Chrome (no prompts) |

See [skill reference](guides/skills-reference.md) and [lifecycle and responsibility map](guides/lifecycle.md) for details.

### Editor-specific usage

| Editor | Skill location | Invocation |
|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `/skill-name` |
| Cursor | `.cursor/skills/<name>/` | `/skill-name` |
| Codex CLI | `.agents/skills/<name>/` | `$skill-name` (slash syntax rewritten to `$`) |
| Gemini CLI | `.gemini/skills/<name>/` | `/skill-name` |

Cross-agent conventions (`CLAUDE.md` + `rules/` aggregated) are distributed as `AGENTS.md` / `GEMINI.md` (the same file under two names).

## Development flow

### New project

```
/catalog                                     ← check what already exists and can be reused
/sync-connectors <provider>                  ← fetch metadata + regenerate the lint pack
/create-recipe "<project-name>"              ← interview → generate recipe JSON
wk lint ... --skills-path kit/skills         ← deterministic validation
/push-project --start                        ← push + start recipes
(adjust in the Workato UI)
/pull-project → /learn-recipe                ← learning cycle
```

### Learning cycle

```
workato pull → /learn-recipe → update docs/ → next generation is more accurate
             → /learn-pattern → update pattern catalog → PR back to workato-dev-kit
```

## Repository layout

This is the layout of the workato-dev-kit repository itself, which consumers add as a `kit/` submodule.

The canonical source is `framework/claude/`. The Cursor / Codex / Gemini variants are auto-generated by `scripts/sync_agents.py`. The root-level `.claude/` only contains settings **for developing this repository itself**, so that opening kit/ in Claude Code does not accidentally surface the Workato authoring skills like `/create-recipe`.

```
workato-dev-kit/                 ← this repository (add as a kit/ submodule)
├── .claude/                     # for developing the kit itself (no Workato authoring skills)
├── framework/                   # distributables (symlinked / copied into the consumer's editor configs)
│   ├── claude/                  # canonical source
│   │   ├── CLAUDE.md            #   consumer-facing conventions (Workato authoring rules)
│   │   ├── rules/               #   8 rules (recipe format, etc.)
│   │   ├── skills/              #   19 skills
│   │   ├── hooks/               #   automation hooks
│   │   └── settings.json        #   consumer-facing settings template
│   ├── cursor/                  # auto-generated: rules/*.mdc + skills/ + hooks.json (hand-maintained)
│   ├── codex/skills/            # auto-generated (slash syntax rewritten to $)
│   ├── gemini/skills/           # auto-generated
│   └── AGENTS.md                # auto-generated: CLAUDE.md + rules aggregated. GEMINI.md is the same file.
├── docs/                        # knowledge base
│   ├── connectors/              #   316 connectors
│   ├── connector-sdk/           #   Connector SDK reference
│   ├── logic/                   #   7 logic patterns
│   ├── platform/                #   13 platform features
│   └── patterns/                #   deployment guide, shared assets, construction patterns
├── guides/                      # consumer-facing guides
├── scripts/
│   ├── sync_agents.py           #   framework/claude/ → cursor/codex/gemini/ + AGENTS.md
│   ├── sync-cursor-rules.sh     #   backwards-compatible wrapper
│   └── workato-api.py
├── templates/                   # templates for consumer repositories (.gitignore, etc.)
├── i18n/GLOSSARY.md             # canonical English wording for terms used across the kit
└── setup.sh                     # setup script run inside a consumer repository
```

### Editing distributables

- Edit `framework/claude/` for skills and rules
- After editing, always run **`python3 scripts/sync_agents.py`** to regenerate `framework/{cursor,codex,gemini}/` and `AGENTS.md`
- Commit both the source edit and the regenerated outputs (CI detects drift automatically)

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for details.

## CLI quick reference

```bash
workato projects list --source remote   # list projects
workato projects use "<name>"           # switch project
workato pull                            # pull from remote
workato push                            # push to remote
workato push --restart-recipes          # push and restart any running recipes
workato push --delete                   # also delete remote assets that no longer exist locally
workato assets                          # list project assets (with IDs)
workato recipes start --id <id>         # start a recipe
workato jobs list --recipe-id <id>      # list jobs for a recipe
```

## License

MIT License. See [LICENSE](LICENSE).

> **Note**: this toolkit is not an official Workato product. Refer to the [Workato Terms of Service](https://www.workato.com/legal/terms-of-service) for the terms governing your use of Workato.
