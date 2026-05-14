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

| Operator | Supported types | Description |
|---|---|---|
| `contains` | Array, String | Contains the value (case-sensitive) |
| `doesn't contain` | Array, String | Does not contain the value |
| `starts with` | String | Starts with the value |
| `doesn't start with` | String | Does not start with the value |
| `ends with` | String | Ends with the value |
| `doesn't end with` | String | Does not end with the value |
| `equals` | All | Exact match (numerics compared as floats) |
| `doesn't equal` | All | Does not match |
| `greater than` | String, Integer, Number | Greater than (strings compared by ASCII) |
| `less than` | String, Integer, Number | Less than |
| `is true` | Boolean | Is true |
| `is not true` | Boolean | Is not true |
| `is present` | All | A value exists (null/empty string is false) |
| `is not present` | All | No value exists |

### Notes

- All text comparisons are **case-sensitive**
- Comparing a null value with `greater_than` / `less_than` raises an error → combine with `is_present`
- `equals` converts strings to floats for numeric comparison. Watch out for octal notation (`"0123"` → `83`). Floats with more than 15 digits may lose precision
- `contains` / `does not contain` return false for null (no error)
- `starts_with` / `ends_with` raise a trigger error when comparing non-string types directly (datapills are auto-converted)
- Multiple conditions can be combined with `and` / `or`
- Conditions are used in three places: IF branches, While loops, and trigger filters
- Trigger `filter` uses the same condition structure

---

## 2. JSON structure (knowledge from recipe JSON analysis)

> The structural details below are not in the official Workato documentation;
> they are findings derived from analysing actual recipe JSON.

### if (conditional branch)
```json
{
  "number": N,
  "keyword": "if",
  "input": {
    "conditions": [
      {
        "operand": "contains",
        "lhs": "#{_dp('...')}",
        "rhs": "value",
        "uuid": "..."
      }
    ],
    "operand": "and",
    "type": "compound"
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
  "block": [ /* default actions */ ]
}
```

### elsif (additional conditional branch = ELSE IF)
```json
{
  "number": N,
  "keyword": "elsif",
  "input": {
    "conditions": [ /* conditions required */ ],
    "operand": "and",
    "type": "compound"
  },
  "block": [ /* actions when the condition is true */ ]
}
```

### Placement rules

- `else` / `elsif` are placed at the **end of the `if` block array**
- Use `else` for the default branch without a condition (using `elsif` without a condition is incorrect)
- `elsif` can be chained multiple times (`if` → `elsif` → `elsif` → `else`)

