Great. Since you confirmed the file has been created, we can now populate the **Phase 16-B architecture document**.

Use the following as the complete content of:

`C:\Users\ASUS\Desktop\PurjeStore\docs\architecture\PHASE_16B_CONTROLLED_REFRESH_ARCHITECTURE.md`

````markdown
# Phase 16-B — Controlled Refresh Architecture & Minimal Reusable Construction Design

**Project:** PurjeStore  
**Phase:** 16-B — Automation and Refreshability  
**Status:** In Progress  
**Architecture Basis:** Phase 15 Architecture Reconciliation + validated Milestone 5.3-C construction evidence  
**Primary Analytical Layer:** `data/processed/analytical/`  
**Source Layer:** `data/cleaned/`

---

## 1. Purpose

Phase 16-B defines the controlled refresh architecture required to make the existing PurjeStore analytical layer reproducibly refreshable from the validated cleaned source layer.

The purpose is not to introduce a generic ETL framework or unnecessary orchestration infrastructure.

The purpose is to establish a small, deterministic, contract-driven refresh mechanism that:

1. discovers the authorized cleaned sources;
2. validates source availability and structure;
3. applies the already validated analytical construction contracts;
4. preserves the authorized source grain;
5. performs source-only analytical projection;
6. validates the resulting analytical datasets;
7. protects the previously validated analytical state when refresh validation fails;
8. publishes only validated outputs;
9. records sufficient evidence to make the refresh reproducible and auditable;
10. provides validated outputs for the existing dashboard layer.

---

## 2. Phase 16-B Boundary

Phase 16-B is a design and implementation-readiness phase.

It defines the architecture that Phase 16-C will implement.

### In scope

- controlled cleaned-source access;
- source discovery;
- analytical contract registry usage;
- source schema validation;
- required-column validation;
- source-grain validation;
- source-only projection;
- row-count validation;
- output-schema validation;
- duplicate validation;
- applicable null validation;
- read-back validation;
- controlled staging;
- controlled publication;
- failure visibility;
- preservation of the previous valid analytical state;
- development/live separation;
- refresh evidence and reproducibility;
- dashboard consumption boundary.

### Out of scope

The following are explicitly outside the Phase 16-B implementation boundary:

- new analytical datasets;
- unsupported analytical questions;
- new cross-dataset joins;
- new KPI activation;
- generic ETL frameworks;
- unnecessary orchestration platforms;
- Airflow;
- Dagster;
- Prefect;
- arbitrary aggregation;
- unsupported business-impact calculations;
- ML training;
- ML inference;
- model retraining;
- forecasting;
- recommendation systems;
- churn prediction;
- fraud prediction;
- feature engineering for an unselected ML problem;
- dashboard redesign;
- source mutation;
- replacement of validated analytical data with unvalidated data;
- generic database abstraction without an established live-use requirement.

---

## 3. Authoritative Evidence Basis

The refresh architecture is based on evidence already established during the earlier milestones.

The relevant evidence includes:

- Major Milestone 4 analytical dataset design and relationship validation;
- Major Milestone 5 analytical contract finalization;
- 5.3-C controlled construction specification register;
- 5.3-C construction validation evidence;
- 5.3-C persistence and read-back validation;
- Phase 15 architecture reconciliation;
- Phase 16-A entry and implementation-readiness audit.

The historical construction notebook is treated as evidence of the validated construction process.

It is not treated as the permanent production refresh dependency.

---

## 4. Current Analytical Baseline

The current validated analytical layer contains:

- **26 analytical datasets**
- **12,148 total rows**
- **289 physical columns across the analytical datasets**
- **0 approved cross-dataset joins**
- **0 approved final KPIs**
- **0 selected ML problems**

The 26 analytical CSV outputs currently reside under:

`data/processed/analytical/`

The analytical layer is source-native and does not currently require cross-dataset physical joins for its approved construction.

This baseline must be preserved unless a future milestone produces explicit evidence for a change.

---

## 5. 5.3-C Construction Basis

The recovered 5.3-C construction evidence establishes:

