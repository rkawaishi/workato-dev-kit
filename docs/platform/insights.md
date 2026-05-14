# Insights

Official: https://docs.workato.com/en/insights.html

## Overview

Workato's built-in data visualization and analytics engine. Build analytical reports of automation data without code. No ETL / ELT infrastructure required.

## Core components

| Component | Description |
|---|---|
| **Data sources** | Where data is retrieved from |
| **Query components** | Tools to transform and prepare data |
| **Chart components** | Elements that visualize data |
| **Dashboards** | Collections of reports and visualizations |

## Data sources

### Standard sources
- Project, recipe, job history, and Workflow Apps metadata
- Detailed job execution data (retained for 365 days)

### Custom sources
- Calculated columns inside job reports
- Supplementary information from Data Tables

## Chart types (6)

| Type | Description |
|---|---|
| Table | Tabular format (default) |
| Line | Line chart |
| Bar | Bar chart |
| Area | Area chart |
| Pie | Pie chart |
| Number | Numeric display |

## Primary use cases

- **Usage analysis**: Task consumption, error rate, execution time
- **Automation impact measurement**: ROI calculation, time / cost savings tracking
- **App analytics**: User processing time, approval workflows
- **Performance analysis**: Process metrics, throughput

## Relationship to recipes

Custom columns defined in a recipe's `job_report_schema` / `job_report_config` are available as Insights data sources.
