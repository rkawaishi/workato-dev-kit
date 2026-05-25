# Triggers

Official: https://docs.workato.com/en/recipes/triggers.html

## What is a trigger

The event definition that starts recipe execution. Every recipe requires exactly one.

## Trigger classification

### Mechanism (detection method)

| Kind | Behaviour | Characteristics |
|---|---|---|
| **Polling** | Checks data on a schedule (minimum 5-minute interval) | Most common. Resumes from the last position after a stop |
| **Real-time** | Immediate notification via webhook | Many include a backup poll (hourly) |
| **Scheduled** | Runs on a specified date/time or interval | Supports cron expressions (minimum 5-minute interval). May reprocess |
| **CDC** | Real-time monitoring of database changes | Detects INSERT/UPDATE/DELETE |

### Dispatch (how events are delivered)

| Kind | Behaviour | Use |
|---|---|---|
| **Single** | Each event is processed as an individual job | Real-time sync. Most common |
| **Batch** | Fetches multiple events together (configurable batch size) | Efficient processing of large data volumes |
| **Bulk** | Bulk transfer via CSV streaming (no upper limit) | Exports, daily large-scale sync. Test mode not supported |

## Key guarantees

- **Order preservation**: events are delivered in chronological order (oldest first)
- **Durable cursor**: resumes from the last processed position after a stop
- **Deduplication**: prevents the same event from being processed twice
- **Delivery guarantee**: polling triggers reliably recover events that occurred during downtime

## Since/From parameter

Field that specifies "from when to fetch events when the recipe starts."

- Can capture events from before the recipe started
- **Cannot be changed once set** (after the recipe has run)
- Default: recipe start time, 1 hour ago, or 1 day ago (depends on the trigger)
- The user's time zone applies

## Trigger conditions

Apply additional filtering after events are fetched.

### Important behaviour

- Evaluated **after** events are fetched (not before)
- Checks the current value at fetch time, not a field change
- **Case-sensitive**
- **Not recommended for Batch/Bulk triggers** (only the first record is evaluated)
  - Use app-side filtering (SOQL WHERE clauses, etc.) instead

### How to configure

1. Toggle "Set trigger condition"
2. Map a datapill from the Recipe data menu
3. Pick a condition type from the dropdown
4. Enter the value in the Value field
5. Combine multiple conditions with AND/OR

### JSON structure (inside the recipe)

```json
"filter": {
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
}
```

See `@docs/logic/if-conditions.md` for the full list of condition operators.

Each entry's `uuid` is a UUID v4 and must be **36 characters or fewer** (push rejects longer values). Generate with `uuidgen` and use the raw 36-character output without prefixes.
