# PurjeStore — A.3.8 Power BI OLAP Readiness Audit

## Status

**FINAL STATUS: PASS — A.3.8 POWER BI OLAP READINESS APPROVED**

This document records the completed read-only readiness audit for the second Power BI approach: controlled subject-area / OLAP reporting.

The audit confirms that the physically constructed subject-area package is sufficiently validated for the next controlled stage: **A.3.9 — Power BI Model Construction Specification**.

No Power BI semantic model, report, visual, KPI, or analytical dataset was created or modified by this audit.

---

# 1. Purpose

A.3.8 validates whether the physically constructed subject-area CSV package satisfies the approved OLAP model contract defined in A.3.7.

The audit specifically verifies:

- physical package completeness
- source preservation
- output count
- FACT / REFERENCE role counts
- source-native grain
- candidate key uniqueness and non-null behavior
- approved Power BI relationship paths
- referential integrity
- nullable relationship behavior
- transformation restrictions
- analytical-layer protection
- subject-area boundaries
- readiness for controlled Power BI model construction

The audit is read-only.

---

# 2. Evidence Baseline

The audit operates against the established PurjeStore evidence baseline.

| Evidence item | Validated value |
|---|---:|
| Cleaned source CSVs | 177 |
| Physical subject-area outputs | 35 |
| FACT outputs | 26 |
| REFERENCE outputs | 9 |
| Approved Power BI relationships | 13 |
| Subject areas approved | 4 |
| Approved final business KPIs | 0 |
| Selected ML problems | 0 |
| Analytical joins in this construction | 0 |

The original source CSV universe remains protected.

The existing 26-dataset analytical layer remains outside this construction.

---

# 3. Approved Subject Areas

Four subject areas were approved for controlled OLAP construction.

| Subject Area | FACT outputs | REFERENCE outputs | Total |
|---|---:|---:|---:|
| Commerce_Orders_Products | 2 | 2 | 4 |
| Fulfillment_Shipping | 9 | 4 | 13 |
| Payments_Invoicing | 8 | 1 | 9 |
| Returns_Exchange_QC | 7 | 2 | 9 |
| **Total** | **26** | **9** | **35** |

Customer/Account was not promoted into the physical OLAP package.

Its status remains:

**DEFERRED / REQUIRES REVIEW**

This preserves the previously established evidence boundary around customer/account and wallet grain.

---

# 4. Physical Package

The physical package is located at:

```text
PowerBI Dashboard\groups_csv\
````

The package contains exactly 35 CSV outputs.

## 4.1 Commerce_Orders_Products

### FACT

* `fact_orders.csv`
* `fact_order_items.csv`

### REFERENCE

* `ref_product.csv`
* `ref_variants.csv`

## 4.2 Fulfillment_Shipping

### FACT

* `fact_shipment_booking.csv`
* `fact_shipment_items.csv`
* `fact_shipment_status_history.csv`
* `fact_shipment_cost_breakdown.csv`
* `fact_packaging.csv`
* `fact_outbound_packaging.csv`
* `fact_delivery_challans.csv`
* `fact_einvoice_records.csv`
* `fact_eway_bill_records.csv`

### REFERENCE

* `ref_orders.csv`
* `ref_order_items.csv`
* `ref_return_request.csv`
* `ref_invoices.csv`

## 4.3 Payments_Invoicing

### FACT

* `fact_payments.csv`
* `fact_payment_orders.csv`
* `fact_payment_transactions.csv`
* `fact_payment_receipts.csv`
* `fact_invoices.csv`
* `fact_delivery_challans.csv`
* `fact_einvoice_records.csv`
* `fact_eway_bill_records.csv`

### REFERENCE

* `ref_orders.csv`

## 4.4 Returns_Exchange_QC

### FACT

* `fact_return_request.csv`
* `fact_exchange_request.csv`
* `fact_exchange_attempt.csv`
* `fact_hub_returns.csv`
* `fact_hub_inventory_units.csv`
* `fact_rtv_batch.csv`
* `fact_rtv_batch_item.csv`

### REFERENCE

* `ref_orders.csv`
* `ref_shipment_booking.csv`

---

# 5. Grain Validation

Every physical output was checked against its source-native grain contract.

All 35 physical outputs passed.

## 5.1 Commerce

| Output           | Grain key       | Rows |
| ---------------- | --------------- | ---: |
| fact_orders      | `order_id`      |  374 |
| fact_order_items | `order_item_id` |  374 |
| ref_product      | `product_id`    |   87 |
| ref_variants     | `id`            |  112 |

## 5.2 Fulfillment

| Output                       | Grain key                    |  Rows |
| ---------------------------- | ---------------------------- | ----: |
| fact_shipment_booking        | `shipment_booking_id`        |   348 |
| fact_shipment_items          | `shipment_item_id`           |   352 |
| fact_shipment_status_history | `shipment_status_history_id` | 1,746 |
| fact_shipment_cost_breakdown | `shipment_cost_breakdown_id` |    10 |
| fact_packaging               | `id`                         |   134 |
| fact_outbound_packaging      | `outbound_packaging_id`      |   132 |
| fact_delivery_challans       | `id`                         |    18 |
| fact_einvoice_records        | `id`                         |    33 |
| fact_eway_bill_records       | `id`                         |    71 |
| ref_orders                   | `order_id`                   |   374 |
| ref_order_items              | `order_item_id`              |   374 |
| ref_return_request           | `return_request_id`          |    63 |
| ref_invoices                 | `id`                         |   320 |

## 5.3 Payments

| Output                    | Grain key    | Rows |
| ------------------------- | ------------ | ---: |
| fact_payments             | `payment_id` |  337 |
| fact_payment_orders       | `id`         |  348 |
| fact_payment_transactions | `id`         |  191 |
| fact_payment_receipts     | `id`         |  246 |
| fact_invoices             | `id`         |  320 |
| fact_delivery_challans    | `id`         |   18 |
| fact_einvoice_records     | `id`         |   33 |
| fact_eway_bill_records    | `id`         |   71 |
| ref_orders                | `order_id`   |  374 |

## 5.4 Returns

| Output                   | Grain key               | Rows |
| ------------------------ | ----------------------- | ---: |
| fact_return_request      | `return_request_id`     |   63 |
| fact_exchange_request    | `exchange_request_id`   |   27 |
| fact_exchange_attempt    | `exchange_attempt_id`   |   10 |
| fact_hub_returns         | `hub_return_id`         |   67 |
| fact_hub_inventory_units | `hub_inventory_unit_id` |  237 |
| fact_rtv_batch           | `rtv_batch_id`          |   20 |
| fact_rtv_batch_item      | `rtv_batch_item_id`     |   21 |
| ref_orders               | `order_id`              |  374 |
| ref_shipment_booking     | `shipment_booking_id`   |  348 |

### Grain conclusion

All 35 outputs have a validated source-native candidate grain key that is:

* non-null
* unique
* consistent with the source row count

**Result: PASS — 35/35 grain validations.**

---

# 6. Approved Power BI Relationship Contract

The relationship evidence has two directions that must not be confused.

### Source evidence direction

```text
CHILD.FK → PARENT.KEY
```

### Power BI model direction

```text
PARENT.KEY → CHILD.FK
```

The second form is the direction used for the controlled semantic model.

All 13 approved Power BI relationships passed referential validation.

---

# 7. Approved Relationships

## 7.1 Commerce_Orders_Products

```text
ref_product.product_id
    →
