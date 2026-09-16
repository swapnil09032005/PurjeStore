from pathlib import Path

# ============================================================
# PurjeStore - Updated Project Structure Setup
# Milestone 0 | Step 1A
#
# Architecture:
#   Development  -> 177 CSV files
#   Production   -> Live MariaDB/MySQL database
#
# SAFE TO RUN AGAIN
# - Does not delete files
# - Does not move files
# - Does not copy CSV files
# - Does not modify raw data
# - Does not connect to database
# ============================================================


# ============================================================
# 1. PROJECT ROOT
# ============================================================

# Current command location:
# C:\Users\ASUS\Desktop\PurjeStore
#
# This creates:
# C:\Users\ASUS\Desktop\PurjeStore\PurjeStore

PROJECT_ROOT = Path.cwd() / "PurjeStore"


# ============================================================
# 2. PROJECT FOLDER STRUCTURE
# ============================================================

folders = [

    # --------------------------------------------------------
    # DATA LAYER
    # --------------------------------------------------------
    "data/raw",
    "data/cleaned",
    "data/processed",
    "data/features",
    "data/sample",

    # --------------------------------------------------------
    # JUPYTER / EXPLORATION
    # --------------------------------------------------------
    "notebooks/01_data_discovery",
    "notebooks/02_relationships",
    "notebooks/03_data_quality",
    "notebooks/04_eda",
    "notebooks/05_modeling",
    "notebooks/06_experiments",

    # --------------------------------------------------------
    # PYTHON SOURCE CODE
    # --------------------------------------------------------
    "src/discovery",
    "src/validation",
    "src/cleaning",
    "src/integration",
    "src/features",
    "src/modeling",
    "src/database",
    "src/dashboard",
    "src/utilities",

    # --------------------------------------------------------
    # DATA / ML PIPELINES
    # --------------------------------------------------------
    "pipelines/data",
    "pipelines/features",
    "pipelines/ml",
    "pipelines/refresh",

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------
    "config",
    "config/development",
    "config/production",

    # --------------------------------------------------------
    # MODEL ARTIFACTS
    # --------------------------------------------------------
    "models",

    # --------------------------------------------------------
    # DASHBOARD APPLICATION
    # --------------------------------------------------------
    "dashboard",

    # --------------------------------------------------------
    # TESTING
    # --------------------------------------------------------
    "tests",
    "tests/data",
    "tests/database",
    "tests/features",
    "tests/modeling",
    "tests/pipelines",
    "tests/dashboard",

    # --------------------------------------------------------
    # OUTPUTS
    # --------------------------------------------------------
    "outputs/profiling",
    "outputs/quality",
    "outputs/analytics",
    "outputs/predictions",
    "outputs/reports",

    # --------------------------------------------------------
    # DOCUMENTATION
    # --------------------------------------------------------
    "docs",
    "docs/architecture",
    "docs/data",
    "docs/database",
    "docs/ml",
    "docs/dashboard",
    "docs/testing",

    # --------------------------------------------------------
    # FINAL REPORTING
    # --------------------------------------------------------
    "reports",
]


# ============================================================
# 3. CREATE FOLDERS
# ============================================================

PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

for folder in folders:
    folder_path = PROJECT_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)


# ============================================================
# 4. PROJECT FILES
# ============================================================

