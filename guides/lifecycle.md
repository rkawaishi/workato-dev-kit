# Lifecycle and responsibility map

A consolidated reference for **when, by whom, and for what purpose** each skill is invoked, and each docs file is read or written.

The "knowledge lookup priority" in `@.claude/CLAUDE.md` defines the **reading order**, while this document presents the bigger picture including **write timing and responsibilities**. Use it as a map for "remembering the skill you should actually run before falling back to grep."

## Overall flow

Proceed in the order `/spec` → `/implement` along the spec-driven workflow.

```
[Specification]   /spec                   → Write user experience and requirements in spec.md (technology-neutral)
                  /clarify                → Resolve Open Questions and reflect them in spec.md
                     ↓
[Design]          /plan                   → Write Workato configuration in plan.md (HOW)
                  /tasks                  → Decompose into executable tasks in tasks.md ([P]/[recipe]/[learn] tags)
                  /analyze                → Verify spec ↔ plan ↔ tasks consistency (read-only)
                     ↓
[Preparation]     /catalog                → Survey existing reusable assets (skip if already referenced in plan)
                  /sync-connectors        → Fetch metadata for connectors to be used
                     ↓
[Build]           /implement              → Read tasks.md and dispatch to the skills below
                  /create-recipe          → Read plan.md and generate a recipe
                  /create-workflow-app    → Read plan.md and generate a full Workflow App
                  /create-genie           → Generate Genie / MCP
                  /create-connector       → Generate a custom connector
                     ↓
[Validation]      /validate-recipe        → Validate JSON structure
                     ↓
[Sync]            /push-project                  → Push to the Workato remote (with validation)
                  (Adjust pick_list etc. in the UI)
                  /pull-project                  → Pull adjustments back locally
                     ↓
[Learning]        /learn-recipe           → Enrich org/docs/ from the adjusted recipe
                                            and tidy plan.md.Unlearned and tasks.md.[learn]
                  /learn-pattern          → Record a reusable construction pattern in org/docs/patterns/recipe-patterns/
                     ↓
[Cleanup]         /catalog                → Reflect newly shared assets in the catalog
                  /tasks --update         → Regenerate remaining tasks (optional)
```

> **`/design` is deprecated**: existing projects written in the legacy `DESIGN.md` format are converted to `specs/` via `/design migrate` and then join this flow. New projects do not use the `/design` family. `/design new` has been retired (if invoked, refuse and direct the user to `/spec`); `/design` (view) and `/design update` operate only in a compatibility mode with a warning.

## Skill responsibility map

A list of "when each skill is invoked, what it reads, and what it writes."

### Specification phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/spec <project>` | At project / feature start | (interview) | `projects/<name>/specs/<NNN>-<slug>/spec.md` (new) |
| `/clarify <project>/<NNN>-<slug>` | When Open Questions remain in spec.md, or when resuming after an interruption | `spec.md` (`## Open Questions`) | `spec.md` (body + Open Questions checked off) |

### Design phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/plan <project>/<NNN>-<slug>` | After Open Questions are resolved | `spec.md`, `projects/CATALOG.md`, `.resource-providers.yml`, `docs/patterns/recipe-patterns/`, `org/docs/patterns/recipe-patterns/`, `projects/docs/patterns/` (legacy) | `plan.md` (new) |
| `/tasks <project>/<NNN>-<slug>` | After plan.md is finalized | `plan.md` | `tasks.md` (new, with `[P]` / `[recipe]` etc. tags) |
| `/analyze <project>/<NNN>-<slug>` | Consistency check before `/implement` | `spec.md`, `plan.md`, `tasks.md` | None (read-only report) |

