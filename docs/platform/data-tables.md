# Data Tables

Official: https://docs.workato.com/en/data-tables.html
Connector: https://docs.workato.com/en/data-tables/data-table-connector.html

## Overview

Workato's built-in data store. Manages data through a spreadsheet-like interface and lets recipes read and write to it. Retains data without depending on external APIs or databases.

## Primary use cases

- Caching responses from third-party APIs
- Data store for slow APIs
- Data foundation for Workflow Apps (single or multiple linked tables)

## Discouraged use cases

- Replacement for a relational database
- Storing large amounts of data in a single cell
- Storing PCI-sensitive data (credit card numbers, etc.)

## Building blocks

| Term | Description |
|---|---|
| **Record** | One row in the table. Uniquely identified by an auto-generated Record ID |
| **Column** | A table field (column). Has an auto-generated Column ID |
| **Record ID** | Unique identifier required for update and delete operations |
| **Column ID** | Internal identifier resilient to column-name changes |

## Column types

- Standard data types (string, number, boolean, date, etc.)
- **Long text**: up to 10,000 characters per cell

## Triggers (4)

| Name | Description |
|---|---|
| New record (real-time) | When a new record is created (real-time) |
| New records (batch) | Batch detection of new records |
| New/updated record (real-time) | New or updated record (real-time) |
| New/updated records (batch) | Batch detection of new or updated records |

## Actions (10)

| Name | Description |
|---|---|
| Create record | Create a record |
| Create records (batch) | Bulk create multiple records |
| Update record | Update a record |
| Update records (batch) | Bulk update multiple records |
| Upsert record | Create or update a record (based on matching criteria) |
| Delete record | Delete a record |
| Delete records (batch) | Bulk delete multiple records |
| Remove values from a record | Clear specified field values from a record |
| Search records (batch) | Search records matching given criteria |
| Truncate table (batch) | Delete all records from the table |

## Lookup in formulas

Records in a Data Table can be referenced directly from recipe formula mode.

Official: https://docs.workato.com/en/formulas/other-formulas.html#data-table-lookup

## Notes

- Scalable, secure, and maintenance-free
- Tables can be created and columns changed from the UI
- Recipes access them through the Data Tables connector
- Using Column IDs prevents recipes from breaking when column names change
