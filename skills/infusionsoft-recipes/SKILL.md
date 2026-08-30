# Infusionsoft recipes

Provider value to use in every step: `infusionsoft`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "infusionsoft"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (14)

| Internal name | Title | Batch |
|---|---|---|
| `new_company` | New company | - |
| `new_contact` | New contact | - |
| `new_invoice` | New order | - |
| `new_opportunity` | New opportunity | - |
| `new_payment_v2` | New payment | - |
| `new_tag_assigned_to_contact` | New tag assigned to contact | - |
| `new_updated_contact` | New/updated contact | - |
| `new_updated_invoice` | New/updated order | - |
| `new_updated_note` | New/updated note | - |
| `new_updated_product` | New/updated product | - |
| `product_created` | Product created | - |
| `updated_contact` | Updated contact | - |
| `updated_invoice` | Updated order | - |
| `updated_opportunity` | Updated opportunity | - |


## Actions (37)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_line_item_to_order` | Add line item to Order | - |
| `add_payment_to_invoice` | Add payment to order | - |
| `add_tax_to_order` | Add tax to order | - |
| `assign_tag_to_contact` | Assign tag to contact | - |
| `charge_invoice` | Charge an invoice | - |
| `create_company` | Create company | - |
| `create_contact` | Create contact | - |
| `create_note` | Create note | - |
| `create_opportunity` | Create opportunity | - |
| `create_order` | Create order | - |
| `create_product` | Create product | - |
| `create_task` | Create Task | - |
| `get_company` | Get company details by ID | - |
| `get_contact` | Get contact details by ID | - |
| `get_invoice` | Get invoice by ID | - |
| `get_pay_plan` | Get payment plan by Invoice ID | - |
| `get_payment_by_id` | Get payment by ID | - |
| `get_payments` | Get payments by Invoice ID | - |
| `get_product` | Get product details by ID | - |
| `make_marketable_contact` | Make contact marketable | - |
| `search_companies` | Search companies | yes |
| `search_contact` | Search contacts | yes |
| `search_credit_cards` | Search credit cards | yes |
| `search_invoices` | Search invoices | yes |
| `search_order_items` | Search order items | yes |
| `search_orders` | Search orders | yes |
| `search_product` | Search products | yes |
| `search_tags` | Search tags | yes |
| `search_tags_by_contact_id` | Search tags by contact ID | yes |
| `search_user` | Search users | yes |
| `update_company` | Update company | - |
| `update_contact` | Update contact | - |
| `update_note` | Update note | - |
| `update_opportunity` | Update opportunity | - |
| `update_order` | Update order | - |
| `update_product` | Update product | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_payment` | New payment | - |
| `new_product` | New product | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
