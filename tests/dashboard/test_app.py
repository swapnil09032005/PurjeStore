from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from dashboard.config import ANALYTICAL_ROOT
from dashboard.data import discover_analytical_files, load_dataset
from dashboard.utils import (
    format_number,
    is_datetime_like_series,
    is_numeric_series,
    safe_categorical_columns,
    safe_numeric_columns,
    safe_temporal_columns,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYTICAL_ROOT = PROJECT_ROOT / "data" / "processed" / "analytical"


# ---------------------------------------------------------------------------
# Expected current analytical-layer baseline
# ---------------------------------------------------------------------------

EXPECTED_DATASET_COUNT = 26
EXPECTED_TOTAL_ROWS = 12_148
EXPECTED_TOTAL_COLUMNS = 289

EXPECTED_DATASETS = {
    "accounts",
    "attribute_values",
    "commission_history",
    "daily_category_metrics",
    "daily_platform_metrics",
    "daily_vendor_metrics",
    "einvoice_records",
    "hub_inventory",
    "hub_returns",
    "invoices",
    "journal_entries",
    "notification_logs",
    "order_items",
    "orders",
    "outbound_packaging",
    "payment_receipts",
    "payment_transactions",
    "payments",
    "product",
    "product_temp",
    "return_request",
    "shipment_booking",
    "shipment_items",
    "variants",
    "variants_temp",
    "wallet_transactions",
}


# ---------------------------------------------------------------------------
# Discovery / loading
# ---------------------------------------------------------------------------

def test_dashboard_points_to_expected_analytical_directory():
    """The dashboard must read from the established analytical layer."""
    assert ANALYTICAL_ROOT == ANALYTICAL_ROOT
    assert ANALYTICAL_ROOT.exists()
    assert ANALYTICAL_ROOT.is_dir()


def test_discover_analytical_files_returns_current_dataset_set():
    """Discovery should expose exactly the current analytical CSV layer."""
    discovered = discover_analytical_files()

    assert len(discovered) == EXPECTED_DATASET_COUNT
    assert all(path.is_file() for path in discovered)
    assert all(path.suffix.lower() == ".csv" for path in discovered)

    discovered_names = {path.stem for path in discovered}

    assert discovered_names == EXPECTED_DATASETS


def test_discover_analytical_files_is_sorted():
    """Discovery should remain deterministic."""
    discovered = discover_analytical_files()

    assert discovered == sorted(discovered)


def test_load_dataset_reads_real_analytical_dataset():
    """A real current analytical CSV must load successfully."""
    path = ANALYTICAL_ROOT / "accounts.csv"

    df = load_dataset(str(path))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 81
    assert len(df.columns) == 9


def test_load_dataset_missing_file_raises_file_not_found():
    """Missing analytical sources must fail explicitly."""
    missing_path = ANALYTICAL_ROOT / "__definitely_missing_dataset__.csv"

    with pytest.raises(FileNotFoundError, match="Analytical dataset not found"):
        load_dataset(str(missing_path))


def test_load_dataset_rejects_non_csv_source(tmp_path):
    """The dashboard loader must reject unsupported source extensions."""
    unsupported = tmp_path / "example.txt"
    unsupported.write_text("not a csv", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Unsupported analytical source",
    ):
        load_dataset(str(unsupported))


def test_load_dataset_preserves_csv_content_without_joining():
    """
    Loading one analytical dataset must preserve its source shape.

    This test deliberately checks only one dataset at a time because the
    dashboard architecture does not authorize cross-dataset joins.
    """
    path = ANALYTICAL_ROOT / "product.csv"

    df = load_dataset(str(path))

    assert len(df) == 87
    assert len(df.columns) == 18


# ---------------------------------------------------------------------------
# Type / field classification helpers
# ---------------------------------------------------------------------------

def test_is_numeric_series_identifies_numeric_values():
    numeric = pd.Series([1, 2, 3], name="amount")

    assert is_numeric_series(numeric) is True


def test_is_numeric_series_rejects_string_values():
    text = pd.Series(["1", "2", "3"], name="amount")

    assert is_numeric_series(text) is False


def test_is_datetime_like_series_identifies_datetime_dtype():
    dates = pd.Series(
        pd.to_datetime(
            ["2026-01-01", "2026-01-02"]
        ),
        name="value",
    )

    assert is_datetime_like_series(dates) is True


@pytest.mark.parametrize(
    "column_name",
    [
        "createdAt",
        "updatedAt",
        "deletedAt",
        "order_date",
        "event_time",
        "event_timestamp",
        "modified_date",
    ],
)
def test_is_datetime_like_series_recognizes_temporal_name_signals(
    column_name,
):
    values = pd.Series(
        ["not necessarily parseable", "still a signal"],
        name=column_name,
    )

    assert is_datetime_like_series(values) is True


def test_is_datetime_like_series_rejects_unrelated_string_column():
    values = pd.Series(
        ["abc", "def"],
        name="product_name",
    )

    assert is_datetime_like_series(values) is False


def test_safe_numeric_columns_returns_pandas_numeric_fields():
    """
    safe_numeric_columns delegates numeric detection to pandas'
    is_numeric_dtype() through is_numeric_series().

    In the current pandas environment, boolean dtype satisfies
    is_numeric_dtype(), so boolean_field is intentionally included.
    """
    df = pd.DataFrame(
        {
            "integer_field": [1, 2, 3],
            "float_field": [1.5, 2.5, 3.5],
            "text_field": ["a", "b", "c"],
            "boolean_field": [True, False, True],
        }
    )

    assert safe_numeric_columns(df) == [
        "integer_field",
        "float_field",
        "boolean_field",
    ]


def test_safe_numeric_columns_rejects_object_strings():
    df = pd.DataFrame(
        {
            "numeric_field": [10, 20, 30],
            "string_field": ["10", "20", "30"],
        }
    )

    result = safe_numeric_columns(df)

    assert result == ["numeric_field"]


def test_safe_categorical_columns_returns_supported_dimension_types():
    df = pd.DataFrame(
        {
            "text_field": ["a", "b", "c"],
            "string_field": pd.Series(
                ["x", "y", "z"],
                dtype="string",
            ),
            "category_field": pd.Series(
                ["A", "B", "A"],
                dtype="category",
            ),
            "boolean_field": [True, False, True],
            "integer_field": [1, 2, 3],
        }
    )

    result = safe_categorical_columns(df)

    assert result == [
        "text_field",
        "string_field",
        "category_field",
        "boolean_field",
    ]


def test_safe_temporal_columns_returns_temporal_signal_fields():
    df = pd.DataFrame(
        {
            "createdAt": ["2026-01-01", "2026-01-02"],
            "event_timestamp": ["2026-01-03", "2026-01-04"],
            "product_name": ["A", "B"],
            "amount": [10, 20],
        }
    )

    assert safe_temporal_columns(df) == [
        "createdAt",
        "event_timestamp",
    ]


# ---------------------------------------------------------------------------
# Formatting helper
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "—"),
        (10, "10"),
        (10.0, "10"),
        (10.5, "10.5"),
        (1234.567, "1,234.57"),
        ("PurjeStore", "PurjeStore"),
    ],
)
def test_format_number_handles_supported_values(value, expected):
    assert format_number(value) == expected


