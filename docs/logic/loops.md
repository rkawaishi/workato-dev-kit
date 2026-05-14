# Loops (Repeat)

## Repeat for each

Official: https://docs.workato.com/en/recipes/repeat-for-each.html

Repeats actions for each item in a list.

### JSON structure

```json
{
  "number": N,
  "keyword": "foreach",
  "as": "foreach",
  "clear_scope": false,
  "input": {},
  "source": "#{_dp('{\"pill_type\":\"output\",...,\"path\":[\"list_field\"]}')}",
  "block": [ /* actions per item */ ]
}
```

### Key points

- `source`: the list to iterate over (datapill)
- `clear_scope: false` keeps the parent scope's variables accessible
- To reference the current item inside the loop: `provider: "foreach"`, `line: "foreach"`, `path: ["fieldName"]`
- When using an IF condition inside a loop, set "Clear step output" to Yes

### Repeat for each in batches

For processing large data in batches:
- Batch size is configurable (default 100)
- Suited to high-throughput data transfer

## Repeat while

Official: https://docs.workato.com/en/recipes/loops.html

Repeats actions while a condition is true (do-while: runs at least once).

### Common use cases

- **Offset pagination**: fetch sequentially via `Index * page_size`
- **Page token**: loop while a next-page token exists
- **Fixed count**: run n times via `Index < (n-1)`
- **Conditional**: repeat until a specific result is reached

### Limits

- Iteration cap of **50,000**
- Always design an exit condition to prevent infinite loops
