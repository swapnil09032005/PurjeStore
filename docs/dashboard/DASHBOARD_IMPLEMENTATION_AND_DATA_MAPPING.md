# PurjeStore Dashboard Implementation and Data Mapping Specification

**Project:** PurjeStore
**Document Type:** Dashboard implementation control and data-mapping specification
**Status:** Pre-implementation specification
**Dashboard Technology:** Streamlit + Plotly + pandas
**Analytical Source:** Validated analytical CSV layer
**Current Analytical Baseline:** 26 datasets, 12,148 rows, 289 columns
**Current Approved Final KPIs:** 0
**Current Approved Cross-Dataset Joins:** 0
**Current Selected ML Problems:** 0
**Current ML Status:** BLOCKED
**Authoritative UX Reference:** `docs/analytical/8.4_dashboard_ux_and_page_specification.md`
**Architecture Reference:** `docs/architecture/PHASE_15_ARCHITECTURE_RECONCILIATION.md`
**Refresh Reference:** `docs/architecture/PHASE_16B_CONTROLLED_REFRESH_ARCHITECTURE.md`
**Refresh Implementation:** `pipelines/refresh/refresh_analytical_datasets.py`
**Testing Reference:** `docs/testing/PHASE_17_TESTING_CLOSURE.md`

---

## 1. Purpose

This document defines the controlled implementation boundary for the PurjeStore dashboard.

Its purpose is to translate the approved dashboard UX specification into an implementation-ready structure without introducing unsupported analytical claims.

The document establishes:

* actual dashboard pages;
* page responsibilities;
* approved source datasets;
* controlled technical-field usage;
* semantic field mapping requirements;
* allowed analytical operations;
* visualization boundaries;
* filter requirements;
* table and drill-down behavior;
* data-health and refresh visibility;
* empty/error states;
* unsupported-feature safeguards;
* implementation sequencing;
* validation requirements.

This document is an implementation control artifact.

It is not permission to invent new KPIs, joins, business definitions, machine-learning outputs, or unsupported interpretations.

---

# 2. Authoritative Project Boundary

The dashboard must operate from the evidence already established by the PurjeStore analytical workflow.

The current validated analytical layer contains:

* **26 analytical datasets**
* **12,148 rows**
* **289 columns**

The current evidence boundary contains:

* **0 approved cross-dataset joins**
* **0 approved final KPIs**
* **0 selected ML problems**
* **0 approved predictive outputs**

Therefore the dashboard implementation must remain primarily:

> **validated analytical dataset → controlled descriptive/statistical presentation → evidence-bounded decision support**

The dashboard must not silently transform technical availability into business approval.

---

# 3. Dashboard Architecture Boundary

The dashboard consumes the validated analytical layer.

The intended implementation boundary is:

```text
Validated Analytical CSVs
        |
        v
Dashboard Data Access
        |
        v
Dataset / Schema Validation
        |
        v
Semantic Mapping
        |
        +----------------------+
        |                      |
        v                      v
Business Pages          Technical / Health Pages
        |                      |
        v                      v
Descriptive Analytics   Refresh / Validation / Schema
        |
        v
Streamlit + Plotly
```

The dashboard does not modify:

* raw source data;
* cleaned source data;
* analytical CSVs;
* refresh pipeline outputs;
* source database data.

The dashboard is read-only with respect to the analytical layer.

---

# 4. Current Dashboard Gap Being Addressed

The existing dashboard foundation successfully provides:

* analytical CSV discovery;
* dataset selection;
* dataset loading;
* row/column inspection;
* missing-value inspection;
* duplicate inspection;
* numeric analysis;
* categorical analysis;
* temporal analysis;
* Plotly visualizations;
* quality snapshots;
* evidence-boundary messaging.

However, the current implementation uses eight conceptual business areas that route into a largely generic dataset explorer.

The following are therefore implementation gaps:

| Capability                    | Current State            | Target                               |
| ----------------------------- | ------------------------ | ------------------------------------ |
| Streamlit application         | Implemented              | Preserve                             |
| Plotly                        | Implemented              | Preserve                             |
| Analytical discovery          | Implemented              | Preserve                             |
| Read-only analytical layer    | Implemented              | Preserve                             |
| Generic dataset exploration   | Implemented              | Preserve as technical capability     |
| Eight conceptual areas        | Partial                  | Convert into actual page experiences |
| Page-specific data mapping    | Missing                  | Implement                            |
| Page-specific filters         | Missing                  | Implement where evidence supports    |
| Page-specific visuals         | Missing                  | Implement where evidence supports    |
| Page-specific tables          | Missing                  | Implement                            |
| Page explanations             | Partial                  | Strengthen                           |
| Data Health                   | Missing                  | Implement                            |
| Refresh Status                | Missing                  | Implement                            |
| Schema Change visibility      | Missing                  | Implement                            |
| Validation visibility         | Missing                  | Implement                            |
| Refresh metadata integration  | Missing                  | Implement                            |
| Unsupported KPI protection    | Implemented conceptually | Preserve and strengthen              |
| ML/prediction protection      | Implemented conceptually | Preserve                             |
| Cross-dataset join protection | Implemented              | Preserve                             |