- 26 analytical contracts;
- 26 construction specifications;
- 26 construction validation records;
- 26 persistence-readiness records;
- source-only construction;
- zero physical joins;
- authorized source grain preservation;
- physical CSV persistence;
- physical read-back validation;
- 23 explicit grain-key validations;
- 3 semantic-grain exceptions;
- preservation of the intentionally retained duplicate behavior in `daily_vendor_metrics`.

The construction process therefore provides a validated basis for a controlled refresh implementation.

---

## 6. Construction Model

The refresh mechanism will use a contract-driven source-only projection model.

Conceptually:

```text
Cleaned Source
      |
      v
Authorized Source Discovery
      |
      v
Construction Contract
      |
      v
Required Field Validation
      |
      v
Source-Grain Validation
      |
      v
Source-Only Projection
      |
      v
Analytical Dataset Validation
      |
      v
Controlled Publication
````

The construction mechanism must not infer new transformations merely because additional source fields happen to exist.

Only contract-authorized fields and rules may be used.

---

## 7. Contract Registry

The validated 5.3-C construction specification register is the authoritative basis for refresh construction.

Each analytical dataset contract provides the information necessary to reproduce its approved source-native construction.

The contract concept includes, as applicable:

* analytical dataset name;
* construction mode;
* requested output field count;
* temporal fields;
* dimension fields;
* measure fields;
* source-grain statement;
* construction readiness;
* grain validation requirements;
* semantic limitations.

The refresh implementation must consume this contract information rather than hard-code independent construction rules for each dataset wherever practical.

---

## 8. Source Discovery

The refresh process must explicitly identify the authorized cleaned source layer.

Expected source location:

`data/cleaned/`

Source discovery must:

1. identify the required source file;
2. verify that it exists;
3. verify that it can be read;
4. verify that it corresponds to the expected source dataset;
5. prevent accidental use of unrelated files.

A missing required source is a refresh failure.

A missing source must not result in silent omission of an analytical dataset.

---

## 9. Source Schema Validation

Before construction, the refresh process must validate the source structure required by the analytical contract.

Validation must include, where applicable:

* required columns present;
* unexpected absence of contract-required fields;
* expected column identity;
* compatible data representation;
* readable source data.

A source-schema failure must stop publication of the affected refresh.

The refresh process must not silently substitute another column merely because its name appears similar.

---

## 10. Source-Grain Validation

The authorized source grain must be preserved.

For the 23 datasets with explicit grain keys, the refresh process must validate the applicable grain key.

The established evidence shows:

* grain key populated;
* zero null grain keys;
* zero duplicate grain-key rows;
* unique non-null grain keys.

For the three semantic-grain exceptions:

* `daily_category_metrics`
* `daily_platform_metrics`
* `daily_vendor_metrics`

the existing semantic-grain limitation must remain explicit.

The refresh process must not invent synthetic grain keys merely to make these datasets conform to the 23 explicit-key datasets.

---

## 11. Source-Only Projection

The refresh construction model is source-only.

For each approved analytical dataset:

```text
Source DataFrame
      |
      +--> select authorized fields
      |
      +--> preserve source record structure
      |
      +--> preserve authorized grain
      |
      v
Analytical DataFrame
```

No physical cross-dataset join is currently authorized.

No unsupported aggregation may be introduced.

No deduplication may be introduced merely to make the output appear cleaner.

The existing `daily_vendor_metrics` duplicate behavior must remain governed by the established evidence.

---

## 12. Row-Count Validation

For source-only construction, row-count preservation is an important integrity gate.

For each dataset, the refresh process must compare:

```text
source rows
      =
