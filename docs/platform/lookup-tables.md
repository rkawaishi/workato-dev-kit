# Lookup Tables

Official: https://docs.workato.com/en/features/lookup-tables.html

## Overview

A data store for cross-reference lookups. Stores data frequently referenced from recipes in a tabular form. Used to reduce API calls and to cache static data.

## Primary use cases

- Unit conversion (meters ↔ feet, etc.)
- Reference cache for business data
- Caching data from slow APIs
- Postal code → city name mapping

## Limits

| Item | Limit |
|---|---|
| Tables per workspace | 100 |
| Columns per table | 10 |
| Rows per table | 100,000 |
| Row size | 128 KB |
| Data per cell | 10 KB |
| Batch operation size | 10,000 |
| CSV export | Cannot export beyond 50,000 rows |
| Get all entries | Up to 10,000 entries |

## Actions (9)

| Name | Description |
|---|---|
| Add entry | Create an entry |
| Add entries (batch) | Bulk create multiple entries |
| Lookup entry | Find an entry by column value (returns the first match) |
| Search entries (batch) | Find all entries matching the criteria |
| Get all entries (batch) | Retrieve all entries (up to 10,000) |
| Update entry | Update an entry |
| Delete entry | Delete an entry |
| Delete multiple entries (batch) | Bulk delete multiple entries |
| Truncate table | Delete all entries in the table |

## Lookup in formulas

```ruby
lookup("TABLE_NAME", "COLUMN": value)["RETURN_COLUMN"]
```

In-memory lookup using the output of Search entries accelerates repeated lookups.

## Differences from Data Tables

| | Lookup Tables | Data Tables |
|---|---|---|
| Purpose | Reference / mapping data | Application data store |
| Column count limit | 10 | Looser limit |
| Row count limit | 100,000 | Scalable |
| Triggers | None | 4 (real-time / batch) |
| Workflow Apps integration | None | Yes |
