Perfect. The empty A.3.9 file exists at the correct path.

Now we can populate it. **Do not stage it yet.** Replace the empty file with the following complete specification.

This document deliberately separates **what has already been validated** from **how Power BI will later implement it**. It does not authorize actual Power BI construction yet.

````markdown
# PurjeStore — Subject-Area Power BI Model Construction Specification

**Project:** PurjeStore — An End-to-End Data Science and Intelligent E-Commerce Decision Support System
**Phase:** Second Power BI Approach
**Artifact:** Controlled Subject-Area Power BI Model Construction Specification
**Status:** A.3.9 — Model Construction Specification
**Date:** 2026-10-03

---

## 1. Purpose

This document defines the controlled construction specification for implementing the validated PurjeStore subject-area OLAP packages in Power BI.

It is the construction-stage specification between:

- the validated physical subject-area package;
- the approved OLAP model contract;
- the Power BI semantic/model layer;
- and the later Power BI report/page construction.

This document does not create new analytical evidence.

It does not replace the existing PurjeStore analytical layer.

It does not modify the finalized Streamlit dashboard.

It does not reopen the relationship-validation work.

It does not authorize unsupported KPIs, predictive models, customer scoring, forecasting, recommendation systems, churn analysis, fraud detection, profitability analysis, or other unsupported business claims.

The purpose of A.3.9 is to define exactly how the already-approved physical package will be represented in Power BI while preserving:

- source lineage;
- physical table grain;
- validated relationship evidence;
- subject-area boundaries;
- cardinality;
- filtering behavior;
- evidence-bounded semantics;
- reproducibility;
- and controlled refresh behavior.

---

# 2. Architecture Position

The second Power BI approach is a separate reporting approach from the finalized Streamlit dashboard.

The controlled lineage is:

```text
177 Cleaned Source CSVs
        |
        v
Evidence-Based Subject-Area Validation
        |
        v
A.3.6 Controlled Physical Subject-Area Package
        |
        v
35 Physical CSV Outputs
        |
        v
A.3.7 OLAP Model Specification
        |
        v
A.3.8 OLAP Readiness Audit
        |
        v
A.3.9 Power BI Model Construction Specification
        |
        v
A.3.10 Power BI Model Construction
        |
        v
A.3.11 Model / Relationship Validation
        |
        v
A.3.12 Power BI Report / Page Construction
        |
        v
A.3.13 Visual / Behavioral QA
        |
        v
A.3.14 Refresh / Reproducibility Validation
        |
        v
Final Power BI Subject-Area Report
````

A.3.9 therefore defines the implementation contract but does not itself construct the Power BI model.

---

# 3. Evidence Baseline

The following evidence is already closed and must be treated as the construction baseline.

| Evidence item                             | Validated result |
| ----------------------------------------- | ---------------: |
| Cleaned source CSVs                       |              177 |
| Formal relationship records               |               69 |
| Resolved relationships                    |               68 |
| Dynamic/polymorphic relationships         |                1 |
| Approved subject areas                    |                4 |
| Blueprint table references                |        25 unique |
| Physical role outputs                     |               35 |
| FACT outputs                              |               26 |
| REFERENCE outputs                         |                9 |
| Approved dimension/reference → fact paths |               13 |
| Approved orphan values                    |                0 |
| Customer/Account subject area             |         Deferred |
| Approved KPIs                             |                0 |
| Selected ML problems                      |                0 |
| Constructed analytical joins              |                0 |
| Source mutation                           |                0 |
| Analytical-layer mutation                 |                0 |

The physical package was validated in A.3.6.

The model contract was documented in A.3.7.

OLAP readiness was validated in A.3.8.

A.3.9 must not contradict or silently expand those decisions.

---

# 4. Approved Subject Areas

Exactly four subject areas are approved for Power BI model construction.

## 4.1 Commerce / Orders & Products

Internal subject-area identifier:

```text
Commerce_Orders_Products
```

Purpose:

Represent the validated order and product/catalog evidence without creating unsupported commercial KPIs.

---

## 4.2 Fulfillment / Shipping

Internal subject-area identifier:

```text
Fulfillment_Shipping
```

Purpose:

Represent shipment, shipment-item, shipment-status, packaging, delivery, e-invoice, e-way bill, and approved reference evidence.

---

## 4.3 Payments / Invoicing

Internal subject-area identifier:

```text
Payments_Invoicing
```

Purpose:

Represent validated payment, payment-order, transaction, receipt, invoice, delivery-challan, e-invoice, and e-way-bill evidence.

---

## 4.4 Returns / Exchange / QC

Internal subject-area identifier:

```text
Returns_Exchange_QC
```

Purpose:

Represent validated return, exchange, hub-return, inventory-unit, RTV, and related reference evidence.

---

# 5. Deferred Subject Area

Customer / Account remains deferred.

It must not be promoted into the Power BI OLAP model merely because customer-related fields appear in source tables.

The previous evidence established that the Customer / Account subject area requires additional review.

Therefore:

```text
Customer / Account
STATUS = DEFERRED
```

No Power BI customer/account model may be constructed under A.3.10 unless a later formally approved evidence change authorizes it.

---

# 6. Physical Power BI Source Boundary

Power BI must consume the controlled physical subject-area package:

```text
C:\Users\ASUS\Desktop\PurjeStore\Power BI Dashboard\groups_csv\
```

Power BI must not directly consume the original 177 cleaned source CSVs for the controlled second approach.

The physical package contains:

```text
Commerce_Orders_Products\
Fulfillment_Shipping\
Payments_Invoicing\
Returns_Exchange_QC\
```

The package contains exactly 35 physical CSV outputs.

The physical package is downstream of the validated subject-area construction contract.

---

# 7. Physical Output Contract

The approved physical package contains:

## Commerce_Orders_Products

```text
fact_orders.csv
fact_order_items.csv
ref_product.csv
ref_variants.csv
```

## Fulfillment_Shipping

```text
fact_shipment_booking.csv
fact_shipment_items.csv
fact_shipment_status_history.csv
fact_shipment_cost_breakdown.csv
fact_packaging.csv
fact_outbound_packaging.csv
fact_delivery_challans.csv
fact_einvoice_records.csv
fact_eway_bill_records.csv

