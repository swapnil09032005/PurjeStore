# PurjeStore Relationship Validation Summary

## Document control

| Property | Value |
|---|---|
| Project | PurjeStore |
| Milestone | Milestone 2 — Relationship & Domain Mapping |
| Status | Validation complete; documentation checkpoint pending |
| Database | `purjestore` |
| DBMS | MariaDB 10.4.32 |
| Host | `127.0.0.1` |
| Port | `3308` |
| Database objects | 178 |
| Base tables | 177 |
| Views | 1 |
| Raw CSV working sources | 177 |
| Validation scope | Declared foreign keys plus high-value semantic relationships |
| Primary evidence | Live database metadata and populated PurjeStore records |

---

## 1. Executive summary

Milestone 2 established the relationship and domain architecture required before analytical dataset construction.

The work was deliberately performed in two layers:

1. **Declared relationship validation** — database foreign keys were checked against their referenced keys using populated child values.
2. **Semantic relationship validation** — important relationships without declared foreign keys, polymorphic identifiers, identity bridges, external identifiers, workflow references, and naming ambiguities were tested against actual PurjeStore data.

The resulting evidence supports the following working conclusion:

> No populated declared foreign-key relationship tested by the automated integrity procedure produced an unmatched parent reference. Important non-FK relationships were separately investigated and classified according to their observed semantics.

This does **not** mean every column in the database is a formal foreign key, nor that every currently NULL candidate has an empirically proven target. Those distinctions are documented explicitly.

---

## 2. Validation approach

### 2.1 Metadata inspection

The database metadata was inspected through `information_schema` to identify:

- primary keys
- foreign keys
- child columns
- referenced tables
- referenced columns
- composite keys
- self-references
- candidate relationships not represented by declared foreign keys

### 2.2 Automated foreign-key integrity test

A dynamic SQL procedure was used to iterate through declared foreign keys and test populated child values against their referenced parent keys.

The test condition was conceptually:

```sql
child_fk IS NOT NULL
AND referenced_parent_key IS NULL
```

The resulting validation showed:

- declared FK orphan count: **0 detected**
- populated declared FK relationships with unmatched parent references: **none detected**

### 2.3 Semantic validation

Declared foreign keys alone were insufficient to describe the full PurjeStore data model. Additional checks were therefore performed for fields that were:

- ID-like but lacked declared FKs
- polymorphic
- business identifiers
- identity bridges
- workflow references
- externally supplied identifiers
- ambiguous by column name
- used in populated analytical or operational tables

### 2.4 Evidence rule

A relationship was considered validated only when the available populated data provided evidence supporting the proposed interpretation.

A NULL field was not treated as an invalid relationship merely because its target could not be tested.

---

## 3. Core validated relationship architecture

### Customer and user

The observed order/customer structure supports:

```text
user
  |
  +--> customers.user_id
  |
  +--> orders.userId
```

Observed order-owning users with customer records were successfully mapped.

For analytical work, customer identity should therefore be resolved through the appropriate user/customer bridge rather than assuming that every user ID is itself a customer ID.

### Orders

The primary order structure is:

```text
user
  |
  +--> orders
          |
          +--> order_items
                  |
                  +--> variants
                  |      |
                  |      +--> product
                  |
                  +--> product
```

Orders also reference billing and shipping addresses:

```text
orders.billingAddressId  -> address.id
orders.shippingAddressId -> address.id
```

Address ownership validation showed alignment with the user owning the order.

### Product and variant

The validated product hierarchy is:

```text
product
   ^
   |
variants
   ^
   |
order_items
```

`order_items.productId` was also checked against the product associated with its variant. The observed records consistently aligned.

---

## 4. Vendor identity architecture

Vendor identity requires special handling because PurjeStore contains both direct vendor identifiers and vendor-user identifiers.

### Direct vendor relationship

```text
orders.vendor_id -> vendors.vendor_id
```

This was validated across the populated orders.

### Vendor represented through user identity

Some operational fields use:

```text
vendor value -> user.user_id
                 |
                 +--> vendors.user_id
```

This was observed for populated fields including:

- `shipment_booking.vendor_id`
- `hub_inventory.vendor_id`
- `daily_vendor_metrics.vendor_user_id`
- `rtv_batch.vendor_user_id`

### Mixed semantics

`daily_product_metrics.vendor_id` contains values whose interpretation is mixed in the current data:

- some values resolve directly to `vendors.vendor_id`
- other values resolve through `vendors.user_id`

Therefore, analytical integration must normalize vendor identity through a controlled mapping layer rather than blindly joining every vendor-like field to `vendors.vendor_id`.

---

## 5. Shipment architecture

The main shipment path is:

```text
orders
   |
   +--> shipment_booking
           |
           +--> shipment_items
                   |
                   +--> order_items
                           |
                           +--> variants
                           +--> product
```

### Consolidated shipment rule

Three shipments were identified where `shipment_booking.order_id` did not equal every order represented by their shipment items.

The affected shipment bookings were:

- shipment 103
- shipment 180
- shipment 218

Their descriptions and item-level relationships showed that these were consolidated shipments containing items from multiple orders.

Therefore:

> `shipment_booking.order_id` must not be treated as the exclusive order attribution for a consolidated shipment.

For shipment-level analytical attribution, the authoritative path is:

```text
shipment_booking
    -> shipment_items
    -> order_items
    -> orders
```

This prevents incorrect one-order assumptions and avoids analytical fan-out.

---

## 6. Shipment destination ambiguity

`shipment_booking.to_address_id` has an address-like name, but its declared relationship points to:

```text
shipment_booking.to_address_id -> hub_master.hub_id
```

The value `1` creates a numeric collision because `address.id = 1` also exists.

The target table defined by the database relationship and semantic investigation is `hub_master`, not `address`.

Therefore:

```text
to_address_id = hub_master.hub_id
```

must be preserved in the analytical semantic mapping.

---

## 7. Payment architecture

The validated payment structure includes:

```text
orders
   |
payment_orders
   |
payments
   |
payment_receipts
```

`payment_orders` records were validated for payment/order user consistency.

### Payment transaction identifier

`payments.transaction_id` does **not** behave as `payment_transactions.id`.

Instead, populated `payment_receipts.transactionId` values matched `payments.transaction_id`.

Therefore:

```text
payment_receipts.transactionId
    -> payments.transaction_id
```

is the observed relationship.

`payments.transaction_id` should be treated as a business/payment transaction identifier rather than being forced into the `payment_transactions.id` key.

---

## 8. Return architecture

The validated return path is:

```text
return_request
    |
    +--> orders
    |
    +--> shipment_booking
            |
            +--> shipment_items
                    |
                    +--> order_items
                            |
                            +--> variants
                            +--> product
```

All 63 return requests could be traced through their shipment to exactly one order item, product, and variant in the validated dataset.

The database does not require an invented direct:

```text
return_request -> product
```

or:

```text
return_request -> variant
```

relationship.

The correct analytical path is through shipment and shipment item.

---

## 9. Exchange architecture

The exchange structure is:

```text
exchange_request
    |
    +--> old_order
    |
    +--> return_request
    |
    +--> replacement_order
    |
    +--> exchange_attempt
```

There were:

- 27 exchange requests
- 10 exchange attempts
- 63 return requests

All exchange requests had validated old-order and return relationships.

Most replacement-order references were populated. One exchange request did not yet have a replacement order.

Some attempts also had no shipment.

These states were classified as workflow-state conditions rather than automatically being treated as data corruption.

---

## 10. Inventory and RTV

Validated relationships include:

```text
rtv_batch.vendor_user_id
    -> vendors.user_id

rtv_batch.hub_id
    -> hub_master.hub_id

rtv_batch_item.rtv_batch_id
    -> rtv_batch.rtv_batch_id

rtv_batch_item.hub_return_id
    -> hub_returns.hub_return_id

rtv_batch_item.hub_inventory_unit_id
    -> hub_inventory_units.hub_inventory_unit_id

hub_inventory_units.return_id
    -> hub_returns.hub_return_id
```

The populated references tested in these relationships resolved successfully.

---

## 11. Event logs and notification logs

### Event logs

Populated references were validated for:

```text
event_logs.user_id
event_logs.product_id
event_logs.order_id
```

All populated references tested resolved to their intended entities.

### Notification logs

The validated notification-log relationships include:

```text
notification_logs.userId
    -> user.user_id

notification_logs.notification_id
    -> notifications.id
```

Both populated relationships resolved successfully.

### Notification reference ID

`notifications.reference_id` is different.

Its values are workflow/context dependent and may refer to different business entities. Numeric collisions also exist.

