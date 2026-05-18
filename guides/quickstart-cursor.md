# Quick Start Guide (Cursor)

This guide walks through setting up Workato Dev Kit with Cursor and creating your first Recipe.

## 1. Check prerequisites

You will need:

- **Workato account** — create one at [workato.com](https://www.workato.com/)
- **Workato API token** — issue one from Workato UI > Settings > API Tokens
- **Cursor** — install from [cursor.com](https://www.cursor.com/)
- **Python 3** — verify with `python3 --version` (required for the Platform CLI)

## 2. Set up the workspace

```bash
# Create your organization's workspace repository
mkdir my-org-workato && cd my-org-workato
git init

# Add workato-dev-kit as a submodule
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# Run the setup script (copies Cursor files, generates config)
bash kit/setup.sh

# Initial commit
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

Structure after setup:

```
my-org-workato/                 ← working root
├── .claude/                    ← symlinked from kit (you can add your own rules/skills)
├── .cursor/                    ← copied from kit (real files because symlinks are unreliable)
│   └── .kit-manifest           # tracks kit-managed files (gitignored)
├── docs/ → kit/docs/           ← symlink
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule (read-only)
├── projects/                   ← your organization's Recipes
└── connectors/                 ← your organization's custom connectors
```

## 3. Install the Workato Platform CLI

```bash
pipx install workato-platform-cli
```

> If you do not have `pipx`: `brew install pipx && pipx ensurepath`

> **Note**: Use the official CLI to pull/push projects. Features not covered by the CLI (job management, connector info retrieval, etc.) are filled in by the bundled API helper (`python3 scripts/workato-api.py`). See `.claude/rules/workato-cli.md` for details.

## 4. Initial CLI authentication

```bash
workato init
```

Enter the following interactively:
- **Profile name**: `default` (use `dev`, `prod`, etc. if you have multiple environments)
- **Data Center**: your data center (`us`, `eu`, `jp`, `sg`)
- **API Token**: the token issued in step 1

## 5. Updating the framework

```bash
git submodule update --remote kit
bash kit/setup.sh    # ← Re-running is required for Cursor (copies latest kit content into .cursor/)
git add kit .cursor && git commit -m "Update workato-dev-kit"
```

Files under `.cursor/` are real-file copies rather than symlinks, so **you must re-run `bash kit/setup.sh` whenever you update the kit**. Without re-running, Cursor will keep using the old rules and skills.

- When new skills or rules are added to the kit, copies are added
- Files removed from the kit are tracked via `.cursor/.kit-manifest` and pruned automatically
- Your own files added under `.cursor/rules/` or `.cursor/skills/` (those not in the manifest) are preserved

> **Why copy only for Cursor?** Cursor cannot reliably resolve symlinks for `.cursor/rules/*.mdc` or `.cursor/skills/<name>/`, and they fail to load silently. See [architecture.md](architecture.md#supported-editors) for details.

## 6. Pull a Workato project

```bash
# List available projects
workato projects list --source remote

# Pull a project
workato projects use "<project name>"
workato pull
```

> If you do not yet have a project, you can create one from scratch in the next step.

## 7. Launch Cursor

```bash
cd my-org-workato
cursor .
```

When Cursor starts, the following are loaded automatically:
- `.cursor/rules/` — format rules per file type (Recipe JSON, page JSON, connector, etc.)
- `.cursor/skills/` — development skills (Recipe generation, deployment, design, etc.)

## How to use skills

In Cursor's Agent mode, type `/` and select a skill by name to invoke it. The same `/skill-name` format as Claude Code.

| Skill | Purpose |
|---|---|
| `/spec` | Create feature requirements (spec.md), technology-neutral |
| `/clarify` | Resolve Open Questions in spec.md |
| `/plan` | spec.md → plan.md (Workato design) |
| `/tasks` | plan.md → tasks.md (tagged tasks) |
| `/analyze` | Consistency check across spec ↔ plan ↔ tasks (read-only) |
| `/implement` | Read tasks.md and dispatch to existing skills |
| `/create-recipe` | Generate Recipe JSON interactively |
| `/create-workflow-app` | Build a Workflow App |
| `/create-genie` | Generate a Genie / MCP server |
| `/create-connector` | Scaffold a custom connector |
| `/catalog` | Scan and catalog shared assets |
| `/validate-recipe` | Validate JSON structure |
| `/pull-project` | Pull a project from Workato |
| `/push-project` | Push a project (with validation) |
| `/learn-recipe` | Learn patterns from a Recipe |
| `/sync-connectors` | Collect and update connector info |
| `/design` | **Deprecated**: only `/design migrate` is for routine use (migrate legacy DESIGN.md to specs/). `/design` and `/design update` still work with a warning; `/design new` has been retired |

> **Tip**: Use this in Agent mode. Based on each skill's `description`, the agent may also pick a relevant skill for your task automatically.

## 8. Create your first project

### Option A: Start with the spec-driven workflow (recommended)

```
You: /spec "[App] Expense request"
```

The Agent will interview you on:
1. Who wants to do what (in business terms)
2. What flow you have in mind
3. Who is involved
4. What outcome counts as success
5. What existing tools or data sources are available

From the interview, `projects/<project>/specs/001-<slug>/spec.md` (requirements, WHAT/WHY) is generated, and any open points are recorded under `## Open Questions`. Then:

```
You: /clarify <project>/001-<slug>   # Resolve Open Questions
You: /plan <project>/001-<slug>      # Workato design (plan.md)
You: /tasks <project>/001-<slug>     # Execution tasks (tasks.md)
You: /analyze <project>/001-<slug>   # Consistency check across spec ↔ plan ↔ tasks
You: /implement <project>/001-<slug> # Dispatch to /create-recipe etc. for implementation
```

### Option B: Jump straight to building

```
You: /create-recipe
```

Or, if you need a Workflow App:

```
You: /create-workflow-app
```

## 9. Deploy

```
You: /push-project --start
```

The Agent will:
1. Validate JSON
2. Run `workato push`
3. Guide you through authentication for any new connections
4. Start the Recipes

## 10. Learning cycle

### Why the learning cycle matters

Workato Recipe JSON contains many structures that are not documented officially. For example:

- Connector-specific field names and schemas (the contents of `extended_output_schema`)
- Auto-generated `dynamicPickListSelection` and `toggleCfg` produced by UI configuration
- Connection-dependent fields (empty after push alone, only revealed once configured in the UI and pulled back)

These are **information you only discover by actually building a Recipe, iterating in the Workato UI, and then pulling**. `/learn-recipe` analyzes this information and feeds it back into the toolkit's knowledge base (`docs/`) and rules (`.cursor/rules/`). The more learning accumulates, the more accurately the next `/create-recipe` or `/create-workflow-app` will generate.

### How to do it

After adjusting a Recipe in the Workato UI, pull those changes back and grow the knowledge.

```
You: /pull-project
You: /learn-recipe
```

### Contributing back to the toolkit

If the patterns you learned would improve the toolkit, submit a PR to workato-dev-kit:

```bash
# In the kit/ directory
cd kit
git checkout -b feature/learn-jira-fields
# Commit changes to docs/ or .claude/rules/
git push origin feature/learn-jira-fields
# Open a PR on GitHub
```

## How rules work

`.cursor/rules/` contains rules that are applied automatically based on file type:

| Rule | Auto-applied to |
|---|---|
| `workato-recipe-format.mdc` | `**/*.recipe.json` |
| `workato-agentic-format.mdc` | `**/*.agentic_genie.json`, `**/*.agentic_skill.json`, etc. |
| `workato-page-components.mdc` | `**/*.lcap_page.json` |
| `workato-connector-sdk.mdc` | `connectors/**/*.rb` |
| `workato-project-structure.mdc` | `projects/**` |
| `workato-cli.mdc` | `.workatoenv`, `projects/**`, `connectors/**` |
| `workato-project.mdc` | Always applied (project-wide context) |

These rules and skills are pre-generated by the kit maintainer from `framework/claude/` via `python3 scripts/sync_agents.py`, and copied into the user's repository when `bash kit/setup.sh` runs (Cursor cannot reliably resolve symlinks). To update the kit:

```bash
git submodule update --remote kit
bash kit/setup.sh    # Copy new skills/rules, prune old ones
```

## Using git worktree

`git worktree add` does **not** populate submodules in a new worktree on its own —
left unhandled, the `kit/` submodule would start out empty there. The `docs/` and
`guides/` symlinks would point at nothing, and although `.cursor/` holds real file
copies, its rules reference `@docs/...`, so the framework would be effectively
broken in that worktree.

To prevent this, `bash kit/setup.sh` installs a git `post-checkout` hook that runs
`git submodule update --init --recursive` automatically. So creating a worktree
fills in `kit/` for you — just re-run setup to refresh the symlinks and re-copy
`.cursor/`:

```bash
git worktree add ../my-org-workato-feature feature-branch   # hook populates kit/
cd ../my-org-workato-feature
bash kit/setup.sh                                            # refresh symlinks + re-copy .cursor/
```

If the hook is not active — you had a pre-existing `post-checkout` hook, or
`core.hooksPath` is set (husky etc.) — `setup.sh` prints a `SKIP` notice. In that
case populate the submodule manually first:

```bash
cd ../my-org-workato-feature
git submodule update --init --recursive
bash kit/setup.sh
```

`bash kit/setup.sh` re-copies `.cursor/` from the now-populated kit and verifies
the symlinks at the end, printing a `DANGLING` warning if the submodule is still
missing.

> **Note on shared submodule state**: all worktrees share one `.git/modules/kit`,
> and its `core.worktree` can only point at one worktree at a time. `git status` /
> `git submodule status` for `kit/` may therefore look noisy across worktrees.
> This is harmless because the kit is consumed read-only — just don't stage a
> `kit` pointer change unless you intentionally bumped the kit version
> (`git submodule update --remote kit`).

## FAQ

### Q: What is a Workato project?

It is the unit that groups Recipes and Connections in the Workato UI. `workato pull` downloads them as local JSON files, and `workato push` uploads them.

### Q: How do I git-manage the projects/ folder?

It lives directly inside the workspace repository. Manage it normally with `git add projects/<name> && git commit`.

### Q: Do spec.md / plan.md / tasks.md get wiped by workato pull?

No, as long as each project's `.workatoignore` lists `specs/`. The `/spec` command sets this up automatically on first run.

> Projects still using the legacy `DESIGN.md` can be converted to `specs/` via `/design migrate <project>`. `/design new` has been retired.

### Q: Can I use this with Claude Code?

Yes. The same rules and skills are placed under `.claude/rules/` and `.claude/skills/`. Invocation uses the same `/skill-name` format. See [QUICKSTART-CLAUDE-CODE.md](quickstart-claude-code.md) for details.

### Q: How do I keep rules and skills up to date?

The source of truth is `framework/claude/` in the kit, and Cursor files are pre-generated by the kit maintainer via `python3 scripts/sync_agents.py`. Users simply update the kit submodule and re-run setup.sh:

```bash
git submodule update --remote kit
bash kit/setup.sh
```

### Q: Can I use it offline?

Reading documentation and generating Recipe JSON works offline. `workato push/pull` requires a connection to the Workato API.

## Next steps

- [README.md](../README.md) — full skill list, directory layout, CLI reference
- [Deployment guide](../docs/patterns/deployment-guide.md) — UI steps after push, common errors
- [Connector list](../docs/connectors/_index.md) — check supported connectors