ref_orders.csv
ref_order_items.csv
ref_return_request.csv
ref_invoices.csv
```

## Payments_Invoicing

```text
fact_payments.csv
fact_payment_orders.csv
fact_payment_transactions.csv
fact_payment_receipts.csv
fact_invoices.csv
fact_delivery_challans.csv
fact_einvoice_records.csv
fact_eway_bill_records.csv

ref_orders.csv
```

## Returns_Exchange_QC

```text
fact_return_request.csv
fact_exchange_request.csv
fact_exchange_attempt.csv
fact_hub_returns.csv
fact_hub_inventory_units.csv
fact_rtv_batch.csv
fact_rtv_batch_item.csv

ref_orders.csv
ref_shipment_booking.csv
```

No additional physical table may be introduced during A.3.10 without a formally approved change to the A.3.9 specification.

---

# 8. Power BI Model Boundary

Each subject area must be treated as a controlled semantic model boundary.

The preferred implementation is subject-area isolation.

The model must not be constructed as one uncontrolled 35-table flat model.

The following principle is mandatory:

```text
Subject Area
    |
    +-- approved reference/dimension tables
    |
    +-- approved fact tables
    |
    +-- approved relationships
```

There must be no automatic cross-subject-area fact network.

---

# 9. Commerce Model Construction

## 9.1 Tables

The Commerce model contains:

```text
fact_orders
fact_order_items
ref_product
ref_variants
```

Roles:

```text
FACT
    fact_orders
    fact_order_items

REFERENCE
    ref_product
    ref_variants
```

---

## 9.2 Approved Relationships

### Relationship C1

```text
ref_product.product_id
        |
        v
fact_order_items.productId
```

Power BI interpretation:

```text
One product
    →
Many order-item records
```

Expected cardinality:

```text
1 : *
```

Filter direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

### Relationship C2

```text
ref_variants.id
        |
        v
fact_order_items.variantId
```

Power BI interpretation:

```text
One variant
    →
Many order-item records
```

Expected cardinality:

```text
1 : *
```

Filter direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## 9.3 Explicit Commerce Constraint

The following source relationship must not be implemented as a Power BI fact-to-fact relationship:

```text
fact_order_items.order_id
        →
