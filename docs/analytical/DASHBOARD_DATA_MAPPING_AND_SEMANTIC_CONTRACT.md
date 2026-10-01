# PurjeStore — Dashboard Data Mapping and Semantic Contract

**Project:** PurjeStore
**Artifact:** Dashboard Data Mapping and Semantic Contract
**Status:** Controlled implementation contract
**Primary dashboard stack:** Streamlit + Plotly + pandas
**Analytical source:** Validated analytical CSV layer
**Current implementation boundary:** Descriptive, evidence-bounded dashboard analytics
**Predictive/ML status:** Blocked — no selected ML problem
**Approved cross-dataset joins:** 0
**Approved final KPIs:** 0

---

## 1. Purpose

This document defines the controlled semantic and data-mapping contract between the validated PurjeStore analytical layer and the dashboard.

The purpose is to ensure that dashboard implementation:

* uses only evidence-supported analytical fields;
* does not convert technical numeric fields into unsupported business metrics;
* does not introduce unsupported joins;
* does not create unsupported KPIs;
* does not expose inappropriate technical or personally identifiable information;
* preserves known analytical limitations and semantic exceptions;
* uses page-specific datasets and fields rather than treating every dataset as a generic dashboard source;
* separates descriptive analytics from business interpretation;
* integrates the existing controlled refresh status into the technical/data-health area;
* remains compatible with the existing 8.4 dashboard UX specification.

This document is an implementation contract, not a replacement for the existing dashboard UX specification.

---

# 2. Authoritative Evidence Baseline

The current analytical layer consists of:

| Evidence item                         |                                Current state |
| ------------------------------------- | -------------------------------------------: |
| Cleaned source datasets               |                                          177 |
| Analytical datasets                   |                                           26 |
| Analytical rows                       |                                       12,148 |
| Analytical columns                    |                                          289 |
| Approved cross-dataset joins          |                                            0 |
| Approved final KPIs                   |                                            0 |
| Selected ML problems                  |                                            0 |
| Dashboard technology                  |                           Streamlit + Plotly |
| Dashboard source                      |                  `data\processed\analytical` |
| Analytical output writes by dashboard |                                            0 |
| Controlled analytical refresh         |                                  Implemented |
| Refresh publication                   |                                   Controlled |
| Refresh report                        | `outputs\refresh\latest_refresh_report.json` |

The values above are the current project baseline and must not be silently changed by dashboard implementation.

If a future milestone changes any of these values, the corresponding evidence and documentation must be updated before the dashboard contract is changed.

---

# 3. Evidence Hierarchy

Dashboard implementation must follow this evidence hierarchy:

1. Validated analytical dataset contracts
2. Analytical CSV schemas and physical contents
3. Milestone 5 analytical evidence
4. Milestone 6 ML feasibility evidence
5. Milestone 8 dashboard UX specification
6. Phase 16 controlled refresh architecture and implementation
7. Phase 17 testing evidence
8. This semantic mapping contract

Where this document conflicts with an earlier authoritative evidence artifact, the conflict must be resolved explicitly rather than silently overwritten.

No dashboard developer may infer a business meaning solely from:

* a column name;
* numeric datatype;
* dataset name;
* common e-commerce practice;
* a familiar KPI pattern;
* a chart that looks commercially useful.

---

# 4. Semantic Classification

Every dashboard-facing field must have an explicit semantic classification.

Allowed classifications:

### APPROVED

The field has sufficient evidence for direct dashboard use within the specified context.

### CONDITIONAL

The field may be displayed only under the exact conditions documented in the field mapping.

### EXCLUDED

The field must not be exposed in the business-facing dashboard.

Typical reasons include:

* technical identifier;
* internal audit field;
* raw payload;
* credential/security-sensitive information;
* inappropriate PII;
* unsupported business interpretation;
* constant/non-actionable field;
* field whose meaning is not sufficiently established.

### DEFERRED

The field requires additional evidence before dashboard use.

No deferred field may be silently promoted to approved status during implementation.

---

# 5. Numeric Fields Are Not Automatically Metrics

A numeric datatype does not establish that a field is:

* revenue;
* sales;
* profit;
* margin;
* ROI;
* customer value;
* conversion;
* retention;
* cost;
* performance;
* inventory value;
* operational KPI.

A numeric field may represent:

* an identifier;
* a count;
* a quantity;
* a technical status;
* a percentage;
* a monetary value;
* a timestamp representation;
* an internal code;
* a measurement with a limited population;
* a legacy representation;
* another technical value.

Therefore every numeric field used in the dashboard requires semantic approval before display as an analytical measure.

---

# 6. Temporal Fields Are Not Automatically Date Dimensions

Datetime parsing or a date-like column name is not sufficient to establish a business date.

Known examples of misleading temporal inference include fields such as:

* `createdBy`;
* `status_updated_by`;
* `handling_time`.

These must not be treated as dates merely because a datatype conversion or heuristic parser succeeds.

Temporal fields require semantic confirmation of their actual meaning before being used for:

* date filters;
* time-series charts;
* period comparisons;
* daily/monthly grouping;
* trend interpretation.

---

# 7. Known Analytical Exceptions

The dashboard must preserve the following known exceptions.

## 7.1 Daily category metrics

`daily_category_metrics`

This dataset has a semantic grain exception.

It must not automatically be treated as a conventional daily KPI table.

In particular:

* fields require semantic mapping;
* legacy and current monetary representations require controlled interpretation;
* no automatic "Revenue" KPI may be created;
* no unsupported aggregation may be introduced.

---

## 7.2 Daily platform metrics

`daily_platform_metrics`

This dataset has a semantic grain exception.

Some fields may be technically numeric but are not necessarily useful business metrics.

Known evidence includes fields such as:

* `total_add_to_cart`;
* `total_checkouts`.

Where observed values are constant or otherwise non-actionable, they must not be presented as meaningful dashboard metrics.

---

## 7.3 Daily vendor metrics

`daily_vendor_metrics`

This dataset has a semantic grain exception.

Known considerations include:

* retained duplicate rows according to the analytical contract;
* monetary fields with different names and meanings;
* commission-related fields;
* possible distinction between `revenue` and `invoiced_sales`.

No field may be labelled "Revenue" merely because its technical name contains `revenue`.

The dashboard must preserve the existing duplicate-row contract rather than silently deduplicating the dataset.

---

## 7.4 Orders

`orders`

The current analytical projection does not expose the source `order_id` as a dashboard-facing field.

Therefore the dashboard must not promise individual order-level drill-down based on the current analytical dataset.

Any future order-level drill-down requires an explicit evidence/contract change.

---

## 7.5 Notification logs

`notification_logs`

This dataset has a substantial missing-value population.

It may support technical or operational descriptive analysis where the relevant fields are semantically approved.

It must not automatically be treated as evidence of:

* customer engagement;
* retention;
* campaign performance;
* conversion;
* communication effectiveness.

---

## 7.6 Variants temporary dataset

`variants_temp`

Known semantic deferrals include fields such as:

* stock;
* deleted;
* handling_time;
* item_length;
* fields whose interpretation depends on `updatedAt`.

These fields remain deferred unless separately approved.

---

# 8. Technical and Sensitive Field Boundary

Technical fields should not automatically be displayed in the business-facing pages.

Examples requiring exclusion or explicit review include:

* internal IDs;
* technical foreign keys;
* audit identifiers;
* raw request payloads;
* signed QR data;
* GSTIN-related technical values;
* internal approval identifiers;
* address IDs;
* raw technical metadata.

The dashboard may expose technical metadata in the **Data/System Health** area where necessary for transparency, but business-facing pages should use meaningful display labels and definitions.

---

# 9. PII Boundary

The analytical layer contains fields that may contain personally identifiable information.

Known examples include fields such as:

* `customerName`;
* `customerEmail`;
* `billingAddress`.

These fields must not simply be exposed in the client-facing dashboard.

The default rule is:

> Prefer aggregated, anonymized, or non-identifying analysis over raw customer-level personal information.

Raw PII requires a separate explicit requirement and access/security review before exposure.

---