---

# 5. Navigation Model

The final dashboard should expose real page experiences rather than treating page names as filters over a generic explorer.

The preferred implementation direction is Streamlit's `st.Page` + `st.navigation` architecture because it supports explicit pages, grouped navigation, and shared entrypoint elements.

The current Streamlit documentation identifies `st.Page` and `st.navigation` as the preferred customizable multipage mechanism.

Recommended navigation structure:

```text
PurjeStore
│
├── Business Analytics
│   ├── Overview
│   ├── Sales / Commercial
│   ├── Orders
│   ├── Products / Catalog
│   ├── Customers / Accounts
│   ├── Fulfillment / Shipping
│   ├── Returns / Exchange
│   └── Operations / Inventory
│
└── Data & System Health
    ├── Data Status
    ├── Refresh Status
    ├── Dataset Health
    ├── Schema Changes
    └── Validation
```

This structure does not imply that every page will have certified KPIs.

A page may contain descriptive statistics, distributions, counts, quality indicators, tables, or source-level observations when those are supported by the underlying dataset.

---

# 6. Business Page 01 — Executive Overview

## 6.1 Purpose

Provide a concise entry point into the analytical system.

The page should help a nontechnical user understand:

* what data is currently available;
* what the dashboard covers;
* the current analytical refresh state;
* what types of analysis are available;
* important data-quality limitations;
* where to navigate for deeper analysis.

## 6.2 Do Not Treat This Page As

The Overview page must not become a conventional executive KPI dashboard containing unsupported:

* revenue;
* profit;
* ROI;
* conversion;
* customer lifetime value;
* churn;
* retention;
* forecasting;
* recommendations;
* fraud scores.

The current approved final KPI count is zero.

## 6.3 Primary Content

The page may show:

1. analytical dataset count;
2. analytical row count;
3. analytical column count;
4. refresh status;
5. refresh timestamp when available;
6. number of validation checks passed;
7. number of warnings;
8. number of schema changes;
9. available business analysis areas;
10. important evidence limitations.

These are system/data-status indicators, not business KPIs.

## 6.4 User Questions

The page should answer:

* What does this dashboard contain?
* When was the analytical layer refreshed?
* Is the current analytical state valid?
* What areas can I explore?
* Are there known data limitations?

---

# 7. Business Page 02 — Sales / Commercial Analytics

## 7.1 Purpose

Provide evidence-bounded descriptive analysis of commercially relevant analytical datasets.

## 7.2 Candidate Source Datasets

Potential sources include:

* `daily_category_metrics`
* `daily_platform_metrics`
* `daily_vendor_metrics`
* `invoices`
* `payments`
* `payment_transactions`
* `payment_receipts`
* `wallet_transactions`
* `commission_history`

These are candidate sources only.

Actual fields must be verified during implementation against the current analytical CSV schemas.

## 7.3 Field Approval Rule

A numeric field must not automatically become:

* revenue;
* sales;
* profit;
* margin;
* commission;
* transaction value;
* commercial KPI.

Before presentation, each field must receive an explicit semantic mapping.

Required mapping:

```text
technical_column
    →
display_label
    →
definition
    →
aggregation
    →
population
    →
format
    →
limitations
```

## 7.4 Allowed Analysis

Subject to field-level validation:

* distributions;
* observed values;
* counts;
* descriptive statistics;
* category comparisons;
* temporal observations;
* missingness;
* quality indicators.

## 7.5 Prohibited Interpretation

Do not claim:

* profitability;
* financial performance;
* growth;
* ROI;
* business success;
* optimization;
* causal impact;

unless separately established by approved evidence.

---

# 8. Business Page 03 — Order Analytics

## 8.1 Purpose

Provide descriptive analysis of order-level and order-related analytical evidence.

## 8.2 Candidate Source Datasets

* `orders`
* `order_items`
* `payment_transactions`
* `payments`
* `shipment_booking`
* `return_request`

The dashboard must not join these datasets merely because their names suggest relationships.

Current approved cross-dataset joins remain zero.

## 8.3 Allowed Presentation

Where supported by individual dataset contracts:

* order-record distributions;
* order status distributions;
* observed categorical values;
* temporal observations;
* order-level field summaries;
* quality and missingness;
* source-level tables.

## 8.4 Relationship Boundary

The existence of fields such as `order_id` does not automatically authorize joining.

If a future analytical relationship is approved, the relevant relationship evidence and grain/fan-out validation must be updated before dashboard use.

---

# 9. Business Page 04 — Products / Catalog Analytics

## 9.1 Purpose

Provide descriptive visibility into product/catalog datasets.

## 9.2 Candidate Source Datasets

* `product`
* `product_temp`
* `variants`
* `variants_temp`
* `attribute_values`

## 9.3 Allowed Analysis

Potential analysis includes:

* product counts;
* category distributions;
* attribute distributions;
* variant distributions;
* missingness;
* field completeness;
* observed value distributions;
* source-level catalog tables.

## 9.4 Semantic Restrictions

`variants_temp` contains documented semantic deferrals.

Fields affected by semantic uncertainty must not be presented with a business interpretation that exceeds the established evidence.

The known semantic review area includes:

* stock;
* deleted;
* handling_time;
* item_length;
* relationship to `updatedAt`.

---

# 10. Business Page 05 — Customers / Accounts Analytics

## 10.1 Purpose

Provide descriptive analysis of account/customer-related evidence without inventing customer-lifecycle metrics.

## 10.2 Candidate Source Dataset

Primary source:

* `accounts`

Potentially related datasets must not be joined without explicit approval.

## 10.3 Allowed Analysis

Subject to field validation:

* account population;
* categorical distributions;
* observed account attributes;
* completeness;
* missingness;
* temporal fields;
* source-level record inspection.

## 10.4 Explicitly Not Activated

The dashboard must not present:

* customer lifetime value;
* RFM scores;
* churn prediction;
* retention prediction;
* customer segmentation models;
* recommendation outputs.

These are not currently approved analytical outputs.

---

# 11. Business Page 06 — Fulfillment / Shipping Analytics

## 11.1 Purpose

Provide descriptive visibility into shipping and fulfillment-related records.

## 11.2 Candidate Source Datasets

* `shipment_booking`
* `shipment_items`
* `outbound_packaging`
* `hub_inventory`
* `hub_returns`

## 11.3 Allowed Analysis

Potential presentation includes:

* record counts;
* status/category distributions;
* observed temporal fields;
* shipping-related field distributions;
* missingness;
* duplicate/quality indicators;
* source-level tables.

## 11.4 Restriction

Do not infer:

* delivery performance;
* SLA compliance;
* logistics optimization;
* shipping cost optimization;
* operational savings;

unless those conclusions are supported by explicit validated evidence.

---

# 12. Business Page 07 — Returns / Exchange Analytics

## 12.1 Purpose

Provide descriptive analysis of return/exchange-related records.

## 12.2 Candidate Source Datasets

* `return_request`
* `hub_returns`

## 12.3 Allowed Analysis

Potentially:

* observed return categories;
* status distributions;
* temporal observations;
* record counts;
* missingness;
* source-level tables;
* descriptive field distributions.

## 12.4 Restrictions

Do not automatically infer:

* return rate;
* customer dissatisfaction;
* product quality;
* financial loss;
* retention impact;

unless these are explicitly derived from an approved analytical contract.

---

# 13. Business Page 08 — Operations / Inventory Analytics

## 13.1 Purpose

Provide descriptive visibility into operational and inventory-related source evidence.

## 13.2 Candidate Source Datasets

* `hub_inventory`
* `product`
* `variants`
* `daily_vendor_metrics`

## 13.3 Important Boundary

The presence of a field such as stock or inventory quantity does not automatically establish:

* inventory optimization;
* stock-out rate;
* inventory turnover;
* demand forecasting;
* replenishment recommendations.

These would require separate evidence and analytical contracts.

---

# 14. Technical / Data Health Area

The final dashboard should include a dedicated technical area.

It is intended for:

* technical/data administrators;
* project demonstrators;
* analysts;
* reviewers;
* client stakeholders who need confidence in data quality.

It should not expose unnecessary implementation complexity to ordinary business users.

---

# 15. Data Status Page

The Data Status page should communicate the current analytical data boundary.

Minimum information:

| Field               | Meaning                                  |
| ------------------- | ---------------------------------------- |
| Analytical datasets | Number of published datasets             |
| Total rows          | Rows across the analytical layer         |
| Total columns       | Columns across the analytical layer      |
| Source availability | Whether expected sources are available   |
| Last valid refresh  | Most recent successfully published state |
| Current status      | PASS / warning / blocked                 |
| Known limitations   | Important evidence constraints           |

