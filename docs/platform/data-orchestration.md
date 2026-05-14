# Data Orchestration

Official: https://docs.workato.com/en/data-orchestration.html

## Overview

A feature that integrates and harmonizes data from disparate sources, applications, and systems, then loads it into databases and data warehouses. Simplifies the creation of data pipelines.

## Features

| Feature | Description |
|---|---|
| **Low-code / no-code** | Build workflows with minimal coding |
| **Flexibility** | Recipe-based and customizable |
| **Scalability** | Handle large data volumes via Bulk actions / triggers |
| **Reuse** | Component reuse via Recipe Functions |
| **Observability** | Monitor with logging services and job reports |
| **Performance** | Efficient execution via Bulk operations and file storage |

## ETL vs ELT

| | ETL | ELT |
|---|---|---|
| Flow | Extract → Transform → Load | Extract → Load → Transform |
| Transform timing | Before load | After load (inside the target system) |
| Applies to | Data warehouses | Data lakes, distributed storage |

For efficient ETL / ELT, Workato recommends **Bulk processing** over batch processing.

## Monitoring dashboard

- 30-day pipeline activity summary
- Number of successful / failed / stopped runs
- Daily row volume and average execution time
- Timeline showing status and outcome
- Object-level run tracking

## Related connectors

Connectors suited to high-volume data transfer:
- Snowflake, Redshift, BigQuery (data warehouses)
- Amazon S3, Google Cloud Storage (file storage)
- PostgreSQL, MySQL, Oracle (databases)
