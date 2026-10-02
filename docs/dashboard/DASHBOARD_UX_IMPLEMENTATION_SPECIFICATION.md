# PurjeStore Dashboard UX Implementation Specification

## 1. Purpose

This document defines the final implementation specification for the PurjeStore dashboard UX redesign.

It translates the existing:

* dashboard architecture,
* analytical evidence,
* approved semantic mapping,
* dashboard UX specification,
* productization assessment,
* controlled refresh architecture,
* testing boundary,
* and page-by-page UX evidence audit

into an implementation-ready dashboard specification.

This document governs the presentation and interaction redesign only.

It does not redefine the analytical methodology, source data, analytical dataset construction, relationship model, KPI approval, ML decision, or refresh architecture.

---

## 2. Current Authoritative Baseline

The dashboard implementation must preserve the following authoritative baseline:

| Item                                    |                 Current value |
| --------------------------------------- | ----------------------------: |
| Analytical datasets                     |                            26 |
| Analytical rows                         |                        12,148 |
| Analytical columns                      |                           289 |
| Approved descriptive page/field records |                            21 |
| Business pages                          |                             8 |
| Technical pages                         |                             2 |
| Approved cross-dataset joins            |                             0 |
| Approved final KPIs                     |                             0 |
| Selected ML problems                    |                             0 |
| ML status                               |                       BLOCKED |
| Analytical dashboard writes             |                             0 |
| Dashboard joins                         |                             0 |
| Analytical layer                        |                     Read-only |
| Refresh mechanism                       | Controlled analytical refresh |
| UI technology                           |            Streamlit + Plotly |

The dashboard redesign must not change these values or their underlying evidence without a separate analytical approval process.

---

# 3. Product UX Principle

The dashboard must communicate:

> **validated evidence first, interpretation second, interaction third, technical transparency where appropriate.**

The dashboard must never compensate for limited evidence by manufacturing analytical sophistication.

A sparse page is acceptable when the approved evidence is sparse.

A descriptive measure must not automatically become a KPI.

A numeric field must not automatically become a business metric.

A dataset relationship must not automatically become a join.

An available source field must not automatically become dashboard evidence.

---

# 4. User Experiences

The dashboard is divided into three experiences.

## 4.1 Business Analytics Experience

Primary users:

* business users,
* management,
* client stakeholders.

Pages:

1. P01 Executive Overview
2. P02 Commercial / Sales
3. P03 Orders
4. P04 Products / Catalog
5. P05 Customers / Accounts
6. P06 Fulfillment / Shipping
7. P07 Returns / Exchange
8. P08 Operations / Inventory

These pages must prioritize readable business evidence.

---

## 4.2 Data & System Health Experience

Primary users:

* technical stakeholders,
* data administrators,
* project evaluators.

Page:

* Data & System Health

This page communicates:

* analytical refresh status,
* dataset availability,
* validation status,
* publication status,
* failure state,
* current analytical baseline,
* system/data limitations.

It must not become another business analytics page.

---

## 4.3 Technical Dataset Explorer

Primary users:

* technical/data users,
* developers,
* analysts.

This page provides controlled inspection of analytical datasets.

It may expose:

* dataset selection,
* row/column counts,
* missing-value counts,
* sample records,
* technical field profiles.

It must clearly state that technical inspection does not certify business semantics.

---

# 5. Global UX Rules

## 5.1 Evidence boundaries

Every business page must make the evidence boundary understandable.

The user must be able to distinguish:

* observed data,
* descriptive interpretation,
* technical information,
* limitations,
* future/deferred capabilities.

---

## 5.2 No automatic KPI promotion

No descriptive record may be displayed as a certified KPI unless the analytical KPI approval gate explicitly approves it.

Current state:

> Final KPIs = 0.

Therefore the redesigned dashboard must not use executive KPI language for the current approved records.

---

## 5.3 No unsupported joins

The dashboard must not create cross-dataset joins.

Current state:

> Approved joins = 0.

Page-level presentation may display fields from multiple approved datasets only when those fields are independently approved for the page.

The UI must not imply that independently displayed fields have been joined or reconciled.

---

## 5.4 No unsupported business inference

The dashboard must not infer:

* profit,
* revenue,
* ROI,
* customer lifetime value,
* churn,
* retention,
* conversion,
* fraud,
* recommendations,
* forecasts,
* savings,
* business impact,
* causal relationships

unless separately supported and approved.

---

## 5.5 No raw PII exposure