fact_order_items.productId
```

* Non-null FK values: 374
* Orphans: 0
* Result: PASS

```text
ref_variants.id
    →
fact_order_items.variantId
```

* Non-null FK values: 374
* Orphans: 0
* Result: PASS

---

# 8. Fulfillment_Shipping Relationships

```text
ref_orders.order_id
    →
fact_shipment_booking.order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_order_items.order_item_id
    →
fact_shipment_items.order_item_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_return_request.return_request_id
    →
fact_delivery_challans.reference_return_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_invoices.id
    →
fact_delivery_challans.reference_invoice_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

---

# 9. Payments_Invoicing Relationships

```text
ref_orders.order_id
    →
fact_payment_orders.order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_orders.order_id
    →
fact_invoices.order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_orders.order_id
    →
fact_einvoice_records.order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

---

# 10. Returns_Exchange_QC Relationships

```text
ref_orders.order_id
    →
fact_return_request.order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_orders.order_id
    →
fact_exchange_request.old_order_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_shipment_booking.shipment_booking_id
    →
fact_return_request.shipment_id
```

* Null FK values: 0
* Orphans: 0
* Result: PASS

```text
ref_shipment_booking.shipment_booking_id
    →
fact_exchange_request.replacement_inbound_shipment_id
```

* Null FK values: 2
* Non-null values: 25
* Orphans: 0
* Result: PASS

The two null values are valid nullable relationship behavior and are not treated as orphan records.

---

# 11. Relationship Summary

| Area        | Approved paths | Passed |
| ----------- | -------------: | -----: |
| Commerce    |              2 |      2 |
| Fulfillment |              4 |      4 |
| Payments    |              3 |      3 |
| Returns     |              4 |      4 |
| **Total**   |         **13** | **13** |

**Result: PASS — 13/13 approved Power BI relationships.**

---

# 12. Shared Source Table Protection

Some source tables participate in more than one subject area.

The following eight source tables require role separation rather than unrestricted physical reuse:

* `delivery_challans`
* `einvoice_records`
* `eway_bill_records`
* `invoices`
* `order_items`
* `orders`
* `return_request`
* `shipment_booking`

The physical package therefore uses subject-area-specific FACT and REFERENCE projections.

This avoids treating a source FACT table as a universal cross-subject semantic object.

---

# 13. Fact-to-Fact Protection

Fact-to-fact relationships are explicitly blocked.

Examples include:

* `order_items → orders`
* `shipment_items → shipment_booking`
* `packaging → shipment_booking`
* payment fact-to-fact relationships
* returns fact-to-fact relationships
* other source relationships that would create uncontrolled fact chains

The presence of a source relationship does not automatically authorize a Power BI relationship.

A relationship must satisfy the approved semantic model contract.

---

# 14. Multiple-Path Protection

The subject-area package contains shared business entities such as orders, invoices, shipment bookings, and return requests.

Because these entities can create multiple possible paths, automatic relationship discovery must not be allowed to determine the semantic model.

The Power BI model must use only the explicitly approved relationship list.

No additional relationship may be created merely because Power BI detects matching column names.

---

# 15. Transformation Restrictions

A.3.8 confirms that the physical construction did not perform prohibited analytical transformations.

| Operation                 | Result |
| ------------------------- | ------ |
| Analytical joins          | 0      |
| Aggregation               | 0      |
| Deduplication             | 0      |
| Invented columns          | 0      |
| KPI creation              | 0      |
| ML output                 | 0      |
| 177-table flat join       | 0      |
| Source mutation           | 0      |
| Analytical-layer mutation | 0      |

The physical package preserves source-native rows and schemas.

---

# 16. Source Preservation

The audit confirmed:

```text
Cleaned source CSVs changed: 0
Analytical CSVs changed: 0
```

The physical subject-area package is therefore an additional controlled reporting layer.

It does not replace or mutate the original cleaned source layer.

---

# 17. KPI Boundary

The established PurjeStore evidence baseline contains:

```text
Approved final business KPIs = 0
```

A.3.8 does not introduce any new KPI.

Power BI model construction must therefore not invent KPI definitions simply because numeric fields exist.

Any future metric requires its own evidence and semantic approval.

---

# 18. ML Boundary

The established project evidence contains:

```text
Selected ML problems = 0
```

A.3.8 does not introduce:

* prediction
* forecasting
* recommendation
* churn modeling
* fraud modeling
* classification
* regression
* clustering output
* SHAP or model explanations

The second Power BI approach remains descriptive/evidence-bounded.

---

# 19. Customer / Account Boundary

Customer/Account was not promoted into the physical subject-area OLAP package.

Status:

```text
DEFERRED / REQUIRES REVIEW
```

This decision remains unchanged.

No customer/account dimension has been invented merely to make the Power BI model appear more complete.

---

# 20. Final Safety Gates

The following controls passed:

| Safety gate                       | Result |
| --------------------------------- | ------ |
| No uncontrolled join operation    | PASS   |
| No aggregation                    | PASS   |
| No deduplication                  | PASS   |
| No KPI creation                   | PASS   |
| No ML output                      | PASS   |
| No source mutation                | PASS   |
| No analytical-layer mutation      | PASS   |
| No 177-table flat join            | PASS   |
| Grain protection                  | PASS   |
| Relationship direction protection | PASS   |
| Referential integrity             | PASS   |
| Nullable relationship handling    | PASS   |
| Fact-to-fact blocking             | PASS   |
| Multiple-path protection          | PASS   |
| Subject-area separation           | PASS   |

---

# 21. A.3.8 Validation Gate Summary

```text
Validation gates: 28
Failed gates: 0
Errors: 0
Warnings: 0
```

Final result:

```text
PASS — A.3.8 POWER BI OLAP READINESS APPROVED.
```

---

# 22. Read-Only Audit Confirmation

The A.3.8 audit itself created no analytical modifications.

```text
Files created by audit: 0
Files modified by audit: 0
Files deleted by audit: 0
Source CSVs changed: 0
Analytical CSVs changed: 0
```

The only durable artifact for this milestone is this documentation record.

---

# 23. Readiness Decision

The evidence supports controlled progression to the next stage.

### Approved

```text
Physical subject-area package
        ↓
