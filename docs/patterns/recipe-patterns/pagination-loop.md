# Pagination loop

## When to use

| Condition | Applies |
|---|---|
| The API caps the number of records returned at once | Yes |
| You need to retrieve all records | Yes |
| You are calling a rate-limited API | Optional |

## Recipe shape

### Offset-based

```
[Context] location that needs to fetch all records
    |
    |-- [Variable] initialize results list variable (columns = fields needed downstream)
    |
    +-- [Repeat while] fetched count == page_size (more pages remain)
        |
        +-- [Handle Errors]
            |-- Monitor block
            |   |-- [Action] fetch records from API (offset = index * page_size)
            |   +-- [Variable] append fetched records to results
            +-- Error block
                |-- (retry: rate limit mitigation)
                +-- [Action] error notification
```

### Token-based

```
[Context] location that needs to fetch all records
    |
    |-- [Variable] initialize results list variable (columns = fields needed downstream)
    |-- [Variable] initialize next_page_token (empty string or initial token)
    |
    +-- [Repeat while] next_page_token is present
        |
        +-- [Handle Errors]
            |-- Monitor block
            |   |-- [Action] fetch records from API (page_token = next_page_token)
            |   |-- [Variable] append fetched records to results
            |   +-- [Variable] update next_page_token with the response value
            +-- Error block
                |-- (retry: rate limit mitigation)
                +-- [Action] error notification
```

## Step composition

### Offset-based

Because Repeat while can compute the offset as `index * page_size`, you do not need a separate offset variable.

| # | keyword / Provider | Action | Purpose |
|---|---|---|---|
| N | workato_variable | create_list | Initialize the results list variable (columns = fields needed downstream) |
| N+1 | repeat_while | | End condition: fetched count < page_size |
| N+1.1 | try | | Error handling |
| N+1.1.1 | External service | search / list | Fetch records with offset = index * page_size |
| N+1.1.2 | workato_variable | append_list | Append fetched records to results |
| N+1.1.3 | catch | | Retry + notification on rate-limit errors |

### Token-based

Store next_page_token in a variable and update it each loop iteration.

| # | keyword / Provider | Action | Purpose |
|---|---|---|---|
| N | workato_variable | create_list | Initialize the results list variable (columns = fields needed downstream) |
| N+1 | workato_variable | create_variable | Initialize next_page_token |
| N+2 | repeat_while | | End condition: next_page_token is empty |
| N+2.1 | try | | Error handling |
| N+2.1.1 | External service | search / list | Fetch records with page_token = next_page_token |
| N+2.1.2 | workato_variable | append_list | Append fetched records to results |
| N+2.1.3 | workato_variable | update_variable | Update next_page_token with the response value |
| N+2.1.4 | catch | | Retry + notification on rate-limit errors |

## Design decision points

| Decision | Options | Criteria |
|---|---|---|
| Pagination scheme | Offset / token | Depends on API spec. Token-based offers stronger data consistency |
| Page size | API maximum / smaller value | If rate limits are strict, use a smaller value to reduce load per request |
| End condition | fetched count < page_size / next_token is empty / reached total count | Use information the API response makes available |
| Error handling | try/catch + retry / break the loop | Rate limits (429) can recover via retry; consider breaking the loop for other errors |
| Processing fetched data | Process inside the loop / process all after fetching | Data volume and memory. Large data is safer processed inside the loop |

## Known caveats

- **Repeat while caps at 50,000 iterations** - if the data volume exceeds page_size x 50,000, a different approach is needed
- **Repeat while is do-while** - it runs at least once. The API is called once even when there are zero records
- **Rate limit (429) mitigation**: set retry inside try/catch. Match the retry interval to the API's limits
- **Offset drift**: if records are added or deleted on the source during the loop, offsets drift, causing duplicates or omissions. Prefer token-based for critical data sync
- **List variable columns**: the columns defined in `create_list` need not include every API `output_fields`; only the columns required downstream are enough. Including unnecessary columns clutters datapill choices
- **Empty response handling**: some APIs return an empty array on the last page. Choose between `fetched count == 0` and `fetched count < page_size` as the end condition based on the API's behavior

## References

- `docs/logic/loops.md` - Repeat while / Repeat for each syntax
- `docs/logic/error-handling.md` - Handle Errors / retry syntax
