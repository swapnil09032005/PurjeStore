# PurjeStore Dashboard Architecture

The dashboard will eventually support two data modes.

## Development Mode

Uses controlled development data.

Purpose:

- dashboard development
- KPI validation
- visualization testing
- UX development
- reproducibility

## Live Mode

Uses current database data.

Purpose:

- current KPIs
- current analytics
- current ML predictions
- decision support

---

## Important Principle

Dashboard metrics must be defined and validated before they are
implemented as production metrics.

No KPI should be created simply because it is common in e-commerce.
