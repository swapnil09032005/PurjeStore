Good. Keep the existing Notepad window open.

**Do not paste the earlier corrupted version.** We need to restore A.3.7 as a clean specification and keep the already-validated A.3.8 audit untouched.

However, because the full document is long, I don't want to make you risk another giant paste that could introduce encoding or truncation problems.

### Use this exact clean A.3.7 content

Replace everything currently in Notepad with the following:

````markdown
# PurjeStore — Subject-Area OLAP Model Specification

**Project:** PurjeStore — An End-to-End Data Science and Intelligent E-Commerce Decision Support System  
**Phase:** Second Power BI Approach  
**Artifact:** Controlled Subject-Area OLAP Model Specification  
**Status:** A.3.7 — Specification Baseline  
**Date:** 2026-10-03

---

## 1. Purpose

This document defines the controlled physical OLAP model contract for the second Power BI approach.

The second Power BI approach is distinct from the finalized Streamlit dashboard and existing analytical-layer architecture.

It uses validated subject-area physical packages derived from the 177 cleaned source CSVs.

This specification defines:

- approved subject areas;
- physical FACT and REFERENCE outputs;
- source-table role separation;
- source-grain preservation;
- approved model relationships;
- relationship direction;
- observed cardinality;
- multiple-path protection;
- Power BI model boundaries;
- refresh boundaries;
- source and analytical-layer preservation;
- prohibited transformations.

This document is a controlled model specification. It does not authorize unsupported KPIs, business-impact claims, machine-learning outputs, recommendations, or predictive functionality.

---

## 2. Evidence Baseline

The specification is based on the validated project evidence:

- 177 cleaned source CSVs;
- 69 formal relationship records;
- 68 resolved relationships;
- 1 dynamic/polymorphic relationship;
- 4 approved subject areas;
- 25 unique blueprint table references;
- 35 physical role-specific CSV outputs;
- 26 FACT outputs;
- 9 REFERENCE outputs;
- 13 approved dimension-to-fact physical model paths;
- 0 orphan values across approved non-null relationship values;
- source row counts preserved;
- source schemas preserved;
- source values preserved;
- source grain preserved;
- 0 source mutations;
- 0 analytical-layer mutations;
- 0 joins during physical construction;
- 0 aggregations;
- 0 deduplications;
- 0 invented columns;
- 0 KPI creation;
- 0 ML output;
- 0 177-table flat join.

The physical package was validated under A.3.6.

---

## 3. Architecture Position

The second Power BI approach follows this controlled flow:

```text
177 Cleaned Source CSVs
        |
        v
Evidence-Based Subject-Area Selection
        |
        v
OLAP Model Integrity Audit
        |
        v
Relationship-Direction Validation
        |
        v
Controlled Physical Construction
        |
        v
35 Role-Specific Physical CSV Outputs
        |
        +-------------------+
        |                   |
        v                   v
Commerce Model       Fulfillment Model
        |                   |
        v                   v
Payments Model       Returns Model
        |
        v
Second Power BI Report
````

The physical construction layer does not perform analytical joins.

Relationships are represented at the subject-area model level.

---

## 4. Approved Subject Areas

Four subject areas are approved:

1. `Commerce_Orders_Products`
2. `Fulfillment_Shipping`
3. `Payments_Invoicing`
4. `Returns_Exchange_QC`

Customer/Account remains:

`DEFERRED / REQUIRES REVIEW`

and is not part of the approved physical package.

---

## 5. Physical Package Contract

The physical package is located under:

`Power BI Dashboard\groups_csv\`

It contains exactly 35 outputs.

### Commerce_Orders_Products

FACT:

* `fact_orders.csv`
* `fact_order_items.csv`

REFERENCE:

* `ref_product.csv`
* `ref_variants.csv`

### Fulfillment_Shipping

FACT:

* `fact_shipment_booking.csv`
* `fact_shipment_items.csv`
* `fact_shipment_status_history.csv`
* `fact_shipment_cost_breakdown.csv`
* `fact_packaging.csv`
* `fact_outbound_packaging.csv`
* `fact_delivery_challans.csv`
* `fact_einvoice_records.csv`
* `fact_eway_bill_records.csv`

REFERENCE:

* `ref_orders.csv`
* `ref_order_items.csv`
* `ref_return_request.csv`
* `ref_invoices.csv`

### Payments_Invoicing

FACT:

* `fact_payments.csv`
* `fact_payment_orders.csv`
* `fact_payment_transactions.csv`
* `fact_payment_receipts.csv`
* `fact_invoices.csv`
* `fact_delivery_challans.csv`
* `fact_einvoice_records.csv`
* `fact_eway_bill_records.csv`

REFERENCE:

* `ref_orders.csv`

### Returns_Exchange_QC

FACT:

* `fact_return_request.csv`
* `fact_exchange_request.csv`
* `fact_exchange_attempt.csv`
* `fact_hub_returns.csv`
* `fact_hub_inventory_units.csv`
* `fact_rtv_batch.csv`
* `fact_rtv_batch_item.csv`

REFERENCE:

* `ref_orders.csv`
* `ref_shipment_booking.csv`

A source table may therefore appear in multiple physical roles. This is intentional role separation, not duplication of analytical evidence.

---

## 6. Grain Protection

Every physical output preserves its source-table grain.

The construction contract does not permit:

* aggregation;
* deduplication;
* row collapsing;
* fact merging;
* synthetic rows;
* invented columns;
* invented measures;
* source corrections;
* unsupported semantic transformations.

Special validated keys include:

* `fact_shipment_status_history.csv` → `shipment_status_history_id`
* `fact_shipment_cost_breakdown.csv` → `shipment_cost_breakdown_id`

All 35 physical outputs passed source-grain validation during A.3.6.

---

## 7. Commerce_Orders_Products

### FACT

`fact_orders.csv` ← `orders.csv`

`fact_order_items.csv` ← `order_items.csv`

### REFERENCE

`ref_product.csv` ← `product.csv`

`ref_variants.csv` ← `variants.csv`

### Approved relationships

```text
ref_product.product_id
        |
        v
