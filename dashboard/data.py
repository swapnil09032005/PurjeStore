"""
PurjeStore Dashboard Data Access

This module is the dashboard's read-only data-access boundary.

Responsibilities:
- Discover validated analytical CSV datasets.
- Load analytical datasets with Streamlit caching.
- Load the actual controlled-refresh report.
- Return explicit missing/error states rather than inventing data.

This module must NOT contain:
- Joins
- Aggregations that create business KPIs
- Analytical dataset construction
- Source-data mutation
- Semantic approval decisions
- ML/predictive logic
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from .config import ANALYTICAL_ROOT, REFRESH_REPORT_PATH


@st.cache_data
def discover_analytical_files() -> list[Path]:
    """
    Discover analytical CSV datasets deterministically.

    The return type intentionally remains a list to preserve the
    observable behavior of the original dashboard implementation.
    """
    if not ANALYTICAL_ROOT.exists():
        return []

    return sorted(
        ANALYTICAL_ROOT.glob("*.csv")
    )


@st.cache_data
def load_dataset(path_string: str) -> pd.DataFrame:
    """
    Load one analytical CSV dataset.

    The exception wording intentionally preserves the existing
    dashboard behavior and test contract for unsupported sources.
    """
    path = Path(path_string)

    if not path.exists():
        raise FileNotFoundError(
            f"Analytical dataset not found: {path}"
        )

    if path.suffix.lower() != ".csv":
        raise ValueError(
            f"Unsupported analytical source: {path}"
        )

    return pd.read_csv(
        path,
        low_memory=False,
    )


@st.cache_data
def load_refresh_report() -> dict[str, Any] | None:
    """
    Load the actual controlled-refresh report.

    Missing, malformed, or non-dictionary reports return None.
    No refresh metadata is invented.
    """
    if not REFRESH_REPORT_PATH.exists():
        return None

    try:
        payload = json.loads(
            REFRESH_REPORT_PATH.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(payload, dict):
            return None

        return payload

    except (OSError, json.JSONDecodeError):
        return None