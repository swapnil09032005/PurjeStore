# PurjeStore — Final Presentation, Client Demo, Viva & Defense Preparation

## 1. Purpose

This document is the speaking and preparation guide for the final PurjeStore academic/client presentation, live demonstration, viva, and technical defense.

The authoritative project principle is:

> The system reports what the available PurjeStore evidence can responsibly support rather than creating unsupported analytics simply to make the project appear more complex.

---

# 1. Purpose

This document is the final preparation reference for the PurjeStore project presentation, client demonstration, and academic viva. It consolidates the project facts, evidence boundaries, technical explanations, demonstration sequence, and defensible answers that should be used when presenting the completed system.

The preparation material must remain consistent with the released PurjeStore project, final report, final presentation, dashboard behavior, controlled refresh architecture, testing evidence, and the evidence-first project methodology.
# 2. Two-Minute Project Introduction

Good morning. My project is **PurjeStore: An End-to-End Data Science and Intelligent E-Commerce Decision Support System**.

The main objective of this project was to build an evidence-driven analytics and decision-support system from the available PurjeStore data, starting from the source database and continuing through data validation, cleaning, analytical dataset construction, analytics, dashboard development, controlled refresh, testing, and final delivery.

The project started with a large data environment containing **177 source tables and 178 database objects**. Instead of blindly joining all the tables, I first investigated the available data, relationships, grains, duplicates, missing values, and referential behavior. This was important because incorrect joins could create fan-out, duplicate records, or misleading business results.

After validation and cleaning, the project established **26 source-native analytical datasets**, containing **12,148 rows and 289 columns**. The analytical layer deliberately preserves the validated source grains rather than forcing unsupported cross-dataset relationships.

The analytics stage was also evidence-driven. We identified **21 approved semantic records**, but we did not artificially convert descriptive quantities into business KPIs. Therefore, the final system has **zero approved certified KPIs and zero approved analytical joins**.

Machine learning was also investigated rather than automatically added. Candidate problems were evaluated against the available evidence, and ultimately **zero ML problems were selected**. Therefore, predictive modelling, forecasting, recommendation, churn, and fraud modelling remain deliberately blocked rather than being presented without sufficient evidence.

For the client-facing application, I developed a **Streamlit and Plotly dashboard** with eight business pages covering areas such as overview, commercial data, orders, products, customers/accounts, fulfillment, returns, and operations, along with separate technical pages for Data & System Health and the Technical Dataset Explorer.

The project also includes a controlled analytical refresh architecture. It validates source schemas and grains, performs controlled source-native projections, validates the outputs, and publishes the analytical datasets without introducing uncontrolled joins or analytical writes.

Finally, the system was tested extensively. The final automated test suite contains **62 passing tests**, and the dashboard underwent behavioral equivalence and visual QA before release.

The key principle of the project is that **the system reports what the available evidence can responsibly support rather than creating artificial analytics simply to make the project appear more complex**.

---

# 3. Thirty-Second Project Introduction

My project is **PurjeStore: An End-to-End Data Science and Intelligent E-Commerce Decision Support System**.

I developed an evidence-driven pipeline from source data discovery and validation through cleaning, analytical dataset construction, analytics, dashboard development, controlled refresh, and testing.

The source environment contained **177 tables and 178 database objects**, which were validated rather than blindly joined. The final analytical layer contains **26 datasets, 12,148 rows, and 289 columns**.

The project has **21 approved semantic records, zero approved certified KPIs, zero approved analytical joins, and zero selected ML problems** because the available evidence did not justify those claims.

The final system uses **Streamlit and Plotly**, includes eight business pages plus technical monitoring and dataset-explorer pages, supports controlled analytical refresh, and has **62 passing automated tests**.

---

# 4. Five Numbers to Remember

Memorize this chain:

**177 / 178 → validate → clean → 26 / 12,148 / 289 → 21 approved records → 8 business pages + 2 technical pages → 62 tests**

Meaning:

- **177** source tables
- **178** database objects
- **26** analytical datasets
- **12,148** analytical rows
- **289** analytical columns
- **21** approved semantic records
- **8** business dashboard pages
- **2** technical pages
- **62** passing automated tests

Additional critical boundaries:

- Approved KPIs: **0**
- Approved analytical joins: **0**
- Selected ML problems: **0**
- ML status: **BLOCKED**

---

# 5. Core Project Principle

The most important sentence for the presentation and viva:

> We did not add analytics simply because they are common in e-commerce; we added them only when the PurjeStore evidence justified them.

This principle explains:

- why all source tables were not joined;
- why analytical grains were preserved;
- why certified KPIs were not invented;
- why revenue/profit/ROI claims were not introduced;
- why predictive models were not created;
- why ML remains blocked;
- why descriptive quantities are presented carefully;
- why controlled refresh validates before publication.

---

# 6. Technical Project Story

The overall project lineage is:

**Source Database / Development Sources**
→ **Discovery**
→ **Validation**
→ **Physical Cleaning**
→ **Validated Analytical Construction**
→ **26 Analytical Datasets**
→ **Evidence-Bounded Analytics**
→ **Streamlit + Plotly Dashboard**

Controlled refresh extends this with:

**Cleaned Source**
→ **Controlled Source Discovery**
→ **Contract Registry**
→ **Source Schema / Field Validation**
→ **Grain Validation**
→ **Source-Only Projection**
→ **Row / Schema / Duplicate / Null Validation**
→ **Atomic Controlled Publication**
→ **Validated Analytical Layer**
→ **Dashboard**

---

# 7. Why Were the 177 Tables Not Blindly Joined?

Answer:

The database contained many tables, but the existence of tables does not automatically prove that they should be combined analytically.

Before constructing analytical datasets, relationships were evaluated for:

- source and target fields;
- availability;
- population;
- uniqueness;
- grain;
- cardinality;
- fan-out;
- referential behavior;
- duplicates;
- semantic compatibility.

The project identified relationship candidates, but a relationship candidate is not automatically an approved analytical join.

The final analytical layer therefore uses **source-native analytical datasets** where the evidence and grain are defensible.

The final approved analytical join count is **0**.

This avoids:

- row multiplication;
- measure inflation;
- accidental many-to-many behavior;
- misleading totals;
- unsupported business interpretations.

---

# 8. Analytical Dataset Explanation

The final analytical layer contains:

- 26 analytical datasets;
- 12,148 total rows;
- 289 total columns.

These datasets preserve validated source-native grains.

Important grain exceptions were documented rather than silently corrected.

In particular:

- `daily_category_metrics`
- `daily_platform_metrics`
- `daily_vendor_metrics`

have documented grain considerations.

`daily_vendor_metrics` contains **6 duplicate rows that were intentionally preserved** because deduplicating them without an approved semantic basis would alter the source evidence.

Therefore:

> A duplicate is not automatically an error. Whether it should be removed depends on the validated grain and semantic contract.

---

# 9. Why Are There Zero Certified KPIs?

Answer:

The project identified candidate measures, but a candidate measure is not automatically a certified business KPI.

A KPI requires sufficient evidence about:

- meaning;
- grain;
- calculation;
- semantic stability;
- business interpretation;
- supporting relationships;
- validation.

The project therefore deliberately kept:

**Approved certified KPIs = 0**

This does not mean that the data is useless.

It means the system distinguishes descriptive evidence from formally certified business-performance measures.

For example, quantities and counts can be displayed descriptively without claiming that they represent revenue, profit, conversion, retention, ROI, or another certified KPI.

---

# 10. Machine-Learning Defense

## Question: Why did you not build ML models?

Answer:

Machine learning was evaluated as part of the project rather than automatically added.

Candidate datasets and possible prediction problems were reviewed against the available evidence.

After the feasibility assessment, **zero ML problems satisfied the evidence requirements for responsible implementation**.

Therefore:

- no predictive model was created;
- no forecasting model was created;
- no recommendation engine was created;
- no churn model was created;
- no fraud model was created;
- no model artifacts were created.

The final ML status is:

**BLOCKED**

This is an evidence-based scope decision, not an unfinished model implementation.

---

# 11. Dashboard Explanation

Technology selected:

**STREAMLIT_PRIMARY_WITH_PLOTLY**

The final dashboard contains:

## Business pages

1. P01 — Executive Overview
2. P02 — Commercial / Sales
3. P03 — Orders
4. P04 — Products / Catalog
5. P05 — Customers / Accounts
6. P06 — Fulfillment / Shipping
7. P07 — Returns / Exchange
8. P08 — Operations / Inventory

## Technical pages

9. Data & System Health
10. Technical Dataset Explorer

The dashboard intentionally separates:

- business-facing descriptive evidence;
- technical system health;
- technical dataset inspection.

Predictive pages are not presented because ML remains blocked.

---

# 12. Dashboard Speaking Pattern

For every business page, explain in this order:

1. What is the page about?
2. What evidence is available?
3. What does the displayed record actually represent?
4. What can the user observe?
5. What should the user not infer?

Use:

> “This page presents descriptive evidence from the approved source-native analytical record.”

Avoid:

> “This proves business performance.”

unless the evidence and approved semantic contract actually support that claim.

---

