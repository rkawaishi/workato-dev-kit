# Error handling

Official: https://docs.workato.com/en/recipes/steps.html

## Handle Errors step

Consists of two blocks:

```
Handle errors
  ├── Monitor block — actions to monitor
  │     ├── action 1
  │     ├── action 2
  │     └── ...
  └── Error block — actions on error
        ├── retry settings (count + interval)
        └── recovery actions
```

### Behaviour

1. All actions in the **Monitor block** succeed → Error block is skipped
2. An error occurs inside the Monitor block → Error block executes
3. If retry is configured → retry the specified number of times at the specified interval
4. All retries fail → remaining steps in the Error block execute

### Retry settings

- Retry count
- Retry interval
- Conditional retry (decide whether to retry based on a condition)

## Stop Job step

Stops recipe execution partway through.

- Mark as **Failed**: ends as a failure with an error message
- Mark as **Successful**: ends as a successful run

### Use cases

- Early termination when business-logic validation fails
- Defensive termination when required data is missing

## Recipe Functions

Call another recipe to reuse logic.

Official: https://docs.workato.com/en/connectors/recipe-functions.html

- Share logic across recipes
- Pass input parameters and receive a result
- Centralise maintenance

### How to create

1. Create a new recipe and choose "Recipe function" as the trigger
2. Define the Input Schema (JSON) — parameters received from the caller
3. Define the Response Schema (JSON) — data returned to the caller
4. Build the logic inside the recipe

### How to call

1. Add a "Call recipe" action in the caller recipe
2. Select the target Recipe function
3. Map datapills to the Input Schema fields
4. Response datapills become available to subsequent steps

> **Note**: the legacy Callable recipes connector is deprecated. Use the Recipe functions connector for new work.

## `try` keyword (JSON representation)

In recipe JSON, `keyword: "try"` denotes an error handling block (try/catch pattern). It is the JSON representation of the UI's Monitor/Error blocks.

- When a step inside the try block raises an error, control transfers to the catch block (error handler)
