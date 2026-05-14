# File handling

Official: https://docs.workato.com/en/handling-files-and-attachments.html

## Overview

Workato transfers files and attachments between apps via FTP, file systems, APIs, S3, and similar transports.

## File types

### Text files (parseable)

| Format | Use |
|---|---|
| CSV | Tabular data |
| TXT, RTF | Plain text |
| HTML | Web content |
| JSON | API data |
| XML, SOAP | Structured data |
| YAML | Configuration files |

- Content can be **parsed** inside a recipe and used as individual fields
- Example: fetch a CSV file → parse → insert each row into Redshift

### Binary files (not parseable)

| Format | Examples |
|---|---|
| Images | jpg, png, gif, bmp, psd |
| Documents | pdf, doc, docx, ppt, xls, odt |

- Workato passes content through without interpreting it
- Example: upload a Salesforce attachment to Zendesk

## Processing patterns

### Text file processing
1. Fetch the file with a connector (FTP, S3, Google Drive, etc.)
2. Parse the content (CSV → row data, JSON → object)
3. Use the parsed data in subsequent actions

### Binary file transfer
1. Fetch the file content from the source app
2. Upload it directly to the destination app (via the `fileContent` datapill, etc.)

### File streaming
For large files, use connectors that support streaming transfer.
