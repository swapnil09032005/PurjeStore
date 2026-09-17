# PurjeStore Database Relationship Architecture

## Document Control

| Property | Value |
|---|---|
| Project | PurjeStore |
| Milestone | Milestone 2 — Relationship & Domain Mapping |
| Status | Complete — relationship validation record |
| Database | `purjestore` |
| DBMS | MariaDB 10.4.32 |
| Host | `127.0.0.1` |
| Port | `3308` |
| Database objects | 178 |
| Base tables | 177 |
| Views | 1 |
| Raw CSV working sources | 177 |

---

## 1. Purpose

This document records the relationship architecture established during PurjeStore Milestone 2.

The objective was to determine which relationships can safely support later data-quality work, analytical datasets, business analytics, machine learning, dashboards, and decision-support components.

The recovered source database and raw CSV files remain protected. Relationship interpretation and identity normalization are to be handled in downstream analytical layers rather than by changing recovered source data.

---

## 2. Validation Method

Relationship analysis was performed in four stages.

### 2.1 Declared relationship metadata

`information_schema` was used to inspect:

- primary keys
- foreign keys
- child columns
- referenced parent tables
- referenced parent columns
- composite keys
- self-references

### 2.2 Declared foreign-key integrity

A dynamic validation procedure checked populated child FK values against their referenced parent keys.

Result:

```text
0 unmatched populated references detected
```

Therefore, no orphaned populated references were detected among the declared foreign-key relationships checked.

### 2.3 Semantic validation

Columns that appeared relational but did not have declared foreign keys were investigated against actual PurjeStore data.

Examples included vendor identity, customer identity, invoice identity, shipment/order relationships, accounting parties, daily metrics, operational audit records, and business transaction identifiers.

### 2.4 Workflow validation

Special workflows were checked separately where a simple FK interpretation could produce incorrect analytics.

Examples include:

- consolidated shipments
- exchange attempts
- shipment-level QC
- temporary product/variant records
- polymorphic references
- external identifiers
- workflow/sentinel values

---

# 3. Relationship Classification

| Classification | Meaning |
|---|---|
| `DECLARED_FK` | Explicitly declared database foreign key |
| `SEMANTIC` | Relationship supported by actual data |
| `IDENTITY_CHAIN` | Relationship requires an intermediate identity mapping |
| `SELF_REFERENCE` | Relationship to another record in the same table |
| `POLYMORPHIC` | Target depends on a type/context field |
| `BUSINESS_IDENTIFIER` | Operational/business identifier rather than an internal key |
| `EXTERNAL_IDENTIFIER` | Identifier belonging to an external/business system |
| `WORKFLOW_EXCEPTION` | Valid interpretation depends on workflow state |
| `WORKFLOW_REFERENCE` | Workflow/rule/sentinel code |
| `UNUSED_NULL` | Candidate field currently has no populated values |

---

# 4. Core Customer and User Relationships

The validated customer identity chain is:

```text
orders.userId
    -> user.user_id
    -> customers.user_id
    -> customers.customer_id
```

All six users observed as order owners were associated with customer records.

### Analytical rule

Do not treat `user.user_id` and `customers.customer_id` as interchangeable identifiers.

Customer-level analytical datasets should use the validated user-to-customer bridge.

---

# 5. Vendor Identity Relationships

## 5.1 Orders

The order vendor field is directly supported as:

```text
orders.vendor_id
    -> vendors.vendor_id
```

All 374 populated order vendor values were valid direct vendor IDs.

## 5.2 Shipment bookings

Shipment bookings use vendor user identities:

```text
shipment_booking.vendor_id
    -> user.user_id
    -> vendors.user_id
    -> vendors.vendor_id
```

The populated shipment vendor values resolved through the vendor-user relationship.

This is not the same as a direct `shipment_booking.vendor_id -> vendors.vendor_id` FK.

## 5.3 Daily product metrics

`daily_product_metrics.vendor_id` uses mixed semantics in the recovered data.

Observed values include:

- direct `vendors.vendor_id` values
- values corresponding to `vendors.user_id`

All 254 metric records were semantically resolvable.

### Analytical rule