files = {

    # --------------------------------------------------------
    # README
    # --------------------------------------------------------
    "README.md": """# PurjeStore

## End-to-End Data Science and Intelligent E-Commerce
## Decision Support System

PurjeStore is an end-to-end project combining:

- Data Engineering
- Data Science
- Machine Learning
- Business Intelligence
- Interactive Dashboard
- Decision Support

---

## Data Architecture

PurjeStore uses two separate data sources.

### Development Data

The recovered 177 CSV files are used for:

- Data discovery
- Schema analysis
- Relationship investigation
- Data quality analysis
- Data cleaning
- Exploratory Data Analysis
- Analytical dataset development
- Feature engineering
- ML experimentation
- Reproducible development

### Live Data

The live MariaDB/MySQL database is used for:

- Current business data
- Dashboard refresh
- Current analytical queries
- ML inference
- Production-style pipelines
- Future automated refresh/retraining

---

## High-Level Architecture

    Recovered SQL / CSV Data
             |
             v
       Data Discovery
             |
             v
     Relationship Validation
             |
             v
       Data Quality
             |
             v
      Analytical Datasets
             |
       +-----+------+
       |            |
       v            v
    Analytics       ML
       |            |
       +-----+------+
             |
             v
      Decision Support
             |
             v
        Dashboard

Live Database
      |
      v
Current Data Access
      |
      +------------------+
      |                  |
      v                  v
 Dashboard           ML Inference

---

## Project Principles

1. Raw data must remain unchanged.
2. Original SQL dumps must remain protected.
3. Development and production/live data must remain separated.
4. Database credentials must never be committed to Git.
5. Analytical datasets must have a clearly defined grain.
6. Relationships must be validated using evidence.
7. ML problems must be supported by the actual data.
8. Every important result must be reproducible.
9. Dashboard metrics must have documented definitions.
10. No production-style automation will be implemented before validation.

---

## Current Status

Milestone 0 - Project Setup & Protection

Status: IN PROGRESS

Current Step:

Step 1A - Project Structure
Status: COMPLETE
""",


    # --------------------------------------------------------
    # GITIGNORE
    # --------------------------------------------------------
    ".gitignore": """# ============================================================
# Python
# ============================================================

__pycache__/
*.py[cod]
*.pyo
*.pyd

# ============================================================
# Virtual Environments
# ============================================================

.venv/
venv/
env/

# ============================================================
# Jupyter
# ============================================================

.ipynb_checkpoints/

# ============================================================
# Environment / Secrets
# ============================================================

.env
.env.*
!.env.example

*.key
*.pem

# ============================================================
# RAW / WORKING DATA
# ============================================================

data/raw/*
data/cleaned/*
data/processed/*
data/features/*

# Samples may be committed only intentionally
# data/sample/*

# ============================================================
# GENERATED OUTPUTS
# ============================================================

outputs/*
models/*

# ============================================================
# Logs
# ============================================================

*.log
logs/

# ============================================================
# OS
# ============================================================

.DS_Store
Thumbs.db

# ============================================================
# IDE
# ============================================================

.vscode/
.idea/

# ============================================================
# Temporary files
# ============================================================

*.tmp
*.temp
*.bak
""",


    # --------------------------------------------------------
    # ENVIRONMENT TEMPLATE
    # --------------------------------------------------------
    ".env.example": """# ============================================================
# PurjeStore Environment Variables
#
# COPY this file to .env for local development.
#
# NEVER commit the real .env file.
# NEVER place passwords in Python source code.
# ============================================================


# ------------------------------------------------------------
# Application
# ------------------------------------------------------------

APP_ENV=development


# ------------------------------------------------------------
# Live Database
# ------------------------------------------------------------

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=


# ------------------------------------------------------------
# Optional Dashboard Settings
# ------------------------------------------------------------

DASHBOARD_ENV=development


# ------------------------------------------------------------
# Optional ML Settings
# ------------------------------------------------------------

MODEL_ENV=development
""",


    # --------------------------------------------------------
    # PROJECT STATUS
    # --------------------------------------------------------
    "docs/PROJECT_STATUS.md": """# PurjeStore Project Status

## Overall Project

PurjeStore - End-to-End Data Science and Intelligent E-Commerce
Decision Support System

---

# Milestone 0 - Project Setup & Protection

## Status

IN PROGRESS

---

## Step 1A - Project Structure

Status: COMPLETE

Completed:

- Base project structure created
- Development data layer created
- Live database architecture area created
- Database source-code area created
- Dashboard source-code area created
- Pipeline structure created
- Configuration structure created
- Testing structure created
- Documentation structure created
- Environment template created
- Git protection rules created

---

## Step 1B - Environment Verification

Status: NOT STARTED

Pending:

- Operating system verification
- Python version verification
- Python environment verification
- VS Code verification
- Jupyter verification
- Required package verification

---

## Step 1C - Git Verification

Status: NOT STARTED

Pending:

- Git installation
- Repository status
- Initial repository decision
- .gitignore verification

---

## Step 1D - Raw Data Protection

Status: NOT STARTED

Pending:

- Locate 177 CSV files
- Verify original CSV location
- Verify CSV integrity
- Confirm raw-data protection strategy
- Confirm original SQL dump location

---

## Step 1E - Live Database Configuration

Status: NOT STARTED

Pending:

- Live database host
- Live database port
- Database name
- Database access method
- Credential protection
- Connection test

IMPORTANT:

No live database credentials should be stored in Git.

---

## Step 1F - Milestone 0 Validation

Status: NOT STARTED

Milestone 0 can only be marked COMPLETE after all required
environment, data protection, Git and live database checks
have been validated.
""",


    # --------------------------------------------------------
    # DECISION LOG
    # --------------------------------------------------------
    "docs/DECISION_LOG.md": """# PurjeStore Decision Log

| Date | Decision | Reason | Evidence | Status |
|---|---|---|---|---|
| 2026-09-16 | Use VS Code + Jupyter | VS Code for engineering/application work; Jupyter for exploration and experiments | Project workflow decision | Confirmed |
| 2026-09-16 | Use 177 CSV files for development | Provides a controlled and reproducible development data source | Project architecture decision | Confirmed |
| 2026-09-16 | Maintain separate live database connection | Required for current data, dashboard refresh and ML inference | Project architecture decision | Confirmed |
| 2026-09-16 | Keep development and live data logically separated | Prevent accidental modification of live data and preserve reproducibility | Architecture principle | Confirmed |
| 2026-09-16 | Store database credentials through environment configuration | Prevent credentials from entering source control | Security principle | Confirmed |
| 2026-09-16 | Train ML models through validated development pipelines before live inference | Separates model development from production inference | ML architecture principle | Confirmed |
""",


    # --------------------------------------------------------
    # ISSUE LOG
    # --------------------------------------------------------
    "docs/ISSUE_LOG.md": """# PurjeStore Issue Log

| ID | Date | Milestone | Issue | Status | Resolution |
|---|---|---|---|---|---|
""",


    # --------------------------------------------------------
    # ENVIRONMENT
    # --------------------------------------------------------
    "docs/ENVIRONMENT.md": """# PurjeStore Environment

## Operating System

To be recorded.

## Python Version

To be recorded.

## Python Environment

To be recorded.

## IDE

VS Code

## Exploration Environment

Jupyter

## Database Technology

MariaDB/MySQL

## Live Database Host

To be recorded.

## Live Database Port

To be recorded.

## Live Database Name

To be recorded.

## Git

To be verified.

## Important Security Rule

Database credentials must never be written directly into:

- Python source files
- Jupyter notebooks
- Git repositories
- README files
- screenshots
- reports

Credentials will be managed through environment configuration.
""",


    # --------------------------------------------------------
    # DATA PROTECTION
    # --------------------------------------------------------
    "docs/DATA_PROTECTION.md": """# PurjeStore Data Protection Rules

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
""",


    # --------------------------------------------------------
    # DATA ARCHITECTURE
    # --------------------------------------------------------
    "docs/architecture/DATA_ARCHITECTURE.md": """# PurjeStore Data Architecture

## 1. Development Data Source

The recovered 177 CSV files are the primary development source.

Purpose:

- discovery
- profiling
- relationship analysis
- cleaning
- EDA
- analytical dataset construction
- feature engineering
- ML experimentation

---

## 2. Live Data Source

A separate MariaDB/MySQL connection provides current data.

Purpose:

- dashboard refresh
- current analytics
- current predictions
- ML inference
- future automation

---

## 3. Separation Principle

Development data and live data must remain logically separated.

Development:

    CSV
      |
      v
    Cleaning
      |
      v
    Processing
      |
      v
    Features
      |
      v
    Analytics / ML

Live:

    MariaDB/MySQL
          |
          v
    Read / Extraction Layer
          |
          v
    Validated Processing
          |
       +--+--+
       |     |
       v     v
    Dashboard ML Inference

---

## 4. ML Training vs Inference

Training:

    Development Data
          |
          v
    Feature Engineering
          |
          v
    Model Training
          |
          v
    Model Validation
          |
          v
    Approved Model

Inference:

    Live Database
          |
          v
    Current Features
          |
          v
    Approved Model
          |
          v
    Predictions

---

## 5. Future Retraining

Automated retraining is NOT assumed.

It will only be implemented if:

- sufficient data exists
- target remains valid
- data quality is acceptable
- model performance can be validated
- retraining provides business value
""",


    # --------------------------------------------------------
    # DATABASE ARCHITECTURE
    # --------------------------------------------------------
    "docs/database/DATABASE_ARCHITECTURE.md": """# PurjeStore Database Architecture

## Development Database Access

Development work may use:

- CSV files
- local recovered database
- controlled database extracts

depending on the specific task.

---

## Live Database

The live MariaDB/MySQL database is treated as the current source.

The application will use a dedicated database access layer.

Expected responsibilities:

- connection management
- read-only extraction where possible
- query execution
- connection validation
- error handling
- logging
- connection cleanup

---

## Credentials

Credentials must come from environment configuration or
another secure secret-management mechanism.

They must never be hard-coded.

---

## Safety

Development code should default to read-only access against the
live database.

Destructive database operations are outside normal analytics
and ML workflows.
""",


    # --------------------------------------------------------
    # ML ARCHITECTURE
    # --------------------------------------------------------
    "docs/ml/ML_ARCHITECTURE.md": """# PurjeStore ML Architecture

Machine learning problems will NOT be selected merely because
they are common e-commerce problems.

The actual PurjeStore data will determine:

- target availability
- target quality
- prediction horizon
- feature availability
- sample size
- class balance
- business relevance
- feasibility

---

## Development

    CSV Data
       |
       v
    Feature Engineering
       |
       v
    Training Dataset
       |
       v
    Model Experimentation
       |
       v
    Validation
       |
       v
    Approved Model

---

## Live Inference

    Live Database
          |
          v
    Current Feature Data
          |
          v
    Approved Model
          |
          v
    Prediction
          |
          v
    Dashboard / Decision Support
""",


    # --------------------------------------------------------
    # DASHBOARD ARCHITECTURE
    # --------------------------------------------------------
    "docs/dashboard/DASHBOARD_ARCHITECTURE.md": """# PurjeStore Dashboard Architecture

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
""",


    # --------------------------------------------------------
    # TESTING
    # --------------------------------------------------------
    "docs/testing/TESTING_STRATEGY.md": """# PurjeStore Testing Strategy

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
"""
}