fact_order_items.productId
```

```text
ref_variants.id
        |
        v
fact_order_items.variantId
```

Both paths:

* use unique reference keys;
* have zero non-null FK orphans;
* are observed MANY_TO_ONE relationships from fact rows to reference keys.

### Blocked relationship

```text
fact_order_items.order_id
        |
        v
fact_orders.order_id
```

This source relationship is not promoted into the Power BI model because both outputs are FACT roles.

The source relationship remains evidence; it is not discarded.

---

## 8. Fulfillment_Shipping

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

### Approved relationships

```text
ref_orders.order_id
        |
        v
fact_shipment_booking.order_id
```

Observed: MANY_TO_ONE, zero non-null FK orphans.

```text
ref_order_items.order_item_id
        |
        v
fact_shipment_items.order_item_id
```

Observed: MANY_TO_ONE, zero non-null FK orphans.

```text
ref_return_request.return_request_id
        |
        v
fact_delivery_challans.reference_return_id
```

Observed: approved path, zero non-null FK orphans.

```text
ref_invoices.id
        |
        v
fact_delivery_challans.reference_invoice_id
```

Observed: approved path, zero non-null FK orphans.

Direct FACT-to-FACT relationships are blocked.

---

## 9. Payments_Invoicing

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

### Approved relationships

```text
ref_orders.order_id
        |
        v
fact_payment_orders.order_id
```

Observed: ONE_TO_ONE, zero non-null FK orphans.

```text
ref_orders.order_id
        |
        v
fact_invoices.order_id
```

Observed: MANY_TO_ONE, zero non-null FK orphans.

```text
ref_orders.order_id
        |
        v
fact_einvoice_records.order_id
```

Observed: approved path, zero non-null FK orphans.

Direct FACT-to-FACT payment/invoicing relationships are blocked.

---

## 10. Returns_Exchange_QC

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

### Approved relationships

```text
ref_orders.order_id
        |
        v
fact_return_request.order_id
```

Observed: ONE_TO_ONE, zero non-null FK orphans.

```text
ref_orders.order_id
        |
        v
fact_exchange_request.old_order_id
```

Observed: ONE_TO_ONE, zero non-null FK orphans.

```text
ref_shipment_booking.shipment_booking_id
        |
        v
fact_return_request.shipment_id
```

Observed: ONE_TO_ONE, zero non-null FK orphans.

```text
ref_shipment_booking.shipment_booking_id
        |
        v
fact_exchange_request.replacement_inbound_shipment_id
```

Observed:

* 25 non-null;
* 2 null;
* 0 orphan.

The two null values are preserved and are not treated as orphan violations.

Direct FACT-to-FACT relationships are blocked.

---

## 11. Relationship Direction

Source evidence uses:

```text
CHILD.FK -> PARENT.KEY
```

The Power BI model uses the corresponding parent/reference-to-child/fact structure:

```text
PARENT.KEY -> CHILD.FK
```

Example:

```text
Source evidence:

order_items.productId
        ->
product.product_id


Power BI model:

ref_product.product_id
        ->
fact_order_items.productId
```

The source evidence direction must not be confused with the Power BI model navigation direction.

---

## 12. Cardinality

Cardinality is based on validated source evidence.

Approved paths include observed:

* `ONE_TO_ONE`;
* `MANY_TO_ONE`.

The model must not claim stronger cardinality than the evidence supports.

Column-name similarity alone is never sufficient to create a relationship.

---

## 13. Shared Source Table Strategy

The following eight source tables require subject-area role separation:

1. `delivery_challans`
2. `einvoice_records`
3. `eway_bill_records`
4. `invoices`
5. `order_items`
6. `orders`
7. `return_request`
8. `shipment_booking`

Role strategy:

### orders

* FACT in Commerce;
* REFERENCE in Fulfillment;
* REFERENCE in Payments;
* REFERENCE in Returns.

### order_items

* FACT in Commerce;
* REFERENCE in Fulfillment.

### invoices

* REFERENCE in Fulfillment;
* FACT in Payments.

### shipment_booking

* FACT in Fulfillment;
* REFERENCE in Returns.

### return_request

* REFERENCE in Fulfillment;
* FACT in Returns.

The remaining shared tables are similarly separated by subject-area role.

No physical FACT output from one subject area is reused directly as a FACT output in another subject area.

---

## 14. Multiple-Path Protection

The source evidence contains multiple possible paths.

The Power BI model must not automatically activate all source relationships.

Only the 13 explicitly approved dimension/reference-to-fact paths are part of this contract.

Blocked behavior includes:

* automatic alternate relationships;
* uncontrolled bidirectional relationships;
* ambiguous active paths;
* relationship inference from column names;
* uncontrolled cross-subject fact paths.

---

## 15. Power BI Model Boundary

The four subject areas are independent model boundaries for the purpose of this second Power BI approach.

Conceptually:

```text
Commerce Model
        X
Fulfillment Model
        X
Payments Model
        X
Returns Model
```

The `X` means that no uncontrolled cross-subject FACT model is authorized.

The implementation must not create a giant 177-table model.

---

## 16. KPI Boundary

Current approved KPI count:

`0`

Therefore this model does not authorize creation of:

* revenue KPIs;
* profit KPIs;
* ROI;
* CLV;
* churn;
* conversion;
* retention;
* customer-value scores;
* forecasting;
* recommendation scores;
* fraud scores;
* unsupported business-impact measures.

A source numeric field does not automatically become a KPI.

Any future measure requires separate semantic and evidence validation.

---

## 17. ML Boundary

Current selected ML problems:

`0`

Current ML outputs:

`0`

This Power BI model therefore does not contain:

* predictions;
* forecasts;
* recommendation outputs;
* churn scores;
* fraud scores;
* SHAP outputs;
* model-generated scores.

The ML boundary remains closed.

---

## 18. Customer / Account Boundary

Customer/Account remains:

`DEFERRED / REQUIRES REVIEW`

It is not part of the approved 35-output physical package.

No Customer/Account Power BI model is authorized under A.3.7.

---

## 19. Source Preservation

The following remain protected:

* original SQL/recovery sources;
* cleaned source CSVs;
* validated analytical datasets.

The 35-output physical package is a downstream controlled projection.

No source CSV may be:

* overwritten;
* deduplicated;
* aggregated;
* manually corrected;
* merged into a giant table.

A.3.6 confirmed:

* source mutation: 0;
* source schemas preserved;
* source values preserved;
* source row counts preserved;
* source grain preserved.

---

## 20. Analytical Layer Boundary

The existing 26 analytical datasets are not modified by this second Power BI approach.

No physical subject-area output is promoted into the existing analytical layer.

No new analytical join is added.

No existing Streamlit dashboard architecture is modified.

No ML scope is reopened.

---

## 21. Lineage

The controlled lineage is:

```text
Cleaned Source CSV
        |
        v
Validated Subject-Area Role
        |
        v
Physical FACT / REFERENCE CSV
        |
        v
Power BI Subject-Area Model
        |
        v
Power BI Report
```

Example:

```text
orders.csv
   |
   +--> Commerce_Orders_Products/fact_orders.csv
   |
   +--> Fulfillment_Shipping/ref_orders.csv
   |
   +--> Payments_Invoicing/ref_orders.csv
   |
   +--> Returns_Exchange_QC/ref_orders.csv