Vendor identity must be normalized in the analytical layer before combining order, shipment, inventory, and metric datasets.

---

# 6. Order, Variant, and Product Relationships

The principal product/order chain is:

```text
orders
    -> order_items
    -> variants
    -> product
```

Validated relationships include:

```text
order_items.order_id
    -> orders.order_id

order_items.variantId
    -> variants.id

order_items.productId
    -> product.product_id

variants.product_id
    -> product.product_id
```

The order-item grain must be preserved when analyzing item-level product information.

### Analytical rule

Do not join order-level and order-item-level data without explicitly controlling the grain.

---

# 7. Shipment Relationships

The main shipment path is:

```text
orders
    |
shipment_booking
    |
shipment_items
    |
order_items
    |
orders
```

Validated relationships:

```text
shipment_items.shipment_id
    -> shipment_booking.shipment_booking_id

shipment_items.order_item_id
    -> order_items.order_item_id
```

## 7.1 Consolidated shipments

Three validated shipment groups contain order items from multiple orders:

| Shipment | Orders represented by shipment items |
|---:|---|
| 103 | 46, 47, 48 |
| 180 | 79, 80 |
| 218 | 66, 75 |

The shipment booking `order_id` therefore does not necessarily represent every order included in a shipment.

For complete shipment-to-order attribution, the authoritative analytical path is:

```text
shipment_booking
    -> shipment_items
    -> order_items
    -> orders
```

### Critical analytical rule

Do not assume `shipment_booking.order_id` is the only order represented by a shipment.

This rule is required to avoid incorrect shipment counts, order counts, and join fan-out.

---

# 8. Shipment Destination Interpretation

The field:

```text
shipment_booking.to_address_id
```

has an address-like name, but the declared relationship points to:

```text
hub_master.hub_id
```

The populated data was consistent with the hub interpretation.

### Analytical rule

Interpret this field according to the actual database relationship:

```text
shipment_booking.to_address_id
    -> hub_master.hub_id
```

Do not infer an `address.id` relationship from the column name.

---

# 9. Shipment Self-References

## 9.1 Linked outbound

```text
shipment_booking.linked_outbound_id
    -> shipment_booking.shipment_booking_id
```

Validated:

```text
125 / 125 populated references resolved
```

Referenced records include outbound and RTV workflow types.

## 9.2 Linked inbound

```text
shipment_booking.linked_inbound_id
    -> shipment_booking.shipment_booking_id
```

Validated:

```text
196 / 196 populated references resolved
```

The target is not necessarily an inbound shipment solely because the source column is named `linked_inbound_id`.

### Analytical rule

Resolve the referenced shipment record and retain its actual workflow/shipment type.

---

# 10. Payment Relationships

The payment/order bridge is:

```text
payment_orders
    -> payments
    -> orders
```

Validated:

```text
payment_orders.payment_id
    -> payments.payment_id

payment_orders.order_id
    -> orders.order_id
```

The payment/order user comparison produced:

```text
348 MATCH
0 USER_MISMATCH
0 NULL_INVOLVED
```

### Analytical rule

Use `payment_orders` as the controlled bridge between payments and orders.

---

# 11. Payment Transaction Identifier

`payments.transaction_id` was checked against `payment_transactions.id`.

The values did not behave as references to `payment_transactions.id`.

The validated receipt relationship is:

```text
payment_receipts.transactionId
    -> payments.transaction_id
```

Validated:

```text
246 / 246
```

Therefore `payments.transaction_id` is treated as a business/payment transaction identifier rather than as `payment_transactions.id`.

---

# 12. Return Relationships

The validated return path is:

```text
return_request
    -> shipment_booking
    -> shipment_items
    -> order_items
    -> product / variants
```

The return request has no direct `order_item_id`, `product_id`, or `variant_id` FK.

All 63 validated return requests could be traced to:

- one order
- one shipment
- one order item
- one product
- one variant

### Analytical rule

Use the validated shipment/item path for return product attribution.

Do not invent direct return-to-product or return-to-variant relationships.

---

# 13. Exchange Relationships

The exchange workflow contains:

```text
exchange_request
    -> old_order
    -> return
```