### Deprecation phase (existing projects only)

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/design migrate <project>` | When converting a project that only has the legacy DESIGN.md into the spec-driven format (**standard operation**) | `projects/<name>/DESIGN.md` | `projects/<name>/specs/<NNN>-<slug>/{spec,plan,tasks}.md`, `DESIGN.md` → `DESIGN.md.legacy.<date>` |
| `/design`, `/design update` | View / update legacy DESIGN.md (**compatibility mode only, with a warning**; switch to `/design migrate` early) | `projects/<name>/DESIGN.md` | `projects/<name>/DESIGN.md` |
| ~~`/design new`~~ | **Retired**. If invoked, refuse and direct the user to `/spec` | — | — |

> **Do not use the `/design` family for new projects**. Start from `/spec`. For legacy DESIGN.md, migrate to `specs/` early via `/design migrate`.

### Preparation phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/catalog` | At session start (reuse check) | `projects/CATALOG.md` | None |
| `/catalog scan` | After shared assets are added or changed | All projects under `projects/`, `projects/CATALOG_CONFIG.yaml` | `projects/CATALOG.md` |
| `/sync-connectors <provider>` | Immediately before using an unknown connector | Workato API | `docs/connectors/<provider>.md` |
| `/sync-connectors --custom <name>` | After custom connector development | `connectors/<name>/connector.rb` | `connectors/docs/<name>.md` |

### Build phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/implement <project>/<NNN>-<slug>` | After tasks.md is finalized | `tasks.md`, `plan.md`, `spec.md` (reference only) | `tasks.md` (check-off and FAILED marks) |
| `/create-recipe <project>/<NNN>-<slug>` | Invoked from `/implement` via [recipe]/[function]/[handler] tasks | `plan.md`, `docs/connectors/<provider>.md`, `connectors/docs/<name>.md`, `docs/logic/`, `docs/patterns/recipe-patterns/`, `org/docs/patterns/recipe-patterns/`, `projects/docs/patterns/` (legacy), `projects/CATALOG.md`, `.claude/rules/workato-recipe-format.md` | `projects/<name>/Recipes/*.recipe.json`, `*.connection.json`; if needed, append to plan.md's Unlearned Actions and tasks.md's `[learn]` tasks |
| `/create-workflow-app <project>/<NNN>-<slug>` | Invoked from `/implement` via [page]/[data-table] tasks | `plan.md`, `docs/platform/workflow-apps.md`, `docs/patterns/deployment-guide.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Data Tables/*.data_table.json`, `Pages/*.page.json`, `lcap_app.json`, `Recipes/*.recipe.json` |
| `/create-genie` | When creating a new AI agent / MCP server (optional `[mcp]` tasks) | `plan.md` (optional), `docs/platform/agent-studio.md`, `docs/platform/mcp.md`, `.claude/rules/workato-agentic-format.md` | `projects/<name>/Agents/*.agentic_genie.json`, `*.agentic_skill.json`, `*.mcp_server.json` |
| `/create-connector <api-name>` | Invoked via a `[connector]` task. Connectors are shared assets and are not tied to a project; the caller's `plan.md` Connections information is passed as arguments | `docs/connector-sdk/connector-rb.md`, `docs/connector-sdk/overview.md`, `.claude/rules/workato-connector-sdk.md`, API documentation (WebFetch) | `connectors/<name>/connector.rb`, `settings.yaml`, `Gemfile` |