# 13. Controlled Refresh Explanation

The controlled refresh system exists to make analytical publication repeatable without changing the approved analytical methodology.

The refresh process:

1. discovers the expected cleaned source;
2. validates the source schema;
3. validates physical grain;
4. performs the controlled source-only analytical projection;
5. validates output schema;
6. validates row counts;
7. validates duplicate behavior;
8. validates projected values;
9. stages the output;
10. reads it back;
11. publishes atomically;
12. produces a refresh report.

The refresh process does **not**:

- invent joins;
- create unsupported datasets;
- deduplicate the source arbitrarily;
- create KPIs;
- train ML models;
- modify the original raw source.

---

# 14. Testing and Quality

The final automated test suite contains:

**62 passing tests**

The project also completed:

- dashboard behavioral equivalence;
- semantic record preservation;
- analytical baseline validation;
- compile validation;
- Git diff validation;
- visual QA;
- release validation.

The dashboard redesign preserved the approved semantic contract.

The final project release was pushed to:

`origin/master`

and the working tree was verified clean.

---

# 15. Important Questions and Answers

## Q: Why not use Power BI?

Answer:

The project selected **Streamlit with Plotly** as the primary dashboard technology because the project required an integrated Python-based analytical application with controlled data access, technical pages, validation boundaries, and a reproducible code-based workflow.

Power BI was considered but was not selected as the primary implementation.

---

## Q: Why Streamlit?

Answer:

Streamlit allows the analytical application to remain closely connected to the Python analytical environment while providing interactive dashboard functionality and clear separation between data access, semantic mapping, page rendering, and technical inspection.

---

## Q: Why Plotly?

Answer:

Plotly provides interactive visualizations that integrate naturally with the Streamlit application and can represent the project's descriptive evidence without requiring unsupported predictive analytics.

---

## Q: Why not calculate revenue?

Answer:

The project does not certify a revenue KPI because the available evidence did not establish a sufficiently defensible analytical contract for such a claim.

Rather than creating a potentially misleading revenue calculation, the project preserves the evidence boundary.

---

## Q: Why not calculate profit or ROI?

Answer:

The same evidence-first principle applies.

Profit and ROI require defensible revenue, cost, and business-impact semantics. Those were not established as approved analytical contracts, so the project does not claim them.

---

## Q: Why not calculate customer lifetime value?

Answer:

Customer lifetime value would require a defensible customer identity, transaction history, revenue or contribution semantics, and an approved methodology.

Those requirements were not established, so CLV was not implemented.

---

## Q: Why not create customer segmentation?

Answer:

Segmentation would require a defensible customer-level analytical grain and approved semantic interpretation.

The project does not infer unsupported customer master relationships merely because account-related tables exist.

---

## Q: Why no recommendation system?

Answer:

A recommendation system would require suitable interaction, product, and outcome evidence and an approved modelling problem.

The ML feasibility assessment did not establish that evidence, so recommendations were not implemented.

---

## Q: Is the project incomplete because ML is blocked?

Answer:

No.

The project completed an explicit ML feasibility assessment. The correct engineering decision was to avoid implementing unsupported predictive functionality.

The project is complete within its evidence-supported scope.

---

# 16. Client Demo Order

Use this order during a live demonstration:

### 1. Open the dashboard

Explain the overall purpose and evidence boundary.

### 2. P01 — Executive Overview

Show the high-level descriptive evidence.

### 3. P02 — Commercial / Sales

Explain the approved payment and invoice-related records.

### 4. P03 — Orders

Explain the approved order-item quantity evidence.

### 5. P04 — Products

Explain the product-status evidence.

### 6. P05 — Customers / Accounts

Explain the wallet transaction records without claiming unsupported customer behavior.

### 7. P06 — Fulfillment / Shipping

Explain shipment-item and hub-inventory quantities.

### 8. P07 — Returns / Exchange

Explain return status and hub-return quantity evidence.

### 9. P08 — Operations / Inventory

Explain the approved operational records.

### 10. Data & System Health

Show controlled refresh status and technical validation.

### 11. Technical Dataset Explorer

Demonstrate that the underlying analytical datasets can be inspected without turning the technical page into an unsupported business-analysis page.

### 12. Close with architecture

Explain the full source → validation → analytical → dashboard lineage.

---

# 17. What NOT to Say During the Demo

Do not casually say:

- “This is revenue.”
- “This is profit.”
- “This proves profitability.”
- “This is customer retention.”
- “This predicts churn.”
- “This forecasts sales.”
- “This recommends products.”
- “This detects fraud.”
- “This calculates ROI.”
- “This proves conversion.”
- “This optimizes inventory.”
- “This predicts future demand.”