Therefore it is classified as:

```text
POLYMORPHIC_BUSINESS_REFERENCE
```

and must be interpreted using notification type/context rather than as one universal foreign key.

---

## 12. Accounting architecture

Accounting includes both declared relationships and semantic party relationships.

### Company identity

```text
journal_entries.companyId
    -> company_details.id
```

was validated.

### Voucher relationship

```text
journal_entries.voucherId
    -> journal_entry_lines.journalEntryId
```

was validated as a semantic/business relationship.

### Party identity

`journal_entry_lines.partyId` is polymorphic.

Its interpretation depends on `party_type`:

```text
party_type = Vendor
    -> vendors.vendor_id

party_type = Customer
    -> customers.customer_id
```

One observed customer identity requires the user/customer bridge because the numeric party value also corresponds to a user ID rather than a direct customer ID.

Analytical code must therefore use `party_type` when resolving accounting party identity.

---

## 13. Operations audit architecture

`ops_audit_log.entity_id` is polymorphic.

Observed entity types included:

| Entity type | Target |
|---|---|
| `SHIPMENT` | `shipment_booking.shipment_booking_id` |
| `ORDER` | `orders.order_id` |
| `VENDOR_BANK_ACCOUNT` | `vendor_bank_detail.id` |
| `QC_RULE` | `qc_rules.qc_rule_id` |

All observed entity IDs resolved against their corresponding target.

Additional audit fields were validated for:

```text
ops_audit_log.order_id
    -> orders.order_id

ops_audit_log.shipment_id
    -> shipment_booking.shipment_booking_id

ops_audit_log.performed_by_user_id
    -> user.user_id
```

`performed_by_employee_id` was currently unpopulated.

---

## 14. Invoice and financial-document architecture

Validated invoice relationships include:

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

### Invoice customer identity

`invoices.customer_id` is an important semantic exception.

The observed populated values align with:

```text
invoices.customer_id
    -> user.user_id
        -> customers.user_id
            -> customers.customer_id
```

Therefore it should not be directly joined to `customers.customer_id`.

---

## 15. Delivery and statutory-document relationships

Validated relationships include:

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

einvoice_records.order_id
    -> orders.order_id

eway_bill_records.delivery_challan_id
    -> delivery_challans.id

eway_bill_records.einvoice_record_id
    -> einvoice_records.id

eway_bill_records.sinv_id
    -> invoices.id
```

`eway_bill_records.transporter_id` was classified as an external/business identifier because its populated values include GST-style transporter identifiers and did not resolve to the tested internal logistics/user keys.

---

## 16. Packaging and operational workflow references

`packaging.shipment_id` was validated against:

```text
shipment_booking.shipment_booking_id
```

`outbound_packaging.rule_id` contains the workflow value:

```text
fallback_default
```

and does not behave as a numeric foreign-key reference to the tested rule tables.

Therefore it is classified as a workflow/business rule code.

---

## 17. Temporary product and variant architecture

Temporary product and variant structures were validated where populated.

Examples include:

```text
variants_temp.original_variant_id
    -> variants.id
```

and populated temporary product unit references:

```text
product_temp.*_unit_id
    -> item_unit.id
```

These relationships support lineage between temporary/staging records and their corresponding reference entities.

---

## 18. Relationships that are currently unused or unvalidated

Some candidate relationship fields could not be empirically validated because the relevant field is entirely NULL or the source table is empty.

Examples include:

- several shipping-rate cache identifiers
- some coupon relationships
- some payment-refund relationships because the table is empty
- some packaging rule references that are entirely NULL
- warranty shipment identifiers that are currently unpopulated
- various temporary or workflow identifiers without populated observations

These are documented as **currently unvalidated/unused**, not as errors.

Future data refreshes may make these relationships testable.

---

## 19. Exception register

The detailed exception register is maintained separately in:

```text
RELATIONSHIP_EXCEPTIONS.csv
```

It currently contains 13 documented decisions covering:

1. vendor identity mapping
2. mixed vendor semantics
3. invoice customer identity
4. consolidated shipments
5. shipment destination naming ambiguity
6. payment transaction business identifiers
7. polymorphic notification references
8. polymorphic accounting party identifiers
9. exchange workflow states
10. shipment-level QC records
11. external transporter identifiers
12. packaging workflow references
13. currently NULL/unvalidated candidates

---

## 20. Analytical join rules

The relationship work establishes the following rules for later analytical dataset construction.

### Rule 1 — Do not join every ID-like column automatically

Column names such as `customer_id`, `vendor_id`, `address_id`, or `party_id` are not sufficient evidence of target identity.

### Rule 2 — Preserve declared database relationships

The analytical layer must not rewrite the source database schema.

Semantic normalization should happen in controlled analytical mapping tables or transformations.

### Rule 3 — Resolve mixed vendor identities before aggregation

Vendor-like fields must first be normalized to a stable vendor identity.

### Rule 4 — Use item-level shipment attribution

For consolidated shipments, use:

```text
shipment_booking
 -> shipment_items
 -> order_items
 -> orders