# 10. Dashboard Information Architecture

The dashboard will contain the following business-facing pages:

1. Executive Overview
2. Commercial / Sales
3. Orders
4. Products / Catalog
5. Customers / Accounts
6. Fulfillment / Shipping
7. Returns / Exchange
8. Operations / Inventory

Technical pages:

9. Data & System Health
10. Refresh Status / Dataset Health

These pages must be implemented as actual page experiences rather than eight labels pointing to the same generic dataset explorer.

---

# 11. P01 — Executive Overview

## Purpose

Provide a concise evidence-based overview of the available analytical layer.

## Candidate source datasets

Potential evidence sources include:

* `daily_category_metrics`
* `daily_platform_metrics`
* `daily_vendor_metrics`
* `orders`
* `payments`
* `invoices`

These are candidates only.

A field may be displayed only after semantic approval.

## Allowed content

The page may contain:

* descriptive observations;
* approved aggregated fields;
* dataset coverage indicators;
* descriptive distributions;
* selected time-based observations where temporal semantics are confirmed;
* data-health indicators.

## Prohibited assumptions

The page must not automatically display:

* Revenue KPI;
* Profit KPI;
* ROI KPI;
* Conversion KPI;
* Retention KPI;
* Churn KPI;
* Forecast;
* Recommendation;
* Fraud prediction;
* ML output.

Current approved final KPI count remains zero.

---

# 12. P02 — Commercial / Sales

## Candidate datasets

Potential sources:

* `daily_category_metrics`
* `daily_platform_metrics`
* `daily_vendor_metrics`
* `commission_history`
* `invoices`
* `payments`
* `payment_receipts`
* `payment_transactions`

## Semantic rule

Commercial fields must be individually approved.

Particular caution is required for:

* `revenue`;
* `revenue_legacy`;
* `invoiced_sales`;
* commission fields;
* payment amounts.

The existence of a field named `revenue` does not itself certify a Revenue KPI.

## Allowed analysis

Where semantically approved:

* descriptive distributions;
* category/platform/vendor comparisons;
* observed counts;
* observed monetary fields with explicit definitions;
* descriptive time patterns.

## Prohibited

* profit calculation;
* margin calculation;
* ROI;
* causal sales conclusions;
* unsupported sales conversion claims.

---

# 13. P03 — Orders

## Candidate datasets

* `orders`
* `order_items`

## Allowed analysis

Potential descriptive analysis includes:

* observed order records;
* order-item quantities where semantically approved;
* available status/category distributions;
* available temporal distributions.

## Important limitation

The current analytical `orders` dataset does not expose `order_id`.

Therefore:

* no individual order lookup;
* no promised order drill-down;
* no customer-order join;
* no order-level navigation based on unavailable identifiers.

Any such functionality requires a future analytical contract change.

---

# 14. P04 — Products / Catalog

## Candidate datasets

* `product`
* `product_temp`
* `variants`
* `variants_temp`
* `attribute_values`

## Allowed analysis

Potential descriptive analysis:

* product/category distributions;
* variant distributions;
* attribute distributions;
* available product measurements;
* observed catalog completeness.

## Restrictions

Temporary datasets must remain clearly identified.

Deferred `variants_temp` fields must not become dashboard metrics.

Technical identifiers should not be used as user-facing analytical dimensions unless explicitly justified.

---

# 15. P05 — Customers / Accounts

## Candidate datasets

Potential sources include:

* `accounts`
* `wallet_transactions`
* `payments`
* `payment_receipts`
* `notification_logs`

## Critical semantic restriction

`accounts` must not automatically be interpreted as customer accounts.

Observed values include accounting classifications such as:

* asset;
* liability;
* equity;
* income;
* expense.

Therefore the page must not label this dataset "Customer Accounts" merely because the dataset is named `accounts`.

## Customer PII

Raw fields such as:

* customer name;
* customer email;
* billing address;

must not be exposed by default.

## Prohibited assumptions

This page must not claim evidence for:

* customer lifetime value;
* churn;
* retention;
* customer segmentation;
* customer satisfaction;
* customer propensity;

