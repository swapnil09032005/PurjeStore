# PurjeStore: An End-to-End Data Science and Intelligent E-Commerce Decision Support System

## Final Project Report

**Project:** PurjeStore
**Report type:** Final Academic and Client Project Report
**Primary technology:** Python, pandas, Streamlit, Plotly, SQL/MariaDB
**Final release:** `6072285abad63c247a3f69cef3416d17dee5637e`

---

# 1. Introduction

## 1.1 Project Background

PurjeStore is an end-to-end data science and analytics project developed around a recovered and validated e-commerce data environment. The project was designed to establish a controlled analytical workflow from source data through validation, cleaning, analytical dataset construction, descriptive analysis, application development, controlled refresh, testing, and final delivery.

The project was developed with two objectives. The first was to establish an academically defensible data science workflow in which analytical conclusions are supported by the available evidence. The second was to produce a client-presentable analytical application that exposes validated descriptive information without introducing unsupported business claims.

The project therefore treats evidence quality and traceability as core design requirements. The workflow follows the lineage:

**Source data → discovery and validation → cleaning → analytical datasets → evidence-bounded analytics → dashboard → controlled refresh → testing and release**

This approach ensures that the final application is connected to the underlying analytical evidence rather than being built around assumptions about what an e-commerce system should contain.

## 1.2 Project Objectives

The completed project addresses the following objectives:

1. Recover and establish a usable PurjeStore data environment.
2. Inventory and understand the available source data.
3. Examine relationships and domain evidence before constructing analytical data.
4. Perform evidence-based data quality assessment and physical cleaning.
5. Define validated analytical datasets with explicit grain and semantic boundaries.
6. Evaluate candidate measures and analytical possibilities without automatically promoting them to business KPIs.
7. Assess whether the available evidence supports machine-learning problems.
8. Build an evidence-bounded Streamlit and Plotly dashboard.
9. Establish a controlled refresh mechanism for the validated analytical layer.
10. Establish automated testing and release validation.
11. Produce a reproducible, traceable, and client-presentable final project.

## 1.3 Evidence-Bounded Analytical Approach

A central principle of the project is that the available PurjeStore evidence determines what can legitimately be claimed.

The project does not assume that the presence of a field automatically establishes its business meaning. Similarly, a numerical field is not automatically treated as a KPI, and a relationship between tables is not automatically used to construct a joined analytical dataset.

The final analytical boundary therefore records the difference between:

- observed source evidence;
- validated data characteristics;
- derived descriptive results;
- interpretation;
- business decisions;
- assumptions;
- exceptions;
- limitations; and
- future or deferred work.

This distinction is particularly important because the completed project contains **0 approved final business KPIs** and **0 approved cross-dataset joins**. The dashboard consequently presents approved descriptive evidence rather than manufacturing KPI or cross-dataset claims.

## 1.4 Machine-Learning Boundary

Machine learning was evaluated as part of the project rather than being assumed as a mandatory component.

The ML feasibility assessment examined potential analytical problems against the available data, target evidence, grain, sample characteristics, and other requirements needed to support a defensible ML problem.

The final assessment selected **0 ML problems**. Consequently, ML remains **BLOCKED** in the completed release. No predictive models, forecasts, recommendation models, churn models, fraud models, or other unsupported predictive outputs are presented as project results.

This is treated as an evidence-based project outcome rather than a missing implementation.

## 1.5 Final Application

The completed analytical application uses **Streamlit with Plotly** as its primary dashboard technology.

The final dashboard contains eight business-oriented pages:

1. P01 Executive Overview
2. P02 Commercial / Sales
3. P03 Orders
4. P04 Products / Catalog
5. P05 Customers / Accounts
6. P06 Fulfillment / Shipping
7. P07 Returns / Exchange
8. P08 Operations / Inventory

It also contains two technical experiences:

- Data & System Health
- Technical Dataset Explorer

The dashboard is designed to expose approved descriptive evidence while maintaining the project's analytical boundaries. It does not write to the analytical layer, introduce unsupported joins, or produce ML outputs.

## 1.6 Final Project Status

At final release, the validated project baseline contains:

- **26 analytical datasets**
- **12,148 analytical rows**
- **289 analytical columns**
- **21 approved dashboard semantic records**
- **0 approved final business KPIs**
- **0 approved cross-dataset joins**
- **0 selected ML problems**
- **8 business dashboard pages**
- **2 technical dashboard experiences**
- **62 automated tests passing**

The final release is synchronized with the remote repository and has a clean working tree.

---

# 2. System and Data Context

## 2.1 PurjeStore Data Environment

The project began with the recovery and establishment of the PurjeStore data environment. The recovered environment contains a substantial source-data universe rather than a single flat analytical table.

The validated source inventory contains **177 base/source tables** and **178 database objects**, including the database view `v_shipment_qc_summary`.

The recovery and inventory work established the source environment required for subsequent discovery, relationship analysis, cleaning, and analytical construction.

The project also established working CSV representations of the development sources and a protected cleaned-source layer. The analytical workflow does not modify the original recovered SQL sources.

## 2.2 Source-to-Analytical Architecture

The completed architecture separates source evidence from analytical outputs.

The implemented development lineage is:

**Development Sources**
↓
**Discovery / Validation**
↓
**Physical Cleaning**
↓
**Validated Analytical Construction**
↓
**26 Analytical Datasets**
↓
**Evidence-Bounded Analytics**
↓
**Streamlit + Plotly Dashboard**

This separation prevents the dashboard from becoming the location where analytical data is silently transformed.

The analytical layer is treated as a validated intermediate product. Dashboard components consume that layer rather than constructing arbitrary relationships at presentation time.

## 2.3 Analytical Dataset Baseline

The final analytical layer contains **26 source-native analytical datasets**, representing **12,148 rows and 289 columns** in the verified project baseline.

The datasets were not created by blindly joining the complete source database. Instead, analytical construction was governed by the validated relationship evidence, dataset contracts, grain definitions, and semantic constraints established during earlier project milestones.

The final analytical construction therefore preserves source-native evidence where that evidence is sufficient and avoids creating unsupported integrated datasets.

## 2.4 Relationship and Grain Constraints

Relationship analysis was performed before analytical construction.

The project identified relationship candidates and evaluated them against available source keys, populated fields, duplicate behavior, fan-out risk, and referential evidence. The completed relationship work did not result in arbitrary constructed analytical joins.

The final analytical layer therefore operates under a strict boundary:

**Approved cross-dataset joins = 0**

This means that the absence of joins is an intentional result of the evidence and analytical contracts, rather than an accidental omission.

Dataset grain is also treated as an explicit analytical property. Where source-native datasets contain legitimate exceptions, those exceptions are preserved rather than silently deduplicated or reshaped.

## 2.5 Data Quality and Cleaning Context

Data quality assessment and physical cleaning were performed before the final analytical layer was established.

The workflow considered issues such as:

- missing values;
- duplicate records;
- source availability;
- populated versus unpopulated fields;
- key integrity;
- grain consistency;
- referential evidence;
- semantic ambiguity; and
- source-specific exceptions.

Cleaning was evidence-based rather than an attempt to make every source uniformly shaped.

Consequently, known exceptions and unresolved semantic issues are retained as documented project limitations or deferred items when the evidence does not justify a stronger interpretation.

## 2.6 Analytical and Dashboard Boundary

The final dashboard reads the validated analytical layer.

The dashboard does not act as an additional data-engineering layer. It does not create unsupported cross-dataset relationships, write analytical results back into the source analytical CSVs, or introduce predictive outputs.

The dashboard's semantic mapping is controlled so that only approved fields are exposed through the business pages.

This architecture provides a clear separation between:

**data preparation → analytical evidence → presentation**

and supports traceability between the analytical datasets and the dashboard experiences.

## 2.7 Controlled Refresh Context

The completed system also contains a controlled analytical refresh mechanism.

The refresh architecture validates source schema and physical grain, performs controlled source-only analytical projection, validates the resulting analytical output, and publishes the validated result through a controlled publication process.

The refresh process does not introduce arbitrary joins, aggregation, deduplication, KPI activation, or ML processing.

This allows the analytical layer to be refreshed while retaining the same evidence and contract boundaries established during project construction.

## 2.8 Final Technology Context

The final implementation uses technologies appropriate to the completed evidence and architecture:

- **Python 3.11.x**
- **pandas 3.0.5**
- **Streamlit 1.64.0**
- **Plotly 7.1.0**
- **MariaDB 10.4.32**
- **pytest 9.1.1**
- **Git / GitHub**

The project deliberately avoids introducing additional application frameworks or infrastructure where they are not required by the evidence or final system responsibilities.

---


# 3. Data Discovery and Inventory

## 3.1 Discovery Objective

The data discovery stage established an evidence-based understanding of the recovered PurjeStore data environment before analytical datasets or dashboard outputs were constructed.

The objective was not simply to count tables. The discovery process established what source objects existed, which sources were available for analysis, what fields and structures they contained, and which characteristics required additional validation before analytical use.

This stage provided the foundation for subsequent relationship analysis, data quality assessment, cleaning, analytical dataset construction, and dashboard development.

## 3.2 Recovered Source Inventory

The validated PurjeStore environment contains:

- **177 base/source tables**
- **178 database objects**
- **177 imported SQL source objects**
- **177 working CSV source representations**
- **177 cleaned CSV source representations**

The additional database object is the view:

`v_shipment_qc_summary`

The inventory therefore distinguishes between base/source tables and the complete database-object count rather than treating every database object as an equivalent analytical source.

## 3.3 Source Representation

The project established working source representations so that discovery, validation, and cleaning could be performed in a controlled development environment.

The source lineage was maintained as:

**Recovered SQL/database evidence → working source representation → cleaned source layer → analytical construction**

The original recovered SQL evidence was kept protected. Cleaning operations were not used as a substitute for the original source evidence.

This separation supports reproducibility because the analytical workflow can be traced back to the recovered source environment rather than only to already-transformed files.

## 3.4 Schema and Field Discovery

Discovery examined the structure of the available source data before deciding how individual datasets could be used.

The process considered:

- table and object availability;
- field names and schemas;
- populated versus unpopulated fields;
- candidate identifiers and keys;
- duplicate behavior;
- apparent grain;
- data types;
- missingness;
- source-specific anomalies; and
- potential relationship evidence.

A field was not treated as analytically meaningful merely because its name appeared to suggest a business concept. Its interpretation had to remain consistent with the available evidence and later validation.

## 3.5 Source Availability and Population

Source availability was treated as a separate validation concern from semantic interpretation.

A source could exist in the recovered environment without necessarily providing sufficient populated evidence for every proposed analytical use. Consequently, later relationship and analytical-contract validation examined whether required fields were actually available and populated.

This prevented unavailable or sparsely evidenced fields from being silently promoted into analytical outputs.

## 3.6 Discovery Findings

The discovery stage established that PurjeStore is a multi-source environment containing substantially more source data than was ultimately required for the final analytical layer.

The final system therefore does not attempt to expose all 177 sources directly through the dashboard.

Instead, source evidence was progressively narrowed through validation and analytical contracts until the completed analytical layer contained **26 validated analytical datasets**.

This reduction is intentional. The analytical layer represents evidence that passed the project's construction boundaries rather than a direct mirror of every source table.

## 3.7 Discovery Boundary

The discovery stage was deliberately separated from analytical interpretation.

At this point in the workflow, identifying a possible relationship, measure, identifier, or business-related field did not automatically authorize its use in a final analytical dataset or dashboard.

Candidates required subsequent validation.

This distinction is important because the final project contains:

- **0 approved cross-dataset joins**
- **0 approved final business KPIs**
- **0 selected ML problems**

The discovery process therefore generated evidence and candidates; it did not manufacture final analytical claims.

---

# 4. Relationship and Domain Validation

## 4.1 Purpose of Relationship Validation

Relationship validation was performed before analytical construction to determine whether apparent connections between source datasets were sufficiently supported for controlled analytical use.

The purpose was to establish evidence about keys, grain, cardinality, fan-out risk, and referential behavior rather than to maximize the number of joins.

This was a critical control because blindly joining the recovered source universe could introduce duplicate rows, measure inflation, incorrect grain, or unsupported business interpretations.

## 4.2 Authoritative Relationship Evidence

The completed relationship assessment established **69 authoritative relationship records**.

These consisted of:

- **68 concrete relationships**
- **1 dynamic relationship**

The relationship evidence was maintained separately from the later analytical construction decision.

A relationship record therefore represents documented evidence of a possible connection; it does not by itself mean that a production analytical join was approved.

## 4.3 Relationship Candidates

The relationship analysis identified **52 analytical relationship candidates** for further evaluation.

Each candidate was evaluated against the available evidence rather than being accepted solely because matching column names appeared across datasets.

The evaluation considered the availability and population of source fields, key behavior, duplicate characteristics, dataset grain, and the possibility of fan-out or semantic distortion.

## 4.4 Key and Grain Validation

Relationship validation examined whether the proposed source and target fields could support the intended analytical grain.

The completed validation established that all **52 relationship candidates** had a locked analytical grain and that their required source evidence was available and populated.

The relationship evidence also identified controlled fallback key mappings where required:

- `accounts → accountId`
- `offer_usage_tracking → usageId`

These fallbacks were documented as controlled evidence rather than silently inferred relationships.

## 4.5 Fan-Out and Cardinality Validation

Potential fan-out was explicitly evaluated because a technically valid key match can still produce analytically incorrect results when one source record expands into multiple target records.

The completed relationship-path validation expanded the relationship evidence into **78 paths**, of which **77 were concrete paths**.

The validation reported:

- **75 paths without source-target fan-out**
- **2 duplicate-target warnings**
- **1 dynamic path**

These results were retained as validation evidence rather than automatically converting every path into an analytical join.

## 4.6 Referential Evidence

Referential behavior was also evaluated across the validated relationship paths.

The completed assessment recorded:

- **43 full matches**
- **1 partial match**
- **33 paths with no matching source keys**
- **1 dynamic relationship**

The presence of non-matching keys was not automatically treated as an error. It was preserved as evidence requiring appropriate interpretation within the source and relationship context.

This prevented the project from forcing referential completeness where the recovered evidence did not establish it.

## 4.7 Relationship Exceptions and Ambiguity

The relationship analysis preserved documented exceptions rather than hiding them during analytical construction.

One example was the invoice relationship discrepancy identified during the relationship-validation stages. An earlier evidence count identified **9** invoice-related relationships, while recomputation from the authoritative relationship file produced **8 direct concrete participations**. A broader text search produced **10** occurrences because terms such as e-invoice and e-way-bill were also detected.

The discrepancy was therefore preserved as an evidence distinction rather than being artificially reconciled into a single number.

This illustrates the project's broader rule that terminology-based discovery and authoritative relationship evidence are not automatically equivalent.

## 4.8 Analytical Join Decision

Although relationship candidates were identified and validated, the final analytical construction process did not approve cross-dataset analytical joins.

The final state is:

**Approved cross-dataset joins = 0**

The reason is methodological: the project required sufficient evidence and an approved analytical dataset contract before a relationship could be used to construct an analytical output.

Where that condition was not met, the relationship remained documented evidence rather than becoming a constructed dataset.

The final relationship-construction assessment therefore recorded:

**0 constructed analytical relationship outputs**

with the documented status:

`NOT_CONSTRUCTED_NO_APPROVED_ANALYTICAL_DATASET_CONTRACT`

## 4.9 Domain and Grain Preservation

Relationship validation also protected dataset grain.

The project did not assume that all source datasets represented the same entity level or temporal level. Source-native analytical datasets were therefore retained where they provided defensible evidence without requiring unsupported integration.

Known grain exceptions were preserved as documented analytical characteristics.

For example, `daily_vendor_metrics` contains **102 rows**, including **6 duplicate rows** that were intentionally preserved. These rows were not silently deduplicated merely to produce a cleaner-looking analytical dataset.

## 4.10 Relationship Validation Outcome

The completed relationship and domain-validation stage established a controlled boundary between:

**relationship evidence → candidate analytical use → approved analytical construction**

The final outcome was:

- **69 authoritative relationship records**
- **68 concrete relationships**
- **1 dynamic relationship**
- **52 analytical relationship candidates**
- **78 expanded relationship paths**
- **77 concrete paths**
- **0 constructed analytical relationship outputs**
- **0 approved cross-dataset joins**

This outcome is consistent with the project's evidence-bounded methodology. The relationship stage successfully documented and tested possible connections without assuming that every detected relationship should be used in the final analytical system.

---


# 5. Data Quality and Cleaning

