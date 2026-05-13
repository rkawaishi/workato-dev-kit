---
name: pull-project
description: Pull a project from the Workato remote. No argument pulls the current project; passing a name switches first and then pulls.
---

# $pull-project

Pull a project from the remote via the Workato Platform CLI.

## Usage

- `$pull-project` — pull the current project
- `$pull-project <project-name>` — switch to the specified project and pull
- `$pull-project --all` — pull every remote project
- `$pull-project --list` — show the list of remote projects

## Procedure

### 0. Pre-pull check (mandatory)

Pull silently overwrites uncommitted local changes. Check the workspace repository for uncommitted changes in the target project:

```bash
git status projects/<project-name>/
```

If there are uncommitted changes, suggest the user commits or stashes them before pulling. Pulling without asking can lose in-progress edits. For `--all`, repeat this check per project. If the workspace repository is not under git, skip this check.

### No argument / project name supplied
```bash
# When a name is supplied, switch first
workato projects use "<project-name>"
# Pull
workato pull
```

### `--all`
1. Get the remote list: `workato projects list --source remote --output-mode json`
2. For each project:
   - Not present locally: `workato init --non-interactive --profile default --project-id <id> --folder-name "projects/<name>"`
   - Present locally: **run the git status check from Step 0** → `workato projects use "<name>" && workato pull`

### `--list`
```bash
workato projects list --source both
```

## Output

After pull completes, list the modified files. If a new pattern emerged, suggest running `$learn-recipe`.