constructed rows
```

unless an explicitly documented contract exception exists.

The existing 5.3-C evidence established row-count preservation across the 26 constructed datasets.

A new refresh that unexpectedly changes row count must fail the relevant validation gate rather than silently publish the changed output.

---

## 13. Output Schema Validation

Every refreshed analytical dataset must be validated against its approved construction specification.

Validation includes:

* expected dataset identity;
* expected field count;
* expected column names;
* expected column order where contractually relevant;
* exact column-set compatibility;
* successful output read-back.

The refresh process must not silently publish a structurally changed analytical dataset.

---

## 14. Duplicate Validation

Duplicate handling must follow the established analytical contract.

The refresh process must distinguish:

1. unexpected duplicates;
2. expected source behavior;
3. semantic-grain exceptions;
4. complete-row duplicates.

The six complete-row duplicates currently observed in `daily_vendor_metrics` must not be removed automatically.

They are part of the documented evidence and must remain visible to the validation process.

---

## 15. Null Validation

Null validation must be contract-aware.

The refresh process must not treat every null value as an error.

Instead it must distinguish:

* structurally required fields;
* grain-key nulls;
* fields where nulls are permitted;
* semantic limitations;
* unexpected null behavior.

A validation failure must identify the affected dataset and validation rule.

---

## 16. Controlled Staging

New analytical outputs must not directly overwrite the validated analytical layer before validation.

The preferred process is:

```text
Cleaned Source
     |
     v
Refresh Construction
     |
     v
Staging Output
     |
     v
Validation
     |
     +------ FAIL ------> Preserve Existing Analytical Layer
     |
     +------ PASS ------> Controlled Publication
```

Staging exists to protect the last known valid analytical state.

---

## 17. Controlled Publication

Publication must occur only after required refresh validation gates pass.

The publication mechanism must avoid leaving a partially refreshed analytical layer.

The desired property is:

```text
Before refresh:
VALID STATE A

Refresh:
STAGING STATE B

Validation:
PASS

After publication:
VALID STATE B
```

If validation fails:

```text
Before refresh:
VALID STATE A

Refresh:
STAGING STATE B

Validation:
FAIL

After failed refresh:
VALID STATE A
```

The previous valid state must therefore remain available after a failed refresh.

---

## 18. Failure Visibility

Refresh failures must be visible.

A failure must identify, where applicable:

* dataset;
* source;
* validation category;
* expected condition;
* observed condition;
* publication status;
* whether the previous analytical state was preserved.

Silent failure is not acceptable.

A refresh process that completes partially without clearly identifying the incomplete state must not be treated as successful.

---

## 19. Refresh Evidence

Each controlled refresh should produce sufficient evidence to establish:

* refresh execution;
* source set used;
* dataset set processed;
* validation results;
* row counts;
* schema validation results;
* grain validation results;
* duplicate/null validation results where applicable;
* publication decision;
* failure information where applicable.

The evidence must support reproducibility without requiring the historical notebook to be manually rerun.

---

## 20. Development and Live Separation

The architecture must distinguish development data from live/current data.

Conceptually:

```text
Development Source
       |
       v
Development Refresh
       |
       v
Development Analytical Output


Live/Current Source
       |
       v
Controlled Refresh
       |
       v
Validated Analytical Output
```

Development validation must not silently mutate or replace protected source data.

Live refresh must not bypass validation merely because the source is considered current.

The exact live database extraction mechanism remains an implementation concern for the appropriate Phase 16 scope and must be justified by actual project requirements.

---

## 21. Dashboard Boundary

The dashboard consumes validated analytical outputs.

The dashboard must not independently reconstruct analytical datasets.

The intended boundary is:

```text
Controlled Refresh
       |
       v
Validated Analytical Layer
       |
       v
Dashboard
```

This maintains a clear separation between:

* data preparation;
* validation;
* analytical datasets;
* presentation.

The existing Streamlit + Plotly dashboard remains the presentation layer.

Phase 16 does not rewrite the dashboard.

---

## 22. Reproducibility Requirement

A successful refresh must be reproducible from:

1. the authorized cleaned source layer;
2. the approved analytical construction contracts;
3. the refresh implementation;
4. the validation rules;
5. the controlled publication process.

The process must not depend on undocumented manual notebook execution.

---

## 23. Minimal Architecture Principle

The refresh architecture must remain proportionate to the actual PurjeStore evidence.

Current evidence supports:

* 26 source-native analytical datasets;
* no approved cross-dataset joins;
* no selected ML problems;
* no need for generic orchestration;
* no need for a distributed processing architecture.

Therefore a small local deterministic refresh mechanism is currently more consistent with the evidence than a large orchestration platform.

Any future increase in complexity must be supported by new evidence or requirements.

---

## 24. Relationship to Phase 15

Phase 15 established the architecture boundary:

```text
Live Database
      |
      v