## 5.1 Data Quality Objective

Data quality assessment was performed before final analytical dataset construction so that analytical outputs would be based on validated source evidence rather than unexamined raw structures.

The objective was not to make every source dataset uniform. Instead, the process identified whether source data was available, populated, structurally consistent, and suitable for the intended analytical use.

The quality workflow considered both physical data characteristics and semantic limitations.

## 5.2 Quality Assessment Areas

The completed quality assessment considered:

- source availability;
- schema and field structure;
- missing values;
- duplicate records;
- candidate key behavior;
- populated versus unpopulated fields;
- dataset grain;
- referential evidence;
- relationship cardinality;
- semantic ambiguity; and
- source-specific exceptions.

These checks were used to determine whether evidence could safely progress into the analytical layer.

A quality issue was not automatically treated as a reason to delete or alter records. The treatment depended on the evidence and the intended analytical grain.

## 5.3 Evidence-Based Physical Cleaning

Physical cleaning was performed on the working source representations before analytical construction.

The cleaning process was deliberately evidence-based. It did not attempt to impose a generic e-commerce schema on the recovered PurjeStore environment.

The original recovered SQL evidence remained protected, while cleaned source representations provided the controlled inputs for subsequent analytical construction.

This created the following separation:

**Original recovered evidence → working source → cleaned source → analytical construction**

The separation allows later validation to distinguish an original source characteristic from a transformation introduced during cleaning.

## 5.4 Missingness and Population

Missingness was evaluated together with field population and intended analytical use.

A field being partially populated did not automatically justify filling, imputing, or otherwise modifying its values.

Where available evidence was insufficient to establish a defensible interpretation, the limitation was preserved rather than replaced with an assumed value.

This approach is particularly important for business-facing analytics because an artificial value can create a more misleading result than an explicitly documented missing value.

## 5.5 Duplicate Handling

Duplicate behavior was evaluated in relation to dataset grain rather than treated as a universal data-quality defect.

Where duplicate records represented a documented characteristic of the source-native analytical grain, they were preserved.

A specific example is `daily_vendor_metrics`, which contains **102 rows**, including **6 duplicate rows** that were intentionally preserved.

These records were not removed merely to produce a numerically cleaner dataset because doing so would have changed the evidence represented by the source-native dataset.

## 5.6 Key and Referential Quality

Key behavior was assessed during the relationship and analytical-contract stages.

The project examined candidate identifiers, source availability, population, duplicate behavior, and referential evidence before allowing relationship evidence to influence analytical construction.

The relationship validation recorded:

- **43 full referential matches**
- **1 partial match**
- **33 paths with no matching source keys**
- **1 dynamic relationship**

Non-matching keys were not automatically converted into synthetic matches.

This prevented the analytical layer from implying referential certainty that was not established by the recovered evidence.

## 5.7 Grain Validation

Dataset grain was treated as a fundamental data-quality property.

Before analytical construction, candidate datasets and relationships were evaluated to determine whether their intended grain could be identified and protected.

This prevented transformations such as arbitrary joins or deduplication from silently changing the meaning of the data.

Known grain exceptions were documented and preserved rather than normalized away.

## 5.8 Semantic Quality and Ambiguity

Physical data quality and semantic quality were treated as separate concerns.

A field can be technically valid while its business meaning remains uncertain. Therefore, field names, values, and apparent business concepts were not automatically converted into certified measures or KPIs.

The project preserved documented semantic warnings and deferred interpretations where the available evidence did not support a stronger conclusion.

Examples include source-specific warning areas involving revenue-related fields, `ackNo`, notification/order evidence gaps, and temporary semantic variants.

These issues were retained as documented analytical boundaries rather than being silently resolved through assumptions.

## 5.9 Cleaning Boundaries

The cleaning stage deliberately avoided transformations that would alter the analytical methodology without evidence.

The completed project did not use cleaning to:

- manufacture business KPIs;
- create unsupported relationships;
- infer missing business meaning;
- remove legitimate source-native duplicate behavior;
- create predictive targets; or
- prepare unsupported ML outputs.

Cleaning therefore served as a quality-control stage rather than as a mechanism for manufacturing analytical conclusions.

## 5.10 Data Quality Outcome

The completed quality and cleaning process established a controlled cleaned-source layer suitable for validated analytical construction.

The resulting principle was:

**Clean what is demonstrably a physical data-quality issue; preserve what is a meaningful source characteristic; document what remains uncertain.**

This approach supports reproducibility and protects the distinction between source evidence and analytical interpretation.

---

# 6. Analytical Dataset Design

## 6.1 Analytical Design Objective

The analytical dataset stage transformed validated source evidence into controlled analytical outputs while preserving explicit dataset contracts and grain.

The objective was not to integrate every available source into a single enterprise dataset.

Instead, each analytical dataset had to have a defensible source basis, identifiable grain, controlled fields, and a documented analytical purpose.

## 6.2 Analytical Dataset Baseline

The completed analytical layer contains:

- **26 analytical datasets**
- **12,148 total rows**
- **289 analytical columns**

These datasets form the validated analytical layer consumed by the dashboard and controlled refresh process.

The analytical layer is therefore a curated evidence layer rather than a copy of the complete 177-table source environment.

## 6.3 Source-Native Analytical Construction

The analytical datasets were constructed using source-native evidence where that evidence could support a defensible analytical output.

The project deliberately avoided blind integration of the full source database.

The final construction boundary is:

**validated source evidence → controlled analytical projection/construction → analytical dataset**

This preserves traceability between source fields and analytical outputs.

## 6.4 Dataset Contracts and Grain

Analytical dataset contracts were used to define the expected structure and behavior of the datasets.

The contracts establish controlled expectations around:

- source dataset;
- analytical fields;
- field order;
- dataset grain;
- row behavior;
- duplicate behavior;
- semantic exceptions; and
- validation requirements.

The contract approach prevents downstream dashboard code from becoming the authority for analytical meaning.

## 6.5 No Approved Cross-Dataset Joins

The final analytical layer contains **0 approved cross-dataset joins**.

This is an intentional methodological boundary.

Although relationship evidence and candidates were evaluated earlier, a relationship was not sufficient by itself to authorize an analytical join. Construction required an approved analytical dataset contract and sufficient supporting evidence.

Where those conditions were not satisfied, the relationship remained documented evidence rather than becoming an analytical output.

Consequently, the 26 analytical datasets remain source-native within the completed release.

## 6.6 Candidate Measures and KPI Boundary

The analytical design process identified **193 candidate measures** for consideration.

Candidate identification did not automatically activate a measure as a business KPI.

After evidence and semantic evaluation, the completed project contains:

**0 approved final business KPIs**

This distinction prevents numerical fields from being presented as certified business-performance indicators without sufficient evidence for their definition and interpretation.

The dashboard therefore presents approved descriptive evidence rather than claiming unsupported KPI performance.

## 6.7 Grain Exceptions

The analytical layer preserves documented source-native grain exceptions.

Known exceptions include:

- `daily_category_metrics`;
- `daily_platform_metrics`; and
- `daily_vendor_metrics`.

The `daily_vendor_metrics` dataset contains **102 rows**, including **6 duplicate rows** that were intentionally preserved.

These characteristics are part of the documented analytical evidence and were not removed solely for presentation convenience.

## 6.8 Analytical Schema Validation

The analytical construction process validates the resulting datasets against their expected contracts.

Validation includes controls such as:

- expected schema;
- expected field order;
- row-count behavior;
- duplicate behavior;
- source-projection values; and
- documented semantic exceptions.

The controlled refresh process uses the same contract boundary when regenerating the analytical layer.

This ensures that refreshability does not silently change the analytical dataset definition.

## 6.9 Analytical Layer and Dashboard Boundary

The analytical layer is consumed by the Streamlit and Plotly dashboard.

The dashboard does not become an additional analytical transformation layer.

In particular, the completed dashboard does not introduce:

- cross-dataset joins;
- analytical writes;
- unsupported KPI calculations;
- predictive outputs; or
- new analytical datasets.

This separation keeps analytical methodology in the validated data layer and presentation logic in the dashboard layer.

## 6.10 Final Analytical Design Outcome

The final analytical design establishes the following controlled baseline:

- **26 analytical datasets**
- **12,148 analytical rows**
- **289 analytical columns**
- **193 candidate measures**
- **0 approved final business KPIs**
- **0 approved cross-dataset joins**

