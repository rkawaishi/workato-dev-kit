# Shopify recipes

Provider value to use in every step: `shopify`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "shopify"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (17)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer` | New customer | - |
| `new_order` | New order | - |
| `new_product` | New product | - |
| `new_product_graphql` | New product (GraphQL) | - |
| `new_updated_abandoned_checkout_graphql` | New/updated abandoned checkout (GraphQL) | - |
| `new_updated_customer_batch` | New/updated customer | yes |
| `new_updated_draft_order_batch` | New/updated draft order | yes |
| `new_updated_object_graphql_batch` | New/updated object (GraphQL) | yes |
| `new_updated_order_batch` | New/updated order | yes |
| `new_updated_product_batch` | New/updated product | yes |
| `new_updated_product_graphql` | New/updated product (GraphQL) | - |
| `new_updated_product_variant_graphql` | New/updated product variant (GraphQL) | - |
| `new_variant` | New product variant | - |
| `updated_abandoned_checkout` | New/updated abandoned checkout | - |
| `updated_customer` | New/updated customer | - |
| `updated_order` | New/updated order | - |
| `updated_product` | New/updated product | - |


## Actions (55)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_metafield_to_object` | Add metafield to objects | - |
| `add_metafield_to_store` | Add metafield to store | - |
| `adjust_inventory_level` | Adjust inventory level | - |
| `attach_file_graphql` | Attach file to a product variant using GraphQL | yes |
| `calculate_refund` | Calculate refund transaction | - |
| `cancel_fulfillment` | Cancel a fulfillment | - |
| `connect_inventory_levels` | Connect inventory item to location | - |
| `create_customer` | Create customer | - |
| `create_draft_order` | Create draft order | - |
| `create_file_graphql` | Create File using GraphQL | yes |
| `create_fulfillment_for_fulfillment_order` | Create fulfillment | - |
| `create_object_graphql` | Create object using GraphQL | - |
| `create_order` | Create order | - |
| `create_product` | Create product | - |
| `create_product_image` | Create product image | - |
| `create_product_variant` | Create product variant | - |
| `create_refund` | Create refund transaction | - |
| `create_transaction` | Create transaction | - |
| `delete_draft_order` | Delete draft order | - |
| `delete_object_graphql` | Delete object by ID using GraphQL | yes |
| `delete_product_image` | Delete product image | - |
| `detach_file_graphql` | Detach file from a product variant using GraphQL | yes |
| `fetch_store_metafields` | Get store metafields | yes |
| `find_customers` | Search customers | yes |
| `get_draft_order` | Get draft order by ID | - |
| `get_draft_orders_list` | List draft orders | - |
| `get_fulfillment_by_id` | Get fulfillment by ID | - |
| `get_object_graphql` | Get object by ID using GraphQL | - |
| `get_object_metafields` | Get object metafields | yes |
| `get_order_by_id` | Get order by ID | - |
| `get_product_image` | Get product image by ID | - |
| `get_transaction_by_order` | Get transactions | yes |
| `list_fulfillment_orders_for_order` | List fulfillment orders for an order | yes |
| `list_fulfillments_by_fulfillment_order` | List fulfillments by fulfillment order | yes |
| `list_locations` | List locations | yes |
| `list_product_images` | List product images | - |
| `list_variants` | List product variants | yes |
| `reorder_product_media` | Reorder product media using GraphQL | yes |
| `search_object_graphql` | Search object using GraphQL | yes |
| `search_order` | Search orders | yes |
| `search_product` | Search products | yes |
| `send_invoice` | Send email invoice | - |
| `set_inventory_level` | Set inventory level | - |
| `update_customer` | Update customer | - |
| `update_draft_order` | Update draft order | - |
| `update_inventory_item` | Update SKU | - |
| `update_object_graphql` | Update object using GraphQL | - |
| `update_object_metafield` | Update object metafield | - |
| `update_order` | Update order | - |
| `update_product` | Update product | - |
| `update_product_image` | Update product image | - |
| `update_product_variant` | Update product variant | - |
| `update_store_metafield` | Update store metafield | - |
| `update_tracking_information_fulfillment` | Update tracking information of a fulfillment | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_fulfillment` | Create fulfillment (Old) | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