unless a future evidence-based contract explicitly approves such analysis.

---

# 16. P06 — Fulfillment / Shipping

## Candidate datasets

* `shipment_booking`
* `shipment_items`
* `outbound_packaging`
* `hub_inventory`

## Allowed analysis

Potential descriptive analysis:

* shipment records;
* shipment statuses;
* packaging observations;
* available shipment timing;
* hub-related operational distributions.

## Temporal caution

Fields such as technical user/status fields must not be interpreted as shipment dates.

The dashboard must distinguish actual event timestamps from technical actor fields.

---

# 17. P07 — Returns / Exchange

## Candidate datasets

* `return_request`
* `hub_returns`
* `variants`

## Allowed analysis

Potential descriptive analysis:

* observed return records;
* return statuses;
* available return categories;
* temporal distribution where valid;
* variant-related descriptive information where supported.

## Prohibited assumptions

Do not infer:

* customer dissatisfaction;
* churn;
* retention impact;
* financial loss;
* causal product quality problems;

from return records alone.

---

# 18. P08 — Operations / Inventory

## Candidate datasets

* `hub_inventory`
* `daily_vendor_metrics`
* `daily_platform_metrics`
* `notification_logs`
* `journal_entries`

## Allowed analysis

Potential descriptive analysis:

* inventory observations;
* operational record distributions;
* available vendor/platform observations;
* journal-entry distributions;
* technical monitoring indicators where explicitly defined.

## Restrictions

Technical fields and constant/non-actionable fields should not be promoted to business metrics.

---

# 19. Cross-Dataset Join Boundary

Current approved joins:

> **0**

Therefore dashboard implementation must not introduce joins between:

* orders and customers;
* orders and products;
* orders and payments;
* products and variants;
* shipments and orders;
* returns and orders;
* vendors and sales;
* any other analytical datasets.

A dataset may be shown independently on a page.

A future join requires:

1. relationship evidence;
2. grain compatibility;
3. cardinality validation;
4. fan-out validation;
5. measure-inflation validation;
6. analytical contract approval;
7. updated documentation;
8. updated tests.

---

# 20. Aggregation Contract

Every displayed numeric field must specify an aggregation policy.

Allowed aggregation policies must be selected according to the field's semantic meaning.

Examples include:

* count;
* distinct count where a valid identifier exists;
* sum;
* mean;
* minimum;
* maximum;
* median;
* distribution;
* no aggregation.

The dashboard must never use `sum()` merely because a field is numeric.

For fields where aggregation is not semantically established, the field remains unavailable for aggregate KPI-style display.

---

# 21. Filter Contract

Filters must be driven by actual available and semantically approved fields.

The dashboard should dynamically derive:

* available categories;
* available temporal ranges;
* available values;

from the current analytical dataset.

It must not hard-code:

* future dates;
* fixed years;
* assumed months;
* assumed categories;
* assumed status values.

A filter should be shown only when:

1. the field exists;
2. its semantics are established;
3. it has useful population;
4. its values provide meaningful filtering.

---

# 22. Dynamic Period Handling

The dashboard must derive the available date range from the validated dataset.

It must not contain hard-coded statements such as:

* "2025 sales";
* "January 2026";
* "latest month";
* "last 30 days";

unless those values are dynamically calculated from the actual data.

If no valid temporal field exists for a page, the page should clearly state that temporal filtering is unavailable.

---

# 23. Visualization Eligibility

A field may be visualized only when:

* semantic meaning is known;
* population is adequate;
* aggregation is valid;
* visualization type matches the field;
* limitations are documented.

Examples:

### Categorical fields

Potential:

* bar chart;
* frequency table.

### Valid temporal fields

Potential:

* line chart;
* time-distribution table.

### Valid numeric fields

Potential:

* histogram;
* box plot;
* distribution table;
* approved aggregate comparison.

### Technical fields

Normally:

* excluded from business visualization.

---

# 24. Empty and Sparse Data

The dashboard must handle:

* empty datasets;
* empty filtered results;
* all-null fields;
* sparse fields;
* unavailable temporal fields;
* unavailable categorical values.

It must not produce misleading empty charts.

