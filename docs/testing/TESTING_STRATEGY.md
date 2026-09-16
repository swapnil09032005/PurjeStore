# PurjeStore Testing Strategy

Testing will eventually cover:

## Data

- file availability
- schema validation
- row counts
- null checks
- duplicate checks
- data-type validation

## Database

- connection validation
- query validation
- read-only safety
- error handling

## Features

- feature correctness
- missing-value handling
- leakage checks

## ML

- training reproducibility
- target validation
- evaluation metrics
- prediction schema

## Dashboard

- KPI correctness
- filters
- refresh behavior
- visualization correctness

## Pipelines

- end-to-end execution
- failure handling
- logging