Business pages must not expose raw:

* customer names,
* email addresses,
* phone numbers,
* addresses,
* sensitive identifiers,
* technical request payloads,
* internal technical fields

unless a future security/privacy approval explicitly permits such exposure.

---

# 6. Navigation Architecture

The primary navigation order is:

```text
BUSINESS ANALYTICS

P01 Executive Overview
P02 Commercial / Sales
P03 Orders
P04 Products / Catalog
P05 Customers / Accounts
P06 Fulfillment / Shipping
P07 Returns / Exchange
P08 Operations / Inventory

TECHNICAL

Data & System Health
Technical Dataset Explorer
```

Business pages should visually form the primary experience.

Technical pages should remain clearly separated.

---

# 7. Global Page Structure

Each business page should follow this hierarchy where applicable:

```text
Page title
    ↓
Purpose / short description
    ↓
Evidence boundary
    ↓
Observed evidence section
    ↓
Primary visualization or descriptive summary
    ↓
Supporting exact-value table
    ↓
Interpretation / limitation note
```

The exact number of sections must depend on available evidence.

The structure must not force empty sections onto sparse pages.

---

# 8. P01 — Executive Overview

## 8.1 Purpose

P01 is the orientation page for the entire analytical dashboard.

It should answer:

> What does the current PurjeStore analytical evidence contain, and what can this dashboard currently show?

---

## 8.2 Approved evidence

Seven approved records:

* `daily_category_metrics.order_count`
* `daily_category_metrics.units_sold`
* `daily_platform_metrics.total_orders`
* `daily_platform_metrics.total_product_views`
* `daily_vendor_metrics.orders`
* `daily_vendor_metrics.units_sold`
* `daily_vendor_metrics.cancelled_orders`

Datasets:

* `daily_category_metrics`
* `daily_platform_metrics`
* `daily_vendor_metrics`

---

## 8.3 UX structure

Recommended structure:

```text
Executive Overview
    ↓
Current evidence summary
    ↓
Analytical coverage
    ↓
Descriptive evidence
    ↓
Operational observations
    ↓
Evidence boundary
```

The page may use compact summary cards for descriptive dataset coverage, but these must not be labelled as business KPIs.

---

## 8.4 Visualization

Potential treatments:

* bar chart,
* line chart where temporal structure is explicitly supported,
* compact table.

Visualization selection must depend on actual field structure and cardinality.

No arbitrary chart type must be imposed.

---

## 8.5 Important restriction

The page must not become:

> "Executive KPI Dashboard"

because no final KPI set has been approved.

It should instead be:

> "Executive Overview of Available Analytical Evidence."

---

# 9. P02 — Commercial / Sales

## 9.1 Purpose

Present approved descriptive evidence related to payment status and invoice quantity.

---

## 9.2 Approved evidence

* `payment_transactions.status`
* `payments.status`
* `invoices.quantity`

Datasets:

* `payment_transactions`
* `payments`
* `invoices`

---

## 9.3 UX structure

```text
Commercial / Sales
    ↓
Payment transaction status
    ↓
Payment status
    ↓
Invoice quantity
    ↓
Evidence boundary
```

Status fields should use categorical distributions.

Invoice quantity may use an appropriate descriptive visualization or table.

---

## 9.4 Restriction

Do not display:

* revenue,
* gross sales,
* net sales,
* profit,
* margin,
* ROI,
* payment success rate as a certified KPI

unless separately approved.

Observed status distributions may be shown descriptively.

---

# 10. P03 — Orders

## 10.1 Purpose

Present approved order-item quantity evidence.

---

## 10.2 Approved evidence

* `order_items.quantity`

---

## 10.3 UX approach

This page intentionally contains limited evidence.

The page should therefore use a focused presentation:

```text
Orders
    ↓
Order-item quantity
    ↓
Observed distribution / summary
    ↓
Exact supporting values
    ↓
Evidence limitation
```

Do not fill the page with unrelated order metrics.

---

## 10.4 Restriction

The presence of `order_items.quantity` does not authorize:

* order revenue,
* order value,
* average order value,
* conversion rate,
* customer order frequency,
* order growth KPI.

---

# 11. P04 — Products / Catalog

## 11.1 Purpose

Present observed product status information.

---

## 11.2 Approved evidence

* `product.status`

---

## 11.3 UX approach

Preferred presentation:

* categorical status distribution,
* supporting table where useful.