fact_orders.order_id
```

Both tables are FACT roles in the Commerce model.

Therefore this relationship is blocked by the controlled OLAP contract.

Power BI must not automatically create it.

---

# 10. Fulfillment / Shipping Model Construction

## 10.1 FACT Tables

```text
fact_shipment_booking
fact_shipment_items
fact_shipment_status_history
fact_shipment_cost_breakdown
fact_packaging
fact_outbound_packaging
fact_delivery_challans
fact_einvoice_records
fact_eway_bill_records
```

## 10.2 REFERENCE Tables

```text
ref_orders
ref_order_items
ref_return_request
ref_invoices
```

---

# 11. Fulfillment Approved Relationships

## Relationship F1

```text
ref_orders.order_id
        →
fact_shipment_booking.order_id
```

Cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship F2

```text
ref_order_items.order_item_id
        →
fact_shipment_items.order_item_id
```

Cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship F3

```text
ref_return_request.return_request_id
        →
fact_delivery_challans.reference_return_id
```

Cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship F4

```text
ref_invoices.id
        →
fact_delivery_challans.reference_invoice_id
```

Cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

# 12. Fulfillment Blocked Relationships

The following relationships must not be automatically created merely because source-level relationships exist.

## Fact-to-fact examples

```text
fact_shipment_items
    →
fact_shipment_booking
```

```text
fact_packaging
    →
fact_shipment_booking
```

```text
fact_einvoice_records
    →
fact_shipment_booking
```

```text
fact_eway_bill_records
    →
fact_shipment_booking
```

```text
fact_delivery_challans
    →
fact_shipment_booking
```

These are blocked because they would create fact-to-fact model paths.

---

# 13. Payments / Invoicing Model Construction

## 13.1 FACT Tables

```text
fact_payments
fact_payment_orders
fact_payment_transactions
fact_payment_receipts
fact_invoices
fact_delivery_challans
fact_einvoice_records
fact_eway_bill_records
```

## 13.2 REFERENCE Tables

```text
ref_orders
```

---

# 14. Payments Approved Relationships

## Relationship P1

```text
ref_orders.order_id
        →
fact_payment_orders.order_id
```

Observed cardinality:

```text
1 : 1
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship P2

```text
ref_orders.order_id
        →
fact_invoices.order_id
```

Observed cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship P3

```text
ref_orders.order_id
        →
fact_einvoice_records.order_id
```

Observed cardinality:

```text
1 : *
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

# 15. Payments Fact-to-Fact Protection

Source relationships among the payment facts must not automatically become Power BI relationships.

Examples include:

```text
fact_payments
fact_payment_transactions
fact_payment_receipts
fact_invoices
fact_delivery_challans
fact_einvoice_records
fact_eway_bill_records
```

The Power BI model must not form an uncontrolled fact-to-fact network.

---

# 16. Returns / Exchange / QC Model Construction

## 16.1 FACT Tables

```text
fact_return_request
fact_exchange_request
fact_exchange_attempt
fact_hub_returns
fact_hub_inventory_units
fact_rtv_batch
fact_rtv_batch_item
```

## 16.2 REFERENCE Tables

```text
ref_orders
ref_shipment_booking
```

---

# 17. Returns Approved Relationships

## Relationship R1

```text
ref_orders.order_id
        →
fact_return_request.order_id
```

Observed cardinality:

```text
1 : 1
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship R2

```text
ref_orders.order_id
        →
fact_exchange_request.old_order_id
```

Observed cardinality:

```text
1 : 1
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship R3

```text
ref_shipment_booking.shipment_booking_id
        →
fact_return_request.shipment_id
```

Observed cardinality:

```text
1 : 1
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

---

## Relationship R4

```text
ref_shipment_booking.shipment_booking_id
        →
fact_exchange_request.replacement_inbound_shipment_id
```

Observed cardinality:

```text
1 : 1
```

Direction:

```text
REFERENCE → FACT
```

Status:

```text
ACTIVE
```

Null behavior:

```text
25 non-null
2 null
0 orphan
```

Nulls are valid source-state behavior and must not be replaced.

---

# 18. Complete Approved Relationship Set

The Power BI construction may use only the following 13 paths.

