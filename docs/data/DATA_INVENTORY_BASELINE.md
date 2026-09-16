# PurjeStore Data Inventory Baseline

## 1. Document Purpose

This document records the validated baseline inventory of the recovered PurjeStore
data sources.

The purpose of this baseline is to establish a reproducible and auditable
understanding of the available data before performing relationship discovery,
data cleaning, analytical dataset construction, exploratory analysis, or machine
learning.

No analytical joins, business assumptions, or machine-learning assumptions are
made by this inventory document.

---

## 2. Inventory Scope

The PurjeStore project currently contains:

- 177 raw CSV data sources.
- All 177 CSV files are located under `data/raw`.
- All 177 CSV files were successfully profiled.
- The CSV sources correspond exactly to the 177 BASE TABLE objects in the
  recovered PurjeStore database.

The recovered database contains:

- 178 database objects in total.
- 177 BASE TABLE objects.
- 1 VIEW object.

The database view identified during inventory is:

`v_shipment_qc_summary`

---

## 3. Inventory Baseline Metrics

| Metric | Validated Value |
|---|---:|
| Total CSV sources | 177 |
| Successfully profiled CSV sources | 177 |
| Failed CSV reads | 0 |
| Populated tables | 132 |
| Empty tables | 45 |
| Total rows across CSV sources | 52,270 |
| Total columns across CSV sources | 2,462 |
| Duplicate rows detected by inventory profiler | 0 |
| Initially unclassified tables | 15 |
| Final unclassified tables | 0 |
| Multi-domain tables | 40 |

These values represent the inventory baseline at the time of profiling.

---

## 4. CSV-to-Database Reconciliation

The CSV inventory was reconciled against the recovered MariaDB database.

Validation result:

| Check | Result |
|---|---:|
| CSV files | 177 |
| Database BASE TABLEs | 177 |
| Exact table-name matches | 177 |
| CSV files without matching database table | 0 |
| Database tables without matching CSV | 0 |
| MySQL/MariaDB reconciliation errors | 0 |

Therefore, the working CSV inventory has complete name-level coverage of the
recovered database BASE TABLE layer.

This reconciliation establishes source coverage only. It does not yet prove
primary keys, foreign keys, relationship cardinality, semantic correctness,
or analytical suitability.

---

## 5. Table Population Status

Of the 177 inventoried tables:

- 132 contain data.
- 45 contain zero rows.

Empty tables are retained in the inventory because their presence is part of
the recovered database architecture and may provide useful structural
information during later relationship and schema analysis.

They should not automatically be treated as analytical datasets.

---

## 6. Domain Classification

The first-pass domain classification was initially generated using table-name
rules.

The initial classification contained 15 unclassified tables and several
keyword-based false positives.

Those tables were subsequently reviewed using their actual column schemas.

The classification rules were then updated in:

`Milestones Handeler/classify_inventory_domains.py`

The classification output was regenerated and spot-checked.

Final result:

- 177/177 tables have a candidate domain classification.
- 0 tables remain unclassified.
- 40 tables have multiple candidate domains.

### Final Domain Distribution

| Candidate Domain | Table Count |
|---|---:|
| Audit_Logging | 9 |
| Customer_User | 15 |
| Finance_Accounting | 24 |
| Inventory | 7 |
| Marketing_Communication | 12 |
| Orders_Sales | 27 |
| Payments | 14 |
| Product_Catalog | 31 |
| Returns_QC | 11 |
| Security_Access | 7 |
| Shipping_Logistics | 23 |
| Support | 11 |
| System_Configuration | 12 |
| Temporary_Staging | 7 |
| Vendor | 10 |

Because multi-domain tables are included in more than one domain count, these
domain counts are not intended to sum to 177.

---

## 7. Multi-Domain Tables

Some tables naturally represent more than one business or technical domain.

Examples include:

- `cancel_request.csv`
  - Orders_Sales
  - Returns_QC

- `commission_history.csv`
  - Finance_Accounting
  - Product_Catalog

- `company_details.csv`
  - System_Configuration
  - Finance_Accounting

- `daily_platform_metrics.csv`
  - Orders_Sales
  - Customer_User
  - Product_Catalog

- `notification_logs.csv`
  - Marketing_Communication
  - Audit_Logging

- `package_rules.csv`
  - Shipping_Logistics
  - Product_Catalog

- `reviews.csv`
  - Product_Catalog
  - Customer_User