### Validation and sync phases

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/validate-recipe` | Before push, after editing JSON | The project's JSON files, `.claude/rules/` | None (validation report only) |
| `/push-project` | Before deploy | The project's assets | Workato remote (does not modify local) |
| `/pull-project` | After UI adjustments, at handover time | Workato remote | Assets under `projects/<name>/` (overwritten) |

### Learning phase

| Skill | When to invoke | Reads | Writes |
|---|---|---|---|
| `/learn-recipe` | Immediately after `/pull-project`, or after implementing previously unlearned actions | `projects/<name>/Recipes/*.recipe.json`, `projects/<name>/specs/*/plan.md` / `tasks.md` (the targets to tidy for learned actions), and the kit canonical `docs/<...>` as a cross-reference | `org/docs/connectors/<provider>.md` (input/output/snippet additions), `org/docs/logic/data-pills.md`, `org/docs/patterns/deployment-guide.md`, `org/docs/learned-patterns.md`; in addition, `projects/<name>/specs/*/plan.md` (remove relevant rows from the Unlearned Actions table) and `tasks.md` (check off `[learn]` tasks) |
| `/learn-pattern` | When you notice a reusable construction pattern | Reference recipes (optional), existing `docs/patterns/recipe-patterns/` (kit) + `org/docs/patterns/recipe-patterns/` (org) + `projects/docs/patterns/` (legacy, if present) | `org/docs/patterns/recipe-patterns/<name>.md` (single write target; distinguish generic vs. org-domain in the pattern body) |

## docs responsibility map

A list of "who writes and who reads" for each docs directory.

### Framework side (`workato-dev-kit` repo)

The kit canonical `docs/` is **written only by kit maintainers and the sync skills**; user learning results accumulate on the `org/docs/` side (see `@.claude/rules/org-knowledge-overlay.md`).

| Path | Writer | Reader | Contents |
|---|---|---|---|
| `docs/connectors/<provider>.md` | `/sync-connectors` | `/create-recipe`, `/create-workflow-app`, `/create-genie` | Pre-built connector trigger/action/field specs (kit canonical) |
| `docs/connector-sdk/` | Manual | `/create-connector` | Connector SDK reference |
| `docs/logic/` | Manual | `/create-recipe`, `/create-workflow-app` | datapill syntax, formulas, loops, error handling, triggers |
| `docs/platform/` | Manual | `/create-workflow-app`, `/create-genie`, `/plan` | Data Table, Lookup Table, Agent Studio, MCP, Workflow App |
| `docs/patterns/recipe-patterns/` | Manual (kit maintainers) | `/create-recipe`, `/plan`, `/learn-pattern` (cross-reference at load time) | Recipe construction patterns (kit canonical, read-only) |
| `docs/patterns/deployment-guide.md` | Manual | `/push-project`, `/create-workflow-app` | Deployment procedures, common errors |
| `docs/patterns/shared-assets.md` | Manual | `/create-recipe`, `/catalog`, `/plan` | Shared asset design policy |
| `docs/patterns/workspace-management.md` | Manual | `/plan`, `/catalog` | Workspace structure and naming conventions |
| `.claude/rules/` | Manual | All skills | JSON format, per-path rules |
| `docs/learned-patterns.md` | Manual (kit maintainers' temporary buffer) | Manual (triage work) | Kit canonical buffer. Users use `org/docs/learned-patterns.md` |

### Organization side (`connectors/`, `projects/`, `org/`)

| Path | Writer | Reader | Contents |
|---|---|---|---|
| `connectors/docs/<name>.md` | `/sync-connectors --custom` | `/create-recipe`, `/create-workflow-app` | Custom connector trigger/action/field specs |
| `connectors/<name>/connector.rb` | `/create-connector`, manual | `/sync-connectors --custom` | Custom connector implementation |
| `projects/<name>/specs/<NNN>-<slug>/spec.md` | `/spec`, `/clarify` | `/plan`, `/analyze`, Claude at session start | Feature requirements (WHAT/WHY, no Workato vocabulary) |
| `projects/<name>/specs/<NNN>-<slug>/plan.md` | `/plan` | `/tasks`, `/analyze`, `/create-recipe`, `/create-workflow-app`, `/learn-recipe` (tidies Unlearned Actions) | Workato configuration (HOW). Includes the Unlearned Actions table |
| `projects/<name>/specs/<NNN>-<slug>/tasks.md` | `/tasks`, `/implement` (check-off), `/learn-recipe` (`[learn]` completion) | `/analyze`, `/implement` | Executable tasks (with `[P]` / type tags) |
| `projects/<name>/DESIGN.md` / `DESIGN.md.legacy.*` | `/design update` (legacy, compatibility mode with warning) | `/design migrate`, manual review | **Deprecated**. Not generated for new projects. `/design new` is retired (refuse if invoked) |
| `projects/<name>/Recipes/*.json` | `/create-recipe`, `/pull-project` | `/learn-recipe`, `/validate-recipe`, `/push-project` | Recipe body |
| `projects/CATALOG.md` | `/catalog scan` | `/create-recipe`, `/plan` | List of organization shared assets (Recipe Function, Connection) |
| `projects/CATALOG_CONFIG.yaml` | Manual | `/catalog` | Scope settings (global / team / private) |
| `projects/docs/patterns/` | Legacy (no writer; record new entries in `org/docs/patterns/recipe-patterns/`) | `/create-recipe`, `/plan`, `/learn-pattern` (read only) | Org-domain patterns recorded in older versions (backward compatibility) |
| `org/docs/connectors/<provider>.md` | `/learn-recipe` | `/create-recipe`, `/create-workflow-app`, `/create-genie` | Corrections / additions to the kit version, org-specific field information |
| `org/docs/logic/`, `org/docs/platform/`, `org/docs/patterns/deployment-guide.md` | `/learn-recipe` | All create-family skills | Corrections / additions to the kit version |
| `org/docs/patterns/recipe-patterns/` | `/learn-pattern` | `/create-recipe`, `/plan` | Recipe construction patterns recorded by the organization (both generic and org-domain consolidated here) |
| `org/docs/learned-patterns.md` | `/learn-recipe` (fallback when the destination is undecided) | Manual (triage work) | Org-side temporary buffer |

## Lifecycle principles

### 1. docs-first

Build skills (`/create-recipe`, etc.) must **read the docs first**.

- If the information is in the documentation, implement directly from it
- If the information is missing:
  1. Implement as a best-effort implementation (including UI verification)
  2. Append to the **`## Unlearned Actions`** table in the feature's `plan.md`, and add a matching `[learn]` task to `tasks.md` (or record it as a GitHub Issue in this repo)
  3. After implementation, run `/learn-recipe` to enrich the docs. The corresponding entries in plan.md / tasks.md are tidied automatically at the same time
  4. Manually review anything that remains

### 2. Do not grep other projects

Do not grep under `projects/<other-project>/Recipes/` to dig out sample JSON.
Logic, naming, and datapill references that are specific to individual projects leak in as noise, and gaps in the knowledge base stop being visible.

**Exception**: pattern learning is fine (`/learn-pattern` references `docs/patterns/recipe-patterns/`, `org/docs/patterns/recipe-patterns/`, and `projects/docs/patterns/` (legacy)). However, grepping to obtain input/output schemas is not allowed.

### 3. Separation of learning responsibilities

| Learning content | Skill to use | Write target |
|---|---|---|
| Connector field specs (from the official API/SDK) | `/sync-connectors` | `docs/connectors/` (kit canonical), `connectors/docs/` (custom) |
| Connector field specs (from a recipe the org has used) | `/learn-recipe` | `org/docs/connectors/` |
| Reusable construction patterns | `/learn-pattern` | `org/docs/patterns/recipe-patterns/` (both generic and org-domain consolidated here) |
| New findings about JSON structure | `/learn-recipe` | `org/docs/learned-patterns.md` (use this for findings you may later upstream to the kit) |
| datapill reference patterns | `/learn-recipe` | `org/docs/logic/data-pills.md` |

**Key point**: learning skills do not create intermediate files; they append directly to the relevant document. Only `org/docs/learned-patterns.md` is tolerated as a staging area, and even that should be triaged promptly. Learning skills do not write into the kit canonical `docs/` (only kit maintainers and the sync skills do).

### 4. Build skills do not write docs

Build skills like `/create-recipe` only generate assets under `projects/`; they do not write to `docs/connectors/` or `docs/patterns/`.
Knowledge writes are the responsibility of the **learning skills** (`/learn-recipe`, `/learn-pattern`, `/sync-connectors`). This separation prevents incorrect information from leaking into the docs as a side effect of building.

## Typical scenarios

### Scenario A: New project (using a connector for the first time)

```
/spec <project>                       # Create spec.md (business requirements, technology-neutral)
/clarify <project>/001-<slug>         # Resolve Open Questions
/plan <project>/001-<slug>            # Create plan.md (CATALOG / pattern / resource lookup)
/tasks <project>/001-<slug>           # Create tasks.md (tagged task decomposition)
/analyze <project>/001-<slug>         # spec ↔ plan ↔ tasks consistency check
/sync-connectors <provider>           # Fetch metadata for unlearned connectors
/implement <project>/001-<slug>       # Dispatch tasks to /create-recipe etc.
/validate-recipe <project>            # Validate JSON structure (usually triggered inside /implement)
/push-project --start                 # Deploy + start (via the [push] task)
(Adjust pick_list etc. in the UI)
/pull-project                         # Pull adjustments (via the [pull] task)
/learn-recipe <project>               # Enrich docs + tidy plan.md / tasks.md [learn] entries
```

### Scenario B: New feature with a known connector

```
/spec <project>
/clarify <project>/<NNN>-<slug>       # For existing projects, 002, 003...
/plan <project>/<NNN>-<slug>
/tasks <project>/<NNN>-<slug>
/analyze <project>/<NNN>-<slug>
/implement <project>/<NNN>-<slug>
/push-project --start
```

If connector information is already in place, `/sync-connectors` and `/learn-recipe` are not needed.

### Scenario C: Building a custom connector

```
/spec <project>                       # Define the feature that uses the connector
.../tasks                             # tasks.md will include a [connector] task
/implement <project>/<NNN>-<slug>     # /create-connector is invoked from the [connector] task
(Implement and test with the Workato SDK)
/sync-connectors --custom <name>      # Update connectors/docs/<name>.md
(Continue /implement to the [recipe] tasks)
```

### Scenario D: Handover (understanding an existing project)

```
/pull-project --all                   # Pull all projects locally
ls projects/<project>/specs/          # Check the feature list
cat projects/<project>/specs/<NNN>-<slug>/spec.md   # Read the requirements
cat .../plan.md                       # Read the Workato configuration
/learn-recipe <project>               # Enrich docs from the implementation
/catalog scan                         # Inventory shared assets
```

### Scenario E: Migrating a legacy DESIGN.md project

```
/design migrate <project>             # DESIGN.md → specs/001-<slug>/{spec,plan,tasks}.md
/clarify <project>/001-<slug>         # Resolve the Open Questions emitted during migration
/analyze <project>/001-<slug>         # Consistency check
# From here, follow Scenario A / B
```

## When you are about to move outside this map

- "Let me grep `projects/<other-project>/Recipes/` to investigate input/output" → **stop**. Read `docs/connectors/<provider>.md`, or run `/sync-connectors` if it does not exist
- "Let me append to `docs/connectors/` while building" → **stop**. Build skills do not write docs. Leave it to `/learn-recipe`
- "Skip the spec and jump straight to implementation" → **stop**. Going through `/spec` → `/clarify` → `/plan` → `/tasks` prevents leftover Open Questions and missed Unlearned Actions. Even a one-line `/spec` is fine; tighten it with `/clarify`
- "Move to `/plan` while Open Questions remain" → **stop**. Resolve them with `/clarify` first, then `/plan`. `/plan` halts when it detects unresolved questions
- "Just write DESIGN.md and call it done" → **stop**. `/design new` has been retired. Start from `/spec`. If there is an existing DESIGN.md, convert it with `/design migrate` to `specs/` and join this flow
- "It's a new connector but let me just try implementing it" → OK, but record it in **plan.md's Unlearned Actions and tasks.md's `[learn]` task**, and run `/learn-recipe` afterward (it tidies automatically)