```text
C1  ref_product.product_id
        → fact_order_items.productId

C2  ref_variants.id
        → fact_order_items.variantId

F1  ref_orders.order_id
        → fact_shipment_booking.order_id

F2  ref_order_items.order_item_id
        → fact_shipment_items.order_item_id

F3  ref_return_request.return_request_id
        → fact_delivery_challans.reference_return_id

F4  ref_invoices.id
        → fact_delivery_challans.reference_invoice_id

P1  ref_orders.order_id
        → fact_payment_orders.order_id

P2  ref_orders.order_id
        → fact_invoices.order_id

P3  ref_orders.order_id
        → fact_einvoice_records.order_id

R1  ref_orders.order_id
        → fact_return_request.order_id

R2  ref_orders.order_id
        → fact_exchange_request.old_order_id

R3  ref_shipment_booking.shipment_booking_id
        → fact_return_request.shipment_id

R4  ref_shipment_booking.shipment_booking_id
        → fact_exchange_request.replacement_inbound_shipment_id
```

No additional relationship may be inferred from matching column names.

---

# 19. Relationship Direction

The source evidence direction is:

```text
CHILD.FK → PARENT.KEY
```

Power BI model direction is:

```text
PARENT.KEY → CHILD.FK
```

Therefore Power BI relationship configuration must follow:

```text
REFERENCE / DIMENSION
        |
        v
FACT
```

The filter must flow from the validated reference side toward the fact side.

---

# 20. Cross-Filter Direction

Default cross-filter direction:

```text
Single
```

with filtering from:

```text
REFERENCE → FACT
```

Bidirectional filtering is prohibited unless a later formal evidence-based change explicitly authorizes it.

A.3.10 must not enable bidirectional filtering simply to make visuals appear to work.

---

# 21. Cardinality Rules

Power BI cardinality must be configured according to the validated source evidence.

Allowed configurations in the current contract:

```text
1 : 1
1 : *
```

The following are prohibited unless separately approved:

```text
* : *
many-to-many
automatic ambiguous cardinality
```

Power BI must not silently convert an intended one-to-many relationship into many-to-many.

---

# 22. Automatic Relationship Detection

Power BI automatic relationship detection must not be trusted as the architecture authority.

During A.3.10:

1. Load the controlled tables.
2. Inspect Power BI's detected relationships.
3. Remove or disable relationships not present in the approved 13-path contract.
4. Create only the approved relationships.
5. Validate the final model against the A.3.9 contract.

Matching column names alone are insufficient evidence.

---

# 23. Multiple-Path Protection

Multiple paths are a known design risk.

The model must not create alternative filter routes that were not explicitly approved.

Examples of potentially dangerous shared structures include:

```text
orders
order_items
shipment_booking
return_request
invoices
delivery_challans
```

The construction must preserve subject-area-specific reference projections rather than reusing fact tables as universal cross-subject dimensions.

---

# 24. Shared Source Table Strategy

The same source table may appear in multiple subject-area physical packages under different roles.

This is intentional.

Known shared source structures include:

```text
orders
order_items
invoices
shipment_booking
return_request
delivery_challans
einvoice_records
eway_bill_records
```

The physical package uses role-specific names such as:

```text
fact_orders
ref_orders

fact_invoices
ref_invoices
```

where required.

Power BI must respect those physical role boundaries.

It must not assume that identical source lineage means the tables can be merged into a single unrestricted semantic table.

---

# 25. Grain Protection

Every Power BI table must retain the physical grain established in A.3.6.

Power BI construction must not:

* aggregate a fact table into a replacement table;
* deduplicate rows;
* remove duplicate source records;
* flatten multiple fact tables;
* merge fact tables;
* explode rows through calculated joins;
* replace null values solely for visual convenience;
* create synthetic records;
* create synthetic surrogate keys;
* alter source values.

The Power BI model is a semantic layer over the controlled physical package.

It is not a new data-engineering layer.

---

# 26. Primary / Candidate Key Protection

The validated candidate keys must remain unique on the reference side.

Power BI construction must verify:

```text
Reference key
    = unique
    = non-null
```

before activating the relationship.

Fact foreign-key columns may contain nulls where the source contract permits them.

Nulls must not be converted into artificial keys.

---

# 27. Special Validated Grain Keys

The following keys were specifically validated during the readiness audit.

Shipment status history:

```text
shipment_status_history_id
```

Shipment cost breakdown:

```text
shipment_cost_breakdown_id
```

Power BI must not assume that the generic column name `id` is the key for these tables.

