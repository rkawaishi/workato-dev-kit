---
name: pull-project
description: Pull a project from the Workato remote. No argument pulls the current project; passing a name switches first and then pulls.
---

# /pull-project

Pull a project from the remote via the Workato Platform CLI.

## Usage

- `/pull-project` — pull the current project
- `/pull-project <project-name>` — switch to the specified project and pull
- `/pull-project --all` — pull every remote project
- `/pull-project --list` — show the list of remote projects

## Procedure

### 0. Pre-pull check (mandatory)

Pull silently overwrites uncommitted local changes. Check the workspace repository for uncommitted changes in the target project:

```bash
git status projects/<project-name>/
```

If there are uncommitted changes, suggest the user commits or stashes them before pulling. Pulling without asking can lose in-progress edits. For `--all`, repeat this check per project. If the workspace repository is not under git, skip this check.

### 0.5. Ensure `.workatoignore` (mandatory, before every pull)

`workato pull` silently overwrites and deletes local files. Before pulling a project, make sure its `.workatoignore` exists so local-only artifacts (`specs/`, `DESIGN.md`, custom connector source, …) survive. Run the kit helper once the project directory exists — for a brand-new project, after `workato init`:

```bash
bash scripts/ensure-workatoignore.sh "projects/<project-name>"
```

The helper creates `.workatoignore` from the base template (`templates/workatoignore.template`) when absent, or appends only the missing entries otherwise. It is idempotent and never removes or reorders existing lines.

The template ignores `*.custom_adapter.{rb,json}` by default: a connector pulled into the project would otherwise be re-pushed by a later `workato push` and could roll the connector back to an older version. If this project intentionally manages a connector as code, tell the user to delete those two lines from `.workatoignore` (keeping the `>>> opt-out <<<` marker comments) — the helper will then leave the opt-out alone.

### No argument / project name supplied
```bash
# When a name is supplied, switch first
workato projects use "<project-name>"
```
Then run **Step 0.5** for the project, and pull:
```bash
workato pull
```

### `--all`
1. Get the remote list: `workato projects list --source remote --output-mode json`
2. For each project:
   - Not present locally: `workato init --non-interactive --profile default --project-id <id> --folder-name "projects/<name>"`, then **run Step 0.5** for it.
   - Present locally: **run the git status check from Step 0**, then **Step 0.5** → `workato projects use "<name>" && workato pull`

### `--list`
```bash
workato projects list --source both
```

## Output

After pull completes, list the modified files. Report whether `.workatoignore` was created or topped up. If a new pattern emerged, suggest running `/learn-recipe`.