The page should clearly communicate that it represents observed product status rather than complete catalog performance analytics.

---

## 11.4 Restriction

Do not infer:

* product profitability,
* product popularity,
* inventory availability,
* product conversion,
* product recommendation,
* product performance ranking

from status alone.

---

# 12. P05 — Customers / Accounts

## 12.1 Important semantic boundary

The current evidence does not establish broad customer behavioral analytics.

Approved evidence consists of:

* `wallet_transactions.type`
* `wallet_transactions.method`
* `wallet_transactions.status`

Therefore the page must not imply that comprehensive customer analytics are currently available.

---

## 12.2 UX structure

Recommended explanatory text:

> Current customer/account evidence is limited to approved wallet transaction attributes. Broader customer behavioral analytics are not activated in the current evidence contract.

Then present:

* transaction type distribution,
* transaction method distribution,
* transaction status distribution.

---

## 12.3 Restriction

Do not add:

* customer lifetime value,
* churn,
* retention,
* customer segmentation,
* customer profitability,
* customer recommendations,
* raw customer PII

without a future evidence and analytical approval gate.

---

# 13. P06 — Fulfillment / Shipping

## 13.1 Approved evidence

* `shipment_items.quantity`
* `hub_inventory.quantity`

---

## 13.2 UX structure

The page may present:

```text
Fulfillment / Shipping
    ↓
Shipment-item quantity
    ↓
Hub inventory quantity
    ↓
Supporting evidence
```

The two fields must remain semantically distinct.

---

## 13.3 No implicit join

Displaying these two approved fields on one page does not authorize a relationship between shipment quantities and inventory quantities.

Do not calculate:

* fulfillment rate,
* stock coverage,
* inventory turnover,
* shipment efficiency

unless separately approved.

---

# 14. P07 — Returns / Exchange

## 14.1 Approved evidence

* `return_request.status`
* `hub_returns.quantity`

---

## 14.2 UX structure

```text
Returns / Exchange
    ↓
Return-request status
    ↓
Hub-return quantity
    ↓
Supporting evidence
```

Status should use categorical visualization.

Quantity should use an appropriate descriptive visualization.

---

## 14.3 Restriction

Do not infer:

* return rate,
* refund rate,
* customer dissatisfaction,
* return causes,
* financial return impact

unless those measures are independently established.

---

# 15. P08 — Operations / Inventory

## 15.1 Approved evidence

* `hub_inventory.quantity`
* `daily_vendor_metrics.product_views`

---

## 15.2 UX structure

The page should emphasize operational observation rather than predictive optimization.

Potential sections:

```text
Operations / Inventory
    ↓
Inventory quantity
    ↓
Vendor-level product views
    ↓
Observed evidence
```

---

## 15.3 Shared field

`hub_inventory.quantity` is legitimately reused on P06 and P08.

The presentation context may differ:

* P06: fulfillment/shipping context
* P08: operations/inventory context

The implementation must not create contradictory definitions for the same field.

---

# 16. Data & System Health

## 16.1 Purpose

This is a technical transparency page.

It should communicate:

* refresh state,
* publication status,
* analytical dataset availability,
* validation results,
* current baseline,
* failure information where applicable.

---

## 16.2 Current authoritative baseline

```text
26 analytical datasets
12,148 rows
289 columns
```

---

## 16.3 Failure behavior

If the latest controlled refresh fails:

* the dashboard must not imply that the new analytical state was successfully published;
* the previous valid analytical state must remain protected;
* the health page must communicate the failure clearly;
* technical error information may be shown to appropriate users.

---

## 16.4 Business/technical separation

Health information must not be presented as business performance.

For example:

> Refresh status: PASS

is a technical status, not a business KPI.

---

# 17. Technical Dataset Explorer

## 17.1 Purpose

Provide controlled inspection of the analytical layer.

---

## 17.2 Supported interactions

The existing dataset selector should remain.

The explorer may allow:

* dataset selection,
* row/column inspection,
* missing-value inspection,
* sample record viewing,
* technical field profiling.

---

## 17.3 Important disclaimer

The page must clearly state:

> Technical field characteristics do not automatically certify business meaning.

---

## 17.4 Business-page separation

Technical field inspection must not be copied into business pages simply because the information is available.

---

# 18. Visualization Rules

## 18.1 Categorical/status evidence

Preferred:

1. horizontal/vertical bar chart,
2. exact-value table.

Avoid pie/donut charts unless a future evidence-specific review demonstrates that the category structure is appropriate.

