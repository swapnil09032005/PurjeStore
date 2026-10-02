"""
PurjeStore Dashboard Utilities

Business-semantic-neutral helpers for dashboard data inspection and display.

Responsibilities:
- Series type inspection
- Dataset field inspection
- Safe display formatting
- Descriptive series summaries

This module must NOT contain:
- Approved semantic mappings
- KPI logic
- Business definitions
- Dataset construction
- Joins
- ML logic
- Source-data mutation
- File writes
"""

import math
from typing import Any

import pandas as pd


# ---------------------------------------------------------------------------
# Series inspection
# ---------------------------------------------------------------------------

def is_numeric_series(
    series: pd.Series,
) -> bool:
    """Return whether a Series has a numeric pandas dtype."""

    return pd.api.types.is_numeric_dtype(series)


def is_datetime_like_series(
    series: pd.Series,
) -> bool:
    """
    Return whether a Series is explicitly datetime-like or has a
    name containing a controlled temporal token.

    The name-based check is only a technical inspection heuristic.
    It does not establish business meaning.
    """

    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    name = str(series.name).lower()

    temporal_tokens = (
        "date",
        "time",
        "timestamp",
        "created",
        "updated",
        "modified",
        "deleted",
        "at",
    )

    return any(
        token in name
        for token in temporal_tokens
    )


# ---------------------------------------------------------------------------
# Dataset field inspection
# ---------------------------------------------------------------------------

def safe_numeric_columns(
    df: pd.DataFrame,
) -> list[str]:
    """Return columns whose pandas dtype is numeric."""

    return [
        column
        for column in df.columns
        if is_numeric_series(df[column])
    ]


def safe_categorical_columns(
    df: pd.DataFrame,
) -> list[str]:
    """
    Return columns suitable for categorical-style technical inspection.

    This is a dtype-based classification only and does not imply
    business-semantic approval.
    """

    result: list[str] = []

    for column in df.columns:
        series = df[column]
        dtype = series.dtype

        if (
            pd.api.types.is_object_dtype(dtype)
            or pd.api.types.is_string_dtype(dtype)
            or isinstance(
                dtype,
                pd.CategoricalDtype,
            )
            or pd.api.types.is_bool_dtype(dtype)
        ):
            result.append(column)

    return result


def safe_temporal_columns(
    df: pd.DataFrame,
) -> list[str]:
    """Return columns identified as technically datetime-like."""

    return [
        column
        for column in df.columns
        if is_datetime_like_series(df[column])
    ]


# ---------------------------------------------------------------------------
# Display formatting
# ---------------------------------------------------------------------------

def format_number(
    value: Any,
) -> str:
    """
    Format a scalar for dashboard display without assigning business meaning.

    Non-numeric values are returned as strings.
    Missing numeric values are represented by an em dash.
    """

    if value is None:
        return "—"

    try:
        if (
            isinstance(value, float)
            and math.isnan(value)
        ):
            return "—"

        if isinstance(value, (int, float)):
            return (
                f"{value:,.2f}"
                .rstrip("0")
                .rstrip(".")
            )

    except Exception:
        pass

    return str(value)


# ---------------------------------------------------------------------------
# Descriptive inspection
# ---------------------------------------------------------------------------

def descriptive_summary(
    series: pd.Series,
) -> dict[str, Any]:
    """
    Return basic descriptive information for a Series.

    The result is descriptive only:
    rows, non-null values, missing values, and distinct populated values.
    """

    clean = series.dropna()

    return {
        "rows": int(len(series)),
        "non_null": int(clean.shape[0]),
        "missing": int(series.isna().sum()),
        "unique": int(clean.nunique()),
    }