The page should derive values dynamically.

It must not contain hard-coded historical dates or manually maintained refresh timestamps.

---

# 16. Refresh Status Page

The Phase 16-C refresh pipeline already produces:

`outputs/refresh/latest_refresh_report.json`

The dashboard should consume this metadata read-only.

Expected fields include:

* refresh ID;
* start time;
* end time;
* status;
* source count;
* dataset count;
* rows processed;
* rows published;
* schema changes;
* warnings;
* errors;
* validation summary;
* publication result.

The dashboard should show whether the most recent refresh:

```text
PASS
WARNING
BLOCKED / FAILED
```

The dashboard must never report a refresh as successful merely because the report file exists.

---

# 17. Dataset Health Page

For each analytical dataset, show relevant health information.

Potential fields:

* dataset name;
* row count;
* column count;
* readable status;
* source availability;
* grain;
* duplicate status;
* missing-value summary;
* schema status;
* last successful publication;
* warnings.

The page should distinguish:

```text
Dataset exists
Dataset is readable
Dataset passed validation
Dataset contains warnings
Dataset contains known semantic limitations
```

These are different conditions and must not be collapsed into a single misleading status.

---

# 18. Schema Changes Page

The refresh architecture defines schema-drift categories.

The dashboard should be capable of displaying detected changes such as:

```text
NO_CHANGE
ADDITIVE_COLUMN
REMOVED_OPTIONAL_COLUMN
REMOVED_REQUIRED_COLUMN
TYPE_CHANGE
NULLABILITY_CHANGE
NEW_CATEGORY
KEY_PROBLEM
GRAIN_PROBLEM
NEW_SOURCE
SOURCE_MISSING
```

Structural and semantic changes must be distinguished.

Examples:

### Potentially safe structural change

A new source column that does not affect an approved analytical projection may be classified as:

`ADDITIVE_COLUMN`

and may be safely ignored by the current projection if contract rules allow it.

### Potentially breaking change

A required analytical source field disappearing may be:

`REMOVED_REQUIRED_COLUMN`

and should block publication.

### Semantic change

A column retaining its name but changing its meaning must not be silently accepted.

The dashboard should communicate such a condition as requiring review.

---

# 19. Validation Page

The Validation page should expose the result of the analytical validation process.

At minimum:

* source schema validation;
* source grain validation;
* source-only projection;
* output schema validation;
* row-count preservation;
* duplicate validation;
* semantic exception handling;
* staging validation;
* readback validation;
* publication result.

The dashboard must distinguish:

```text
PASS
WARNING
BLOCKED
```

Warnings must not be presented as failures.

Failures must not be presented as successful publication.

---

# 20. Semantic Data Mapping

A central implementation requirement is the semantic mapping layer.

Technical CSV fields are not automatically business metrics.

Each field used in a business-facing visual should be mapped using:

| Mapping Attribute   | Required |
| ------------------- | -------- |
| Dataset             | Yes      |
| Technical column    | Yes      |
| Display label       | Yes      |
| Definition          | Yes      |
| Population          | Yes      |
| Aggregation         | Yes      |
| Format              | Yes      |
| Allowed visual type | Yes      |
| Page                | Yes      |
| Limitations         | Yes      |
| Evidence status     | Yes      |

Example structure:

```text
dataset:
    invoices

technical_column:
    <verified field>

display_label:
    <approved label>

definition:
    <evidence-backed definition>

population:
    <records covered>

aggregation:
    count / sum / mean / min / max / distribution / none

format:
    integer / decimal / percentage / date / text

allowed_visual:
    table / bar / line / histogram / metric / none

limitations:
    <documented limitation>

evidence_status:
    observed / derived / deferred / excluded
```

No field should be promoted to a business-facing KPI simply because it is numeric.

---

# 21. KPI Boundary

Current approved final KPI count:

> **0**

Therefore the implementation must not manufacture a KPI layer.

A visual may still show a descriptive statistic when it is clearly labelled and its meaning is supported.

Examples of acceptable distinction:

```text
Record count
```

is not automatically:

```text
Orders KPI
```

Likewise:

```text
Sum of a numeric column
```

is not automatically:

```text
Revenue
```

unless the field's business definition and population have been explicitly established.

---

# 22. Join Boundary

Current approved cross-dataset joins:

> **0**

The dashboard must therefore treat analytical CSVs as independent datasets unless an approved future analytical contract explicitly authorizes a relationship.

Do not join based solely on:

* matching column names;
* matching IDs;
* similar business names;
* assumed foreign keys;
* common e-commerce conventions.

No dashboard feature may introduce an implicit join.

