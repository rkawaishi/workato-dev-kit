# Lifecycle and responsibility map

A consolidated reference for **when, by whom, and for what purpose** each skill is invoked, and each docs file is read or written.

The "knowledge lookup priority" in `@.claude/CLAUDE.md` defines the **reading order**, while this document presents the bigger picture including **write timing and responsibilities**. Use it as a map for "remembering the skill you should actually run before falling back to grep."

## Overall flow

The loop is short on purpose: describe the automation, generate it, let the linter reject what the connector cannot actually do, push, then feed what you learned back into the docs so the next generation starts sharper.

```
[Preparation]     /catalog                → Survey existing reusable assets
                  /sync-connectors        → Fetch metadata for connectors to be used
                     ↓
[Build]           /create-recipe          → Generate a recipe from a short interview
                  /create-workflow-app    → Generate a full Workflow App
                  /create-genie           → Generate Genie / MCP
                  /create-connector       → Generate a custom connector
                     ↓
[Validation]      wk lint --skills-path kit/skills
                                          → Reject hallucinated actions, datapill and
                                            control-flow errors (deterministic)
                  /validate-recipe        → Check the asset types wk lint does not cover
                                            (Genie, Workflow App, connection files)
                     ↓
[Sync]            /push-project                  → Push to the Workato remote (with validation)
                  (Adjust pick_list etc. in the UI)
                  /pull-project                  → Pull adjustments back locally
                     ↓
[Learning]        /learn-recipe           → Enrich org/docs/ from the adjusted recipe
                  /learn-pattern          → Record a reusable construction pattern in
                                            org/docs/patterns/recipe-patterns/
                     ↓
[Cleanup]         /catalog                → Reflect newly shared assets in the catalog
                  /sync-connectors        → Regenerate kit/skills/ so the linter knows
                                            what you just learned
```

> **The learning phase is what makes the loop worth running.** `/learn-recipe` and `/sync-connectors` are the only steps that make the *next* recipe easier to generate. Skipping them turns this into a plain code generator.

## Skill responsibility map

A list of "when each skill is invoked, what it reads, and what it writes."

### Preparation phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/catalog` | At session start (reuse check) | `projects/CATALOG.md` | None |
| `/catalog scan` | After shared assets are added or changed | All projects under `projects/`, `projects/CATALOG_CONFIG.yaml` | `projects/CATALOG.md` |
| `/sync-connectors <provider>` | Immediately before using an unknown connector | Workato API | `docs/connectors/<provider>.md`, then `kit/skills/<provider>-recipes/` via `scripts/gen_lint_rules.py` |
| `/sync-connectors --custom <name>` | After custom connector development | `connectors/<name>/connector.rb` | `connectors/docs/<name>.md` |

### Build phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/create-recipe <project>` | When you need a new recipe | `docs/connectors/<provider>.md`, `connectors/docs/<name>.md`, `docs/logic/`, `docs/patterns/recipe-patterns/`, `org/docs/patterns/recipe-patterns/`, `projects/docs/patterns/` (legacy), `projects/CATALOG.md`, `.claude/rules/workato-recipe-format.md` | `projects/<name>/Recipes/*.recipe.json`, `*.connection.json` |
| `/create-workflow-app` | When you need Data Tables + pages + the recipes behind them | `docs/platform/workflow-apps.md`, `docs/patterns/deployment-guide.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Data Tables/*.data_table.json`, `Pages/*.page.json`, `lcap_app.json`, `Recipes/*.recipe.json` |
| `/create-genie` | When creating a new AI agent / MCP server | `docs/platform/agent-studio.md`, `docs/platform/mcp.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Agents/*.agentic_genie.json`, `*.agentic_skill.json`, `*.mcp_server.json` |
| `/create-connector <api-name>` | When no pre-built or universal connector fits. Connectors are shared assets and are not tied to a project | `docs/connector-sdk/connector-rb.md`, `docs/connector-sdk/overview.md`, `.claude/rules/workato-connector-sdk.md`, API documentation (WebFetch) | `connectors/<name>/connector.rb`, `settings.yaml`, `Gemfile` |

### Validation and sync phases

| Step | When to invoke | Reads | Writes |
|---|---|---|---|
| `wk lint <file> --skills-path kit/skills` | Before every push, and after any hand edit to a recipe | `*.recipe.json`, `kit/skills/*/lint-rules.json` | None (diagnostics only) |
| `/validate-recipe` | Before push, for Genie / Workflow App / connection files | The project's JSON files, `.claude/rules/` | None (validation report only) |
| `/push-project` | Before deploy | The project's assets | Workato remote (does not modify local) |
| `/pull-project` | After UI adjustments, at handover time | Workato remote | Assets under `projects/<name>/` (overwritten) |