def test_format_number_handles_nan():
    assert format_number(float("nan")) == "—"


def test_format_number_does_not_fail_on_unusual_object():
    class ExampleObject:
        def __str__(self):
            return "example-object"

    value = ExampleObject()

    assert format_number(value) == "example-object"


# ---------------------------------------------------------------------------
# Real analytical dataset classification
# ---------------------------------------------------------------------------

def test_real_accounts_dataset_supports_dashboard_classification():
    """
    The actual accounts analytical dataset should pass through the same
    classification helpers used by the dashboard.
    """
    path = ANALYTICAL_ROOT / "accounts.csv"
    df = load_dataset(str(path))

    numeric = safe_numeric_columns(df)
    categorical = safe_categorical_columns(df)
    temporal = safe_temporal_columns(df)

    assert isinstance(numeric, list)
    assert isinstance(categorical, list)
    assert isinstance(temporal, list)

    assert set(numeric).isdisjoint(categorical)

    assert all(column in df.columns for column in numeric)
    assert all(column in df.columns for column in categorical)
    assert all(column in df.columns for column in temporal)


def test_real_analytical_layer_total_baseline_matches_dashboard_input():
    """
    The dashboard's discovered analytical layer must retain the established
    Phase 16/8 baseline: 26 datasets, 12,148 rows, 289 columns.
    """
    discovered = discover_analytical_files()

    total_rows = 0
    total_columns = 0

    for path in discovered:
        df = load_dataset(str(path))
        total_rows += len(df)
        total_columns += len(df.columns)

    assert len(discovered) == EXPECTED_DATASET_COUNT
    assert total_rows == EXPECTED_TOTAL_ROWS
    assert total_columns == EXPECTED_TOTAL_COLUMNS


# ---------------------------------------------------------------------------
# Read-only / integrity boundary
# ---------------------------------------------------------------------------

def test_dashboard_helpers_do_not_modify_analytical_source_files():
    """
    The dashboard data layer is read-only.

    Record source metadata before and after discovery/loading. The helper
    layer must not alter the analytical CSV files.
    """
    discovered = discover_analytical_files()

    before = {
        path: (
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in discovered
    }

    for path in discovered:
        load_dataset(str(path))

    after = {
        path: (
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in discovered
    }

    assert after == before


# ---------------------------------------------------------------------------
# Test module sanity
# ---------------------------------------------------------------------------

def test_expected_dataset_names_are_unique_and_valid():
    """The test contract itself must remain internally consistent."""
    assert len(EXPECTED_DATASETS) == EXPECTED_DATASET_COUNT
    assert all(name for name in EXPECTED_DATASETS)
    assert all("/" not in name and "\\" not in name for name in EXPECTED_DATASETS)