---

# 28. Measures and KPI Boundary

The current project evidence contains:

```text
Approved KPIs = 0
```

Therefore A.3.10 must not create unsupported business KPIs.

The following are not authorized merely because Power BI can calculate them:

* revenue KPI;
* profit KPI;
* ROI;
* CLV;
* RFM score;
* conversion rate;
* retention rate;
* churn rate;
* customer lifetime value;
* fraud rate;
* forecast;
* recommendation score;
* satisfaction score;
* marketing attribution;
* profitability;
* business impact;
* inventory optimization score.

A field may be displayed descriptively when its source semantics are established.

Displaying a source field is not equivalent to declaring it an approved KPI.

---

# 29. Raw Field vs Measure

The construction must distinguish:

```text
SOURCE FIELD
```

from:

```text
POWER BI MEASURE
```

No measure may be introduced solely to produce an attractive dashboard number.

If a later report requirement requires a derived metric, that metric must first have:

1. documented semantic definition;
2. evidence support;
3. grain compatibility;
4. validation;
5. explicit approval.

Without those conditions, it remains outside the current model contract.

---

# 30. Calculated Columns

Calculated columns are not automatically permitted.

A calculated column must not be used to:

* invent missing business attributes;
* infer unsupported customer segments;
* infer product categories;
* infer profitability;
* create synthetic statuses;
* repair source data;
* simulate missing relationships.

Technical display transformations may only be introduced after confirming they do not alter the analytical meaning of the source evidence.

---

# 31. Date Handling

Date fields must be used according to their actual source semantics.

A.3.10 must not automatically create a universal date dimension and connect every date column to it.

Different date fields may represent different events, including examples such as:

```text
created_at
updated_at
changed_at
received_at
charged_at
shipment dates
return dates
exchange dates
payment dates
invoice dates
```

A date dimension may only be introduced later if its purpose and relationship semantics are explicitly documented and validated.

No date relationship may be inferred merely because a column contains a date.

---

# 32. Null Handling

Nulls are valid source-state information unless the evidence contract explicitly states otherwise.

Power BI construction must not:

* replace nulls with zero;
* replace nulls with "Unknown";
* replace nulls with fabricated IDs;
* convert nulls to empty strings;
* remove rows containing nulls.

Any visual handling of nulls must preserve their source meaning.

The approved nullable Returns relationship is:

```text
ref_shipment_booking.shipment_booking_id
    →
fact_exchange_request.replacement_inbound_shipment_id
```

with:

```text
25 non-null
2 null
0 orphan
```

---

# 33. Subject-Area Isolation

The second Power BI approach must not recreate the 177-table source universe as a single semantic model.

The following is explicitly prohibited:

```text
177 source tables
      ↓
one giant Power BI model
      ↓
automatic relationship detection
```

The controlled architecture is:

```text
Subject Area 1 → controlled model
Subject Area 2 → controlled model
Subject Area 3 → controlled model
Subject Area 4 → controlled model
```

Each model must remain understandable and auditable.

---

# 34. No Cross-Subject Fact Reuse

A physical FACT output belonging to one subject area must not be reused as a cross-subject universal fact table.

Where shared business concepts are needed, the validated REFERENCE projections must be used according to the physical package.

Examples:

```text
Commerce:
    fact_orders

Fulfillment:
    ref_orders

Payments:
    ref_orders

Returns:
    ref_orders
```

This is intentional role separation.

---

# 35. Source Lineage

Every Power BI table must retain a traceable lineage:

```text
Power BI table
    ↓
physical role output
    ↓
source CSV
    ↓
cleaned source table
```

The table name, source path, and role must remain auditable.

Power BI transformations must not obscure the physical source identity.

---

# 36. Power Query Boundary

Power Query may be used to connect to the controlled CSV package.

The preferred Power Query behavior is:

```text
Read
→ type-preserving import
→ controlled presentation preparation
```

Power Query must not become an untracked replacement data-engineering pipeline.

The following transformations are prohibited:

* joins not specified by the contract;
* aggregation;
* deduplication;
* source mutation;
* unsupported derived business fields;
* row generation;
* unsupported calculated metrics;
* hidden relationship reconstruction.

If a transformation is necessary for technical compatibility, it must preserve the source evidence and be documented.

---

# 37. Source File Preservation

The following remain immutable inputs:

```text
data\cleaned\
```

and the original source/recovery evidence.

Power BI must never write back to those files.

Power BI refresh must be read-only with respect to the source package.

---

# 38. Controlled Physical Package Preservation

The A.3.6 package under:

```text
Power BI Dashboard\groups_csv\
```

is a controlled output.

Power BI construction must not modify its CSV values or schemas.

If a physical package correction is required, it must be handled through the controlled physical construction/validation process rather than edited manually inside Power BI.

---

# 39. Table Naming

Power BI table names should preserve the role-aware physical naming.

Examples:

```text
fact_orders
fact_order_items
ref_product
ref_variants
```

This makes the semantic distinction visible.

The construction must not rename tables in a way that hides whether a table is a FACT or REFERENCE role.

If a presentation-friendly display name is required later, the underlying lineage and role must remain documented.

---

# 40. Column Naming

Column names should remain source-faithful.

Do not rename columns merely to make them appear more business-friendly if doing so obscures source lineage.

If a display alias is used later, the source column identity must remain recoverable.

---

# 41. Hidden Fields

Fields should not be hidden merely to conceal complex or uncertain semantics.

A field may be hidden for technical/model-management reasons only when:

* its source lineage remains documented;
* hiding does not change its semantic interpretation;
* it does not conceal unsupported calculations.

No field should be hidden solely because it would expose a data-quality limitation.

---

# 42. Auto Date/Time

Power BI automatic date/time behavior must be reviewed during construction.

It must not silently create a network of hidden date tables that introduces unintended model complexity.

If automatic date/time behavior creates unwanted model objects, it should be disabled for the controlled model.

Date modeling must remain explicit.

---

# 43. Model Relationship Construction Procedure

For each subject area, A.3.10 must follow:

```text
1. Open/create the controlled Power BI model.
2. Connect only to the approved physical subject-area folder.
3. Load only the approved physical outputs.
4. Inspect automatically detected relationships.
5. Remove relationships not present in A.3.9.
6. Configure the approved relationships explicitly.
7. Set validated cardinality.
8. Set single-direction filtering.
9. Verify no fact-to-fact relationships remain.
10. Verify no many-to-many relationships exist.
11. Verify no ambiguous paths exist.
12. Validate table count.
13. Validate column availability.
14. Validate key uniqueness.
15. Save the model.
```

The procedure must be repeated independently for each approved subject area.

---

# 44. Automatic Relationship Review Gate

After loading tables, Power BI may suggest relationships.

Every suggestion must be classified:

```text
APPROVED
```

or:

```text
REJECTED — NOT IN CONTROLLED RELATIONSHIP CONTRACT
```

Only the 13 approved paths may become active model relationships.

No additional relationship should be accepted because Power BI labels it as "Many to one", "One to many", or "Both".

Power BI suggestions are implementation hints, not evidence.

---

# 45. Model Validation Requirements

Before A.3.10 can be considered complete, every subject-area model must pass:

## Table completeness

All expected physical outputs are loaded.

## Schema completeness

Required source columns are present.

## Key integrity

Reference keys are unique and non-null.

## Relationship completeness

Every approved relationship is implemented.

## Relationship exclusivity

No unapproved relationship remains active.

## Cardinality

Every relationship matches the approved cardinality.

## Filter direction

Filtering follows:

```text
REFERENCE → FACT
```

## Fact-to-fact protection

No fact-to-fact relationship exists.

## Many-to-many protection

No unintended many-to-many relationship exists.

## Multiple-path protection

No uncontrolled ambiguous filter path exists.

## Source integrity

Physical CSVs remain unchanged.

---

# 46. Model Validation Evidence

A.3.11 must capture evidence for at least:

```text
Subject area
Table
Role
Source path
Row count
Column count
Candidate key
Key uniqueness
Relationship
Cardinality
Cross-filter direction
Active/inactive state
Unexpected relationship count
Many-to-many count
Ambiguous path count
```

The validation must be reproducible.

---

# 47. Page-to-Model Boundary

The planned second Power BI report will contain four primary subject-area pages.

## Page 1 — Commerce / Orders & Products

Model:

```text
Commerce_Orders_Products
```

Expected table scope:

```text
fact_orders
fact_order_items
ref_product
ref_variants
```

---

## Page 2 — Fulfillment / Shipping

