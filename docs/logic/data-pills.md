# Datapills and data mapping

Official: https://docs.workato.com/en/recipes/data-pills-and-mapping.html

## What is a datapill

An output variable of a trigger or action step. Referenced by subsequent steps to construct the data flow.

## Data types

| Type | Description |
|---|---|
| String | Text string |
| Integer / Number | Integer / numeric value |
| Date / Datetime | Date / datetime |
| Boolean | Boolean value |
| Object | Object (group of nested fields) |
| List (Array) | List (array) |

### Type conversion formulas

| Convert to | Formula |
|---|---|
| Integer | `.to_i` |
| Float | `.to_f` |
| String | `.to_s` |
| Date | `.to_date` |
| Datetime | `.to_time` |
| Currency | `.to_currency` |

## Mapping rules

### Variables vs constants

- **Variable (datapill)**: value changes per trigger event (e.g. Account Name for each lead)
- **Constant**: fixed value (e.g. fixed text inside an email template)
- **Hybrid**: mix datapills and constants in a single field

### System datapills

Built-in datapills available in every job:

| datapill | Description |
|---|---|
| User ID / User name / User email | Executing user information |
| Recipe ID / Recipe URL / Recipe name | Recipe information |
| Job ID / Job created at | Job information |
| Root recipe ID / Root job ID | Nested call origin |
| Is repeat / Repeat count | Retry information |
| Is test | Whether running in test mode |

### Error datapills

Available inside an error handling (Handle errors) block:

| datapill | Description |
|---|---|
| Error type | Error category |
| Error message | Error message |
| Retry count | Retry count |
| Errored step number | Step number where the error occurred |
| Errored app | App where the error occurred |
| Errored action | Action where the error occurred |
| Inner message | Raw third-party response |

## Datapill representation inside JSON (knowledge from recipe analysis)

> The structural details below are not in the official Workato documentation;
> they are findings derived from analysing actual recipe JSON.

### `_dp()` function (structured reference)

```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["field"]}')}
```

- `pill_type`: usually `"output"`
- `provider`: provider name of the referenced step
- `line`: `as` value of the referenced step
- `path`: field path array. For the current item in a list, use `{"path_element_type":"current_item"}`

### `_()` dot notation

```ruby
#{_('data.provider.step.field')}                    # dot notation
```

### `=_()` reference with formula

```ruby
=_('data.provider.step.list').pluck('f').join(', ') # Ruby expression (prefix with =)
```

### `path_element_type` in foreach

To reference the current item inside a loop, use `{"path_element_type":"current_item"}` inside the `path` array:
```json
"path": [{"path_element_type":"current_item"}, "field_name"]
```

## Notes

- **Hidden fields**: fields not defined in the schema must be referenced with bracket notation: `Parent_object['field_name']`
- **Unexecuted branches**: datapills from a branch that did not execute are null
- **Same-named fields**: watch out for datapills with the same name across different steps. Verify the source step
- **Required fields**: a value mapped at design time may still be missing at runtime