### Learning phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/learn-recipe` | Immediately after `/pull-project`, or after implementing previously undocumented actions | `projects/<name>/Recipes/*.recipe.json`, and the kit canonical `docs/<...>` as a cross-reference | `org/docs/connectors/<provider>.md` (input/output/snippet additions), `org/docs/logic/data-pills.md`, `org/docs/patterns/deployment-guide.md`, `org/docs/learned-patterns.md` |
| `/learn-pattern` | When you notice a reusable construction pattern | Reference recipes (optional), existing `docs/patterns/recipe-patterns/` (kit) + `org/docs/patterns/recipe-patterns/` (org) + `projects/docs/patterns/` (legacy, if present) | `org/docs/patterns/recipe-patterns/<name>.md` (single write target; distinguish generic vs. org-domain in the pattern body) |
| `/auto-learn <provider>` | When a connector's input/output fields are still unknown after `/sync-connectors` | The Workato UI, via Claude in Chrome | `docs/connectors/<provider>.md` `## Field details` |

## docs responsibility map

A list of "who writes and who reads" for each docs directory.

### Framework side (`workato-dev-kit` repo)

The kit canonical `docs/` is **written only by kit maintainers and the sync skills**; user learning results accumulate on the `org/docs/` side (see `@.claude/rules/org-knowledge-overlay.md`).

