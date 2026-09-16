# PurjeStore Database Architecture

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
