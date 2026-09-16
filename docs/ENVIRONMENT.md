# PurjeStore Environment

## Project Root

`C:\Users\ASUS\Desktop\PurjeStore`

## Operating System

- Microsoft Windows 11 Home Single Language
- 64-bit
- OS Version: `10.0.26200`

## Python Version

Python `3.11.9`

## Python Environment

- Environment name: `PurjeStore_environment`
- Environment path:
  `C:\Users\ASUS\Desktop\PurjeStore\PurjeStore_environment`
- Python executable:
  `C:\Users\ASUS\Desktop\PurjeStore\PurjeStore_environment\Scripts\python.exe`

## IDE

VS Code

## Exploration Environment

Jupyter

### Verified Jupyter Components

- JupyterLab: `4.6.3`
- Notebook: `7.6.2`
- IPython: `9.17.1`
- ipykernel: `7.3.0`
- ipywidgets: `8.1.9`
- jupyter_client: `8.10.0`
- jupyter_core: `5.9.1`
- jupyter_server: `2.21.1`
- nbclient: `0.11.0`
- nbconvert: `7.17.1`
- nbformat: `5.11.1`
- traitlets: `5.16.1`
- qtconsole: Not installed

## Database Technology

MariaDB

## Live Database

- DBMS: MariaDB `10.4.32`
- Host: `127.0.0.1`
- Port: `3308`
- Database name: `purjestore`

## Database Object Verification

- Total database objects: `178`
- Base tables: `177`
- Views: `1`
- View identified: `v_shipment_qc_summary`

## Development Data Verification

- Raw CSV files: `177`
- CSV-to-database base-table exact matches: `177 / 177`
- CSV files without matching database table: `0`
- Database base tables without matching CSV: `0`

The 177 CSV sources correspond exactly to the 177 MariaDB base tables by name.

The additional database object is the view:

`v_shipment_qc_summary`

Therefore:

`177 base tables + 1 view = 178 database objects`

## Git

Git version: `2.48.1.windows.1`

Initial project baseline commit has been created.

## Data Sources

### Original Recovery Source

The original recovery archive is maintained outside the PurjeStore project:

`C:\Users\ASUS\Desktop\DP-Project\Dump20260916.zip`

The extracted SQL recovery source is also maintained outside the PurjeStore project:

`C:\Users\ASUS\Desktop\DP-Project\Dump20260916\Dump20260916\`

These recovery sources are preserved and should not be modified, moved, renamed, or deleted as part of normal project development.

### Project Development Data

The current controlled development CSV data is stored in:

`C:\Users\ASUS\Desktop\PurjeStore\data\raw\`

Count verified: `177` CSV files.

## Environment Mode

Current project environment:

`development`

The development workflow uses:

- Controlled CSV data for reproducible analysis and development
- Live MariaDB for database validation and future live-data workflows
- Environment configuration for database credentials

## Security Rules

Database credentials must never be written directly into:

- Python source files
- Jupyter notebooks
- Git repositories
- README files
- reports
- screenshots
- documentation

Database passwords must not be committed to Git.

Credentials will be managed through environment configuration.

Raw data and recovery sources must be protected from accidental modification or deletion.

Destructive database operations such as `DROP`, `DELETE`, `TRUNCATE`, `UPDATE`, and `ALTER` are prohibited during normal analytics and ML development unless separately authorized.

## Verification Status

Environment verification completed:

- Project structure: Verified
- Python environment: Verified
- Jupyter: Verified
- Git: Verified
- Live MariaDB connection: Verified
- Database selection: Verified
- Database object count: Verified
- CSV-to-database reconciliation: Verified

Milestone 0 remains in progress until the final project setup validation is completed.