The result is an evidence-bounded analytical layer that prioritizes traceability, explicit grain, contract validation, and reproducibility over artificial integration or unsupported analytical complexity.

---

# 7. Exploratory and Descriptive Analytics

## 7.1 Analytical Objective

Exploratory and descriptive analysis was performed after the analytical layer had been validated.

The purpose was to understand and communicate what the available PurjeStore evidence could legitimately show without extending the data beyond its approved analytical boundaries.

The analysis therefore focused on descriptive evidence rather than forcing predictive or causal interpretations.

The analytical workflow maintained the distinction between:

- observed evidence;
- derived descriptive results;
- interpretation;
- business decision;
- assumption;
- limitation; and
- future or deferred analysis.

## 7.2 Evidence-Bounded Exploration

Exploratory analysis was constrained by the validated analytical datasets and their documented grain.

The project did not treat every numerical field as a business metric and did not automatically convert counts, quantities, statuses, or categorical values into certified KPIs.

This was necessary because the completed analytical assessment resulted in:

**0 approved final business KPIs**

Consequently, descriptive analysis was used to expose the structure and observed characteristics of the available evidence rather than to manufacture performance indicators.

## 7.3 Descriptive Evidence Categories

The completed dashboard semantic contract contains **21 approved descriptive records**.

These records span the eight business pages and represent evidence such as:

- order counts;
- units sold;
- product views;
- cancelled-order counts;
- transaction and payment statuses;
- order-item quantities;
- product status;
- wallet transaction types;
- wallet transaction methods;
- wallet transaction statuses;
- shipment-item quantities;
- inventory quantities;
- return-request statuses;
- hub-return quantities; and
- vendor product-view evidence.

These records were selected from the validated analytical layer rather than being invented during dashboard implementation.

## 7.4 Executive-Level Descriptive Evidence

The Executive Overview page presents approved descriptive evidence from:

- `daily_category_metrics.order_count`;
- `daily_category_metrics.units_sold`;
- `daily_platform_metrics.total_orders`;
- `daily_platform_metrics.total_product_views`;
- `daily_vendor_metrics.orders`;
- `daily_vendor_metrics.units_sold`; and
- `daily_vendor_metrics.cancelled_orders`.

These fields support descriptive examination of observed counts and quantities at their respective source-native grains.

They are not presented as certified revenue, profitability, conversion, retention, or other business-performance KPIs.

## 7.5 Commercial and Order Evidence

The Commercial / Sales page exposes approved status and quantity evidence from:

- `payment_transactions.status`;
- `payments.status`; and
- `invoices.quantity`.

The Orders page exposes:

- `order_items.quantity`.

These fields allow the application to communicate observed transaction, payment, invoice, and order-item characteristics without requiring unsupported cross-dataset integration.

## 7.6 Product, Customer, Fulfillment, Returns, and Operations Evidence

The remaining business pages expose approved descriptive fields within their documented analytical boundaries.

Product / Catalog uses:

- `product.status`.

Customers / Accounts uses:

- `wallet_transactions.type`;
- `wallet_transactions.method`; and
- `wallet_transactions.status`.

Fulfillment / Shipping uses:

- `shipment_items.quantity`;
- `hub_inventory.quantity`.

Returns / Exchange uses:

- `return_request.status`;
- `hub_returns.quantity`.

Operations / Inventory uses:

- `hub_inventory.quantity`;
- `daily_vendor_metrics.product_views`.

These fields were presented according to their documented source-native meaning and grain.

The project does not infer unsupported customer-level, profitability, conversion, retention, or inventory-optimization conclusions from these fields.

## 7.7 Visualization and Exact-Value Presentation

The dashboard combines descriptive visual presentation with supporting exact-value tables.

This design provides two complementary purposes:

1. visual exploration of approved descriptive evidence; and
2. direct inspection of the underlying values.

The visualization layer therefore supports interpretation without becoming a hidden analytical transformation layer.

Where a field represents a quantity or count, the dashboard communicates it descriptively rather than labeling it as a certified KPI.

## 7.8 Cross-Dataset Analytical Boundary

Exploratory analysis did not bypass the relationship and analytical-dataset controls.

The completed project contains:

**0 approved cross-dataset joins**

Therefore, dashboard analysis does not combine unrelated source-native datasets merely to produce more elaborate charts.

This constraint improves traceability because each approved descriptive record can be connected to a validated analytical source rather than to an undocumented dashboard-side calculation.

## 7.9 Interpretation Boundary

Descriptive evidence was intentionally separated from business interpretation.

For example, an observed count, quantity, status distribution, or product-view value may be displayed as evidence. It does not automatically establish why the value occurred, whether it represents business success or failure, or what financial impact it produced.

Such conclusions would require additional evidence that was not approved within the completed analytical contract.

The final system therefore favors traceable observation over unsupported causal or business-impact claims.

## 7.10 Exploratory Analytics Outcome

The exploratory and descriptive analytics stage produced a controlled evidence presentation layer rather than an unrestricted analytics engine.

The completed boundary is:

- **21 approved dashboard semantic records**
- **8 business dashboard pages**
- **0 approved final business KPIs**
- **0 approved cross-dataset joins**
- **0 ML outputs**

This provides a reproducible descriptive view of the validated PurjeStore analytical evidence while preserving the project's methodological limitations.

---

# 8. Machine-Learning Feasibility Assessment

## 8.1 Purpose of the ML Assessment

Machine learning was evaluated as a possible analytical capability, but it was not treated as a mandatory implementation requirement.

The objective of the ML stage was to determine whether the available PurjeStore evidence supported a defensible machine-learning problem.

A model was considered appropriate only if the available data could support a sufficiently defined target, grain, feature set, sample, and validation strategy.

## 8.2 Initial Candidate Landscape

The ML assessment began from the completed analytical layer containing:

- **26 analytical datasets**
- **12,148 rows**
- **289 columns**

The broader candidate assessment identified **172 preliminary target candidates**.

These candidates were treated as possibilities for investigation, not as confirmed ML targets.

The presence of a numerical or categorical field was not considered sufficient evidence that it should become a prediction target.

## 8.3 Deep Candidate Assessment

A deeper assessment expanded the candidate landscape to **217 ML-related candidates**.

These candidates were evaluated against the evidence required to formulate defensible machine-learning problems.

The assessment considered issues including:

- target availability;
- target definition;
- analytical grain;
- feature availability;
- population and sample characteristics;
- temporal or observational structure where relevant;
- leakage or methodological concerns;
- evidence sufficiency; and
- whether the proposed problem was actually an ML problem.

## 8.4 Problem Formulation Review

The problem-formulation stage reviewed **83 candidate problem formulations**.

The purpose was to move beyond field-level candidate detection and determine whether a candidate could be expressed as a valid analytical problem.

The assessment identified:

- **52 candidates requiring additional evidence**
- **27 candidates rejected as ML problems**
- **4 candidates deferred**
- **0 final ML problem selections**

This outcome demonstrates that candidate discovery and ML problem selection were treated as separate decisions.

## 8.5 Evidence Requirements for ML

The project required stronger evidence before allowing an ML problem into implementation.

A defensible ML problem would require, as applicable:

- a clearly defined target;
- a defensible prediction grain;
- sufficient observations;
- appropriate feature evidence;
- valid training and evaluation boundaries;
- no unacceptable leakage;
- a meaningful analytical objective; and
- evidence that the resulting output could be interpreted responsibly.

Where these requirements were not established, the candidate was not promoted to implementation.

## 8.6 Final ML Decision

The final ML feasibility assessment selected:

**0 ML problems**

The authoritative project status is therefore:

**ML = BLOCKED**

This is an evidence-based project outcome.

It means that the completed release does not contain unsupported predictive models simply for the purpose of claiming that machine learning was implemented.

## 8.7 Predictive Outputs Not Implemented

Because no ML problem passed the final selection gate, the project does not present:

- predictive models;
- model training pipelines;
- inference outputs;
- forecasting;
- recommendation models;
- churn prediction;
- fraud prediction;
- predictive customer scoring; or
- model-explanation outputs such as SHAP results.

These capabilities remain outside the completed analytical release.

## 8.8 Relationship Between ML and the Analytical Layer

The ML decision is connected to the same evidence-bounded methodology used elsewhere in the project.

The analytical layer provides validated source-native evidence, but its existence does not automatically imply that the data supports predictive modeling.

