"""
PurjeStore Dashboard Configuration

This module contains controlled dashboard configuration only.

Responsibilities:
- Project-relative paths
- Analytical data location
- Refresh report location
- Dashboard page definitions
- Controlled dashboard-wide descriptive configuration

This module must NOT contain:
- Analytical transformations
- Dataset construction
- Joins
- KPI calculations
- ML logic
- Source-data mutation
- Semantic approval logic
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ANALYTICAL_ROOT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytical"
)

REFRESH_REPORT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "refresh"
    / "latest_refresh_report.json"
)


# ---------------------------------------------------------------------------
# Dashboard page definitions
# ---------------------------------------------------------------------------

PAGE_AREAS = [
    "P01 Executive Overview",
    "P02 Commercial / Sales",
    "P03 Orders",
    "P04 Products / Catalog",
    "P05 Customers / Accounts",
    "P06 Fulfillment / Shipping",
    "P07 Returns / Exchange",
    "P08 Operations / Inventory",
    "Data & System Health",
    "Technical Dataset Explorer",
]


BUSINESS_PAGES = [
    "P01 Executive Overview",
    "P02 Commercial / Sales",
    "P03 Orders",
    "P04 Products / Catalog",
    "P05 Customers / Accounts",
    "P06 Fulfillment / Shipping",
    "P07 Returns / Exchange",
    "P08 Operations / Inventory",
]


TECHNICAL_PAGES = [
    "Data & System Health",
    "Technical Dataset Explorer",
]


# ---------------------------------------------------------------------------
# Dashboard descriptive boundary
# ---------------------------------------------------------------------------

KNOWN_LIMITATIONS = [
    "Final business KPIs are not activated because no final KPI set was approved.",
    "No cross-dataset joins are used by the current dashboard.",
    "ML and predictive outputs are blocked because no ML problem was selected.",
    "The analytical layer is consumed read-only by the dashboard.",
    "The current analytical evidence does not expose order_id as a dashboard business field.",
    "Raw customer names, emails, addresses, and other raw customer PII are not exposed.",
    "Deferred variants_temp fields remain unavailable for dashboard interpretation.",
    "Numeric dtype alone does not establish business meaning.",
]


# ---------------------------------------------------------------------------
# Streamlit application configuration
# ---------------------------------------------------------------------------

STREAMLIT_PAGE_TITLE = "PurjeStore Analytics"
STREAMLIT_PAGE_ICON = "📊"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"


# ---------------------------------------------------------------------------
# Technical constants
# ---------------------------------------------------------------------------

MAX_CATEGORY_DISPLAY_ROWS = 30
MAX_EXPLORER_ROWS = 100