- `warranty_certificates.csv`
  - Orders_Sales
  - Product_Catalog
  - Shipping_Logistics

These classifications represent candidate business domains and are not
relationship definitions.

---

## 8. Important Data Characteristics Identified During Profiling

### 8.1 Large File/Blob-Like Field

`document_upload.csv` contains a field named:

`fileData`

The field contains large serialized/file-content-like values.

Independent inspection showed:

- 52 rows.
- 52 non-empty `fileData` values.
- Maximum observed field length: 1,982,125 characters.
- Average observed field length: approximately 339,694.81 characters.
- JPEG and PNG markers were detected in sampled/inspected values.

Therefore, `document_upload.fileData` should not be treated as an ordinary
analytical text field.

For normal profiling, joining, and analytical dataset construction, this field
should be handled separately unless a future business requirement explicitly
requires document-content analysis.

Raw file contents should not be printed into project logs or documentation.

---

## 9. Potential Data-Semantic Issues Requiring Later Validation

Inventory profiling identified structural characteristics that require
semantic validation in later milestones.

For example, `orders.csv` contains legacy and newer financial fields.

A representative observation showed differences in scale between fields such as:

- `subtotal`
- `subtotal_legacy`

This observation is not interpreted as an error at the inventory stage.

The appropriate action is to investigate the field definitions, units,
transformations, and historical conventions during the Data Quality and
Analytical Dataset milestones.

Similar legacy/new field patterns may exist in other tables.

---

## 10. Profiling Outputs

The following inventory artifacts were generated:

### Inventory Summary

`outputs/profiling/inventory_summary.csv`

Contains table-level inventory information including:

- file name
- relative path
- file size
- row count
- column count
- duplicate-row information
- read status
- errors, where applicable

### Column Profile

`outputs/profiling/column_profile.csv`

Contains column-level profiling information generated by the inventory
profiler.

### Profiling Issues

`outputs/profiling/profiling_issues.csv`

No CSV read failures were identified during the validated profiling run.

### Profiling Report

`outputs/profiling/profiling_report.json`

Contains the machine-readable profiling summary.

### Domain Classification

`outputs/profiling/inventory_domain_classification.csv`

Contains the final reproducible candidate-domain classification.

---

## 11. Reproducibility

The main reusable inventory scripts are maintained under:

`Milestones Handeler`

Relevant scripts include:

- `compare_csv_db.py`
- `data_inventory_profiler.py`
- `classify_inventory_domains.py`

The domain classification is generated by code rather than manually editing the
output CSV.

This is important because the inventory should be reproducible if the working
environment or source data is reloaded.

---

## 12. Classification Methodology and Limitations

The final candidate-domain classification combines:

1. Automated table-name classification.
2. Manual schema inspection of initially unclassified or questionable tables.
3. Explicit table-level classification rules for known tables.
4. Regeneration of the classification output.
5. Final spot-check of the reviewed tables.

The classification should be treated as a **candidate domain map**, not as a
formal database schema.

It does not establish:

- primary keys
- foreign keys
- inferred relationships
- relationship cardinality
- data lineage
- business definitions
- metric definitions
- data-quality rules
- analytical suitability
- machine-learning suitability

Those topics will be addressed in later milestones.

---

## 13. Current Project Boundary

At the completion of this inventory stage, the project has established a
validated source inventory and preliminary domain structure.

The following activities are intentionally NOT part of this stage:

- No production analytical joins.
- No permanent data cleaning transformations.
- No KPI implementation.
- No machine-learning model selection.
- No feature engineering.
- No dashboard implementation.

Those activities require evidence from subsequent milestones.

---

## 14. Milestone Status

### Milestone 1 — Complete PurjeStore Data Inventory

Current status:

**IN PROGRESS — inventory profiling and domain classification completed.**

Completed components:

- Workspace validation
- Data-source inventory
- CSV/database reconciliation
- Table population assessment
- Column-level profiling
- Profiling issue validation
- Large file/blob identification
- Initial domain classification
- Schema-based classification review
- Reproducible domain-classification implementation
- Final domain-classification spot-check

Remaining Milestone 1 work will be completed before relationship discovery
begins.

---

## 15. Validation Principle

The inventory baseline is a factual description of the recovered data sources.

Where the project has identified a possible issue, it is recorded as a
validation requirement rather than being silently corrected.

This preserves the distinction between:

- what the recovered data currently contains,
- what has been technically validated,
- what has been inferred,
- and what still requires investigation.

This distinction will be maintained throughout the PurjeStore project.