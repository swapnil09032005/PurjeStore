# PurjeStore Data Protection Rules

## 1. Original SQL Dump

The original SQL dump is a protected source.

It must never be modified.

---

## 2. Raw CSV Data

The 177 recovered CSV files are development source data.

They must never be modified directly.

Cleaning and transformation outputs must be written to:

- data/cleaned/
- data/processed/
- data/features/

---

## 3. Live Database

The live database must be treated as an external production/current
data source.

The project must not perform destructive operations against it.

Examples of prohibited development actions:

- DROP
- DELETE
- TRUNCATE
- UPDATE
- ALTER

unless explicitly designed, reviewed and authorized as part of a
separate controlled operation.

---

## 4. Credentials

Database passwords and secrets must never be committed to Git.

Use environment variables or another secure secret mechanism.

---

## 5. PII

Potential personally identifiable information must be identified
before being exposed in:

- reports
- screenshots
- dashboards
- notebooks
- presentations
- external services