The project therefore treats:

**available analytical data ≠ automatically suitable ML problem**

This distinction prevents the system from introducing a model whose target, grain, validation design, or business interpretation cannot be defended.

## 8.9 Future Reopening Condition

The ML boundary is not a claim that machine learning can never be used with PurjeStore.

It means that the completed release does not have sufficient approved evidence to justify an ML implementation.

ML may be reconsidered in a future project phase only if new or improved evidence establishes a defensible problem formulation and satisfies the project's analytical and validation requirements.

Any future reopening should therefore be evidence-driven rather than technology-driven.

## 8.10 ML Feasibility Outcome

The completed ML stage establishes the following final boundary:

- **172 preliminary target candidates**
- **217 deep ML candidates**
- **83 problem formulations reviewed**
- **52 requiring additional evidence**
- **27 rejected as ML problems**
- **4 deferred**
- **0 selected ML problems**
- **ML status: BLOCKED**

The absence of an ML model is therefore a documented analytical decision based on feasibility evidence rather than an unfinished implementation.

---


# 9. Dashboard and Decision-Support Application

## 9.1 Purpose and Application Role

The final PurjeStore application provides an evidence-bounded analytical and descriptive decision-support interface over the validated analytical layer. The dashboard was designed as a client-presentable application while preserving the analytical boundaries established during data discovery, relationship validation, cleaning, analytical dataset construction, and machine-learning feasibility assessment.

The selected dashboard technology is Streamlit with Plotly for interactive descriptive visualization. The application does not introduce a separate analytical methodology, new business definitions, unsupported KPIs, cross-dataset joins, or predictive outputs.

The dashboard therefore represents the validated analytical evidence rather than attempting to manufacture additional business intelligence from unsupported relationships or meanings.

## 9.2 Dashboard Architecture

The application intentionally separates the Streamlit entry point from the internal dashboard application shell.

The root `app.py` is the top-level Streamlit entry point. It owns the authoritative `APPROVED_MAPPING`, configures the dashboard semantic adapter, imports the page renderers, and starts the application shell.

The internal `dashboard/app.py` provides the dashboard application shell and page-selection/navigation behavior. It is not a second top-level Streamlit launcher.

Supporting dashboard responsibilities are separated across configuration, data access, semantic adaptation, utility/rendering logic, shared components, business-page renderers, and technical-page renderers.

This separation improves maintainability without introducing an unnecessary generic application framework or changing the underlying analytical methodology.

## 9.3 Business and Technical Information Architecture

The final dashboard contains eight business-facing analytical pages:

1. Executive Overview
2. Commercial / Sales
3. Orders
4. Products / Catalog
5. Customers / Accounts
6. Fulfillment / Shipping
7. Returns / Exchange
8. Operations / Inventory

Two technical pages are also provided:

9. Data & System Health
10. Technical Dataset Explorer

The business pages communicate descriptive evidence from approved analytical records. The technical pages expose system, validation, schema, and dataset information without turning technical fields into unsupported business interpretations.

## 9.4 Approved Dashboard Semantic Evidence

The final dashboard preserves exactly 21 approved semantic records.

The Executive Overview contains seven approved descriptive records:

- `daily_category_metrics.order_count`
- `daily_category_metrics.units_sold`
- `daily_platform_metrics.total_orders`
- `daily_platform_metrics.total_product_views`
- `daily_vendor_metrics.orders`
- `daily_vendor_metrics.units_sold`
- `daily_vendor_metrics.cancelled_orders`

The Commercial / Sales page contains:

- `payment_transactions.status`
- `payments.status`
- `invoices.quantity`

The Orders page contains:

- `order_items.quantity`

The Products / Catalog page contains:

- `product.status`

The Customers / Accounts page contains:

- `wallet_transactions.type`
- `wallet_transactions.method`
- `wallet_transactions.status`

The Fulfillment / Shipping page contains:

- `shipment_items.quantity`
- `hub_inventory.quantity`

The Returns / Exchange page contains:

- `return_request.status`
- `hub_returns.quantity`

The Operations / Inventory page contains:

- `hub_inventory.quantity`
- `daily_vendor_metrics.product_views`

These records remain descriptive evidence. They are not converted into unsupported financial, customer-value, conversion, retention, profitability, or operational-impact KPIs.

## 9.5 Dashboard Presentation Hierarchy

The business-page UX follows a consistent evidence-first hierarchy:

1. Page title
2. Purpose and short description
3. Evidence boundary
4. Observed evidence section
5. Primary visualization or descriptive summary
6. Supporting exact-value table

This structure separates what the data directly shows from any interpretation that a user may make from the evidence.

Quantity observations are presented as descriptive quantities rather than certified business KPIs. Status and categorical fields are presented as observed distributions or exact-value evidence rather than unsupported performance measures.

## 9.6 Analytical and Predictive Boundaries

The dashboard does not perform cross-dataset joins.

It does not write to the analytical datasets or source data during normal business-page operation.

It does not activate unsupported KPIs.

It does not provide machine-learning predictions, forecasts, recommendations, churn models, fraud models, customer scoring, SHAP analysis, or other predictive outputs.

The machine-learning feasibility assessment established that no defensible ML problem was selected. Consequently, predictive functionality remains blocked unless future evidence establishes a defensible target, grain, feature set, validation strategy, and business meaning.

The dashboard therefore remains aligned with the project's evidence-bounded methodology.

## 9.7 Technical Dataset Explorer

The Technical Dataset Explorer provides controlled technical inspection of the analytical layer.

It provides:

- dataset selection,
- technical dataset summary,
- read-only preview limited to the first 100 rows,
- technical field profile,
- missingness information,
- datatype information,
- cardinality information,
- semantic interpretation boundaries.

The Explorer is intentionally not a business KPI or analytical modeling interface. It does not perform joins, modify analytical data, or create predictive outputs.

## 9.8 Data and System Health

The Data & System Health page communicates the operational state of the controlled analytical refresh and validation process.

The page separates technical system health from business interpretation and communicates refresh timestamps, dataset validation state, and controlled failure information.

The page does not introduce business metrics or contaminate the Operations / Inventory page with technical refresh information.

## 9.9 UX Validation and Behavioral Equivalence

The dashboard redesign was validated against the pre-redesign application baseline.

The validation confirmed preservation of:

- all 21 approved semantic records,
- all eight business pages,
- Data & System Health,
- Technical Dataset Explorer,
- the approved analytical baseline of 26 datasets, 12,148 rows, and 289 columns,
- zero approved joins,
- zero business-page analytical writes,
- zero ML operations.

Automated dashboard and project tests were also retained and expanded during UX work. The final release test suite contained 62 passing tests.

Visual and runtime validation was completed for all ten dashboard experiences: eight business pages, Data & System Health, and Technical Dataset Explorer.

The redesigned application therefore changes presentation and usability while preserving the approved analytical behavior and evidence boundary.

## 9.10 Final Dashboard Outcome

The final dashboard is a client-presentable Streamlit + Plotly application over the validated analytical layer.

It provides a consistent interface for descriptive evidence, technical inspection, and controlled system-health communication while avoiding unsupported analytical claims.

The dashboard is therefore positioned as the presentation and decision-support layer of the PurjeStore system rather than as an independent source of new analytical truth.

# 10. Controlled Refresh and System Architecture

## 10.1 Purpose of Controlled Refresh

The controlled refresh architecture provides a reproducible mechanism for rebuilding the validated analytical layer from cleaned source data without changing the project's analytical contracts.

The refresh process is deliberately constrained. It does not attempt to discover new relationships, construct arbitrary joins, deduplicate data without an approved rule, invent KPIs, or reopen the machine-learning decision.

Its purpose is controlled reproducibility of the already-approved analytical datasets.

## 10.2 Controlled Refresh Flow

The implemented controlled refresh architecture follows this sequence:

Cleaned Source
→ Controlled Source Discovery
→ Contract Registry
→ Source Schema / Field Validation
→ Grain Validation
→ Source-Only Projection
→ Row / Schema / Duplicate / Null Validation
→ Atomic Controlled Publication
→ Validated Analytical Layer
→ Dashboard

Each stage has a defined responsibility and is validated before the analytical output is published.

## 10.3 Refresh Implementation

The controlled refresh implementation is contained in:

`pipelines/refresh/refresh_analytical_datasets.py`

