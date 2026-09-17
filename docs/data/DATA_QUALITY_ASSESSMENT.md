# PurjeStore — Milestone 3.1 Data Quality Assessment

Generated: 2026-09-17 16:22:04

## 1. Assessment scope

This assessment evaluates completeness and missingness patterns across the PurjeStore raw CSV working sources. The assessment is diagnostic only. No raw CSV file was modified, deleted, imputed, or overwritten.

## 2. Completeness baseline

| Metric | Result |
|---|---:|
| CSV tables profiled | 177 |
| Total profiled columns | 2,462 |
| Total profiled cells | 707,892 |
| Total null cells | 185,040 |
| Overall missingness | 26.14% |
| Fully missing columns | 205 |
| High-missingness columns (>25% and <100%) | 388 |
| Extreme high-missingness fields (≤10 populated) | 61 |
| Tables containing extreme fields | 24 |

## 3. Missingness interpretation

Missingness was not automatically treated as a data-quality error. Observed patterns were evaluated in the context of table role, field semantics, workflow state, identifier behavior, temporary/staging structure, and co-population patterns.

The assessment identified 205 completely missing columns across 58 tables.

Among the 388 fields with more than 25% but less than 100% missingness, 125 fields had no more than 10 populated observations and were subjected to additional structural and semantic review.

## 4. Extreme high-missingness classification

| Classification | Field count |
|---|---:|
| IDENTIFIER_REFERENCE | 2 |
| OPTIONAL_ATTRIBUTE | 17 |
| PII_OPTIONAL | 3 |
| TEMPORARY_STAGING | 7 |
| WORKFLOW_CONDITIONAL | 32 |
| **Total** | **61** |

### Classification interpretation

- **WORKFLOW_CONDITIONAL** — field population depends on a particular business or operational workflow state.
- **OPTIONAL_ATTRIBUTE** — field represents optional metadata or attributes for which NULL can be structurally valid.
- **TEMPORARY_STAGING** — field belongs to a temporary/staging table and should be interpreted according to that table's role.
- **PII_OPTIONAL** — sparse personal or business identity/contact information requiring privacy-aware handling and no automatic imputation.
- **IDENTIFIER_REFERENCE** — sparse identifier/reference field whose NULL values may be structurally valid.

## 5. Validated examples

### Support assignment

`support_tickets.assigned_to` was manually validated. Two tickets contain `assigned_to = 1`, and employee ID 1 exists in the employee table. The field is classified as `WORKFLOW_CONDITIONAL`, reflecting support-ticket assignment.

### Shipment RTV workflow

Sparse shipment RTV fields were reviewed together with their co-population patterns. Their population is associated with the RTV workflow and should not be automatically imputed merely because overall missingness is high.

### E-invoice lifecycle

Sparse e-invoice fields such as `irn`, `ackNo`, `ackDt`, `signedInvoice`, and `generated_at` occur within the e-invoice processing lifecycle and are classified as `WORKFLOW_CONDITIONAL`.

### Temporary product/variant data

Fields in `product_temp` and `variants_temp` retain their temporary/staging classification and should not be treated as ordinary production-table missingness without further pipeline-specific validation.

## 6. Data-quality decision

No automatic imputation, deletion, replacement, or NULL conversion is authorized from this assessment alone.

The current evidence indicates that a substantial portion of extreme missingness is associated with optional fields, workflow-dependent fields, staging structures, or sparse operational events.

## 7. Reproducibility evidence

The following machine-readable evidence files were generated:

- `outputs/quality/fully_missing_fields.csv`
- `outputs/quality/high_missingness_fields.csv`
- `outputs/quality/extreme_missingness_classification.csv`

The source raw CSV files remain unchanged.

## 8. Milestone 3.1 status

**Status: COMPLETE — Data Quality Assessment / Completeness Baseline**

The completeness baseline, missingness distribution, fully-missing field review, high-missingness screening, extreme-field semantic classification, and final validation have been completed.

### Extreme Missingness Population vs Semantic Classification Subset

The extreme-missingness analysis identified **125 fields across 38 tables**
with no more than 10 populated observations.

A narrower subset of **61 fields across 24 tables** was subsequently subjected
to detailed semantic classification because those fields required explicit
interpretation beyond the structural missingness screening.

Therefore, the 125-field / 38-table figures represent the **overall extreme
population**, while the 61-field / 24-table figures represent the
**semantically reviewed classification subset**. These are different analytical
populations and should not be interpreted as conflicting counts.
