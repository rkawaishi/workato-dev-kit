# XML tools by Workato recipes

Provider value to use in every step: `xml_parser`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "xml_parser"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `generate_xml_xsd` | Generate XML document from XSD | - |
| `parse_xml` | Parse XML document | - |
| `transform_xml_xslt` | Transform XML using XSLT (Deprecated) | - |
| `transform_xml_xslt_v2` | Transform XML using XSLT | - |
| `validate_xml` | Validate XML document with XSD | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
