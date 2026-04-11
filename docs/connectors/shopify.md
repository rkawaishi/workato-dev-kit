# Shopify コネクタ

Provider: `shopify`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New customer | `new_customer` | - |  |
| New order | `new_order` | - |  |
| New product | `new_product` | - |  |
| New product (GraphQL) | `new_product_graphql` | - |  |
| New/updated abandoned checkout (GraphQL) | `new_updated_abandoned_checkout_graphql` | - |  |
| New/updated customer | `new_updated_customer_batch` | Yes |  |
| New/updated draft order | `new_updated_draft_order_batch` | Yes |  |
| New/updated object (GraphQL) | `new_updated_object_graphql_batch` | Yes |  |
| New/updated order | `new_updated_order_batch` | Yes |  |
| New/updated product | `new_updated_product_batch` | Yes |  |
| New/updated product (GraphQL) | `new_updated_product_graphql` | - |  |
| New/updated product variant (GraphQL) | `new_updated_product_variant_graphql` | - |  |
| New product variant | `new_variant` | - |  |
| New/updated abandoned checkout | `updated_abandoned_checkout` | - |  |
| New/updated customer | `updated_customer` | - |  |
| New/updated order | `updated_order` | - |  |
| New/updated product | `updated_product` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add metafield to objects | `add_metafield_to_object` | - |  |
| Add metafield to store | `add_metafield_to_store` | - |  |
| Adjust inventory level | `adjust_inventory_level` | - |  |
| Attach file to a product variant using GraphQL | `attach_file_graphql` | Yes |  |
| Calculate refund transaction | `calculate_refund` | - |  |
| Cancel a fulfillment | `cancel_fulfillment` | - |  |
| Connect inventory item to location | `connect_inventory_levels` | - |  |
| Create customer | `create_customer` | - |  |
| Create draft order | `create_draft_order` | - |  |
| Create File using GraphQL | `create_file_graphql` | Yes |  |
| Create fulfillment (Old) | `create_fulfillment` | - |  [deprecated] |
| Create fulfillment | `create_fulfillment_for_fulfillment_order` | - |  |
| Create object using GraphQL | `create_object_graphql` | - |  |
| Create order | `create_order` | - |  |
| Create product | `create_product` | - |  |
| Create product image | `create_product_image` | - |  |
| Create product variant | `create_product_variant` | - |  |
| Create refund transaction | `create_refund` | - |  |
| Create transaction | `create_transaction` | - |  |
| Delete draft order | `delete_draft_order` | - |  |
| Delete object by ID using GraphQL | `delete_object_graphql` | Yes |  |
| Delete product image | `delete_product_image` | - |  |
| Detach file from a product variant using GraphQL | `detach_file_graphql` | Yes |  |
| Get store metafields | `fetch_store_metafields` | Yes |  |
| Search customers | `find_customers` | Yes |  |
| Get draft order by ID | `get_draft_order` | - |  |
| List draft orders | `get_draft_orders_list` | - |  |
| Get fulfillment by ID | `get_fulfillment_by_id` | - |  |
| Get object by ID using GraphQL | `get_object_graphql` | - |  |
| Get object metafields | `get_object_metafields` | Yes |  |
| Get order by ID | `get_order_by_id` | - |  |
| Get product image by ID | `get_product_image` | - |  |
| Get transactions | `get_transaction_by_order` | Yes |  |
| List fulfillment orders for an order | `list_fulfillment_orders_for_order` | Yes |  |
| List fulfillments by fulfillment order | `list_fulfillments_by_fulfillment_order` | Yes |  |
| List locations | `list_locations` | Yes |  |
| List product images | `list_product_images` | - |  |
| List product variants | `list_variants` | Yes |  |
| Reorder product media using GraphQL | `reorder_product_media` | Yes |  |
| Search object using GraphQL | `search_object_graphql` | Yes |  |
| Search orders | `search_order` | Yes |  |
| Search products | `search_product` | Yes |  |
| Send email invoice | `send_invoice` | - |  |
| Set inventory level | `set_inventory_level` | - |  |
| Update customer | `update_customer` | - |  |
| Update draft order | `update_draft_order` | - |  |
| Update SKU | `update_inventory_item` | - |  |
| Update object using GraphQL | `update_object_graphql` | - |  |
| Update object metafield | `update_object_metafield` | - |  |
| Update order | `update_order` | - |  |
| Update product | `update_product` | - |  |
| Update product image | `update_product_image` | - |  |
| Update product variant | `update_product_variant` | - |  |
| Update store metafield | `update_store_metafield` | - |  |
| Update tracking information of a fulfillment | `update_tracking_information_fulfillment` | - |  |