and, where a replacement exists:

```text
exchange_request
    -> replacement_order
    -> replacement_variant
    -> replacement_shipment
```

There were 27 exchange requests.

All 27 old-order references matched the order associated with the exchange return.

There was one exchange request without a replacement order. There were also exchange attempts without shipments.

These cases are classified as workflow-state conditions, not automatically as data errors.

### Analytical rule

An exchange request or attempt must not automatically be interpreted as a completed exchange.

---

# 14. QC Relationships

## 14.1 QC history

```text
qc_history.order_item_id
    -> order_items.order_item_id
```

Validated:

```text
274 / 274 populated references valid
```

Five QC history records had NULL `order_item_id` while retaining shipment context. These were interpreted as shipment-level QC workflow records.

## 14.2 QC results

```text
qc_results.order_item_id
    -> order_items.order_item_id
```

Validated:

```text
144 / 144 valid
```

Associated product and shipment relationships were also valid in the tested records.

---

# 15. Inventory and RTV Relationships

## 15.1 Inventory units to hub returns

```text
hub_inventory_units.return_id
    -> hub_returns.hub_return_id
```

Validated:

```text
44 / 44 populated references valid
```

Multiple inventory units can belong to the same return.

## 15.2 RTV batch

```text
rtv_batch.vendor_user_id
    -> vendors.user_id

rtv_batch.hub_id
    -> hub_master.hub_id
```

Validated:

```text
20 / 20 vendor-user references valid
20 / 20 hub references valid
```

## 15.3 RTV batch items

```text
rtv_batch_item.rtv_batch_id
    -> rtv_batch.rtv_batch_id

rtv_batch_item.hub_return_id
    -> hub_returns.hub_return_id

rtv_batch_item.hub_inventory_unit_id
    -> hub_inventory_units.hub_inventory_unit_id
```

Populated references tested during the final validation batch resolved successfully.

---

# 16. Daily Metrics Relationships

## 16.1 Product metrics

```text
daily_product_metrics.product_id
    -> product.product_id
```

Validated:

```text
254 / 254 valid
```

Vendor identity is mixed as documented in Section 5.3.

## 16.2 Category metrics

```text
daily_category_metrics.category_id
    -> category.id
```

Validated:

```text
24 / 24 valid
```

## 16.3 Vendor metrics

```text
daily_vendor_metrics.vendor_user_id
    -> vendors.user_id
```

Validated:

```text
102 / 102 valid
```

---

# 17. Event Log Relationships

Validated:

```text
event_logs.user_id
    -> user.user_id

event_logs.product_id
    -> product.product_id

event_logs.order_id
    -> orders.order_id
```

Valid populated references:

| Relationship | Valid populated references |
|---|---:|
| User | 2061 |
| Product | 977 |
| Order | 628 |

No invalid populated reference was detected in the tested relationships.

---

# 18. Notification Relationships

Validated:

```text
notification_logs.userId
    -> user.user_id
```

```text
notification_logs.notification_id
    -> notifications.id
```

Results:

```text
7140 / 7140 valid user references
7124 / 7124 valid notification references
```

The tested notification log data had no populated order or campaign values for the candidate fields.

## 18.1 Notification reference ID

`notifications.reference_id` was inspected with notification context.

It represents context-dependent workflow references rather than one universal target table.

Classification:

```text
POLYMORPHIC / BUSINESS_REFERENCE
```

### Analytical rule

Resolve `reference_id` using notification type/business context.

Do not create a universal join to a single table.

---

# 19. Accounting Relationships

## 19.1 Company

```text
journal_entries.companyId
    -> company_details.id
```

Validated:

```text
735 / 735 valid
```

## 19.2 Voucher

```text
journal_entries.voucherId
    -> journal_entry_lines.journalEntryId
```

Validated:

```text
728 / 728 populated references valid
```

This is a semantic/business relationship identified from actual data.

## 19.3 Accounting party

`journal_entry_lines.partyId` is polymorphic.

When:

```text
party_type = Vendor
```

the identifier maps to:

```text
vendors.vendor_id
```

When:

```text
party_type = Customer
```

the identifier maps to:

```text
customers.customer_id
```

