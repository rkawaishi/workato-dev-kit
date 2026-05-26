# IF conditions

Official documentation: https://docs.workato.com/en/features/if-conditions.html

---

## 1. Official documentation (based on Workato Docs)

### Structure

```
IF (condition) → actions
ELSE IF (condition) → actions    ← chainable
ELSE → actions                   ← default branch
```

- Branches are evaluated in order; only the first one that evaluates to true executes
- ELSE IF / ELSE are optional

### Condition operators (14)

The first column is the label shown in the Workato UI. The second column is the literal string written to the recipe JSON's `operand` field — this is what you put in `conditions[].operand` when generating recipes.

All 14 values were verified by building a recipe that exercises every operator and reading back the recipe API response (`code` field). Several deviate noticeably from the UI label — in particular **`not_equals_to`** (not `not_equals`), **`present`** (not `is_present`), and **`blank`** (not `is_not_present` — the UI label is "Is not present").

| UI label | JSON `operand` | Supported types | Description |
|---|---|---|---|
| Contains | `contains` | Array, String | Contains the value (case-sensitive) |
| Doesn't contain | `not_contains` | Array, String | Does not contain the value |
| Starts with | `starts_with` | String | Starts with the value |
| Doesn't start with | `not_starts_with` | String | Does not start with the value |
| Ends with | `ends_with` | String | Ends with the value |
| Doesn't end with | `not_ends_with` | String | Does not end with the value |
| Equals | `equals_to` | All | Exact match (numerics compared as floats). **`equals_to`, not `equals` or `eq`** |
| Doesn't equal | `not_equals_to` | All | Does not match. **`not_equals_to`, not `not_equals`** |
| Greater than | `greater_than` | String, Integer, Number | Greater than (strings compared by ASCII) |
| Less than | `less_than` | String, Integer, Number | Less than |
| Is true | `is_true` | Boolean | Is true |
| Is not true | `is_not_true` | Boolean | Is not true |
| Is present | `present` | All | A value exists (null/empty string is false). **`present`, not `is_present`** |
| Is not present | `blank` | All | No value exists. **`blank` — note the UI label is "Is not present"** |

Unary operators (`is_true`, `is_not_true`, `present`, `blank`) still require `rhs` in the JSON — set it to an empty string (`"rhs": ""`).

> The Workato public docs page ([conditions.html](https://docs.workato.com/en/features/conditions.html)) presents short identifiers such as `eq`, `not_eq`, `gt`, `lt`, and `not_present`. **Those are not what the recipe JSON contains.** Use the JSON values in the table above.

### Notes

- All text comparisons are **case-sensitive**
- Comparing a null value with `greater_than` / `less_than` raises an error → combine with `present`
- `equals_to` converts strings to floats for numeric comparison. Watch out for octal notation (`"0123"` → `83`). Floats with more than 15 digits may lose precision
- `contains` / `not_contains` return false for null (no error)
- `starts_with` / `ends_with` raise a trigger error when comparing non-string types directly (datapills are auto-converted)
- Multiple conditions are combined with the top-level `input.operand` field set to `"and"` or `"or"`
- Conditions are used in three places: IF branches, While loops, and trigger filters
- Trigger `filter` uses the same condition structure (see `@docs/logic/triggers.md`)

---

## 2. JSON structure (knowledge from recipe JSON analysis)

> The structural details below are not in the official Workato documentation;
> they are findings derived from analysing actual recipe JSON.

Real recipe JSON places the `input` fields in the order `type`, `operand`, `conditions` (JSON object key order is cosmetic, but matching what `workato pull` writes makes diffs cleaner).

### if (conditional branch)
```json
{
  "number": N,
  "keyword": "if",
  "input": {
    "type": "compound",
    "operand": "and",
    "conditions": [
      {
        "operand": "equals_to",
        "lhs": "#{_dp('...')}",
        "rhs": "value",
        "uuid": "..."
      }
    ]
  },
  "block": [
    /* actions when true */
    { /* else or elsif — placed at the end of block */ }
  ]
}
```

### else (default branch without a condition)
```json
{
  "number": N,
  "keyword": "else",
  "input": {},
  "block": [ /* default actions */ ],
  "uuid": "..."
}
```

`else` still has an empty `input: {}` object (verified from API response). It has no `conditions` field.

### elsif (additional conditional branch = ELSE IF)
```json
{
  "number": N,
  "keyword": "elsif",
  "input": {
    "type": "compound",
    "operand": "and",
    "conditions": [ /* conditions required */ ]
  },
  "block": [ /* actions when the condition is true */ ]
}
```

### Placement rules

- `else` / `elsif` are placed at the **end of the `if` block array**
- Use `else` for the default branch without a condition (using `elsif` without a condition is incorrect)
- `elsif` can be chained multiple times (`if` → `elsif` → `elsif` → `else`)

### `uuid` constraint

Each entry under `conditions[]` has a `uuid` field. It is a UUID v4 and must be **36 characters or fewer** — same limit as the step-level `uuid`. Generate with `uuidgen` and use the raw output (do not add a prefix). Push rejects longer values.