```

Each projection remains traceable to its source.

---

## 22. Refresh Contract

A future controlled refresh must validate:

1. source availability;
2. expected schema;
3. expected grain;
4. role assignment;
5. source-only projection;
6. row count;
7. schema;
8. candidate keys;
9. approved relationship paths;
10. null/orphan behavior;
11. source preservation;
12. atomic publication.

A failed validation must not silently publish a replacement package.

---

## 23. Forbidden Transformations

The following are explicitly blocked:

* FACT-to-FACT joins;
* FACT aggregation during physical construction;
* FACT deduplication;
* source mutation;
* analytical-layer mutation;
* invented columns;
* invented business semantics;
* unsupported KPI creation;
* ML output;
* Customer/Account promotion;
* giant 177-table flat join;
* automatic multiple-path relationships;
* uncontrolled cross-subject FACT reuse;
* silent schema repair;
* silent grain changes.

---

## 24. A.3.6 Validation Evidence

A.3.6 produced:

```text
Cleaned source CSVs: 177 / 177
Subject areas: 4 / 4
Physical CSV outputs: 35 / 35
FACT outputs: 26 / 26
REFERENCE outputs: 9 / 9
Row counts preserved: PASS
Schemas preserved: PASS
Values preserved: PASS
Source grain preserved: PASS
Physical paths: 13 / 13
Orphan FK values: 0
Returns nullable path: 25 non-null, 2 null, 0 orphan
Source CSVs changed: 0
Analytical CSVs changed: 0
Joins: 0
Aggregations: 0
Deduplication: 0
Invented columns: 0
KPI creation: 0
ML output: 0
177-table flat join: 0
```

Final A.3.6 status:

`PASS — CONTROLLED PHYSICAL PACKAGE VALIDATED`

---

## 25. A.3.7 Specification Decision

The validated evidence supports controlled construction of the second Power BI subject-area model.

Approved:

* `Commerce_Orders_Products`
* `Fulfillment_Shipping`
* `Payments_Invoicing`
* `Returns_Exchange_QC`

Physical package:

* 35 outputs;
* 26 FACT;
* 9 REFERENCE.

Approved relationships:

* 13 dimension/reference-to-fact paths.

Deferred:

* Customer/Account.

Blocked:

* FACT-to-FACT modeling;
* uncontrolled cross-subject FACT reuse;
* giant 177-table flat joins;
* automatic multiple-path relationships;
* unsupported KPI creation;
* ML output;
* analytical-layer modification;
* source mutation.

Final A.3.7 status:

`PASS — SPECIFICATION BASELINE ESTABLISHED`

---

## 26. Relationship and Model Contract Summary

The model construction must satisfy all of the following:

```text
177 cleaned sources preserved
35 physical outputs validated
26 FACT outputs
9 REFERENCE outputs
13 approved model paths
0 approved orphan values
0 source mutation
0 analytical-layer mutation
0 aggregation
0 deduplication
0 invented columns
0 approved KPIs
0 selected ML problems
0 giant 177-table join
Customer/Account deferred
FACT-to-FACT modeling blocked
Multiple-path auto-modeling blocked
```

Any violation requires stopping the construction process and returning to evidence review.

---

## 27. Next Controlled Stage

A.3.7 is the specification baseline.

The already completed A.3.8 stage is the readiness audit.

Therefore the next stage after A.3.8 is:

**A.3.9 — Power BI Model Construction Specification**

The controlled sequence is:

```text
A.3.6  Physical Package Construction       PASS / CLOSED
   |
A.3.7  OLAP Model Specification             BASELINE
   |
A.3.8  OLAP Readiness Audit                 PASS / CLOSED
   |
A.3.9  Model Construction Specification
   |
A.3.10 Power BI Model Construction
   |
A.3.11 Model / Relationship Validation
   |
A.3.12 Report / Page Construction
   |
A.3.13 Visual / Behavioral QA
   |
A.3.14 Refresh / Reproducibility Validation
   |
A.3.15 Documentation Integration
   |
A.3.16 Final Git / Project Closure
```

No later stage is authorized merely because files exist. Each stage requires its own validation evidence.

---

## 28. Final Principle

The second Power BI approach is an evidence-bounded subject-area OLAP reporting model.

The project prefers:

```text
validated smaller model
        over
unsupported larger model
```

Every promoted model element must remain traceable to:

```text
Source Evidence
      ->
Validated Relationship / Grain
      ->
Approved Model Contract
      ->
Power BI Model
      ->
Report
```