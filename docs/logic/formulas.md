# Formulas

Official: https://docs.workato.com/en/formulas/formula-mode.html

## What is formula mode

Enabled by clicking the `fx` icon in an input field. Lets you apply transformations and operations to a datapill.

## Text mode vs formula mode

| | Text mode | Formula mode |
|---|---|---|
| Text and datapills | Output as-is | Explicit formatting required via formula |
| Ruby interpolation `#{}` | **Not supported** (datapills only evaluated) | Handled by formula |

## Formulas by type

The formula editor displays the formulas available for the datapill's type.

### String operations (main)

| Formula | Description | Example |
|---|---|---|
| `.upcase` | Convert to uppercase | `"hello".upcase` → `"HELLO"` |
| `.downcase` | Convert to lowercase | |
| `.strip` | Remove leading/trailing whitespace | |
| `.gsub(pattern, replacement)` | Pattern replacement | |
| `.split(delimiter)` | Split into an array | |
| `.length` | Character count | |
| `.present?` | Whether a value exists | |
| `.blank?` | Whether it is empty | |
| `.truncate(n)` | Truncate to n characters | |

### Numeric operations

| Formula | Description |
|---|---|
| `.to_i` | Convert to integer |
| `.to_f` | Convert to float |
| `.round(n)` | Round to n decimal places |
| `.abs` | Absolute value |

### Date/datetime operations

| Formula | Description |
|---|---|
| `.today` | Today's date |
| `.now` | Current datetime |
| `.strftime(format)` | Datetime formatting |
| `.in_time_zone(tz)` | Time-zone conversion |
| `+ N.days` / `- N.hours` | Datetime arithmetic |

### List operations

| Formula | Description |
|---|---|
| `.pluck(field)` | Extract a specific field from a list |
| `.join(delimiter)` | Concatenate an array into a string |
| `.first` / `.last` | First/last element |
| `.where(condition)` | Filter by condition |
| `.map { }` | Transform |
| `.size` / `.length` | Element count |

## Formulas inside recipe JSON

```json
"input": {
  "field": "=_('data.provider.step.list').pluck('name').join(', ')"
}
```

- The `=` prefix marks formula mode
- `_('...')` references a datapill via dot notation
- Multiple formulas can be chained via method chaining

## Notes

- For unsupported Ruby methods, ask your Customer Success Manager to add them to the allow-list
- Formulas are displayed contextually based on the datapill's type