```

rather than assuming `shipment_booking.order_id` represents every order.

### Rule 5 — Resolve polymorphic fields using their discriminator

Examples:

- accounting `party_type`
- operations `entity_type`
- notification type/context

### Rule 6 — Do not convert business identifiers into false primary-key relationships

Examples:

- `payments.transaction_id`
- `eway_bill_records.transporter_id`
- `notifications.reference_id`

### Rule 7 — Preserve NULL workflow states

NULL values may represent incomplete, pending, optional, or not-applicable workflow states.

They must not automatically be converted into errors.

### Rule 8 — Avoid analytical fan-out

Many-to-many and multi-order relationships must be handled at their appropriate grain before KPI aggregation.

---

## 21. Relationship evidence files

This validation checkpoint is supported by the following project files:

```text
docs/database/relationship_validation/
│
├── DATABASE_RELATIONSHIP_ARCHITECTURE.md
├── VALIDATED_RELATIONSHIPS.csv
├── RELATIONSHIP_EXCEPTIONS.csv
└── RELATIONSHIP_VALIDATION_SUMMARY.md
```

### File responsibilities

| File | Purpose |
|---|---|
| `DATABASE_RELATIONSHIP_ARCHITECTURE.md` | Detailed relationship architecture and methodology |
| `VALIDATED_RELATIONSHIPS.csv` | Structured validated relationship register |
| `RELATIONSHIP_EXCEPTIONS.csv` | Structured exception and semantic-decision register |
| `RELATIONSHIP_VALIDATION_SUMMARY.md` | Milestone checkpoint summary |

---

## 22. Relationship validation outcome

### Confirmed

- Declared foreign-key integrity showed no detected populated orphan references.
- Core customer/user relationships were validated.
- Core order/product/variant relationships were validated.
- Vendor identity paths were investigated and documented.
- Shipment and shipment-item relationships were validated.
- Consolidated shipment behavior was identified and documented.
- Payment relationships were validated.
- Return relationships were validated.
- Exchange workflow relationships were investigated.
- Inventory and RTV relationships were validated.
- Event and notification log relationships were validated.
- Accounting party semantics were investigated.
- Operations audit polymorphism was resolved.
- Invoice and statutory-document relationships were validated.
- External identifiers were separated from internal database keys.

### Not claimed

This milestone does **not** claim that every ID-like column in the schema is a foreign key.

It also does not claim that currently NULL or empty-table relationships are permanently invalid or meaningless.

The conclusions apply to the PurjeStore database state that was actually inspected during this milestone.

---

## 23. Milestone 2 decision

**Milestone 2 — Relationship & Domain Mapping is considered analytically complete.**

The relationship evidence required to begin controlled data-quality and cleaning work has been documented.

The next milestone is:

> **Milestone 3 — Data Quality & Cleaning**

However, Milestone 3 should begin only after this four-file documentation set is locally verified and committed as a milestone checkpoint.

---

## 24. Reproducibility requirements

Future relationship changes should be validated against the database again rather than manually editing this documentation.

When the source database changes materially:

1. rerun declared-FK metadata extraction
2. rerun FK integrity validation
3. rerun affected semantic validations
4. compare results with the current relationship register
5. update exceptions where evidence changes
6. record the decision in the project decision log

The relationship documentation is therefore an evidence record, not a substitute for the validation process.

---

## 25. Final status

**Milestone 2 relationship evidence: COMPLETE**

**Documentation checkpoint: READY FOR FINAL VERIFICATION**

**Next controlled milestone: Milestone 3 — Data Quality & Cleaning**

Do not begin cleaning transformations until the relationship documentation checkpoint has been committed.
