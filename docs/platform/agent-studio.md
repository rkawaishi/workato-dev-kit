# Agent Studio

Official: https://docs.workato.com/en/agentic/agent-studio.html

## Overview

A no-code platform for building and managing AI agents (Genie). A Genie is a conversational AI agent that understands context and dynamically executes predefined skills.

## The four components of a Genie

### 1. AI Model & Job Description
- Language model used (`anthropic`, `openai`, etc.)
- Persona, constraints, tone, and formatting instructions (`instructions` field)

### 2. Chat Interface
- The conversational interface with users
- Supported platforms: Slack, Microsoft Teams, Workato GO

### 3. Knowledge Base
- Information sources such as FAQs, policies, and company data
- Structured data, documents, articles, and text resources
- Supported files: PDF, CSV, Markdown, TXT (up to 25 MB), images (up to 5 MB)

### 4. Skills
- Action execution via Workato workflows / recipes
- Data retrieval, message sending, external API calls

## Key features

| Feature | Description |
|---|---|
| Domain expertise | Integrates with existing systems and learns from user interactions |
| Reasoning ability | Natural language understanding, handles multi-step tasks |
| Responsible behavior | Administrators stay in control via approval workflows |
| Continuous learning | Feedback loops and knowledge base updates |
| MCP client | Consumes MCP servers to access external APIs and tools |

## Security

- **RBAC**: Manage view / edit / create / delete permissions for Genies and knowledge bases
- **Verified User Access**: Execute actions with each user's own credentials (based on individual permissions)
- **Audit trail**: Log recording for compliance

## JSON structure

### agentic_genie.json
```json
{
  "name": "Genie name",
  "description": "Short description",
  "instructions": "System prompt",
  "ai_provider": "anthropic",
  "ai_model": null,
  "mcp_servers": [],
  "references": { "ref_0": { "type": "agentic_skill", "id": {...} } }
}
```

### agentic_skill.json
```json
{
  "name": "Skill name",
  "trigger_description": "Conditions under which the skill runs",
  "references": { "recipe_id": { "type": "recipe", "id": {...} } }
}
```

Detailed format: `@.claude/rules/workato-agentic-format.md`

## Invocation from a recipe

A Genie can be invoked from a recipe via the `workato_genie/assign_task_to_genie` action.

```json
{
  "provider": "workato_genie",
  "name": "assign_task_to_genie",
  "keyword": "action",
  "dynamicPickListSelection": { "genie_handle": "Genie name" },
  "toggleCfg": { "genie_handle": true },
  "input": {
    "genie_handle": {
      "zip_name": "genie.agentic_genie.json",
      "name": "Genie name",
      "folder": ""
    },
    "task_instructions": "Task instruction text (datapill allowed)"
  }
}
```

- `genie_handle.zip_name`: Genie JSON filename within the same Project
- `task_instructions`: Task instructions passed to the Genie. Can be assembled dynamically with datapills
- Recipe JSON format details: `@.claude/rules/workato-recipe-format.md`

## Available regions

US, EU, AU, SG, JP data centers (CN is not supported)