---

## 18.2 Quantity evidence

Preferred:

1. bar chart,
2. line chart when temporal structure is genuinely supported,
3. exact-value table.

---

## 18.3 Tables

Tables should be used when:

* exact values matter,
* category count is high,
* chart labels become unreadable,
* the user needs verification rather than visual comparison.

---

## 18.4 Plotly

Plotly remains the approved interactive visualization technology.

The implementation should reuse centralized visualization logic where repeated behavior genuinely exists.

Do not create separate chart modules for every page unless repeated responsibility justifies the abstraction.

---

# 19. Interaction Rules

## 19.1 General principle

Interaction must improve interpretation.

It must not exist merely to make the dashboard look interactive.

---

## 19.2 Filters

Filters may be introduced when:

1. the underlying dataset supports the dimension;
2. the field has approved semantics;
3. filtering does not create unsupported cross-dataset relationships;
4. the resulting interpretation remains valid;
5. the behavior is covered by tests.

---

## 19.3 Date filtering

Date filters are not globally mandatory.

A date filter may be introduced on a page only when:

* the approved evidence has an appropriate temporal field/context;
* filtering is semantically valid;
* the filter does not imply unsupported relationships.

---

## 19.4 Global filters

Avoid global filters unless their semantic scope is explicitly demonstrated.

A global filter must not silently affect multiple independent datasets as though they were joined.

---

## 19.5 Empty selections

If an interaction produces no matching observations:

* do not display a misleading zero;
* explain that no observations match the current selection;
* provide a clear way to reset/change the selection.

---

# 20. Empty and Sparse Data States

Sparse evidence is an acceptable state.

The dashboard must distinguish:

```text
No data available
```

from:

```text
Data exists but no records match the current selection
```

from:

```text
Data exists but the field contains missing values
```

from:

```text
This analysis is not currently approved
```

These states must not be conflated.

---

# 21. Error States

Errors should be:

* clear,
* actionable where possible,
* technically accurate,
* non-misleading.

Do not silently substitute fabricated values.

Do not convert technical failure into:

> No data.

when the actual condition is:

> Dataset failed to load.

---

# 22. Readability and Visual Design

The redesign should prioritize:

* clear typography,
* consistent spacing,
* restrained use of color,
* strong section hierarchy,
* readable chart labels,
* sufficient contrast,
* consistent number formatting,
* concise explanatory text,
* minimal visual clutter.

The dashboard should look professional without becoming a decorative design exercise.

---

# 23. Responsive Layout

The dashboard must work reasonably across:

* standard desktop screens,
* laptop screens,
* narrower browser widths.

Layouts should not depend on excessive fixed-width assumptions.

Charts must remain readable.

Tables should avoid unnecessary horizontal overflow.

---

# 24. Accessibility

The implementation should provide:

* meaningful page titles,
* descriptive section headings,
* readable text contrast,
* clear warning/error messages,
* charts accompanied by understandable textual context,
* no information conveyed only through color,
* consistent navigation.

---

# 25. Business Language Rules

Prefer evidence-grounded language:

* "Observed"
* "Recorded"
* "Distribution"
* "Count"
* "Quantity"
* "Status"
* "Available evidence"
* "Current analytical coverage"

Avoid unsupported language:

* "Performance"
* "Success"
* "Efficiency"
* "Profitability"
* "Customer loyalty"
* "Optimization"
* "Prediction"
* "Opportunity"
* "Risk"

unless the corresponding analytical evidence supports the statement.

---

# 26. Future Capability Reopening

The following capabilities are **deferred, not permanently rejected**:

* certified KPI layer,
* revenue analytics,
* profitability analytics,
* ROI analytics,
* customer lifetime value,
* retention/churn analytics,
* forecasting,
* recommendations,
* fraud analytics,
* approved cross-dataset analytics,
* controlled temporal filtering,
* additional segmentation,
* advanced visualization,
* ML/AI-assisted analytical interpretation.

Each capability must be reopened through the appropriate analytical evidence gate.

---

## 26.1 KPI reopening

Required:

* explicit business definition,
* source evidence,
* grain,
* calculation rule,
* validation,
* reconciliation where applicable,
* semantic approval.

---

## 26.2 Cross-dataset analytics reopening

Required:

* authoritative relationship evidence,
* cardinality validation,
* fan-out analysis,
* duplicate analysis,
* reconciliation,
* approved analytical contract,
* downstream validation.