# ============================================================
# 5. WRITE FILES SAFELY
# ============================================================

created_files = []
existing_files = []

for relative_path, content in files.items():

    file_path = PROJECT_ROOT / relative_path

    if not file_path.exists():

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        created_files.append(relative_path)

    else:
        existing_files.append(relative_path)


# ============================================================
# 6. CREATE .GITKEEP FILES
# ============================================================

gitkeep_folders = [
    "data/cleaned",
    "data/processed",
    "data/features",
    "data/sample",

    "models",

    "outputs/profiling",
    "outputs/quality",
    "outputs/analytics",
    "outputs/predictions",
    "outputs/reports",

    "pipelines/data",
    "pipelines/features",
    "pipelines/ml",
    "pipelines/refresh",
]

gitkeep_created = []

for folder in gitkeep_folders:

    gitkeep_path = PROJECT_ROOT / folder / ".gitkeep"

    if not gitkeep_path.exists():

        gitkeep_path.touch()

        gitkeep_created.append(
            f"{folder}/.gitkeep"
        )


# ============================================================
# 7. FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("PURJESTORE PROJECT STRUCTURE UPDATED SUCCESSFULLY")
print("=" * 70)

print()
print("Project location:")
print(PROJECT_ROOT.resolve())

print()
print("Architecture:")
print("  Development Data : 177 CSV files")
print("  Live Data        : MariaDB/MySQL")
print("  IDE              : VS Code")
print("  Exploration      : Jupyter")

print()
print("Folders:")
print("-" * 70)

for folder in folders:
    print(f"  [OK] {folder}")

print()
print("New / updated project files:")
print("-" * 70)

for file in created_files:
    print(f"  [CREATED] {file}")

for file in existing_files:
    print(f"  [EXISTS]  {file}")

print()
print("Git protection files:")
print("-" * 70)

for file in gitkeep_created:
    print(f"  [CREATED] {file}")

print()
print("=" * 70)
print("IMPORTANT")
print("=" * 70)

print("1. No CSV files were moved.")
print("2. No CSV files were copied.")
print("3. No CSV files were modified.")
print("4. No database connection was made.")
print("5. No database credentials were requested.")
print("6. Existing files were not overwritten.")
print()
print("Milestone 0 -> Step 1A: COMPLETE")
print("Next: Step 1B - Environment Verification")
print("=" * 70)