Validated source-native grains
        ↓
Validated reference keys
        ↓
13 approved semantic relationships
        ↓
Referential integrity PASS
        ↓
Power BI OLAP model construction
```

### Not approved

```text
Automatic relationship discovery
        ↓
Uncontrolled cross-subject fact joins
        ↓
Fact-to-fact modeling
        ↓
Unapproved KPI creation
        ↓
ML outputs
        ↓
Customer/account promotion without evidence
        ↓
177-table flat model
```

---

# 24. Transition to A.3.9

A.3.8 is closed.

The next controlled stage is:

**A.3.9 — Power BI Model Construction Specification**

A.3.9 must define the exact Power BI semantic-model construction procedure before the actual `.pbix` report/model is built.

A.3.9 must remain consistent with:

* the A.3.7 OLAP model specification
* this A.3.8 readiness audit
* the 35 physical outputs
* the 26 FACT outputs
* the 9 REFERENCE outputs
* the 13 approved relationships
* the source-native grain contract
* the fact-to-fact restriction
* the multiple-path restriction
* the zero-KPI boundary
* the zero-ML boundary
* the deferred Customer/Account boundary

No actual Power BI report construction is authorized by this document alone.

---

# 25. Final Milestone Statement

**A.3.8 — POWER BI OLAP READINESS: CLOSED / PASS**

The physical subject-area package has passed the defined readiness gates and is ready for controlled Power BI semantic-model construction specification.

The project may proceed to A.3.9 only after this A.3.8 documentation is validated and committed according to the project's milestone closure procedure.