---

## 26.3 ML reopening

Required:

* valid ML problem,
* target definition,
* predictor availability,
* leakage review,
* temporal availability review,
* sufficient evidence,
* evaluation methodology,
* explicit ML approval.

---

## 26.4 Financial metric reopening

Revenue, profit, ROI and related financial measures require their own semantic and analytical validation.

Numeric dtype alone is never sufficient.

---

# 27. Technology Boundary

The dashboard remains:

* Python,
* Streamlit,
* Plotly,
* pandas-based analytical reads.

Do not introduce:

* React,
* Node.js,
* unnecessary JavaScript frameworks,
* complex frontend build systems,
* microservices,
* Kubernetes,
* unnecessary APIs,
* additional databases,

unless a future requirement genuinely establishes the need.

---

# 28. Architecture Requirements

The existing modular architecture remains the foundation.

Expected responsibilities:

```text
app.py
    ↓
semantic mapping ownership / application launcher

dashboard/app.py
    ↓
application shell

dashboard/config.py
    ↓
controlled configuration

dashboard/data.py
    ↓
analytical data access

dashboard/semantics.py
    ↓
semantic mapping adapter

dashboard/utils.py
    ↓
generic safe utilities

dashboard/record_renderer.py
    ↓
reusable approved-record presentation

dashboard/components/
    ↓
genuinely repeated UI components

dashboard/pages/
    ↓
page-specific presentation
```

Do not create additional modules unless repeated responsibilities justify them.

---

# 29. Dynamic Data Compatibility

The dashboard must continue to work with newly refreshed analytical CSVs when their approved contract remains compatible.

The implementation must not:

* hard-code row counts,
* hard-code current category values,
* assume today's maximum/minimum values,
* silently ignore schema changes,
* fabricate missing fields.

Schema changes must result in controlled behavior.

---

# 30. Semantic Safety

The dashboard must consume approved semantic mapping rather than independently inventing meanings.

`dashboard/semantics.py` remains an adapter around the authoritative mapping.

It must not become a second competing semantic contract.

---

# 31. Analytical Read-Only Requirement

The dashboard must remain read-only with respect to the analytical layer.

It must not:

* modify CSVs,
* construct new analytical datasets,
* deduplicate analytical datasets,
* perform analytical joins,
* rewrite source data,
* mutate the controlled refresh state.

---

# 32. Old/New Behavioral Equivalence

Before final UX release, the redesigned dashboard must be compared against the pre-redesign behavior.

The equivalence verification must confirm:

1. all 21 approved records remain represented;
2. all 8 business pages remain available;
3. Health remains available;
4. Explorer remains available;
5. no approved field disappears accidentally;
6. no unsupported field appears;
7. no analytical join is introduced;
8. no analytical write is introduced;
9. no ML functionality is introduced;
10. semantic meanings remain unchanged;
11. existing refresh-health behavior remains valid;
12. existing analytical data-loading boundaries remain intact.

UX improvements may change presentation.

They must not silently change analytical meaning.

---

# 33. Automated Testing Requirements

The existing dashboard test suite must be preserved and expanded where necessary.

The implementation must test:

### Navigation

* all business pages resolve;
* Health resolves;
* Explorer resolves.

### Semantic mapping

* 21 approved records remain available;
* expected pages remain represented;
* no unauthorized field is introduced.

### Data loading

* approved analytical datasets load;
* missing datasets produce controlled errors;
* invalid analytical sources are not silently accepted.

### Visualization

* approved record renderers handle valid data;
* categorical data receives appropriate treatment;
* numeric/quantity data receives appropriate treatment;
* empty data does not produce misleading output.

### Interaction

For each newly introduced interaction:

* valid selection,
* empty selection,
* reset behavior,
* boundary values,
* compatible refreshed data.

### Refresh boundary

* dashboard continues to consume the controlled analytical output;
* failed refresh does not silently masquerade as successful publication.

---

# 34. Visual QA Requirements

After implementation, each page must be visually inspected.

Minimum QA:

* P01 Overview
* P02 Commercial / Sales
* P03 Orders
* P04 Products / Catalog
* P05 Customers / Accounts
* P06 Fulfillment / Shipping
* P07 Returns / Exchange
* P08 Operations / Inventory
* Data & System Health
* Technical Dataset Explorer

Check:

* page hierarchy,
* alignment,
* spacing,
* chart readability,
* table readability,
* warnings,
* empty states,
* error states,
* sidebar navigation,
* responsive behavior,
* no clipped text,
* no misleading labels.