Model:

```text
Fulfillment_Shipping
```

Expected table scope:

```text
9 FACT
4 REFERENCE
```

---

## Page 3 — Payments / Invoicing

Model:

```text
Payments_Invoicing
```

Expected table scope:

```text
8 FACT
1 REFERENCE
```

---

## Page 4 — Returns / Exchange / QC

Model:

```text
Returns_Exchange_QC
```

Expected table scope:

```text
7 FACT
2 REFERENCE
```

The exact visual design belongs to A.3.12.

---

# 48. Visual Boundary

A.3.9 does not prescribe unsupported KPI cards.

The report may later contain evidence-bounded descriptive views such as:

* source counts;
* status distributions;
* record-level tables;
* categorical distributions;
* documented operational fields;
* validated descriptive quantities.

The actual visual selection must be based on available fields and approved semantics.

A visual is not evidence merely because the underlying column exists.

---

# 49. Business Interpretation Boundary

The Power BI model must not imply unsupported conclusions.

Examples of prohibited inference:

```text
payment amount
    ≠ automatically approved revenue KPI

shipment cost
    ≠ automatically approved profitability metric

order count
    ≠ automatically approved sales KPI

return records
    ≠ automatically approved return-rate KPI

customer identifiers
    ≠ automatically approved customer segmentation

timestamps
    ≠ automatically approved forecasting capability
```

Descriptive source evidence and derived business conclusions must remain separate.

---

# 50. ML Boundary

Current ML status:

```text
Selected ML problems = 0
```

Therefore A.3.10 must not add:

* prediction columns;
* forecast outputs;
* churn scores;
* fraud scores;
* recommendation scores;
* customer propensity;
* anomaly scores;
* SHAP outputs;
* model probabilities.

The second Power BI approach is descriptive/evidence-bounded unless a future formally approved ML stage changes this boundary.

---

# 51. Refresh Contract

The Power BI model must refresh from the controlled physical package.

The expected source boundary is:

```text
Power BI Dashboard\groups_csv\<SubjectArea>\
```

The refresh must not depend on:

* a developer's temporary folder;
* notebook state;
* manually edited source files;
* local intermediate files outside the project;
* the original 177-table source universe.

The source path must be configurable/reproducible where technically appropriate.

---

# 52. Refresh Integrity

A refresh must preserve:

```text
table count
column structure
source grain
source values
approved relationships
approved cardinality
subject-area boundary
```

A refresh failure must not be silently resolved by modifying source data.

---

# 53. Reproducibility

A second user or a future project session should be able to understand:

```text
where Power BI data comes from;
which physical package is used;
which tables belong to each model;
which relationships are approved;
which relationships are intentionally absent;
which fields are descriptive;
which KPIs are unavailable;
which subject areas remain deferred.
```

The model must therefore remain traceable to the A.3.7 and A.3.8 contracts.

---

# 54. Prohibited Construction Actions

The following are explicitly prohibited during A.3.10:

```text
GIANT_177_TABLE_FLAT_JOIN
FACT_TO_FACT_JOIN
FACT_AGGREGATION
FACT_DEDUPLICATION
SOURCE_MUTATION
ANALYTICAL_LAYER_CHANGE
INVENTED_COLUMNS
UNSUPPORTED_KPI_CREATION
ML_OUTPUT
CUSTOMER_ACCOUNT_PROMOTION
AUTOMATIC_RELATIONSHIP_ACCEPTANCE
UNCONTROLLED_MANY_TO_MANY
UNCONTROLLED_BIDIRECTIONAL_FILTERING
MULTIPLE_PATH_AUTO_RELATIONSHIPS
CROSS_SUBJECT_FACT_REUSE
SOURCE_FILE_EDITING
```

---

# 55. Power BI Model Construction Gate

A.3.10 may be considered complete only when:

```text
[ ] All four approved subject-area models exist.
[ ] All 35 approved physical outputs are represented.
[ ] 26 FACT outputs are represented.
[ ] 9 REFERENCE outputs are represented.
[ ] All 13 approved relationships are implemented where applicable.
[ ] No unapproved relationship remains active.
[ ] No fact-to-fact relationship exists.
[ ] No unintended many-to-many relationship exists.
[ ] Cardinalities match the contract.
[ ] Filter directions match the contract.
[ ] No ambiguous relationship path exists.
[ ] Source package remains unchanged.
[ ] Analytical datasets remain unchanged.
[ ] No unsupported KPI is introduced.
[ ] No ML output is introduced.
[ ] Customer/Account remains deferred.
[ ] Model lineage is documented.
[ ] Refresh source paths are documented.
```