Preferred behavior:

1. explain why the visualization is unavailable;
2. show the relevant data limitation;
3. avoid fabricating zeros;
4. avoid replacing missing evidence with assumptions.

---

# 25. Data & System Health

The technical health area may use:

```text
outputs/refresh/latest_refresh_report.json
```

The current authoritative structure is:

```text
phase
operation
started_at_utc
status
dataset_count_expected
datasets[]
publication
failure
finished_at_utc
report_path
```

Each dataset record provides:

```text
dataset
source_path
analytical_path
source_rows
output_rows
source_fields
output_fields
source_grain_key
source_grain_nulls
source_grain_duplicate_values
source_grain_unique_non_null
expected_duplicate_rows
actual_duplicate_rows
status
error
```

Publication provides:

```text
attempted
status
```

---

# 26. Refresh Status Mapping

The dashboard may display:

### Overall refresh

* phase;
* operation;
* status;
* started time;
* finished time;
* expected dataset count;
* publication status;
* failure message when present.

### Dataset health

For each dataset:

* dataset name;
* source row count;
* output row count;
* source field count;
* output field count;
* grain key;
* grain nulls;
* duplicate grain values;
* expected duplicate rows;
* actual duplicate rows;
* validation status;
* error.

This information comes directly from the existing refresh report.

---

# 27. Metadata That Must Not Be Invented

The current refresh report does **not** expose the following as explicit top-level metadata:

* `refresh_id`;
* `rows_processed`;
* `rows_published`;
* `warnings`;
* `schema_changes`;
* historical refresh count;
* schema-drift classification.

Therefore the dashboard must not display these as if they were current refresh-report facts.

If future refresh architecture adds them, the semantic contract may be extended.

---

# 28. Schema-Change Boundary

The broader project requires future schema-drift handling including classifications such as:

* `NO_CHANGE`;
* `ADDITIVE_COLUMN`;
* `REMOVED_OPTIONAL_COLUMN`;
* `REMOVED_REQUIRED_COLUMN`;
* `TYPE_CHANGE`;
* `NULLABILITY_CHANGE`;
* `NEW_CATEGORY`;
* `KEY_PROBLEM`;
* `GRAIN_PROBLEM`;
* `NEW_SOURCE`;
* `SOURCE_MISSING`.

However, the current Phase 16-C refresh report does not provide a persisted schema-change classification structure.

Therefore:

> Schema-change visualization is a future capability, not a currently implemented dashboard fact.

The dashboard must not simulate schema-change history.

---

# 29. Refresh Failure Safety

The dashboard must respect the Phase 16 controlled-publication boundary.

A failed refresh must not cause the dashboard to assume that partially processed data is valid.

The expected system behavior is:

```text
New Source
    ↓
Validation
    ↓
PASS ─────────→ Publish new analytical state
    │
FAIL
    ↓
Preserve previous valid analytical state
```

The dashboard should communicate refresh failure separately from analytical-data availability when necessary.

---

# 30. Semantic Display Mapping

Every approved business-facing field should eventually have the following mapping:

```text
technical_column
        ↓
display_label
        ↓
definition
        ↓
aggregation
        ↓
population
        ↓
format
        ↓
limitations
        ↓
allowed_page
        ↓
allowed_visualization
```

Example structure:

| Technical field | Display label           | Definition                   | Aggregation       | Population                 | Format      | Limitation          |
| --------------- | ----------------------- | ---------------------------- | ----------------- | -------------------------- | ----------- | ------------------- |
| Field-specific  | Evidence-approved label | Evidence-approved definition | Evidence-approved | Actual non-null population | Appropriate | Explicit limitation |

No display label should change the underlying semantic meaning.

---

# 31. KPI Boundary

Current approved final KPIs:

> **0**

Therefore the dashboard may contain descriptive analytical summaries but must not falsely imply that every prominently displayed number is a certified KPI.

A future KPI requires:

1. business question;
2. source field evidence;
3. semantic definition;
4. aggregation definition;
5. population definition;
6. limitation;
7. validation;
8. approval;
9. documentation;
10. test coverage.

