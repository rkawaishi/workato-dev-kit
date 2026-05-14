# MCP (Model Context Protocol)

Official: https://docs.workato.com/en/mcp.html

## Overview

An open standard for connecting AI models to external tools and data sources. Lets AI agents access databases, APIs, and business applications through a common protocol.

## Types of MCP servers

| Type | Description | Hosting |
|---|---|---|
| **MCP Servers** | Connect API Collection endpoints via authenticated MCP URLs | Workato-hosted |
| **MCP Local Servers** | Access local tools, databases, and APIs | Local infrastructure |
| **Developer API MCP Server** | Access the Workato workspace from Claude Desktop, Cursor, ChatGPT, etc. | Workato-hosted |

## Core components

| Component | Description |
|---|---|
| **Servers** | Expose tools / skills to AI agents. Implement authentication and access control |
| **Skills / Tools** | Individual capabilities (search, create, update, analyze, etc.). Have input / output schemas and descriptions |
| **Dynamic Discovery** | AI agents discover available tools at runtime |
| **Identity-Aware Execution** | Execute actions based on the authenticated user / agent's permissions |

## Security & governance

### Authentication
- OAuth-based flow for user authentication
- **MCP Verified User Access**: Calls external APIs with the end user's credentials rather than a static token

### Rate limiting
- Configurable at the server level
- Shared across all skills / tools within the server
- Protects downstream applications and enables fair resource allocation

### Audit & compliance
- All actions via the MCP server are logged
- Identity tracking per operation
- Integration with enterprise audit systems

## Relationship to API Platform

Endpoints in API Collections can be exposed as MCP servers:
```
API Collection → MCP Server → AI Agent (Genie, Claude, ChatGPT)
```

Details: `@docs/platform/api-platform.md`

## Relationship to Agent Studio

A Genie can consume MCP servers as an MCP client:
```
Genie → MCP Client → MCP Server → External API / tools
```

Specify the connection in the `mcp_servers` field of `agentic_genie.json`.

## MCP Server Registry

Search and configure prebuilt MCP servers to add app-specific tool sets to an LLM project.
Official: https://docs.workato.com/en/mcp/mcp-server-registry.html

## MCP Server JSON structure (`*.mcp_server.json`)

Exporting a Workato project includes MCP server definitions as `*.mcp_server.json` files.

### Top-level fields

| Field | Description |
|---|---|
| `name` | Server display name (e.g., "Gmail") |
| `description` | Description that the AI uses when selecting the server |
| `auth_type` | Authentication method. `"workato_idp"` = Workato Identity Provider |
| `tools_type` | `"project_assets"` = expose in-project assets as tools |
| `tools` | Array of tool definitions |
| `references` | `ref_N` → mapping to agentic_skill |

### Structure of the tools array

```json
{
  "tool": "ref_0",
  "description": "Use this tool when... / Do not use this tool when...",
  "vua_required": true
}
```

- `tool`: A reference key inside `references`
- `description`: Detailed instructions the AI uses to select the tool
- `vua_required`: Whether Verified User Access is required (calls the external API with the end user's credentials)

### Structure of the references map

```json
{
  "ref_0": {
    "type": "agentic_skill",
    "id": {
      "zip_name": "Gmail/search_threads.agentic_skill.json",
      "name": "search_threads",
      "folder": "Gmail"
    }
  }
}
```

### Relationship: MCP server → skill → recipe

```
mcp_server.json
  └── tools[] → references → agentic_skill.json (multiple allowed)
                                └── references.recipe_id → recipe.json
```

The MCP server exposes skills to external AI agents (Claude Desktop, Cursor, ChatGPT, etc.) via a different route than a Genie. Whereas a Genie references skills directly through its own `references`, an MCP server exposes skills in an ordered, described list through its `tools[]` array.

### Automatic skill renaming

When a skill is attached to an MCP server, Workato may rename the skill's `zip_name` based on the recipe name:
- On push: `submit_pc_loan_request.agentic_skill.json`
- After pull: `submit_pc_loan_request_via_mcp.agentic_skill.json` (renamed to match the recipe name)

It is safer to keep the skill filename aligned with the recipe name.

### Real example: Gmail MCP Server

The Gmail server defines 20 tools / skills:
search_threads, search_messages, list_labels, get_thread, get_message, list_attachments, add_labels, remove_labels, unstar_messages, star_messages, unarchive_threads, archive_threads, create_draft, get_draft, update_draft, send_draft, mark_message_read_state, list_drafts, add_attachments, remove_attachments

## Available regions

US, EU, AU, JP, SG data centers (CN is not supported)