---

# 23. ML Boundary

Current selected ML problems:

> **0**

ML is currently blocked.

The dashboard must not implement:

* prediction;
* forecasting;
* recommendation;
* churn prediction;
* fraud detection;
* classification;
* regression;
* clustering presented as an approved business model;
* SHAP/model explanations;
* model scores.

Any future ML page requires a formally reopened ML feasibility process and an approved problem.

---

# 24. Filters

Filters should be page-specific and evidence-driven.

Possible filter types include:

* categorical selection;
* date/time range;
* numeric range;
* dataset selection;
* status selection.

However, a filter should only appear when:

1. the relevant field exists;
2. the field meaning is established;
3. filtering is analytically meaningful;
4. the population is understood;
5. the filter does not imply an unsupported business interpretation.

Filters should be dynamically populated from the current validated dataset.

Do not hard-code historical categories or dates when the analytical layer can provide them dynamically.

---

# 25. Temporal Filtering

Temporal filtering must use verified temporal fields.

The dashboard should not assume that:

* `createdAt` means business event date;
* `updatedAt` means event date;
* `date` represents a universal business period;
* all datasets share the same time population.

Each page should document which temporal field it uses, if any.

Where no approved temporal field exists, the page should not manufacture a date filter.

---

# 26. Category Filtering

Categories should be discovered dynamically from the current validated data.

The dashboard must tolerate:

* new categories;
* missing categories;
* blank categories;
* unexpected but valid categories.

A new category should not require a code change merely to appear in a selection control, provided the underlying schema and semantics remain valid.

---

# 27. Visualization Rules

Visualization selection must follow the field's semantic type and evidence boundary.

Potential visual types:

* metric/status card;
* bar chart;
* line chart;
* histogram;
* box plot;
* table;
* descriptive-statistics table;
* quality matrix.

The visualization itself must not imply more than the underlying data supports.

For example:

A line chart of observed daily values may be labelled:

> Observed values by date

rather than:

> Growth trend

unless a validated analytical definition supports the latter.

---

# 28. Tables and Drill-Down

Tables should provide record-level transparency where useful.

Potential table capabilities:

* selected records;
* filtered records;
* source-field values;
* quality indicators;
* missing values;
* selected descriptive fields.

The dashboard should avoid displaying excessive raw technical columns by default.

Technical detail can be placed in expandable sections or technical pages.

---

# 29. Client-Friendly Explanation Pattern

Each business page should answer four questions.

### What am I looking at?

A concise description of the dataset or analytical subject.

### What does this metric/visual mean?

A short evidence-backed definition.

### What can I learn?

A factual description of what the visual can show.

### What should I not conclude?

A concise limitation statement where necessary.

Example:

```text
What am I looking at?
Observed records from the selected analytical dataset.

What does this visual mean?
The chart shows the distribution of the selected field across available records.

What can I learn?
You can identify common values, variation, and missingness.

What should I not conclude?
This view does not establish causation, profitability, forecasting, or business impact.
```

---

# 30. Empty States

Every page must handle empty or unavailable data gracefully.

Possible states:

### No dataset available

Display:

> No validated analytical dataset is currently available for this view.

### Filter returns no records

Display:

> No records match the selected filters.

Do not display an empty chart without explanation.

### Field unavailable

Display:

> This analysis is unavailable because the required field is not present in the current validated schema.

### Semantic mapping unavailable

Display:

> This field is available in the source data but has not been approved for this business interpretation.

---

# 31. Error States

Errors must be explicit.

Examples:

```text
Dataset could not be loaded.
```

```text
Analytical schema validation failed.
```

```text
Refresh publication is blocked.
```

```text
Required field is missing.
```

Do not replace technical failure with:

```text
No data available
```

when the actual issue is an application or validation failure.

---

# 32. Refresh Failure Safety

The dashboard must continue to use the last valid analytical state when a new refresh fails.

Required boundary:

```text
New Data
   |
   v
Validation
   |
   +---- FAIL ----> Preserve previous valid analytical state
   |
   +---- PASS ----> Publish new analytical state
```

The dashboard must never partially display an unvalidated staging dataset.

---

# 33. Dashboard-to-Refresh Boundary

The intended relationship is:

```text
Refresh Pipeline
       |
       v
Validated Analytical Layer
       |
       +----> Refresh Metadata
       |
       v
Dashboard
```

The dashboard does not execute source cleaning or analytical construction.

The dashboard consumes published results.

---

# 34. Dynamic Discovery Requirements

The dashboard should dynamically discover:

* analytical datasets;
* available fields;
* available categories;
* available dates;
* available values;
* refresh metadata;
* schema-change information.