---

# 56. A.3.11 Validation Gate

After construction, A.3.11 must independently validate the implemented Power BI model.

A.3.10 implementation itself is not sufficient evidence of correctness.

The sequence is:

```text
A.3.9 Specification
       ↓
A.3.10 Construction
       ↓
A.3.11 Independent Model Validation
```

A.3.11 must compare the actual model against this specification.

---

# 57. A.3.12 Report Construction Boundary

Only after A.3.11 passes should report/page construction begin.

A.3.12 will determine:

* page layouts;
* visual selection;
* slicers;
* descriptive tables;
* navigation;
* titles;
* explanatory text;
* field placement;
* visual-level filtering.

A.3.12 must not modify the underlying data architecture.

---

# 58. A.3.13 Visual / Behavioral QA

Visual validation will verify:

* page rendering;
* labels;
* filters;
* interactions;
* relationship behavior;
* absence of unexpected blank states;
* absence of unsupported KPI claims;
* subject-area isolation;
* readable layouts;
* reproducibility.

Visual appearance alone cannot override model validation.

---

# 59. A.3.14 Refresh / Reproducibility Validation

The completed Power BI report must be refreshed from the controlled package and checked for:

```text
successful refresh
stable row counts
stable schema
stable relationships
stable descriptive outputs
```

Any change must be investigated rather than silently accepted.

---

# 60. A.3.15 Documentation Integration

Final documentation must describe:

* the second Power BI approach;
* four approved subject areas;
* physical package;
* model construction;
* relationship boundaries;
* deferred Customer/Account scope;
* KPI boundary;
* ML boundary;
* refresh design;
* validation results;
* limitations.

Documentation must distinguish the second Power BI approach from the finalized Streamlit dashboard.

---

# 61. A.3.16 Final Closure

Final project closure will occur only after:

```text
A.3.10 PASS
A.3.11 PASS
A.3.12 PASS
A.3.13 PASS
A.3.14 PASS
A.3.15 PASS
```

followed by:

```text
git diff --check
file review
test/validation review
commit
push
HEAD == origin/master
clean working tree except intentionally retained artifacts
```

---

# 62. Existing Evidence That Must Remain Unchanged

The following closed evidence remains authoritative:

```text
A.3.6 — Controlled Physical Subject-Area Package
A.3.7 — Subject-Area OLAP Model Specification
A.3.8 — Power BI OLAP Readiness Audit
```

A.3.9 does not replace these artifacts.

It translates their validated constraints into a construction specification.

---

# 63. Current Decision

A.3.9 establishes:

```text
STATUS:
READY FOR CONTROLLED POWER BI MODEL CONSTRUCTION

BUT:

NOT YET CONSTRUCTED
```

The actual Power BI model remains deferred to A.3.10.

No `.pbix` construction is authorized by this document alone until the A.3.9 specification has been validated and formally closed.

---

# 64. Final Construction Principle

The second Power BI approach is not intended to make the PurjeStore dataset appear more complex.

Its purpose is to make the validated evidence usable in a controlled subject-area OLAP reporting environment.

Therefore:

```text
Evidence first
      ↓
Validated physical package
      ↓
Controlled model
      ↓
Independent validation
      ↓
Evidence-bounded report
```

and never:

```text
Power BI convenience
      ↓
automatic relationships
      ↓
unsupported metrics
      ↓
business conclusions
```

The Power BI model must remain subordinate to the validated PurjeStore evidence.

---

# 65. Stage Transition

Current project position:

```text
A.3.6  Controlled Physical Package
       PASS / CLOSED
          ↓
A.3.7  OLAP Model Specification
       PASS / CLOSED
          ↓
A.3.8  OLAP Readiness Audit
       PASS / CLOSED
          ↓
A.3.9  Model Construction Specification
       CURRENT
          ↓
A.3.10 Power BI Model Construction
       NEXT — AFTER A.3.9 CLOSURE
```

A.3.10 must not begin until this A.3.9 specification has been validated and closed.

````
