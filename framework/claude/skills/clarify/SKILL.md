---
description: Resolve spec.md's Open Questions one by one and fold the answers into the body. Run after `/spec` and before `/plan`. Resume from this skill after an interruption. Japanese prompts are also supported.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /clarify

Resolve the unresolved items in `spec.md`'s `## Open Questions` section **one at a time** and reflect each answer in the body of spec.md.

In the spec-driven workflow this skill sits between `/spec` and `/plan`. Closing every ambiguity here, before moving to design, avoids rework downstream.

**Key to resumability**: even if `/spec`'s working state is lost to context exhaustion or an interruption, as long as Open Questions remain in the file you can resume with `/clarify`.

## Usage

- `/clarify <project>/<NNN>-<slug>` — resolve Open Questions for a specific feature
- `/clarify <project>` — auto-pick the latest feature in the project that still has Open Questions
- `/clarify` — infer from the current session context (ask if ambiguous)

## Workflow

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
          ↑
       you are here
```

## Procedure

### 1. Read spec.md

- Read `projects/<project>/specs/<NNN>-<slug>/spec.md`.
- Extract unchecked items (`- [ ] ...`) from the `## Open Questions` section.
- If everything is checked, say "All Open Questions are resolved. Proceed to `/plan`." and stop.

### 2. Ask one question at a time

Present **one question at a time**. Don't batch — answer quality drops when you do.

```
<N> Open Questions remain. Let me confirm them one at a time.

[1/N] <question>

Possible options (if any):
- A: <option>
- B: <option>
- C: Other (free text)

Please answer.
```

### 3. Reflect the answer

As soon as you have an answer, **update spec.md immediately**:

1. Check off the matching Open Question item (`- [x]`).
2. Update the relevant section of the spec body based on the answer.
   - Approver scope decided → update the corresponding role in User Stories.
   - Notification channel decided → update External Touchpoints.
   - Constraint found → add to Constraints / Non-functional.
   - Confirmed out of scope → move to Out of Scope.
3. Append `<YYYY-MM-DD>: <decision> — <reason>` to `## Decisions`.
4. Update `Last updated`.

### 4. Add derived Open Questions

If an answer reveals **new ambiguities**, append them to Open Questions immediately (you can keep resolving them in the same session).

Example:
```
Q: Is there a single approver or multiple?
A: One manager + a department head when needed.
→ New Open Question: "Under what conditions is department-head approval required? Amount / category / role?"
```

### 5. Wrap-up after everything is resolved

When every Open Question is checked off:

```
✓ All Open Questions resolved (<N> total).

Key decisions:
- <summarize 3–5 important entries from Decisions>

Next, proceed to /plan <project>/<NNN>-<slug> to map this into Workato configuration.
```

## Tips for asking

### Turn yes/no questions into multiple choice

```
✗ "Is resubmission allowed?" (open-ended)
○ "After a rejection, do you allow resubmission? A: yes (edit + resubmit), B: yes (only as a new request), C: no"
```

### Ask in business scenarios, not technology choices

```
✗ "Is the Slack notification channel public or private?"
○ "When an approval request lands, who needs to see it? Only the approver / the whole department / the whole company?"
```

### Accept "I don't know"

If the user says "I can't decide right now":
- Keep the item in Open Questions but rewrite it as `- [ ] <question> (deferred: undecided as of <YYYY-MM-DD>)`.
- Treat it in `/plan` as a **placeholder + Decision Required**.
- The user can call `/clarify` again later.

## Reflection rules

| Question kind | Section to update |
|---|---|
| User behavior or experience | User Stories |
| Success conditions / observable points | Success Criteria |
| External services we integrate with | External Touchpoints |
| Performance, security, operational requirements | Constraints / Non-functional |
| What we are not going to do | Out of Scope |
| Why we decided this way | Decisions |

**Prohibited**: do not introduce technical terms (Recipe, Datapill, Workflow App, etc.) into spec.md. Mapping to technology is `/plan`'s responsibility.

## Rules to follow

- **One at a time**: batching makes answers shallow. Always close the loop on each question — including the file update — before moving to the next.
- **Update the file each time**: do not interview 5 items and write all the changes at the end. Save spec.md after each answer (interruption insurance).
- **Decisions get reasons**: not just `decided on A`, but `decided on A — B is too expensive and C needs user training`.

## Git management

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/spec.md
git commit -m "clarify(<project>/<slug>): resolve open questions"
git push origin
```