The implementation contains 26 static dataset contract specifications corresponding to the 26 approved analytical datasets.

The analytical projection is derived from the current validated analytical dataset schemas. The refresh process validates the source against the required contract and then produces the controlled analytical projection.

The source-validation logic permits additional source fields where appropriate while enforcing the required contract fields and output structure.

## 10.4 Dataset Contract Validation

Each analytical dataset contract establishes the expected analytical output structure and validation behavior.

The refresh process validates:

- required source fields,
- expected analytical output fields,
- exact output column order,
- physical grain,
- row count,
- duplicate behavior,
- source-to-projection values,
- schema consistency,
- missing/null behavior where required,
- known semantic exceptions.

The process does not silently alter approved analytical meaning to make validation pass.

Known grain exceptions remain governed by their established contracts. In particular, the intentional duplicate rows in `daily_vendor_metrics` remain preserved rather than being removed through generic deduplication.

## 10.5 Controlled Projection Boundary

The refresh process performs source-only analytical projection.

It does not perform:

- cross-dataset joins,
- arbitrary aggregation,
- generic deduplication,
- unsupported transformations,
- KPI activation,
- machine-learning processing,
- predictive inference.

This keeps the refresh process consistent with the project's approved analytical dataset construction methodology.

## 10.6 Safe Publication

The refresh process stages the generated analytical outputs before publication.

The staged outputs are read back and validated before being published to the analytical layer.

Publication uses controlled replacement behavior with backup and restore protection so that an unsuccessful publication does not silently leave an invalid analytical layer in place.

This provides a controlled boundary between transformation and published analytical data.

## 10.7 Refresh Modes

The refresh implementation provides a read-only contract-validation mode:

`--validate-contracts`

This mode validates the registered contracts without performing an analytical refresh.

The implementation also provides the controlled refresh mode:

`--refresh`

The refresh operation writes the resulting refresh report to:

`outputs/refresh/latest_refresh_report.json`

The refresh report provides an execution record for the controlled refresh process.

## 10.8 Refresh Validation Result

The completed refresh validation established that all 26 approved analytical dataset contracts can be validated and refreshed successfully under the controlled architecture.

The refresh process therefore provides reproducibility for the existing analytical layer without expanding the analytical scope.

The final analytical baseline remains:

- 26 analytical datasets,
- 12,148 rows in total,
- 289 columns in total.

## 10.9 Final End-to-End Architecture

The implemented development and analytical architecture is:

Development Sources
→ Discovery / Validation
→ Physical Cleaning
→ Validated Analytical Construction
→ 26 Analytical Datasets
→ Evidence-Bounded Analytics
→ Streamlit + Plotly Dashboard

The controlled refresh path provides the repeatable route from cleaned sources back into the validated analytical layer:

Cleaned Source
→ Controlled Refresh
→ Validation
→ Analytical Layer
→ Dashboard

This architecture keeps source data, analytical construction, analytics, dashboard presentation, and refresh responsibilities conceptually separated.

## 10.10 Architecture Principles

The final system follows these principles:

1. Raw and original source evidence remains protected.
2. Cleaning is evidence-based and does not manufacture meaning.
3. Analytical datasets are governed by explicit contracts.
4. Grain and duplicate behavior are validated rather than assumed.
5. Cross-dataset joins remain disabled because no approved analytical join contract exists.
6. Unsupported KPIs are not activated.
7. Machine learning remains blocked because no defensible ML problem was selected.
8. Dashboard presentation does not modify analytical methodology.
9. Controlled refresh validates outputs before publication.
10. Technical system information remains separate from business-facing descriptive evidence.
11. Reproducibility is preferred over uncontrolled transformation.
12. Future capabilities are conditional on new evidence rather than assumed.

## 10.11 Technology Scope

The implemented system uses the established PurjeStore technology environment, including:

- Python 3.11.x
- pandas
- Streamlit
- Plotly
- pytest
- MariaDB for the recovered source environment
- Git for version control

The final architecture does not require React, Node.js, Kubernetes, or another separate web application framework.

These technologies were not introduced merely to increase architectural complexity because the implemented Streamlit-based application and controlled Python refresh process satisfy the validated project requirements.

## 10.12 Reproducibility and Delivery Boundary

The controlled refresh architecture, analytical contracts, dashboard architecture, automated tests, documentation, dependency declarations, and Git history together provide the reproducibility boundary for the completed PurjeStore system.

The final project therefore has a traceable progression from recovered source evidence through validated analytical datasets and descriptive analytics to the client-facing dashboard.

The system remains intentionally evidence-bounded. Any future analytical expansion must first establish supporting source evidence, grain, relationships, semantic meaning, validation rules, and an approved analytical contract before being incorporated into the production workflow.


# 11. Testing, Validation, and Quality Assurance

## 11.1 Testing Strategy

Testing was treated as a continuous quality-control activity rather than a final-stage activity performed only after implementation.

Validation was applied at multiple boundaries of the PurjeStore system, including source and analytical data, dataset contracts, controlled refresh, dashboard behavior, user-interface behavior, and final release state.

The testing strategy was designed to protect the evidence-bounded analytical methodology while allowing the dashboard and supporting software architecture to evolve.

## 11.2 Analytical and Data Validation

The analytical layer was validated against its approved dataset contracts.

The final analytical baseline contains:

- 26 analytical datasets,
- 12,148 rows,
- 289 columns.

Validation covered dataset availability, expected schemas, physical grain, row behavior, duplicate behavior, source-to-output consistency, and established semantic exceptions.

The validation process also preserved known exceptions rather than treating every duplicate or unusual record as an error. In particular, the six intentional duplicate rows in `daily_vendor_metrics` were preserved according to the approved grain behavior.

The project therefore distinguishes between an actual validation failure and a documented data characteristic that must remain preserved.

## 11.3 Controlled Refresh Testing

The controlled refresh implementation was tested against all 26 analytical dataset contracts.

The contract-validation mode provides a read-only mechanism for verifying the registered analytical contracts.

The refresh mode validates staged analytical outputs before controlled publication.

Testing verifies the expected source fields, output fields, column order, grain, row behavior, duplicate behavior, source-projection values, and relevant null or semantic conditions.

The controlled refresh design also includes backup and restore protection around publication so that an unsuccessful publication does not silently replace the validated analytical layer with an invalid output.

## 11.4 Automated Test Suite

Automated testing was implemented using pytest.

The test coverage includes both pipeline behavior and dashboard behavior.

The dashboard UX regression suite specifically verifies the approved semantic records, page contracts, analytical baseline, unsupported-operation boundaries, technical-page boundaries, and the machine-learning boundary.

The final project test suite contains 62 passing tests.

The test count is not treated as a permanent requirement. The important requirement is preservation and expansion of the behavioral assertions as the system evolves.

## 11.5 Dashboard Regression Testing

Dashboard regression testing verifies that presentation changes do not alter the approved analytical contract.

The final validation confirmed:

- all 21 approved semantic records remain available,
- all eight business pages remain available,
- Data & System Health remains available,
- Technical Dataset Explorer remains available,
- no unsupported analytical field was introduced,
- no approved field disappeared,
- no cross-dataset join was introduced,
- no business-page analytical write was introduced,
- no machine-learning operation was introduced.

This testing boundary allows UX improvements without silently changing the analytical methodology.

## 11.6 Old/New Behavioral Equivalence

The final dashboard was compared with the pre-redesign baseline.

The equivalence assessment confirmed preservation of the approved semantic and structural behavior while allowing the interface to be redesigned for improved readability and usability.

The comparison covered:

- 21 approved semantic records,
- eight business pages,
- Data & System Health,
- Technical Dataset Explorer,
- the 26-dataset analytical baseline,
- 12,148 analytical rows,
- 289 analytical columns,
- zero approved joins,
- zero business-page analytical writes,
- zero ML operations.

No approved analytical field disappeared during the redesign, and no unsupported analytical field appeared as a result of the UX work.

## 11.7 Runtime Validation

Runtime validation was performed across all ten dashboard experiences:

1. Executive Overview
2. Commercial / Sales
3. Orders
4. Products / Catalog
5. Customers / Accounts
6. Fulfillment / Shipping
7. Returns / Exchange
8. Operations / Inventory
9. Data & System Health
10. Technical Dataset Explorer

The rendered interfaces were inspected for successful loading, controlled states, page separation, evidence presentation, and absence of the known technical/runtime defects.