| Path | Writer | Reader | Contents |
|---|---|---|---|
| `docs/connectors/<provider>.md` | `/sync-connectors`, `/auto-learn` | `/create-recipe`, `/create-workflow-app`, `/create-genie`, `scripts/gen_lint_rules.py` | Pre-built connector trigger/action/field specs (kit canonical) |
| `skills/<provider>-recipes/` | `scripts/gen_lint_rules.py` (generated — never hand-edit) | `wk lint --skills-path` | Connector allow-lists and agent-facing knowledge, derived from `docs/connectors/` |
| `docs/connector-sdk/` | Manual | `/create-connector` | Connector SDK reference |
| `docs/logic/` | Manual | `/create-recipe`, `/create-workflow-app` | datapill syntax, formulas, loops, error handling, triggers |
| `docs/platform/` | Manual | `/create-workflow-app`, `/create-genie` | Data Table, Lookup Table, Agent Studio, MCP, Workflow App |
| `docs/patterns/recipe-patterns/` | Manual (kit maintainers) | `/create-recipe`, `/learn-pattern` (cross-reference at load time) | Recipe construction patterns (kit canonical, read-only) |
| `docs/patterns/deployment-guide.md` | Manual | `/push-project`, `/create-workflow-app` | Deployment procedures, common errors |
| `docs/patterns/shared-assets.md` | Manual | `/create-recipe`, `/catalog` | Shared asset design policy |
| `docs/patterns/workspace-management.md` | Manual | `/catalog` | Workspace structure and naming conventions |
| `.claude/rules/` | Manual | All skills | JSON format, per-path rules |
| `docs/learned-patterns.md` | Manual (kit maintainers' temporary buffer) | Manual (triage work) | Kit canonical buffer. Users use `org/docs/learned-patterns.md` |

### Organization side (`connectors/`, `projects/`, `org/`)

| Path | Writer | Reader | Contents |
|---|---|---|---|
| `connectors/docs/<name>.md` | `/sync-connectors --custom` | `/create-recipe`, `/create-workflow-app` | Custom connector trigger/action/field specs |
| `connectors/<name>/connector.rb` | `/create-connector`, manual | `/sync-connectors --custom` | Custom connector implementation |
| `projects/<name>/Recipes/*.json` | `/create-recipe`, `/pull-project` | `/learn-recipe`, `wk lint`, `/push-project` | Recipe body |
| `projects/CATALOG.md` | `/catalog scan` | `/create-recipe` | List of organization shared assets (Recipe Function, Connection) |
| `projects/CATALOG_CONFIG.yaml` | Manual | `/catalog` | Scope settings (global / team / private) |
| `projects/docs/patterns/` | Legacy (no writer; record new entries in `org/docs/patterns/recipe-patterns/`) | `/create-recipe`, `/learn-pattern` (read only) | Org-domain patterns recorded in older versions (backward compatibility) |
| `org/docs/connectors/<provider>.md` | `/learn-recipe` | `/create-recipe`, `/create-workflow-app`, `/create-genie` | Corrections / additions to the kit version, org-specific field information, and any `## Unlearned` entries still open |
| `org/docs/logic/`, `org/docs/platform/`, `org/docs/patterns/deployment-guide.md` | `/learn-recipe` | All create-family skills | Corrections / additions to the kit version |
| `org/docs/patterns/recipe-patterns/` | `/learn-pattern` | `/create-recipe` | Recipe construction patterns recorded by the organization (both generic and org-domain consolidated here) |
| `org/docs/learned-patterns.md` | `/learn-recipe` (fallback when the destination is undecided) | Manual (triage work) | Org-side temporary buffer |

## Lifecycle principles

### 1. docs-first

Build skills (`/create-recipe`, etc.) must **read the docs first**.

- If the information is in the documentation, implement directly from it
- If the information is missing:
  1. Implement as a best-effort implementation (including UI verification)
  2. Record it under `## Unlearned` in `org/docs/connectors/<provider>.md` (or as a GitHub Issue in this repo), and say so in the session
  3. After implementation, run `/learn-recipe` to enrich the docs and clear the entry
  4. Manually review anything that remains

### 2. Do not grep other projects

Do not grep under `projects/<other-project>/Recipes/` to dig out sample JSON.
Logic, naming, and datapill references that are specific to individual projects leak in as noise, and gaps in the knowledge base stop being visible.

**Exception**: pattern learning is fine (`/learn-pattern` references `docs/patterns/recipe-patterns/`, `org/docs/patterns/recipe-patterns/`, and `projects/docs/patterns/` (legacy)). However, grepping to obtain input/output schemas is not allowed.

### 3. Separation of learning responsibilities

| Learning content | Skill to use | Write target |
|---|---|---|
| Connector action/trigger names (from the official API) | `/sync-connectors` | `docs/connectors/` (kit canonical) → regenerates `skills/` |
| Connector input/output fields (the API does not expose these) | `/auto-learn` | `docs/connectors/<provider>.md` `## Field details` |
| Custom connector specs | `/sync-connectors --custom` | `connectors/docs/` |
| Connector field specs (from a recipe the org has used) | `/learn-recipe` | `org/docs/connectors/` |
| Reusable construction patterns | `/learn-pattern` | `org/docs/patterns/recipe-patterns/` (both generic and org-domain consolidated here) |
| New findings about JSON structure | `/learn-recipe` | `org/docs/learned-patterns.md` (use this for findings you may later upstream to the kit) |
| datapill reference patterns | `/learn-recipe` | `org/docs/logic/data-pills.md` |

**Key point**: learning skills do not create intermediate files; they append directly to the relevant document. Only `org/docs/learned-patterns.md` is tolerated as a staging area, and even that should be triaged promptly. Learning skills do not write into the kit canonical `docs/` (only kit maintainers and the sync skills do).

### 4. Build skills do not write docs

Build skills like `/create-recipe` only generate assets under `projects/`; they do not write to `docs/connectors/` or `docs/patterns/`.
Knowledge writes are the responsibility of the **learning skills** (`/learn-recipe`, `/learn-pattern`, `/sync-connectors`, `/auto-learn`). This separation prevents incorrect information from leaking into the docs as a side effect of building.

### 5. The linter is the gate, not your judgement

`wk lint` is deterministic and knows every valid action name for 300+ connectors. Never talk yourself past one of its errors — an `ACTION_NAME_VALID` failure means the operation does not exist on that connector, no matter how plausible the name looks. If you believe the linter is wrong, the fix is `/sync-connectors <provider>` (the allow-list is stale), not `--skip-lint`.

## Typical scenarios

### Scenario A: New project (using a connector for the first time)

```
/catalog                              # Check what already exists and can be reused
/sync-connectors <provider>           # Fetch metadata + regenerate the lint allow-list
/create-recipe <project>              # Interview → generate
wk lint projects/<project>/Recipes/*.recipe.json --skills-path kit/skills
/push-project --start                 # Deploy + start
(Adjust pick_list etc. in the UI)
/pull-project                         # Pull adjustments
/learn-recipe <project>               # Enrich org/docs/ from what the UI corrected
```

### Scenario B: New feature with a known connector

```
/create-recipe <project>
wk lint projects/<project>/Recipes/*.recipe.json --skills-path kit/skills
/push-project --start
```

If connector information is already in place, `/sync-connectors` and `/learn-recipe` are not needed.

### Scenario C: Building a custom connector

```
/create-connector <api-name>          # Scaffold connector.rb from the API docs
(Implement and test with the Workato SDK)
/sync-connectors --custom <name>      # Update connectors/docs/<name>.md
/create-recipe <project>              # Now build recipes against it
```

### Scenario D: Handover (understanding an existing project)

```
/pull-project --all                   # Pull all projects locally
ls projects/<project>/Recipes/        # See what the project actually runs
/learn-recipe <project>               # Enrich docs from the implementation
/catalog scan                         # Inventory shared assets
```

## When you are about to move outside this map

- "Let me grep `projects/<other-project>/Recipes/` to investigate input/output" → **stop**. Read `docs/connectors/<provider>.md`, or run `/sync-connectors` if it does not exist
- "Let me append to `docs/connectors/` while building" → **stop**. Build skills do not write docs. Leave it to `/learn-recipe`
- "`wk lint` says the action name is invalid but I'm sure it exists" → **stop**. Run `/sync-connectors <provider>` and regenerate the allow-list. If the name really is missing from the Workato API, that is a finding worth recording — do not bypass the linter
- "Push now, lint later" → **stop**. `wk push` runs the linter as a pre-push gate for a reason; a recipe that fails lint will usually fail in the Workato UI too, just more expensively
- "It's a new connector but let me just try implementing it" → OK, but record it under `## Unlearned` in `org/docs/connectors/<provider>.md` and run `/learn-recipe` afterward
