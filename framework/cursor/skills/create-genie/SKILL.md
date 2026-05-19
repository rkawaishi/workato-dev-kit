---
name: create-genie
description: Interactively generate a Workato Genie (AI agent), its skills, and the supporting recipes. Japanese prompts are also supported.
---

# /create-genie

Generate the full file set for a Workato Genie (AI agent).
Supports Genie alone, MCP server alone, or both.

## Genie vs MCP Server — when to use which

| | Genie | MCP Server |
|---|---|---|
| **Purpose** | Conversational AI agent | Expose tools to external AIs |
| **Channels** | Slack, Teams, Workato GO | Claude Desktop, Cursor, ChatGPT |
| **Files** | `.agentic_genie.json` | `.mcp_server.json` |
| **Skill references** | Direct via `references` | Ordered + described via the `tools[]` array |
| **AI instructions** | `instructions` (system prompt) | `tools[].description` (tool-selection guidance) |

- **Genie only**: a conversational agent for internal chat.
- **MCP Server only**: tools callable from external AI editors / chat.
- **Both**: usable inside Genie and callable externally (skills/recipes can be shared).

## Procedure

1. Interview the user:
   - **Genie purpose**: what AI agent are we building?
   - **Target users**: who uses it?
   - **Skill list**: which skills should the Genie have (purposes of each)?
   - **AI provider**: `anthropic` / `openai` (default: `anthropic`).
   - **Target project**: which project directory to create in.
   - **MCP exposure**: also expose as an MCP server? (default: No.)
   - **VUA**: is Verified User Access needed (API calls using the end user's credentials)?

2. Read the references:
   - `.cursor/rules/workato-agentic-format.mdc`
   - `.cursor/rules/workato-recipe-format.mdc`
   - `.cursor/rules/workato-project-structure.mdc`
   - `docs/connectors/_index.md` + relevant connector knowledge
   - `docs/platform/agent-studio.md`
   - `docs/platform/mcp.md`

3. If an existing Genie is available, reference its structure.

4. Generate the Genie configuration files (following `.cursor/rules/workato-project-structure.mdc`):
   - `<project>/Agents/<name>.agentic_genie.json` — the Genie itself.
   - For each skill:
     - `<project>/Agents/<skill_name>.agentic_skill.json` — skill definition.
   - For MCP exposure: `<project>/Agents/<name>.mcp_server.json` — MCP server definition.
   - Make sure `zip_name` / `folder` inside the JSON include the subfolder path.

   > **Dispatch the generation.** In Claude Code, hand this file generation to the **`workato-builder` subagent** (`Agent` tool, `subagent_type: workato-builder`, asset type `genie`): pass the design from steps 1–3, the `instructions` / skill-recipe / MCP-server conventions in the sections below, and the target paths. The subagent runs on Sonnet, writes the files, and returns a short summary, keeping the JSON out of the main context. In editors without subagents, generate inline.

5. **Delegate skill recipes to `/create-recipe`**:
   - Lay out each skill's recipe requirements (trigger: `workato_genie/start_workflow`, parameters, external integration targets).
   - Invoke `/create-recipe` to generate the recipe (with interview).
   - `/create-recipe` handles the Genie-skill-recipe specifics (`as` is random hex, `parameters_schema_json`, etc.).

## Generating the Genie's `instructions`

Generate the prompt using this section structure:

```markdown
You are a [Role] Agent

**What's my job?**
[Description of the primary responsibilities]

**Who will need my help?**
[List of target users]

**How do I get things done?**
[List of behavior patterns]

**What should I avoid?**
[List of prohibitions]

**What results do you want me to track?**
[Metrics to follow]

**How should I talk to people?**
[Communication style]

**Any extra tips?**
[Anything else]
```

## Rules for generating a skill recipe

- Trigger: `workato_genie` / `start_workflow`.
- Use a random 8-character hex value for `as` (Genie-skill-recipe convention).
- `input.parameters_schema_json`: input parameter schema (JSON string).
- `input.result_schema_json`: output schema (JSON string).
- `input.requires_user_confirmation`: `"false"` (default).
- `input.description`: same as the skill's `trigger_description`.
- Parameter reference: `path:["parameters","<param_name>"]` — nested under `parameters`.
- Final step: `workato_genie` / `workflow_return_result` returns the result.
- `workflow_return_result` input: map each field individually as `input.result.<field>`.
  ```json
  "input": {
    "result": {
      "field1": "#{_dp('...')}",
      "field2": "#{_dp('...')}"
    }
  }
  ```
- `extended_output_schema` / `extended_input_schema` expand the `result_schema_json` fields under a `result` object.
- Intermediate steps: the actual business logic (Salesforce lookup, API calls, etc.).

## Generating the MCP server file

For MCP exposure, generate `<project>/Agents/<name>.mcp_server.json`:

```json
{
  "name": "Server name",
  "description": "MCP server description (the AI uses this to choose a server)",
  "auth_type": "workato_idp",
  "tools_type": "project_assets",
  "tools": [
    {
      "tool": "ref_0",
      "description": "Use this tool when... / Do not use this tool when...",
      "vua_required": true
    }
  ],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "Agents/skill_name.agentic_skill.json",
        "name": "skill_name",
        "folder": "Agents"
      }
    }
  }
}
```

### Guidelines for MCP tool `description`

- This is the instruction the AI uses to pick a tool. Make it more detailed than a Genie's `trigger_description`.
- Prefer "Use this tool when..." / "Do not use this tool when..." phrasing.
- Make the distinction between tools unambiguous.

### Caveats around skill names

When you attach a skill to an MCP server, Workato may rename the skill's `zip_name` to match the recipe name. Keep the skill's file name in lockstep with the recipe name.

### MCP server deployment caveats

- **First push**: the MCP server, skills, and skill recipes are created together.
- **`PG::UniqueViolation` on update**: re-pushing while the skill already exists triggers this error. `agentic_skill` and `mcp_server` cannot be removed via the CLI's `--delete` (they show up as `Skipped`). **Ask the user to delete them manually in the UI**, then re-push.
- **`extended_output_schema` on skill recipes**: actions like `add_record` need `extended_output_schema`; without it, downstream steps can't see the datapills and the recipe fails to start. Set it on every action.

### MCP only (no Genie)

When building only an MCP server without a Genie:
1. Generate the skill recipe (`workato_genie/start_workflow` trigger).
2. Generate the skill definition (`.agentic_skill.json`).
3. Generate the MCP server definition (`.mcp_server.json`).
4. No Genie file (`.agentic_genie.json`) needed.

```
MCP Server → Skills → Recipes (no Genie)
```

## Calling a Genie from a recipe: `assign_task_to_genie`

Delegate a task to a Genie from inside a recipe:

```json
{
  "provider": "workato_genie",
  "name": "assign_task_to_genie",
  "keyword": "action",
  "dynamicPickListSelection": { "genie_handle": "Genie name" },
  "toggleCfg": { "genie_handle": true },
  "input": {
    "genie_handle": {
      "zip_name": "Agents/genie.agentic_genie.json",
      "name": "Genie name",
      "folder": "Agents"
    },
    "task_instructions": "Task instructions (datapills allowed)"
  }
}
```

- `genie_handle`: references the Genie to invoke (by `zip_name`).
- `task_instructions`: task instructions for the Genie (you can inject context via datapills).
- Use cases: ask a Genie to analyze something during an approval flow, dispatch tasks to a Genie on event triggers, etc.

## Output and deployment guide

After generation, display:
- The list of generated files.
- Architecture diagram:
  - Genie only: `Genie → Skills → Recipes`.
  - With MCP: `Genie → Skills → Recipes ← MCP Server`.
- A summary of each skill's `trigger_description`.
- For MCP: a summary of the MCP server's `tools[]`.

Follow `docs/patterns/deployment-guide.md` and walk through the deploy:
1. Push connections first → guide UI auth (for new connections).
2. Push every other asset.
3. Guide the user through the field-mapping review of skill recipes in the UI.
4. For MCP: guide server enablement and AI-client configuration.
5. Guide the test run.

## Git management

Generated files (`Agents/`, `Recipes/`, `Connections/`) live under `projects/<project-name>/`. Commit them in the workspace repository:

```bash
git add projects/<project-name>/Agents/ projects/<project-name>/Recipes/ projects/<project-name>/Connections/
git commit -m "Add genie: <name>"
git push origin
```