The validation confirmed that the final dashboard operates within the approved architecture.

## 11.8 Visual Quality Assurance

Visual QA was performed after the dashboard UX redesign.

The review covered all eight business pages and both technical pages.

The visual review focused on:

- page hierarchy,
- readability,
- evidence-boundary communication,
- business/technical separation,
- descriptive visualization presentation,
- exact-value tables,
- controlled empty and error states,
- navigation consistency,
- removal of misleading analytical implications.

The visual review did not use visual polish as a reason to introduce unsupported business metrics or analytical claims.

## 11.9 Machine-Learning Boundary Validation

Testing also protects the explicit machine-learning decision.

The feasibility assessment resulted in zero selected ML problems.

Therefore the final application and test suite verify the continued absence of:

- predictive models,
- model training,
- inference,
- forecasting,
- recommendation engines,
- churn modeling,
- fraud modeling,
- predictive scoring,
- SHAP or model-explanation outputs.

This is an intentional quality boundary rather than an incomplete implementation.

Future ML work can only be reopened when new evidence establishes a defensible target, grain, features, validation strategy, and analytical contract.

## 11.10 Technical Page Validation

The technical pages were tested separately from business-facing pages.

Data & System Health is responsible for communicating controlled refresh and system validation information.

Technical Dataset Explorer is responsible for read-only technical inspection of analytical datasets.

Neither technical page is permitted to manufacture business KPIs or reinterpret technical fields as unsupported business measures.

This separation was included in automated regression coverage and runtime validation.

## 11.11 Release Validation

Before final release, the project underwent a consolidated release validation.

The release checks covered:

- required project artifacts,
- dashboard UX specification anchors,
- approved semantic contract,
- business-page contracts,
- analytical baseline,
- approved join boundary,
- analytical-write boundary,
- machine-learning boundary,
- compilation,
- automated tests,
- Git diff validation,
- remote synchronization,
- clean working tree.

The final release validation completed successfully.

The project reached a state in which the local Git `HEAD` matched the remote `origin/master` and the working tree was clean.

## 11.12 Dependency and Reproducibility Validation

Runtime dependencies were explicitly documented in `requirements.txt`.

The documented runtime environment includes:

- Python 3.11.x,
- Streamlit 1.64.0,
- pandas 3.0.5,
- Plotly 7.1.0.

The installed environment was validated against the declared runtime dependencies.

Compilation and automated tests were also executed successfully, providing additional evidence that the delivered source tree is internally consistent.

## 11.13 Documentation and Evidence Validation

Formal project documentation was maintained alongside implementation.

The testing and release process verified that the relevant architecture, analytical, UX, testing, and delivery artifacts were present and consistent with the implemented system.

The final report is also being constructed from the completed project evidence rather than from assumed project capabilities.

This ensures that the final academic and client-facing documentation does not claim functionality that was not implemented or supported by evidence.

## 11.14 Final Quality Status

The completed testing and validation process establishes the following final quality position:

- analytical datasets: validated,
- controlled refresh: validated,
- dashboard application: validated,
- 21 approved semantic records: preserved,
- eight business pages: preserved,
- technical pages: validated,
- automated tests: 62 passing,
- old/new behavioral equivalence: passed,
- visual QA: passed,
- unsupported joins: absent,
- unsupported analytical writes: absent,
- ML operations: absent,
- declared runtime dependencies: documented,
- Git release state: synchronized and clean.

The resulting system is therefore validated as an evidence-bounded, reproducible analytical and dashboard application rather than merely a collection of independently working components.


# 12. Limitations, Risks, and Future Scope

## 12.1 Purpose of the Limitation Analysis

The final PurjeStore system is intentionally evidence-bounded. Its limitations are therefore documented as part of the analytical result rather than treated only as implementation shortcomings.

A limitation is recorded where the available evidence does not support a stronger analytical claim, relationship, KPI, predictive problem, or business interpretation.

This approach prevents unsupported conclusions from being introduced into the final system or report.

## 12.2 Absence of Approved Business KPIs

The analytical validation process identified candidate measures, but no final business KPI was approved.

The project therefore does not present generic e-commerce measures as certified PurjeStore KPIs.

Observed quantities, statuses, and distributions are presented as descriptive evidence. They should not automatically be interpreted as revenue, profitability, conversion, retention, customer value, operational efficiency, or business impact measures.

Any future KPI activation requires evidence for its definition, source fields, grain, calculation logic, validation, and business interpretation.

## 12.3 Absence of Approved Cross-Dataset Joins

No approved cross-dataset analytical join was constructed.

This is a deliberate limitation arising from the relationship, grain, referential, and analytical-contract validation.

Although relationship candidates were investigated, the project did not construct analytical outputs merely because technically plausible relationships existed.

Future cross-dataset analysis would require an approved relationship contract, validated cardinality, compatible grain, sufficient population evidence, and a clearly defined analytical purpose.

## 12.4 Machine-Learning Limitation

The machine-learning feasibility assessment resulted in zero selected ML problems.

The project therefore does not claim predictive modeling capability.

The final system contains no predictive models, training pipelines, inference outputs, forecasting, recommendations, churn prediction, fraud prediction, predictive scoring, or SHAP analysis.

This limitation is evidence-driven. It prevents the project from presenting a technically complex model whose target, features, grain, validation strategy, or business interpretation cannot be defended from the available evidence.

## 12.5 Data and Semantic Limitations

Several source-level limitations remain documented.

These include:

- evidence gaps involving `notification_logs` and orders,
- warnings associated with revenue-related fields,
- ambiguity associated with `ackNo`,
- temporary semantic variants requiring controlled interpretation,
- relationship paths with incomplete or absent referential matches,
- documented duplicate behavior in `daily_vendor_metrics`.

These conditions are not silently corrected through unsupported assumptions.

Where evidence is insufficient, the project preserves the limitation and prevents it from becoming an unsupported analytical claim.

## 12.6 Grain and Duplicate Limitations

The analytical layer contains documented grain exceptions.

The established exceptions include:

- `daily_category_metrics`,
- `daily_platform_metrics`,
- `daily_vendor_metrics`.

`daily_vendor_metrics` contains six duplicate rows under its validated dataset behavior.

These rows are intentionally preserved. Generic deduplication would potentially alter the meaning or row behavior of the approved analytical dataset.

Consequently, users of the analytical layer must interpret quantities according to their documented dataset grain rather than assuming that every row represents a unique business event.

## 12.7 Referential and Relationship Limitations

Relationship validation identified different levels of referential evidence.

The expanded relationship-path assessment contained:

- 43 full referential matches,
- 1 partial match,
- 33 paths with no match,
- 1 dynamic relationship.

The project therefore does not treat every discovered or suggested relationship as a valid analytical integration.

The historical invoice discrepancy was also preserved rather than artificially reconciled: an earlier assessment recorded nine invoice-related relationship findings, direct concrete recomputation produced eight participating records, and broader text search identified ten invoice-related references because of additional textual matches such as e-invoice and e-way-bill terminology.

This demonstrates why relationship evidence must remain traceable to its exact definition and search boundary.

## 12.8 Refresh Limitations

The controlled refresh architecture is intentionally limited to the approved analytical contracts.

It does not automatically discover new analytical datasets, create new joins, activate new KPIs, or infer new semantic meanings.

The refresh process is therefore reproducible for the approved analytical layer but is not intended to be an unrestricted data-engineering framework.

Any change to analytical scope requires a separate evidence and contract decision before it can become part of the controlled refresh path.

## 12.9 Dashboard Limitations

The dashboard is a descriptive decision-support application rather than a general-purpose business intelligence platform.

Its current limitations include:

- no certified business KPI layer,
- no cross-dataset analytical joins,
- no predictive pages,
- no unsupported customer-level inference,
- no revenue/profit/ROI certification,
- no automated recommendations,
- no analytical writes from business pages.

The dashboard should therefore be interpreted according to the evidence shown on each page and the documented semantic boundary.

## 12.10 Client and Academic Interpretation Boundary

The system is suitable for presenting validated descriptive evidence and the implemented analytical workflow.

However, dashboard observations should not be presented as causal conclusions unless an appropriate causal methodology and supporting evidence are separately established.

Similarly, descriptive quantities should not automatically be described as business performance improvements, cost savings, profitability, ROI, customer retention, or operational optimization.

The report and presentation should maintain the distinction between:

- observed evidence,
- derived descriptive result,
- interpretation,
- decision,
- assumption,
- limitation,
- deferred capability.

This distinction is central to the academic defensibility of the project.

## 12.11 Future Analytical Expansion

Future analytical capabilities may be considered if new evidence becomes available.

Potential future work is conditional rather than currently implemented.

Examples include additional KPI development, cross-dataset analytical integration, predictive modeling, forecasting, recommendation systems, customer analytics, or other advanced decision-support capabilities.

Such work should only be introduced after the relevant evidence establishes:

1. a defensible analytical question,
2. appropriate source data,
3. stable semantic meaning,
4. valid grain,
5. validated relationships where required,
6. sufficient population and quality,
7. appropriate validation methodology,
8. an approved analytical or model contract.

This prevents future expansion from weakening the evidence boundary of the existing system.

## 12.12 Future Machine-Learning Reopening Conditions

The ML decision may be revisited if future evidence supports a defensible ML problem.

A future ML reopening should establish:

- a clearly defined target,
- target availability and population,
- appropriate observation grain,
- valid feature availability before the prediction point,
- sufficient observations,
- acceptable missingness and quality,
- leakage controls,
- an appropriate train/validation/test strategy,
- suitable evaluation metrics,
- meaningful business interpretation,
- an approved model contract.

Until these conditions are established, ML remains blocked.

## 12.13 Future Data and Refresh Expansion

The controlled refresh architecture can provide a foundation for future expansion, but new sources or analytical datasets should not be added merely because they are technically accessible.

A future refresh expansion should first validate:

- source availability,
- schema compatibility,
- field meaning,
- grain,
- duplicate behavior,
- null behavior,
- semantic exceptions,
- analytical purpose,
- publication requirements.

Only after these conditions are approved should a new dataset become part of the controlled analytical layer.

## 12.14 Future Productization

Future productization may include additional operational capabilities if justified by actual project requirements.

Examples may include stronger deployment packaging, environment automation, monitoring, broader user-access controls, scheduled execution, or additional reporting interfaces.

These are future possibilities rather than claims about the current implementation.

The current project intentionally prioritizes a reproducible and evidence-bounded architecture over adding infrastructure that does not have a demonstrated requirement.

## 12.15 Risk Management Principles

The principal project risks are managed through explicit boundaries.

### Risk: Unsupported analytical claims

Mitigation: approved semantic records, evidence-bounded dashboard pages, and explicit KPI boundaries.

### Risk: Incorrect joins or grain inflation

Mitigation: relationship validation, grain contracts, referential evidence, and zero approved cross-dataset joins.

### Risk: Silent data alteration

Mitigation: protected source evidence, controlled cleaning, contract validation, and controlled publication.

### Risk: Uncontrolled duplicate removal

Mitigation: dataset-specific duplicate behavior and preservation of documented grain exceptions.

### Risk: Unsupported predictive modeling

Mitigation: formal ML feasibility gate with zero selected problems and blocked predictive functionality.

### Risk: Dashboard changes altering analytical behavior

Mitigation: automated UX regression testing, old/new behavioral equivalence, runtime validation, and visual QA.

### Risk: Refresh producing invalid analytical outputs

Mitigation: staged output validation, readback validation, and controlled publication with backup/restore protection.

## 12.16 Final Limitation Statement

The limitations documented in this section are part of the final project's evidence record.

They define where the available data and validation do not justify stronger claims.

The project therefore prioritizes correctness, traceability, reproducibility, and academic defensibility over artificially expanding functionality.

The resulting system is complete within its approved scope while remaining open to future expansion when additional evidence supports that expansion.


# 13. Conclusion

## 13.1 Overall Project Outcome

PurjeStore was developed as an end-to-end, evidence-bounded data science and intelligent e-commerce analytics and decision-support system.

The completed project establishes a traceable progression from recovered source evidence through discovery, validation, physical cleaning, analytical dataset construction, descriptive analytics, controlled refresh, testing, and a client-facing Streamlit + Plotly dashboard.

The final system is designed around the principle that analytical complexity should only be introduced when the available evidence supports it.

## 13.2 Data Foundation

The project established a validated data foundation covering:

- 177 base/source tables,
- 178 database objects including `v_shipment_qc_summary`,
- 177 imported SQL source objects,
- 177 working CSV source representations,
- 177 cleaned CSV representations.

The source and cleaning stages preserved the original evidence and avoided unsupported assumptions about relationships, meaning, missing values, or duplicates.

## 13.3 Analytical Layer

The final analytical layer contains:

- 26 analytical datasets,
- 12,148 rows,
- 289 columns.

The analytical datasets are governed by explicit contracts covering source fields, output schema, column order, grain, row behavior, duplicate behavior, and documented semantic exceptions.

No approved cross-dataset analytical joins were constructed.

This preserves analytical traceability and prevents unsupported relationships from becoming part of the final decision-support layer.

## 13.4 Evidence-Bounded Analytics

The project evaluated available analytical evidence before deciding which business-facing information could be presented.

The final dashboard semantic contract contains 21 approved descriptive records across eight business pages.

These records provide observed quantities, statuses, and categorical evidence.

No unsupported business KPI was introduced.

The project therefore avoids presenting descriptive quantities as automatically representing revenue, profitability, ROI, customer value, conversion, retention, or other business outcomes that are not established by the underlying evidence.

## 13.5 Machine-Learning Decision

Machine learning was formally assessed rather than assumed to be mandatory for a data science project.

The feasibility assessment resulted in zero selected ML problems.

Consequently, the final system does not contain predictive models, training pipelines, inference, forecasting, recommendations, churn prediction, fraud prediction, predictive scoring, or SHAP analysis.

This outcome is an evidence-based project decision. It demonstrates that the project evaluates whether a predictive problem is defensible before implementing predictive technology.

## 13.6 Dashboard and Decision Support

The completed dashboard provides:

- eight business-facing analytical pages,
- Data & System Health,
- Technical Dataset Explorer.

The application uses Streamlit and Plotly and presents approved descriptive evidence through a consistent user-interface hierarchy.

The dashboard redesign was validated against the pre-redesign behavior and preserved all 21 approved semantic records.

The final application therefore provides a client-presentable interface without changing the underlying analytical methodology or introducing unsupported analytical claims.

## 13.7 Controlled Refresh and Reproducibility

The controlled refresh architecture provides a reproducible route from cleaned source data to the validated analytical layer.

The refresh process uses 26 analytical dataset contracts and validates source fields, output schema, grain, row behavior, duplicate behavior, and source-to-projection consistency before controlled publication.

The process intentionally does not perform arbitrary joins, unsupported aggregation, generic deduplication, KPI activation, or machine-learning processing.

This establishes a controlled boundary between source data, analytical outputs, and dashboard presentation.

## 13.8 Testing and Quality Assurance

The completed project includes automated testing, analytical validation, dashboard regression testing, old/new behavioral equivalence, runtime validation, visual QA, and release validation.

The final automated suite contains 62 passing tests.

The final validation confirmed preservation of:

- 21 approved semantic records,
- eight business pages,
- technical pages,
- 26 analytical datasets,
- 12,148 analytical rows,
- 289 analytical columns,
- zero approved joins,
- zero business-page analytical writes,
- zero ML operations.

The final release was synchronized with the remote Git repository and the working tree was clean.

## 13.9 Academic and Client Value

From an academic perspective, the project demonstrates a complete workflow in which data discovery, validation, cleaning, analytical construction, descriptive analysis, feasibility assessment, software architecture, testing, and documentation are connected through evidence and explicit decision gates.

From a client perspective, the project provides a usable analytical dashboard and a controlled analytical refresh process while clearly communicating the boundaries of what the available data can support.

The project therefore prioritizes defensible results over artificially maximizing the number of models, KPIs, dashboards, or technologies.

## 13.10 Final Statement

The completed PurjeStore system provides a reproducible and evidence-bounded foundation for e-commerce analytics and decision support.

Its final architecture connects recovered source evidence, validated analytical datasets, descriptive analytics, controlled refresh, software testing, and a client-facing dashboard into one traceable project.

The most important outcome is not the number of technologies or analytical features implemented, but the establishment of a system in which each implemented capability can be traced to validated evidence and each unsupported capability is explicitly bounded.

The project is complete within its approved scope and provides a structured foundation for future expansion if additional evidence establishes new analytical, predictive, or business requirements.