Avoid hard-coding:

* date periods;
* category lists;
* row counts;
* refresh timestamps;
* dataset counts.

Known project-boundary constants may remain documented where they represent controlled contracts rather than live values.

---

# 35. Current Dataset Inventory for Mapping

The following analytical datasets currently exist:

| Dataset                  | Current Grain / Boundary                                        |
| ------------------------ | --------------------------------------------------------------- |
| `accounts`               | `accountId`                                                     |
| `attribute_values`       | `id`                                                            |
| `commission_history`     | `id`                                                            |
| `daily_category_metrics` | Semantic grain exception                                        |
| `daily_platform_metrics` | Semantic grain exception                                        |
| `daily_vendor_metrics`   | Semantic grain exception; 6 intentional complete-row duplicates |
| `einvoice_records`       | `id`                                                            |
| `hub_inventory`          | `hub_inventory_id`                                              |
| `hub_returns`            | `order_id`                                                      |
| `invoices`               | `id`                                                            |
| `journal_entries`        | `journalEntryId`                                                |
| `notification_logs`      | `id`                                                            |
| `order_items`            | `order_id`                                                      |
| `orders`                 | `order_id`                                                      |
| `outbound_packaging`     | `shipment_id`                                                   |
| `payment_receipts`       | `id`                                                            |
| `payment_transactions`   | `payment_id`                                                    |
| `payments`               | `payment_id`                                                    |
| `product`                | `product_id`                                                    |
| `product_temp`           | `product_temp_id`                                               |
| `return_request`         | `order_id`                                                      |
| `shipment_booking`       | `shipment_booking_id`                                           |
| `shipment_items`         | `shipment_item_id`                                              |
| `variants`               | `id`                                                            |
| `variants_temp`          | `id`                                                            |
| `wallet_transactions`    | `wallet_id`                                                     |

This inventory is a mapping starting point, not permission to use every dataset on every page.

---

# 36. Known Evidence Limitations

The dashboard must preserve the known analytical limitations.

Important limitations include:

* notification logs coverage gap;
* orders coverage gap;
* four `variants_temp` semantic deferrals;
* three grain exceptions;
* three identifier/code warnings;
* daily vendor duplicate-row exception;
* no approved cross-dataset joins;
* no approved final KPIs;
* no selected ML problems.

The limitations must be visible where they affect interpretation.

---

# 37. Existing Generic Explorer

The existing generic dataset explorer should not necessarily be removed.

It remains useful as a technical exploration capability.

However, it must no longer be the primary representation of the eight business pages.

Recommended architecture:

```text
Business Pages
     |
     +--> Controlled page-specific analysis
     |
     +--> Controlled semantic mapping
     |
     +--> Controlled visuals
     |
     v
Shared analytical access utilities

Technical Explorer
     |
     +--> Dataset inspection
     +--> Schema inspection
     +--> Quality inspection
     +--> Descriptive exploration
```

This allows technical transparency without confusing business users.

---

# 38. Shared Dashboard Utilities

Before implementation, reusable dashboard logic should be identified.

Potential shared functions:

```text
discover_analytical_files()
load_dataset()
validate_dataset_schema()
get_dataset_metadata()
get_refresh_metadata()
get_schema_changes()
get_quality_summary()
get_temporal_columns()
get_categorical_columns()
get_numeric_columns()
apply_safe_filter()
format_display_value()
render_empty_state()
render_error_state()
render_definition()
render_limitation()
```

These are implementation candidates.

They must not be created as a large framework merely for architectural appearance.

Only reusable logic that genuinely reduces duplication should be extracted.

---

# 39. Page Implementation Pattern

Each business page should follow a consistent structure:

```text
Page title
    |
    v
Purpose / "What am I looking at?"
    |
    v
Page filters
    |
    v
Evidence / data-status context
    |
    v
Primary descriptive views
    |
    v
Supporting table / detail
    |
    v
Interpretation guidance
    |
    v
Limitations
```

Technical pages may use a different structure appropriate to system monitoring.

---

# 40. Dashboard Page Mapping Matrix

The implementation should maintain a mapping similar to:

| Page                   | Primary Dataset(s)                          | Joins | KPI Status             | Visual Scope         |
| ---------------------- | ------------------------------------------- | ----: | ---------------------- | -------------------- |
| Overview               | Refresh metadata + analytical inventory     |     0 | System indicators only | Status / descriptive |
| Sales / Commercial     | Verified commercial datasets                |     0 | No approved final KPIs | Descriptive          |
| Orders                 | `orders`, subject to field-level validation |     0 | No approved final KPIs | Descriptive          |
| Products / Catalog     | Product/catalog datasets                    |     0 | No approved final KPIs | Descriptive          |
| Customers / Accounts   | `accounts`                                  |     0 | No approved final KPIs | Descriptive          |
| Fulfillment / Shipping | Shipping datasets                           |     0 | No approved final KPIs | Descriptive          |
| Returns / Exchange     | Return datasets                             |     0 | No approved final KPIs | Descriptive          |
| Operations / Inventory | Operational datasets                        |     0 | No approved final KPIs | Descriptive          |
| Data Status            | Analytical inventory                        |     0 | System indicators      | Status               |
| Refresh Status         | Refresh metadata                            |     0 | System indicators      | Status / table       |
| Dataset Health         | Dataset metadata                            |     0 | System indicators      | Table                |
| Schema Changes         | Refresh/schema metadata                     |     0 | System indicators      | Table / status       |
| Validation             | Validation metadata                         |     0 | System indicators      | Status / table       |

This matrix must be refined using actual field-level schema inspection before implementation.

---

# 41. Implementation Sequencing

Dashboard implementation should occur in controlled stages.

## Stage 1 — Data Mapping Validation

Inspect the current 26 analytical CSV schemas and confirm:

* candidate page datasets;
* actual field names;
* data types;
* temporal fields;
* categorical fields;
* numeric fields;
* grain;
* known semantic limitations.

No dashboard code changes yet.

## Stage 2 — Semantic Mapping

Define the approved field mapping for each page.

No unsupported business terminology should be introduced.

## Stage 3 — Shared Dashboard Utilities

Refactor only reusable logic that is actually required.

## Stage 4 — Navigation

Convert the conceptual page selector into actual page navigation.

## Stage 5 — Page-by-Page Implementation

Implement each page according to this document and the 8.4 UX specification.

## Stage 6 — Technical Health

Add:

* Data Status;
* Refresh Status;
* Dataset Health;
* Schema Changes;
* Validation.

## Stage 7 — Integration Validation

Validate dashboard against:

* analytical layer;
* refresh metadata;
* refresh failure behavior;
* dynamic categories;
* dynamic periods;
* missing fields;
* empty datasets;
* warnings.

## Stage 8 — UI Review

Review the application as a nontechnical user.

## Stage 9 — Automated Testing

Extend the existing 48-test baseline only for newly implemented behavior.

---

# 42. Testing Requirements

The dashboard implementation must add tests for applicable behavior.

Minimum areas:

### Navigation

* all intended pages are registered;
* default page loads;
* page routing does not fail.

### Dataset loading

* analytical directory is readable;
* expected datasets load;
* missing dataset is handled.

### Semantic mapping

* mapped fields exist;
* unmapped fields are not silently promoted;
* unsupported KPI labels are absent.

### Filters

* valid filter works;
* empty filter result is handled;
* dynamic categories work;
* date filtering works only where a validated temporal field exists.

### Refresh metadata

* valid refresh report loads;
* missing report is handled;
* failed refresh is represented correctly.

### Schema changes

* additive column is represented;
* removed required field is represented as breaking;
* type change is represented;
* semantic review is not silently ignored.

### Failure safety

* dashboard never loads staging data;
* last valid analytical layer remains usable after failed refresh.

### Visuals

* empty data does not crash;
* unsupported field type does not crash;
* missing optional field does not crash.

---

# 43. Regression Protection

The following must remain true after dashboard implementation:

```text
0 approved cross-dataset joins
0 approved final KPIs unless formally reopened
0 selected ML problems unless formally reopened
0 source-data writes
0 analytical-layer writes from dashboard
0 unsupported predictive pages
```

The existing analytical layer must remain unchanged by dashboard development.

The refresh pipeline must remain independently executable.

---

# 44. Performance Boundary

The dashboard should remain simple and Data Science-native.

Avoid unnecessary:

* API layers;
* backend services;
* frontend frameworks;
* microservices;
* distributed processing;
* cloud infrastructure;
* database rewrites.

The current analytical layer is only 26 CSV datasets and 12,148 rows.

The dashboard should therefore prioritize:

* clarity;
* correctness;
* maintainability;
* reproducibility;
* evidence traceability.

---

# 45. Security / Authentication Boundary

Authentication and role-based access control are not automatically required.

They should only be introduced if a genuine deployment requirement exists.

Do not create:

* fake enterprise roles;
* arbitrary permissions;
* unnecessary login systems;
* complicated RBAC.

If a real client deployment later requires authentication, it should be evaluated as a separate requirement.

---

# 46. Customer Portal Boundary

The PurjeStore analytics dashboard is an internal analytical/decision-support product.

