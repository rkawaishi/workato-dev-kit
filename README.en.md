# Workato Dev Kit

English | [日本語](README.md)

A toolkit for building Workato (enterprise iPaaS) automations with AI coding agents.
Supports [Claude Code](https://claude.com/claude-code), [Cursor](https://cursor.com), [Codex CLI](https://github.com/openai/codex), and [Gemini CLI](https://github.com/google-gemini/gemini-cli).

Covers recipe development, Workflow App construction, AI agent (Genie / MCP) authoring, and custom connector development.

## Features

- **Recipe JSON generation** — Build Workato recipes interactively and deploy with `workato push`
- **Workflow Apps** — Define Data Tables, pages, and approval flows in JSON
- **MCP servers** — Expose tools for AI agents over the MCP protocol
- **Genies (AI agents)** — Generate Genie configurations with attached skills
- **Custom connectors** — Connector SDK (Ruby DSL) authoring support
- **Knowledge base** — Docs for 316 connectors, 7 logic patterns, 13 platform features
- **Learning loop** — pull → analyze → accumulate patterns → improve future generation
- **Design docs** — `DESIGN.md` per project for cross-session planning and progress tracking

## Prerequisites

- A [Workato](https://www.workato.com/) account + API token
- [Workato Platform CLI](https://github.com/workato-devs/workato-platform-cli) (`pipx install workato-platform-cli`)
- One of the supported editors — [Claude Code](https://claude.com/claude-code) / [Cursor](https://cursor.com) / [Codex CLI](https://github.com/openai/codex) / [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## Setup

> See **[Quick Start (Claude Code)](guides/quickstart-claude-code.md)** or **[Quick Start (Cursor)](guides/quickstart-cursor.md)** for detailed walkthroughs (Japanese).

Add `workato-dev-kit` to your organization's workspace repository as a submodule. Framework updates can then be pulled in with `git submodule update`.

```bash
# Create your workspace repo
mkdir my-org-workato && cd my-org-workato
git init

# Add workato-dev-kit as a submodule under kit/
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# Run the setup script (creates symlinks, generates settings)
bash kit/setup.sh

# Initialize the Platform CLI
workato init

# First commit
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

Resulting layout:

```
my-org-workato/                 ← your workspace (working root)
├── .claude/                    ← Claude Code
│   ├── CLAUDE.md               # generated (customizable)
│   ├── rules/                  # symlinks to kit + your own rules
│   ├── skills/                 # symlinks to kit + your own skills
│   ├── hooks/                  # symlinks to kit
│   └── settings.json           # generated (customizable)
├── .cursor/                    ← Cursor (symlinks)
│   ├── rules/, skills/, hooks.json
├── .agents/skills/             ← Codex CLI (symlinks)
├── .gemini/skills/             ← Gemini CLI (symlinks)
├── AGENTS.md → kit/...         ← agent-neutral spec (Codex / Aider / etc.)
├── GEMINI.md → kit/...         ← same target as AGENTS.md
├── docs/ → kit/docs/           ← knowledge base (symlink)
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule (read-only)
├── projects/                   ← your recipes
└── connectors/                 ← your custom connectors
```

**Updating the framework:**

```bash
git submodule update --remote kit
bash kit/setup.sh    # add new symlinks, prune removed ones
git add kit && git commit -m "Update workato-dev-kit"
```

**Adding your own skills/rules:** drop regular files into `.claude/rules/` or `.claude/skills/`. They coexist with kit-managed symlinks — `setup.sh` never overwrites real (non-symlink) files.

## Workspace structure

Your recipes and connectors live under `projects/` and `connectors/`.

### Recipe projects (`projects/`)

```bash
# Pull a project from Workato
workato projects use "<project-name>"
workato pull

# Develop and commit
git add projects/<project-name> && git commit -m "Add IT Onboarding workflow"
```

### Design docs (`DESIGN.md`)

Each project gets a `DESIGN.md` to capture design, progress, and decisions.
Add it to `.workatoignore` so `workato pull` doesn't blow it away.

```bash
/design new "[App] IT Onboarding"   # create
/design "[App] IT Onboarding"       # view
/design update                      # auto-update implementation status
```

## Skills

| Skill | Purpose |
|---|---|
| `/create-recipe` | Generate recipe JSON interactively |
| `/create-workflow-app` | Build a Workflow App in stages (Data Tables, pages, recipes) |
| `/create-genie` | Generate Genie / MCP server + skill configs |
| `/create-connector` | Scaffold a custom connector |
| `/catalog` | Scan and catalog shared assets |
| `/validate-recipe` | Validate recipe JSON structure |
| `/pull-project` | Pull a project from Workato |
| `/push-project` | Push local changes (validates, optionally starts recipes) |
| `/learn-recipe` | Learn field info from a pulled recipe |
| `/learn-pattern` | Record/update recipe construction patterns in the catalog |
| `/sync-connectors` | Refresh connector docs (Pre-built via API, custom via `connector.rb` parse) |
| `/auto-learn` | Autonomously harvest all ops of one connector via Claude in Chrome |
| `/design` | Create / update / view project design docs |

See [skills reference](guides/skills-reference.md) and [lifecycle & responsibility map](guides/lifecycle.md) for detail (Japanese).

### Per-editor invocation

| Editor | Skill location | Invocation |
|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `/skill-name` |
| Cursor | `.cursor/skills/<name>/` | `/skill-name` |
| Codex CLI | `.agents/skills/<name>/` | `$skill-name` (slash syntax rewritten to `$`) |
| Gemini CLI | `.gemini/skills/<name>/` | `/skill-name` |

The agent-neutral spec (a consolidation of `CLAUDE.md` + the `rules/` directory) is shipped as `AGENTS.md` / `GEMINI.md` (same file, two names).

## Development flow

### New project

```
/design new "<project-name>"     ← create design doc
/create-workflow-app             ← build a Workflow App (or a single recipe)
/push-project --start            ← push and start recipes
   verify in the Workato UI
/pull-project → /learn-recipe    ← learning loop
/design update                   ← refresh implementation status
```

### Learning loop

```
workato pull → /learn-recipe → update docs/ → next generation is more accurate
             → /learn-pattern → update pattern catalog → PR back to workato-dev-kit
```

## Repository layout

This is the layout of `workato-dev-kit` itself. Organizations consume it as `kit/` via git submodule.

`framework/claude/` is the canonical source. The Cursor / Codex / Gemini variants are auto-generated by `scripts/sync_agents.py`. The repo's own `.claude/` only contains kit-development settings — it deliberately does NOT ship Workato user-facing skills, so opening this repo in Claude Code won't surface `/create-recipe` etc. by accident.

```
workato-dev-kit/                 ← this repo (added as kit/ submodule downstream)
├── .claude/                     # for kit dev itself (no Workato user skills)
├── framework/                   # the distribution (symlinked into user editors)
│   ├── claude/                  # canonical source
│   │   ├── CLAUDE.md            #   user-facing spec (Workato dev rules)
│   │   ├── rules/               #   8 rules (recipe format, etc.)
│   │   ├── skills/              #   13 skills
│   │   ├── hooks/               #   automation hooks
│   │   └── settings.json        #   user settings template
│   ├── cursor/                  # generated: rules/*.mdc + skills/ + hooks.json (handwritten)
│   ├── codex/skills/            # generated (slash syntax rewritten to $)
│   ├── gemini/skills/           # generated
│   └── AGENTS.md                # generated: CLAUDE.md + rules consolidated. GEMINI.md is the same file
├── docs/                        # knowledge base
│   ├── connectors/              #   316 connectors
│   ├── connector-sdk/           #   Connector SDK reference
│   ├── logic/                   #   7 logic patterns
│   ├── platform/                #   13 platform features
│   └── patterns/                #   deployment, shared assets, recipe patterns
├── guides/                      # user guides
├── scripts/
│   ├── sync_agents.py           #   framework/claude/ → cursor/codex/gemini/ + AGENTS.md
│   ├── sync-cursor-rules.sh     #   backwards-compat wrapper
│   └── workato-api.py
├── templates/                   # workspace templates (.gitignore, etc.)
└── setup.sh                     # workspace setup script (idempotent)
```

### Editing the distribution

- Edit skills and rules under `framework/claude/`
- After editing, **always** run `python3 scripts/sync_agents.py` to regenerate `framework/{cursor,codex,gemini}/` and `AGENTS.md`
- Commit both the source edits and the regenerated artifacts (CI checks for drift)

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for full kit-development guidelines (Japanese).

## CLI quick reference

```bash
workato projects list --source remote   # list projects
workato projects use "<name>"           # switch project
workato pull                            # pull from remote
workato push                            # push to remote
workato push --restart-recipes          # push and restart running recipes
workato push --delete                   # also delete remote assets that no longer exist locally
workato assets                          # list project assets (with IDs)
workato recipes start --id <id>         # start a recipe
workato jobs list --recipe-id <id>      # list jobs
```

## License

MIT License. See [LICENSE](LICENSE).

> **Note:** This toolkit is not an official Workato product. Your use of Workato is governed by the [Workato Terms of Service](https://www.workato.com/legal/terms-of-service).