---

# 35. Release Gates

The UX redesign may be considered complete only when all required gates pass.

## Gate A — Analytical integrity

* 26 datasets preserved
* 12,148-row baseline preserved unless controlled refresh changes it legitimately
* 289-column baseline preserved unless controlled schema change is approved
* 0 unauthorized joins
* 0 unauthorized analytical writes
* ML remains blocked unless separately reopened

## Gate B — Semantic integrity

* 21 approved records preserved
* no unsupported dashboard fields
* no semantic reinterpretation

## Gate C — Architecture

* modular dashboard remains intact
* no unnecessary fragmentation
* no duplicated data-access logic
* no monolithic page implementation

## Gate D — Behavioral equivalence

* old/new comparison passes

## Gate E — Automated testing

* full test suite passes

## Gate F — Visual QA

* all ten dashboard experiences reviewed

## Gate G — Git/release

* `git diff --check` passes
* intended files reviewed
* one coherent commit
* push succeeds
* local HEAD equals `origin/master`
* working tree clean except intentionally held artifacts

---

# 36. Implementation Sequence

Implementation must occur incrementally.

## Stage 1 — Shared UX foundation

Review and, only where justified, improve:

* page header,
* common spacing,
* evidence-boundary presentation,
* number formatting,
* common visualization presentation.

## Stage 2 — P01 Overview

Implement the new Overview hierarchy first.

Validate before proceeding.

## Stage 3 — P02–P08

Implement business pages individually according to their evidence.

Validate each group before proceeding.

## Stage 4 — Health

Improve technical transparency without changing refresh logic.

## Stage 5 — Explorer

Improve technical usability without turning it into a business page.

## Stage 6 — Automated tests

Update and run the full test suite.

## Stage 7 — Old/new behavioral verification

Compare the redesigned dashboard with the pre-redesign checkpoint.

## Stage 8 — Visual QA

Inspect all pages.

## Stage 9 — Release closure

Run:

* validation,
* tests,
* `git diff --check`,
* file review,
* commit,
* push,
* remote verification,
* clean-tree verification.

---

# 37. Definition of Done

The dashboard UX redesign is complete only when:

* the interface is clearly more readable than the baseline;
* business and technical experiences are clearly separated;
* all 21 approved records remain correctly represented;
* the eight business pages remain available;
* Health and Explorer remain available;
* no unsupported analytics are introduced;
* no joins are introduced;
* no analytical writes are introduced;
* ML remains correctly blocked;
* approved semantics remain unchanged;
* dynamic compatible analytical refresh remains supported;
* empty/error states are controlled;
* automated tests pass;
* old/new behavioral equivalence passes;
* visual QA passes;
* Git release gates pass.

---

# 38. Final Product Position

The redesigned PurjeStore dashboard should not attempt to look like a generic enterprise BI dashboard by adding unsupported metrics.

Its value comes from:

```text
Reliable source evidence
        ↓
Validated analytical datasets
        ↓
Controlled semantic contract
        ↓
Evidence-bounded analytics
        ↓
Clear business presentation
        ↓
Technical transparency
        ↓
Controlled future expansion
```

The product is therefore designed to be:

* evidence-driven,
* explainable,
* maintainable,
* client-presentable,
* academically defensible,
* refresh-compatible,
* technically transparent,
* and extensible when new analytical evidence legitimately becomes available.

---

# 39. Acceptance Statement

This document is an implementation specification, not an authorization to modify the dashboard.

Implementation begins only after this specification is explicitly accepted.

Any requirement discovered during implementation that would change:

* analytical meaning,
* approved evidence,
* joins,
* KPIs,
* ML scope,
* source/analytical architecture,
* or refresh architecture

must stop implementation and return to the appropriate analytical or architectural approval gate.

---

# 40. Authoritative Boundary

The following remain authoritative and must not be overridden by this UX specification:

1. validated source and analytical evidence;
2. Milestone 4 relationship decisions;
3. Milestone 5 analytical contracts and semantic decisions;
4. Milestone 6 ML feasibility decision;
5. Milestone 8 dashboard evidence and UX specification;
6. Phase 15 architecture reconciliation;
7. Phase 16 controlled refresh architecture and implementation;
8. Phase 17 testing closure;
9. dashboard semantic contract;
10. approved dashboard mapping.

This document controls the **UX implementation layer** within those boundaries.