One customer-party identity required the user-to-customer chain:

```text
user.user_id
    -> customers.user_id
    -> customers.customer_id
```

### Analytical rule

Resolve accounting party IDs using `party_type`.

---

# 20. Operations Audit Relationships

`ops_audit_log.entity_id` is polymorphic.

Validated mappings:

| entity_type | Target |
|---|---|
| SHIPMENT | `shipment_booking.shipment_booking_id` |
| ORDER | `orders.order_id` |
| VENDOR_BANK_ACCOUNT | `vendor_bank_detail.id` |
| QC_RULE | `qc_rules.qc_rule_id` |

Validated records:

| Entity type | Valid |
|---|---:|
| SHIPMENT | 1245 / 1245 |
| ORDER | 416 / 416 |
| VENDOR_BANK_ACCOUNT | 22 / 22 |
| QC_RULE | 8 / 8 |

Additional validated relationships:

```text
ops_audit_log.order_id
    -> orders.order_id
```

```text
1661 / 1661 populated references valid
```

```text
ops_audit_log.shipment_id
    -> shipment_booking.shipment_booking_id
```

```text
1245 / 1245 populated references valid
```

```text
ops_audit_log.performed_by_user_id
    -> user.user_id
```

```text
1168 / 1168 populated references valid
```

`ops_audit_log.performed_by_employee_id` currently has no populated values.

---

# 21. Invoice Relationships

Validated:

```text
invoices.order_id
    -> orders.order_id

invoices.vendor_id
    -> vendors.vendor_id

invoices.receipt_id
    -> payment_receipts.id

invoices.original_invoice_id
    -> invoices.id

invoices.journal_entry_id
    -> journal_entry_lines.journalEntryId
```

Validation results:

```text
320 / 320 invoice order references valid
320 / 320 invoice vendor references valid
98 / 98 invoice receipt references valid
45 / 45 invoice lineage references valid
304 / 304 invoice journal-entry references valid
```

Invoice product references were also validated against products represented by the associated order items.

---

# 22. Invoice Customer Identity

The field:

```text
invoices.customer_id
```

does not behave as a direct `customers.customer_id` relationship.

The data supports:

```text
invoices.customer_id
    -> user.user_id
    -> customers.user_id
    -> customers.customer_id
```

Validated populated invoice customer references:

```text
135 / 135
```

### Analytical rule

Use the user-to-customer identity chain for invoice customer analysis.

Do not directly join `invoices.customer_id` to `customers.customer_id`.

---

# 23. Delivery Challan Relationships

Validated:

```text
delivery_challans.order_id
    -> orders.order_id

delivery_challans.reference_return_id
    -> return_request.return_request_id

delivery_challans.reference_invoice_id
    -> invoices.id

delivery_challans.from_party_id
    -> user.user_id

delivery_challans.to_party_id
    -> user.user_id
```

All populated references tested in the 18 delivery challan records resolved successfully.

---

# 24. E-Invoice and E-Way Bill Relationships

Validated:

```text
einvoice_records.order_id
    -> orders.order_id
```

Result:

```text
33 / 33 valid
```

Validated e-way bill relationships:

```text
eway_bill_records.delivery_challan_id
    -> delivery_challans.id

eway_bill_records.einvoice_record_id
    -> einvoice_records.id

eway_bill_records.sinv_id
    -> invoices.id
```

The populated references tested were valid.

## 24.1 Transporter identifier

`eway_bill_records.transporter_id` contains GST-style/business transporter identifiers.

The populated values did not resolve to the tested internal logistics partner or user identifiers.

Classification:

```text
EXTERNAL_IDENTIFIER
```

Do not force this field into an internal FK relationship.

---

# 25. Packaging Relationships

Validated:

```text
packaging.shipment_id
    -> shipment_booking.shipment_booking_id
```

Result:

```text
130 / 130 populated references valid
```

`outbound_packaging.rule_id` contains the literal value:

```text
fallback_default
```

It did not match the tested numeric rule IDs.

Classification:

```text
WORKFLOW_REFERENCE
```

`packaging_history.rule_id` is currently NULL for all 384 records tested.

---

