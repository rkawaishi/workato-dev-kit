# Quick Start Guide (Claude Code)

This guide walks through setting up Workato Dev Kit with Claude Code and creating your first Recipe.

## 1. Check prerequisites

You will need:

- **Workato account** — create one at [workato.com](https://www.workato.com/)
- **Workato API token** — issue one from Workato UI > Settings > API Tokens
- **Claude Code** — install from [claude.com/claude-code](https://claude.com/claude-code)
- **Python 3** — verify with `python3 --version` (required for the Platform CLI)

## 2. Set up the workspace

```bash
# Create your organization's workspace repository
mkdir my-org-workato && cd my-org-workato
git init

# Add workato-dev-kit as a submodule
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# Run the setup script
bash kit/setup.sh

# Initial commit
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

Structure after setup:

```
my-org-workato/                 ← working root
├── .claude/                    ← symlinked from kit (you can add your own rules/skills)
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

## 5. Updating the framework (when using submodule)

```bash
git submodule update --remote kit
bash kit/setup.sh
git add kit && git commit -m "Update workato-dev-kit"
```

When new skills or rules are added, `setup.sh` automatically creates the symlinks.
Files you added yourself (those that are not symlinks) are not overwritten.

## 6. Pull a Workato project

```bash
# List available projects
workato projects list --source remote

# Pull a project
workato projects use "<project name>"
workato pull
```

> If you do not yet have a project, you can create one from scratch in the next step.

## 7. Launch Claude Code

```bash
cd my-org-workato
claude
```

When Claude Code starts, the skills and rules under `.claude/` are loaded automatically.

## 8. Create your first project

### Option A: Start with the spec-driven workflow (recommended)

```
You: /spec "[App] Expense request"
```

Claude will interview you on:
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

Claude will:
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

These are **information you only discover by actually building a Recipe, iterating in the Workato UI, and then pulling**. `/learn-recipe` analyzes this information and feeds it back into the toolkit's knowledge base (`docs/`) and rules (`.claude/rules/`). The more learning accumulates, the more accurately the next `/create-recipe` or `/create-workflow-app` will generate.

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

## FAQ

### Q: What is a Workato project?

It is the unit that groups Recipes and Connections in the Workato UI. `workato pull` downloads them as local JSON files, and `workato push` uploads them.

### Q: How do I git-manage the projects/ folder?

It lives directly inside the workspace repository. Manage it normally with `git add projects/<name> && git commit`.

### Q: Do spec.md / plan.md / tasks.md get wiped by workato pull?

No, as long as each project's `.workatoignore` lists `specs/`. The `/spec` command sets this up automatically on first run.

> Projects still using the legacy `DESIGN.md` can be converted to `specs/` via `/design migrate <project>`. `/design new` has been retired.

### Q: Can I use this with Cursor?

Yes. The same rules and skill-equivalent rules are placed under `.cursor/rules/` as well. See [QUICKSTART-CURSOR.md](quickstart-cursor.md) for details.

### Q: Can I use it offline?

Reading documentation and generating Recipe JSON works offline. `workato push/pull` requires a connection to the Workato API.

## Next steps

- [README.md](../README.md) — full skill list, directory layout, CLI reference
- [Deployment guide](../docs/patterns/deployment-guide.md) — UI steps after push, common errors
- [Connector list](../docs/connectors/_index.md) — check supported connectors