A customer-facing e-commerce portal is a different product.

Do not combine:

```text
Analytics Dashboard
```

with:

```text
Customer Shopping Portal
```

unless a separate requirement is established.

---

# 47. Evidence and Traceability

Every business-facing analytical view should be traceable to:

```text
Source dataset
    ↓
Technical field
    ↓
Semantic definition
    ↓
Transformation / aggregation
    ↓
Visualization
    ↓
Interpretation boundary
```

If a user asks:

> Where did this number come from?

the dashboard design should make it possible to answer.

---

# 48. Definition of Done for a Business Page

A business page is not complete merely because it renders.

It is complete only when:

* page purpose is documented;
* source dataset is identified;
* fields are verified;
* semantic mapping is defined;
* unsupported fields are excluded;
* filters are validated;
* visuals are appropriate;
* tables are useful;
* empty states work;
* error states work;
* limitations are visible;
* no unauthorized joins exist;
* no unauthorized KPI exists;
* tests pass;
* dashboard read-only boundary is preserved.

---

# 49. Definition of Done for Technical Health

Technical health is complete only when:

* refresh metadata is readable;
* last valid refresh is visible;
* validation result is visible;
* dataset health is visible;
* schema changes are visible;
* warnings/errors are distinguishable;
* failed refresh does not replace valid data;
* dashboard does not expose staging data.

---

# 50. Final Dashboard Product Boundary

The intended final dashboard is:

> A client-friendly, evidence-driven, refresh-aware Streamlit analytics application that presents validated PurjeStore analytical datasets through controlled business pages and technical health pages without inventing unsupported KPIs, joins, predictions, or business interpretations.

The dashboard is not:

* a generic CSV viewer;
* a fabricated executive KPI dashboard;
* a predictive ML product;
* a customer portal;
* an enterprise software platform.

---

# 51. Implementation Guardrails

Before any implementation change, verify:

```text
[ ] Source dataset exists
[ ] Analytical dataset exists
[ ] Field exists
[ ] Field semantics are understood
[ ] Population is understood
[ ] Aggregation is justified
[ ] Visualization is appropriate
[ ] Business interpretation is supported
[ ] No unauthorized join
[ ] No unsupported KPI
[ ] No ML/prediction
[ ] No source mutation
[ ] No analytical-layer mutation
[ ] Empty state handled
[ ] Error state handled
[ ] Tests planned
```

If any required item is unresolved, implementation should stop at that boundary rather than inventing an assumption.

---

# 52. Pre-Implementation Gate

Before modifying `app.py`, the following must be completed:

1. Validate this document against the existing 8.4 UX specification.
2. Inspect actual analytical CSV schemas.
3. Produce the field-level page mapping.
4. Identify which proposed visuals are actually supported.
5. Confirm which filters are possible.
6. Confirm refresh metadata structure.
7. Confirm technical-health information available from the refresh pipeline.
8. Identify the minimum required code changes.
9. Identify whether any genuinely new implementation files are required.
10. Do not implement until this gate passes.

---

# 53. Relationship to Existing Specifications

This document does not replace:

`docs/analytical/8.4_dashboard_ux_and_page_specification.md`

The 8.4 specification remains the authoritative UX/page specification.

This document translates that specification into an implementation/data-mapping control layer.

The hierarchy is:

```text
Master Project Plan
        |
        v
Architecture / Evidence Boundaries
        |
        v
8.4 Dashboard UX Specification
        |
        v
Dashboard Implementation & Data Mapping
        |
        v
Actual Dashboard Implementation
        |
        v
Testing / Validation
```

No lower-level implementation artifact may silently override a higher-level evidence boundary.

---

# 54. Current Status

At creation of this document:

* Dashboard foundation: complete
* Generic analytical exploration: complete
* Eight conceptual business areas: present
* Eight actual page experiences: not yet implemented
* Page-specific semantic mapping: not yet implemented
* Technical health pages: not yet implemented
* Refresh metadata integration: not yet implemented
* 48 baseline automated tests: passing
* Analytical layer: validated
* Refresh pipeline: implemented
* ML: blocked
* Joins: not approved
* Final KPIs: not approved

Therefore:

> **The next implementation boundary is controlled dashboard data mapping and page design validation, not immediate modification of `app.py`.**

---

# 55. Final Principle

PurjeStore should become more useful without becoming less trustworthy.

The dashboard must prefer:

```text
Verified data
    >
Assumed meaning

Evidence
    >
Convention

Clear limitation
    >
Unsupported conclusion

Controlled implementation
    >
Artificial complexity
```

The final product should demonstrate that a Data Science system can be both technically capable and disciplined about what the data actually supports.