# 26. Temporary Product and Variant Relationships

The populated temporary-product unit fields were validated against:

```text
item_unit.id
```

The tested fields were:

```text
item_height_unit_id
item_length_unit_id
item_weight_unit_id
item_width_unit_id
package_height_unit_id
package_length_unit_id
package_weight_unit_id
package_width_unit_id
```

All populated values tested matched item-unit records.

Temporary variant lineage:

```text
variants_temp.original_variant_id
    -> variants.id
```

All populated values tested matched existing variants.

---

# 27. Other Validated Semantic Relationships

Additional validated relationships include:

```text
document_upload.vendorBankDetailId
    -> vendor_bank_detail.id
```

```text
document_upload.uploaded_by_user_id
    -> user.user_id
```

```text
document_upload.vendorId
    -> vendors.vendor_id
```

```text
accounts.companyId
    -> company_details.id
```

```text
accounts.vendorId
    -> vendors.vendor_id
```

```text
vendor_payments.vendorId
    -> vendors.vendor_id
```

```text
vendor_payments.bankAccountId
    -> vendor_bank_detail.id
```

```text
product_bulk_uploads.vendor_id
    -> vendors.vendor_id
```

The populated values tested for these relationships resolved successfully.

---

# 28. Important Empty or Unused Candidates

Some relationship-looking fields were not populated in the recovered data and therefore cannot be semantically validated at this time.

Examples:

```text
shipping_rate_cache.customer_id
shipping_rate_cache.vendor_id
frequently_bought.product_id
frequently_bought.bought_with_id
shipment_booking.pickup_id
warranty_certificates.shipment_id
warranty_certificates.shipment_item_id
packaging_history.rule_id
outbound_packaging.material_master_id
vendors.profile_review_address_id
vendors.profile_reviewed_by_id
```

These are classified as:

```text
UNUSED_NULL
```

This does not mean the relationship is invalid. It means there is currently insufficient populated data to validate it.

---

# 29. Major Exceptions and Decisions

| ID | Area | Decision |
|---|---|---|
| R001 | Vendor | Shipment vendor values use vendor-user identity mapping |
| R002 | Vendor | Daily product metrics contain mixed vendor identity semantics |
| R003 | Customer | Invoice `customer_id` behaves as a user identity |
| R004 | Shipment | Consolidated shipments may represent multiple orders |
| R005 | Shipment | `to_address_id` references `hub_master` |
| R006 | Payment | `payments.transaction_id` is a business/payment identifier |
| R007 | Notification | `reference_id` is polymorphic/context-dependent |
| R008 | Accounting | `partyId` target depends on `party_type` |
| R009 | Exchange | Some requests/attempts represent incomplete workflow states |
| R010 | QC | QC history can contain shipment-level records |
| R011 | E-Way Bill | Transporter ID is an external/business identifier |
| R012 | Packaging | `fallback_default` is a workflow/sentinel value |
| R013 | Empty candidates | NULL-only candidates remain unvalidated |

---

# 30. Analytical Join Rules

## Rule 1 — Column names do not establish relationships

A name such as `customer_id`, `vendor_id`, `transaction_id`, or `address_id` is not sufficient evidence of the target table.

## Rule 2 — Preserve the recovered schema

Do not modify the recovered database to make relationships appear more conventional.

## Rule 3 — Normalize identities downstream

Identity differences must be handled in controlled analytical mapping layers.

## Rule 4 — Respect data grain

Important grains include:

- customer
- order
- order item
- shipment
- shipment item
- payment
- payment-order
- return
- exchange request
- exchange attempt
- inventory unit
- event
- audit record

## Rule 5 — Prevent fan-out

One-to-many and many-to-many paths must be deliberately controlled before calculating metrics.

## Rule 6 — Use item-level attribution for consolidated shipments

Use:

```text
shipment_items
    -> order_items
    -> orders
```

when all orders represented by a shipment are required.

## Rule 7 — Resolve polymorphic references using context

Examples:

```text
notifications.reference_id
ops_audit_log.entity_id
journal_entry_lines.partyId
```

## Rule 8 — Keep external identifiers separate

External business identifiers should not automatically become internal foreign keys.

