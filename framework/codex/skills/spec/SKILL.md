---
name: spec
description: Capture a feature's requirements (UX, WHAT/WHY) in spec.md. No technical detail — that lives in `$plan`. Use at the start of a project or when adding a new feature. Japanese prompts are also supported.
---

# $spec

Write a feature's **requirements (WHAT/WHY)** to `projects/<project>/specs/<NNN>-<slug>/spec.md`.

This is the first step of the spec-driven workflow. Do not touch the technology stack (Workato configuration); only fix the user experience and business requirements. Mapping to technology is `$plan`'s responsibility.

## Usage

- `$spec <project-name>` — create a spec.md for a new feature
- `$spec <project-name> <feature-slug>` — create it with a specific slug
- `$spec <project-name>/<NNN>-<slug>` — update an existing spec.md

## Workflow

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
  ↑
you are here
```

After `$spec` completes, if any `Open Questions` remain, point the user at `$clarify`. If none remain, point at `$plan`.

## Procedure

### 1. Identify the feature

- If `<project-name>` is missing, ask for the project name.
- `ls projects/<project-name>/specs/` and pick the **next sequence number** based on existing features (`001`, `002`, ...).
- Confirm a short kebab-case slug with the user.
  - Examples: `it-onboarding`, `expense-approval`, `slack-digest`.
- Final path: `projects/<project-name>/specs/<NNN>-<slug>/spec.md`.

### 2. UX interview

**Use business language, not technical jargon.** Don't ask everything at once; follow up based on the answers.

```
Tell me about this feature:

1. **Who wants to do what?**
   e.g. submit IT onboarding for a new hire; file an expense for approval

2. **What flow do you have in mind?**
   e.g. fill a form → manager approves → IT team is notified

3. **Who is involved?**
   e.g. requester, manager (approver), IT team (executor)

4. **What does success look like in the end?**
   e.g. a Jira ticket is created and the IT team can start work

5. **Are there existing tools or data sources?**
   e.g. manager info lives in Google Sheets; notifications go to Slack
```

### 3. Summarize and confirm the user experience

Turn the interview into **user stories** and confirm with the user.

```
## User experience (draft)

### Requester
1. Open the form
2. Fill in the details and submit
3. Status changes to "awaiting approval"
4. Receive a notification when approved

### Approver
1. Receive an approval request (notification with buttons)
2. Review and approve or reject
3. Can also act from another channel (e.g. a task page)

### Downstream
- On approval: create an external ticket → notify
- On rejection: notify the requester

Does this match what you have in mind? Anything to add or change?
```

### 4. Extract Open Questions (mandatory for resumability)

Whatever **could not be confirmed** during the interview must be written into `Open Questions`. `$clarify` resolves these.

Typical unresolved items:
- One approver or many? Is hierarchical approval needed?
- Can a rejected request be resubmitted?
- Notifications via Slack, email, or both?
- How long is request data retained?
- Do we need to dedupe against existing accounts?

**Important**: items where there is a tentative answer but it still needs confirmation also go in Open Questions (with a note saying so). Only fully settled items go into the main body.

### 5. Write spec.md

Use the template below. **Do not use Workato terminology** (no Recipe, Datapill, Connection, etc.).

### 6. Next-step guidance

```
✓ Created spec.md: projects/<project>/specs/<NNN>-<slug>/spec.md

<N> Open Questions remain.
Next, run $clarify <project>/<NNN>-<slug> to resolve them.

(Only if no Open Questions remain)
You can proceed directly to $plan <project>/<NNN>-<slug>.
```

## spec.md template

```markdown
# <Feature name>

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Project: <project-name>
- Feature ID: <NNN>-<slug>

## Why
<The business problem, what you want to solve, what value you want. 1–3 paragraphs.>

## User Stories

### <Role 1> (e.g. Requester)
1. <step>
2. <step>
3. <step>

### <Role 2> (e.g. Approver)
1. <step>
2. <step>

### <Role 3> (e.g. Executor)
1. <step>

## Success Criteria
<!-- What constitutes success, written as observable conditions. -->
- [ ] <condition 1>
- [ ] <condition 2>

## External Touchpoints
<!-- External services or data sources we integrate with. Use business names ("ticketing system"), not vendor names; technology choices come in `$plan`. -->
- <service>: <purpose>
- <service>: <purpose>

## Constraints / Non-functional
<!-- Performance, security, operational requirements. Only when applicable. -->
- <constraint>

## Out of Scope
<!-- Explicit non-goals for this feature; what is deferred to a later one. -->
- <item>

## Open Questions
<!-- Unresolved items to be addressed by `$clarify`. This checklist is the resumption point. -->
- [ ] <question 1>
- [ ] <question 2>

## Decisions
<!-- Important decisions made during the interview, with the reasoning. For future reference. -->
- <YYYY-MM-DD>: <decision> — <reason>
```

## Rules to follow

- **No Workato terminology**: spec.md is technology-agnostic. Don't use words like Recipe, Connection, Datapill, Workflow App — translate them into business terms.
- **Persist Open Questions**: never leave unresolved points only in conversational context — write them to the file. The ability to resume via `$clarify` after an interruption depends on this.
- **Do not touch DESIGN.md**: if the project still has a legacy DESIGN.md, create spec.md as a new file anyway. Migrating from DESIGN.md is `$design migrate`'s job.

## `.workatoignore` management

Every project needs a `.workatoignore` so `workato pull` does not wipe local-only artifacts and `workato push` does not deploy them. The kit ships a base template at `templates/workatoignore.template` (it already covers `specs/`).

When you create spec.md, ensure `projects/<project-name>/.workatoignore` exists:

```bash
PROJ="projects/<project-name>"
if [ ! -f "$PROJ/.workatoignore" ]; then
  cp templates/workatoignore.template "$PROJ/.workatoignore"
else
  # Append any base-template entries that are missing — never remove lines.
  while IFS= read -r line; do
    case "$line" in ''|\#*) continue ;; esac
    grep -qxF "$line" "$PROJ/.workatoignore" || echo "$line" >> "$PROJ/.workatoignore"
  done < templates/workatoignore.template
fi
```

Because the template already lists `specs/`, no spec-specific entry is needed.

## Git management

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/spec.md projects/<project-name>/.workatoignore
git commit -m "spec(<project>/<slug>): initial spec"
git push origin
```

`workato push` will not deploy spec.md to Workato (it's excluded by `.workatoignore`).