---

# 32. ML Boundary

Current selected ML problems:

> **0**

Therefore the dashboard must not contain:

* prediction pages;
* forecasting pages;
* recommendation engines;
* churn prediction;
* fraud prediction;
* model probability displays;
* SHAP explanations;
* model-performance panels.

The ML boundary may be reopened only through a future evidence-based ML feasibility decision.

---

# 33. Dashboard Explanation Contract

Each major page should help a nontechnical user answer:

### What am I looking at?

State the dataset/analytical subject.

### What does this measure mean?

Provide the approved definition.

### What can I learn?

Describe the supported descriptive interpretation.

### What should I not conclude?

State important analytical limitations.

The dashboard must prefer transparency over false precision.

---

# 34. Client-Facing Language

Avoid presenting technical implementation terminology as business conclusions.

Prefer:

> "Observed records"

over:

> "Business performance"

when performance semantics are not established.

Prefer:

> "Observed distribution"

over:

> "Trend"

when temporal meaning is uncertain.

Prefer:

> "Available monetary field"

over:

> "Revenue"

when revenue semantics are not certified.

Prefer:

> "Analytical dataset validation"

over:

> "System is fully healthy"

when only the available validation scope has passed.

---

# 35. Data Health vs Business Health

These concepts must remain separate.

### Data Health

Can include:

* dataset availability;
* schema validity;
* row preservation;
* grain validation;
* duplicate validation;
* publication status;
* refresh status.

### Business Health

Would require approved business KPIs and business definitions.

Current approved final KPIs are zero.

Therefore the dashboard must not imply that technical data health equals business health.

---

# 36. Dashboard Source Boundary

Business pages must read from:

```text
data/processed/analytical
```

The dashboard must not:

* modify cleaned sources;
* modify analytical CSVs;
* rebuild analytical datasets independently;
* create hidden joins;
* write dashboard-derived CSVs;
* mutate source data.

The controlled refresh pipeline remains responsible for analytical publication.

---

# 37. Separation of Responsibilities

The system responsibilities are:

```text
Cleaned Sources
      ↓
Controlled Refresh Pipeline
      ↓
Validated Analytical Layer
      ↓
Dashboard
```

The dashboard is a consumer of validated analytical outputs.

It is not an ETL engine.

---

# 38. Dashboard Implementation Contract

The eventual dashboard implementation should replace the current generic conceptual area selector with real page experiences.

Each page should contain:

1. page title;
2. purpose/explanation;
3. approved filters;
4. approved descriptive metrics;
5. approved visualizations;
6. relevant table/drill-down where evidence permits;
7. interpretation notes;
8. limitations;
9. empty-state handling.

The generic dataset explorer may remain as a technical exploration capability if useful, but it must not be mistaken for the final business page architecture.

---

# 39. Testing Requirements

Dashboard implementation must include tests for:

### Data loading

* analytical directory exists;
* expected datasets are discoverable;
* CSVs are readable.

### Semantic boundaries

* excluded fields are not rendered as business metrics;
* deferred fields are not silently activated;
* unsupported KPI labels are not introduced.

### Filtering

* valid filters operate;
* empty selections are handled;
* dynamic categories work;
* dynamic temporal ranges work.

### Refresh integration

* refresh report exists;
* PASS status is correctly displayed;
* failed status is handled;
* dataset-level status is correctly displayed;
* publication status is correctly displayed.

### Missing data

* missing dataset;
* missing field;
* empty filtered result;
* all-null field;
* unavailable temporal dimension.

### Integrity

* dashboard performs no analytical writes;
* dashboard does not introduce joins;
* dashboard does not modify source or analytical data.

---

# 40. Acceptance Criteria

The semantic/dashboard mapping is considered implementation-ready only when:

* [ ] 26 analytical datasets are recognized;
* [ ] current analytical baseline is preserved;
* [ ] semantic classification rules are implemented;
* [ ] page-specific dataset mappings are documented;
* [ ] page-specific field mappings are documented;
* [ ] aggregation rules are explicit;
* [ ] filter rules are explicit;
* [ ] technical-field exclusions are respected;
* [ ] PII boundaries are respected;
* [ ] zero-join boundary is respected;
* [ ] zero-KPI boundary is respected;
* [ ] ML boundary is respected;
* [ ] refresh-report structure is mapped;
* [ ] Data Health uses actual report fields;
* [ ] nonexistent refresh metadata is not invented;
* [ ] empty/error states are defined;
* [ ] dashboard tests cover the new behavior.

---

# 41. Implementation Sequence

The implementation should proceed in this order:

```text
1. Finalize semantic mapping
        ↓
2. Implement page navigation
        ↓
3. Implement shared safe-loading utilities
        ↓
4. Implement page-specific data selection
        ↓
5. Implement approved filters
        ↓
6. Implement approved descriptive visuals
        ↓
7. Implement tables / supported drill-down
        ↓
8. Implement definitions and limitations
        ↓
9. Implement Data & System Health
        ↓
10. Connect refresh metadata
        ↓
11. Add/extend automated tests
        ↓
12. Run complete dashboard validation
        ↓
13. UX review
        ↓
14. Documentation update
        ↓
15. Git validation / commit / push
```

No step should silently expand the analytical scope.

---

# 42. Future Reopening Conditions

The following may be reconsidered only when evidence supports them:

### Cross-dataset joins

Requires validated relationship and grain evidence.

### Final KPIs

Requires certified measure definitions and business relevance.

### ML

Requires a selected evidence-backed problem.

### Schema-change dashboard

Requires refresh-report/schema-drift metadata.

### Customer-level analytics

Requires approved semantic definitions and appropriate privacy/access controls.

---

# 43. Final Contract Position

PurjeStore's dashboard is not intended to manufacture a conventional e-commerce KPI dashboard from generic field names.

The dashboard must communicate what the validated data actually supports.

The current product boundary is:

```text
Validated Analytical Data
        ↓
Evidence-Bounded Descriptive Analytics
        ↓
Page-Specific Dashboard Experiences
        ↓
Transparent Data/System Health
        ↓
Controlled Refresh Visibility
```

The following remain explicitly outside the current implementation boundary:

```text
Unsupported KPI certification
        X

Unvalidated cross-dataset joins
        X

Predictive ML
        X

Forecasting
        X

Recommendations
        X

Churn prediction
        X

Fraud prediction
        X

Unsupported customer conclusions
        X

Fabricated schema-drift history
        X
```

The dashboard therefore remains:

* evidence-driven;
* refresh-aware;
* schema-conscious;
* descriptive where evidence supports description;
* transparent about limitations;
* safe against unsupported semantic expansion;
* compatible with the validated analytical layer;
* suitable for later client-facing productization without compromising analytical integrity.

---

# 44. Relationship to Existing Documentation

This document does not replace:

* `docs/analytical/8.4_dashboard_ux_and_page_specification.md`
* `docs/architecture/PHASE_15_ARCHITECTURE_RECONCILIATION.md`
* `docs/architecture/PHASE_16B_CONTROLLED_REFRESH_ARCHITECTURE.md`
* `docs/testing/PHASE_17_TESTING_CLOSURE.md`

Instead, the documents have separate responsibilities:

```text
8.4 UX Specification
        ↓
What the dashboard should provide

Dashboard Semantic Contract
        ↓
Which evidence may populate it

Phase 15 Architecture
        ↓
Where the dashboard fits in the system

Phase 16-B / 16-C
        ↓
How analytical data is safely refreshed

Phase 17 Testing
        ↓
How implemented behavior is validated
```

---

# 45. Status

**Document status:** Implementation contract prepared.

**Current implementation status:**

* Semantic evidence reviewed: PASS
* Refresh-report structure inspected: PASS
* Dashboard semantic contract defined: PASS
* Dashboard code changed: NO
* Analytical data changed: NO
* Refresh pipeline changed: NO
* New joins introduced: NO
* New KPIs introduced: NO
* ML introduced: NO

**Next implementation boundary:**

> Implement the controlled page architecture and shared dashboard utilities against this contract, without changing the analytical layer or expanding the approved analytical scope.