Controlled Data Access
      |
      v
Refresh / Extraction
      |
      v
Validation
      |
      v
Analytical Layer
      |
      v
Dashboard
```

Phase 16-B now defines the controlled-refresh portion of that architecture in sufficient detail for implementation.

Phase 15 itself remains closed.

No Phase 15 implementation scope is reopened by Phase 16-B.

---

## 25. Relationship to Phase 17

Testing remains a separate phase.

Phase 16-B defines the validation behavior that Phase 16-C and Phase 16-D will implement.

Phase 17 will provide broader project testing and regression validation.

The refresh implementation must therefore be designed so that its validation behavior can be tested independently.

---

## 26. Implementation Boundary for Phase 16-C

Phase 16-C may implement only the architecture defined here.

The implementation should provide, at minimum:

1. controlled source discovery;
2. contract loading;
3. source validation;
4. grain validation;
5. source-only projection;
6. analytical dataset validation;
7. staging;
8. controlled publication;
9. failure protection;
10. refresh evidence.

Implementation should reuse the validated 5.3-C construction rules rather than recreate analytical logic from memory.

---

## 27. Explicit Non-Goals

The following are not goals of Phase 16-B or the immediate Phase 16-C implementation:

* making unsupported business claims;
* creating additional KPIs;
* adding joins for convenience;
* creating predictive functionality;
* improving ML performance;
* generating recommendations;
* creating forecasts;
* adding arbitrary business transformations;
* replacing the current analytical layer with a redesigned schema;
* converting every semantic exception into a synthetic grain;
* deleting duplicate source records;
* hiding data-quality limitations;
* introducing infrastructure for its own sake.

---

## 28. Phase 16-B Design Decision

Based on the recovered 5.3-C construction evidence and Phase 16-A audit:

> **PurjeStore will use a small, deterministic, contract-driven, validation-gated refresh mechanism for the existing 26 source-native analytical datasets.**

The mechanism will:

* use the cleaned source layer;
* consume the validated construction contracts;
* preserve authorized source grain;
* perform source-only projection;
* validate outputs before publication;
* protect the previous valid analytical state;
* provide refresh evidence;
* feed the existing dashboard through the validated analytical layer.

No generic ETL/orchestration framework is justified by the current evidence.

---

## 29. Phase 16-B Implementation-Readiness Criteria

Phase 16-B is ready for implementation when all of the following are established:

| Criterion                   | Required State |
| --------------------------- | -------------- |
| 26 analytical datasets      | Confirmed      |
| 5.3-C construction contract | Recovered      |
| Source-only construction    | Confirmed      |
| Physical joins              | 0              |
| Approved final KPIs         | 0              |
| Selected ML problems        | 0              |
| Grain rules                 | Recovered      |
| Semantic-grain exceptions   | Preserved      |
| Schema validation           | Defined        |
| Row-count validation        | Defined        |
| Duplicate validation        | Defined        |
| Null validation             | Defined        |
| Read-back validation        | Defined        |
| Staging                     | Defined        |
| Controlled publication      | Defined        |
| Failure preservation        | Defined        |
| Refresh evidence            | Defined        |
| Dashboard boundary          | Defined        |
| Phase 17 boundary           | Defined        |

---

## 30. Next Phase

After this architecture document is validated and closed:

**Phase 16-C — Controlled Refresh Implementation**

will implement the smallest reusable mechanism consistent with this design.

No implementation file should be created until this Phase 16-B document has been reviewed and accepted.

---

## 31. Document Control

**Document:** `PHASE_16B_CONTROLLED_REFRESH_ARCHITECTURE.md`

**Phase:** 16-B

**Status:** In Progress

**Basis:** Phase 15 architecture reconciliation, Milestone 5.3-C construction evidence, Phase 16-A implementation-readiness audit.

**Next controlled action:** Validate this architecture document before creating the Phase 16-C implementation artifact.