unless future evidence formally reopens and approves those capabilities.

Instead say:

- “This is an observed count.”
- “This is a descriptive quantity.”
- “This record is presented at its validated source-native grain.”
- “This is an approved semantic record.”
- “This capability is currently outside the evidence-supported scope.”
- “That is a future conditional capability.”

---

# 18. Strong Answers When Challenged

## “Why didn't you just join the data?”

> Because joining data is not automatically equivalent to producing valid analytics. I first validated relationships, grain, uniqueness, cardinality, fan-out, and referential behavior. Where the evidence did not justify an analytical join, I preserved the source-native dataset instead.

## “But a real e-commerce project should have KPIs.”

> Common e-commerce KPIs are useful only when their underlying evidence and calculation semantics are reliable. This project deliberately distinguishes candidate measures from certified KPIs. The final approved KPI count is zero.

## “Why didn't you make the project more advanced with ML?”

> Complexity was not treated as a goal by itself. ML was evaluated, and the evidence did not support a defensible selected problem. Implementing a model anyway would create an unsupported result.

## “Can this become a production system?”

> The architecture already includes controlled refresh, validation, analytical contracts, testing, and a dashboard layer. Production deployment can be developed conditionally around those controls, but it should not bypass the existing evidence and validation boundaries.

## “What happens if the source data changes?”

> The controlled refresh architecture validates the expected source schema, grain, output schema, row behavior, duplicate behavior, and projected values before publication. A change that violates the controlled contract should fail validation rather than silently producing a different analytical result.

---

# 19. Academic Defense

The project demonstrates:

- data discovery;
- database understanding;
- relationship analysis;
- data quality assessment;
- physical cleaning;
- analytical data design;
- grain management;
- descriptive analytics;
- ML feasibility assessment;
- dashboard engineering;
- controlled refresh;
- automated testing;
- behavioral validation;
- visual QA;
- reproducible release management.

The project is therefore not simply a dashboard.

The dashboard is the final presentation layer of a larger validated analytical system.

---

# 20. Final Outcome

The final PurjeStore system contains:

- 177 source tables;
- 178 database objects;
- 69 validated relationship records;
- 52 relationship candidates;
- 26 analytical datasets;
- 12,148 analytical rows;
- 289 analytical columns;
- 21 approved dashboard semantic records;
- 8 business dashboard pages;
- 2 technical dashboard pages;
- 0 approved certified KPIs;
- 0 approved analytical joins;
- 0 selected ML problems;
- 62 passing automated tests;
- controlled analytical refresh;
- Streamlit + Plotly dashboard;
- final project report;
- final presentation;
- Git-controlled release.

---

# 21. Final Closing Statement

A strong closing statement is:

> “The main achievement of this project is not simply producing a dashboard. It is establishing a controlled path from source data to validated analytical evidence and then presenting that evidence through a client-facing application. Where the data supported an analytical claim, it was implemented and validated. Where the evidence did not support a claim, the system deliberately preserved that boundary.”

---

# 22. Emergency Viva Memory Card

If you forget everything, remember:

**PURJESTORE**

**P** — PurjeStore evidence first
**U** — Unsupported claims avoided
**R** — Relationships validated
**J** — Joins only when justified; final approved joins = 0
**E** — Evidence-bounded analytics
**S** — Source-native analytical datasets
**T** — Testing and controlled refresh
**O** — Observed descriptive evidence
**R** — Reproducible release
**E** — Explain limitations honestly

Core numbers:

**177 / 178**

**26 / 12,148 / 289**

**21 approved records**

**8 business + 2 technical pages**

**0 KPIs / 0 joins / 0 selected ML**

**62 tests**

---

# 23. Presentation Release Reference

Final presentation:

`reports/presentation/PURJESTORE_FINAL_PROJECT_PRESENTATION.pptx`

Final presentation release commit:

`d652b85962e1b4b20fab2252b823e720cb465dca`

Commit message:

`docs: release final project presentation`

Release status:

- Presentation exists: PASS
- Visual QA: PASS
- Structural validation: PASS
- Git diff check: PASS
- Push: PASS
- HEAD == origin/master: PASS
- Working tree clean: PASS

---

# 24. Preparation Rule

During the viva or client demonstration:

1. Explain what the evidence supports.
2. Explain the grain.
3. Explain the limitation when necessary.
4. Never invent a business interpretation.
5. Never turn a descriptive quantity into a certified KPI.
6. Never claim ML functionality.
7. Never claim a join exists when the approved analytical join count is zero.
8. If asked about a future feature, describe it as conditional on future evidence and validation.