## Rule 9 — Distinguish NULL from invalid

A NULL relationship value means no value is currently recorded. It does not prove that a relationship is invalid.

## Rule 10 — Keep source data immutable

Cleaning and identity normalization belong in downstream layers.

---

# 31. Relationship Architecture for Later Project Stages

The validated relationship layer feeds later work as:

```text
Recovered Source
      |
      v
Relationship Metadata
      |
      v
FK Integrity Validation
      |
      v
Semantic Validation
      |
      v
Identity Mapping
      |
      v
Workflow Rules
      |
      v
Controlled Analytical Grain
      |
      +------> EDA / Business Analytics
      |
      +------> BI / Dashboard
      |
      +------> Feature Engineering / ML
```

This architecture is intended to prevent unsupported joins and incorrect KPI calculations.

---

# 32. Milestone 2 Validation Summary

| Area | Status |
|---|---|
| Relationship metadata | Complete |
| Declared FK integrity | Complete |
| Customer/user identity | Complete |
| Vendor identity | Complete |
| Product/variant relationships | Complete |
| Order relationships | Complete |
| Shipment relationships | Complete |
| Consolidated shipment semantics | Documented |
| Payment relationships | Complete |
| Payment transaction identifier | Classified |
| Return relationships | Complete |
| Exchange relationships | Complete |
| QC relationships | Complete |
| Inventory/RTV relationships | Complete |
| Daily metrics | Complete |
| Event logs | Complete |
| Notifications | Complete |
| Accounting | Complete |
| Operations audit | Complete |
| Invoice/document relationships | Complete |
| External identifiers | Classified |
| Polymorphic relationships | Classified |
| Empty candidates | Documented |
| Relationship-risk review | Complete |

---

# 33. Milestone Decision

The relationship validation work identified no critical unresolved relationship that prevents the project from proceeding to data-quality analysis.

Important semantic exceptions have been documented instead of silently normalized.

Therefore:

```text
MILESTONE 2 — RELATIONSHIP & DOMAIN MAPPING
STATUS: COMPLETE
```

The next milestone is:

```text
MILESTONE 3 — DATA QUALITY & CLEANING
```

Milestone 3 must begin with a measured quality baseline before any cleaning transformation is applied.

---

# Appendix A — Core Relationship Chains

## Customer

```text
orders.userId
    -> user.user_id
    -> customers.user_id
    -> customers.customer_id
```

## Order/Product

```text
orders
    -> order_items
    -> variants
    -> product
```

## Shipment/Order

```text
shipment_booking
    -> shipment_items
    -> order_items
    -> orders
```

## Shipment Vendor

```text
shipment_booking.vendor_id
    -> user.user_id
    -> vendors.user_id
    -> vendors.vendor_id
```

## Invoice Customer

```text
invoices.customer_id
    -> user.user_id
    -> customers.user_id
    -> customers.customer_id
```

## Return

```text
return_request
    -> shipment_booking
    -> shipment_items
    -> order_items
    -> product / variants
```

## Payment

```text
payment_orders
    -> payments
    -> orders
```

## Accounting Party

```text
journal_entry_lines.partyId
    -> vendors.vendor_id
OR
    -> customers.customer_id
```

Target depends on `party_type`.

## Operations Audit

```text
ops_audit_log.entity_id
    -> target determined by entity_type
```

---

# Appendix B — Source Protection Rules

1. Raw CSV files remain read-only.
2. Original SQL recovery sources remain protected.
3. Credentials must not be stored in project documentation.
4. PII must not be unnecessarily copied into analytical outputs.
5. Relationship validation must not modify source data.
6. Identity normalization must occur in downstream analytical layers.
7. Analytical joins must use validated relationship logic.
8. Unsupported relationships must not be invented.

---

# Appendix C — Evidence Basis

The relationship architecture is based on:

- recovered database metadata
- declared primary and foreign keys
- dynamic FK integrity checks
- populated-value semantic checks
- identity mapping checks
- workflow-specific validations
- actual recovered PurjeStore record behavior

The distinction between formally declared relationships and semantically validated relationships is intentionally preserved for reproducibility and academic defensibility.
