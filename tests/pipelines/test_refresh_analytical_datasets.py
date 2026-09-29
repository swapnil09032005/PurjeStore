"""
Phase 17 pipeline tests — controlled analytical refresh contract.

Scope
-----
This test module validates the currently implemented Phase 16-C refresh
boundary without executing a write-producing refresh.

Covered:
- refresh implementation exists
- expected 26 analytical datasets exist
- analytical dataset names are complete
- analytical datasets are readable
- analytical baseline remains 26 / 12,148 / 289
- analytical columns remain projections of cleaned sources
- source row counts equal analytical output row counts
- explicit source grain keys remain valid
- semantic-grain exceptions remain explicit
- daily_vendor_metrics preserves its documented six complete-row duplicates
- refresh evidence exists and reports PASS
- refresh evidence reports 26 datasets and successful publication
- refresh evidence contains no actual failure value

Not covered yet:
- feature engineering
- ML/model tests
- unsupported joins
- arbitrary database tests
- dashboard tests
- write-producing refresh integration tests

Those belong to later Phase 17 scope where justified.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from collections import Counter


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
ANALYTICAL_DIR = PROJECT_ROOT / "data" / "processed" / "analytical"
REFRESH_SCRIPT = (
    PROJECT_ROOT
    / "pipelines"
    / "refresh"
    / "refresh_analytical_datasets.py"
)
REFRESH_REPORT = (
    PROJECT_ROOT
    / "outputs"
    / "refresh"
    / "latest_refresh_report.json"
)


EXPECTED_DATASETS: tuple[str, ...] = (
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
)


EXPECTED_ROW_COUNTS: dict[str, int] = {
    "accounts": 81,
    "attribute_values": 80,
    "commission_history": 68,
    "daily_category_metrics": 24,
    "daily_platform_metrics": 46,
    "daily_vendor_metrics": 102,
    "einvoice_records": 33,
    "hub_inventory": 90,
    "hub_returns": 67,
    "invoices": 320,
    "journal_entries": 735,
    "notification_logs": 7592,
    "order_items": 374,
    "orders": 374,
    "outbound_packaging": 132,
    "payment_receipts": 246,
    "payment_transactions": 191,
    "payments": 337,
    "product": 87,
    "product_temp": 51,
    "return_request": 63,
    "shipment_booking": 348,
    "shipment_items": 352,
    "variants": 112,
    "variants_temp": 91,
    "wallet_transactions": 152,
}


EXPECTED_ANALYTICAL_COLUMN_COUNTS: dict[str, int] = {
    "accounts": 9,
    "attribute_values": 4,
    "commission_history": 8,
    "daily_category_metrics": 7,
    "daily_platform_metrics": 9,
    "daily_vendor_metrics": 11,
    "einvoice_records": 12,
    "hub_inventory": 5,
    "hub_returns": 10,
    "invoices": 15,
    "journal_entries": 12,
    "notification_logs": 11,
    "order_items": 11,
    "orders": 14,
    "outbound_packaging": 13,
    "payment_receipts": 12,
    "payment_transactions": 10,
    "payments": 11,
    "product": 18,
    "product_temp": 16,
    "return_request": 13,
    "shipment_booking": 20,
    "shipment_items": 4,
    "variants": 14,
    "variants_temp": 13,
    "wallet_transactions": 7,
}


EXPLICIT_GRAIN_KEYS: dict[str, str] = {
    "accounts": "accountId",
    "attribute_values": "id",
    "commission_history": "id",
    "einvoice_records": "id",
    "hub_inventory": "hub_inventory_id",
    "hub_returns": "order_id",
    "invoices": "id",
    "journal_entries": "journalEntryId",
    "notification_logs": "id",
    "order_items": "order_id",
    "orders": "order_id",
    "outbound_packaging": "shipment_id",
    "payment_receipts": "id",
    "payment_transactions": "id",
    "payments": "payment_id",
    "product": "product_id",
    "product_temp": "product_temp_id",
    "return_request": "order_id",
    "shipment_booking": "shipment_booking_id",
    "shipment_items": "shipment_item_id",
    "variants": "id",
    "variants_temp": "id",
    "wallet_transactions": "id",
}


SEMANTIC_GRAIN_EXCEPTIONS: tuple[str, ...] = (
    "daily_category_metrics",
    "daily_platform_metrics",
    "daily_vendor_metrics",
)


EXPECTED_DAILY_VENDOR_DUPLICATES = 6

EXPECTED_TOTAL_ROWS = 12_148
EXPECTED_TOTAL_COLUMNS = 289


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV using the standard library without modifying it."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_columns(path: Path) -> list[str]:
    """Return CSV column names without modifying the source."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def dataset_path(directory: Path, dataset_name: str) -> Path:
    return directory / f"{dataset_name}.csv"


def duplicate_complete_rows(rows):
    """
    Count all rows that belong to complete-row duplicate groups.

    This intentionally counts every row in a duplicated group, rather than
    counting only the occurrences beyond the first.

    Example:
        duplicate group A appears 2 times
        duplicate group B appears 2 times
        duplicate group C appears 2 times

    Result:
        6 rows belong to duplicate groups.

    This matches the established Phase 16-C analytical-layer contract for
    daily_vendor_metrics, where six complete-row duplicate rows are
    intentionally preserved.
    """
    counts = Counter(
        tuple(sorted(row.items()))
        for row in rows
    )

    return sum(
        count
        for count in counts.values()
        if count > 1
    )

def assert_projection(
    dataset_name: str,
    source_columns: list[str],
    analytical_columns: list[str],
) -> None:
    """Ensure the analytical schema is a source-column projection."""
    missing_from_source = [
        column
        for column in analytical_columns
        if column not in source_columns
    ]

    assert not missing_from_source, (
        f"{dataset_name}: analytical columns missing from cleaned source: "
        f"{missing_from_source}"
    )


def load_refresh_report() -> dict[str, Any]:
    assert REFRESH_REPORT.exists(), (
        f"Refresh evidence report does not exist: {REFRESH_REPORT}"
    )

    with REFRESH_REPORT.open("r", encoding="utf-8") as handle:
        report = json.load(handle)

    assert isinstance(report, dict), "Refresh report must be a JSON object."
    return report


def test_refresh_implementation_exists() -> None:
    """The Phase 16-C executable refresh implementation must exist."""
    assert REFRESH_SCRIPT.exists(), (
        f"Missing refresh implementation: {REFRESH_SCRIPT}"
    )
    assert REFRESH_SCRIPT.is_file()


def test_expected_analytical_dataset_set() -> None:
    """Exactly the 26 established analytical datasets must be present."""
    actual = sorted(
        path.stem
        for path in ANALYTICAL_DIR.glob("*.csv")
        if path.is_file()
    )

    assert actual == sorted(EXPECTED_DATASETS)


def test_all_analytical_datasets_are_readable() -> None:
    """Every established analytical CSV must be readable."""
    for dataset_name in EXPECTED_DATASETS:
        path = dataset_path(ANALYTICAL_DIR, dataset_name)

        assert path.exists(), f"Missing analytical dataset: {path}"

        columns = read_csv_columns(path)
        rows = read_csv_rows(path)

        assert columns, f"{dataset_name}: CSV has no columns."
        assert rows is not None


def test_analytical_baseline_counts() -> None:
    """
    Validate the established post-refresh physical baseline.

    Baseline:
    26 datasets
    12,148 total rows
    289 total physical columns
    """
    total_rows = 0
    total_columns = 0

    for dataset_name in EXPECTED_DATASETS:
        path = dataset_path(ANALYTICAL_DIR, dataset_name)

        columns = read_csv_columns(path)
        rows = read_csv_rows(path)

        total_columns += len(columns)
        total_rows += len(rows)

    assert total_rows == EXPECTED_TOTAL_ROWS
    assert total_columns == EXPECTED_TOTAL_COLUMNS


def test_analytical_dataset_row_counts() -> None:
    """Each analytical dataset retains its established source/output row count."""
    for dataset_name, expected_rows in EXPECTED_ROW_COUNTS.items():
        path = dataset_path(ANALYTICAL_DIR, dataset_name)
        rows = read_csv_rows(path)

        assert len(rows) == expected_rows, (
            f"{dataset_name}: expected {expected_rows} rows, "
            f"found {len(rows)}"
        )


def test_analytical_column_counts() -> None:
    """Each analytical dataset retains its established physical schema width."""
    for dataset_name, expected_columns in EXPECTED_ANALYTICAL_COLUMN_COUNTS.items():
        path = dataset_path(ANALYTICAL_DIR, dataset_name)
        columns = read_csv_columns(path)

        assert len(columns) == expected_columns, (
            f"{dataset_name}: expected {expected_columns} columns, "
            f"found {len(columns)}"
        )


def test_analytical_columns_are_cleaned_source_projections() -> None:
    """
    Every analytical column must originate in its corresponding cleaned source.

    This protects the Phase 16-C source-only projection boundary.
    """
    for dataset_name in EXPECTED_DATASETS:
        source_path = dataset_path(CLEANED_DIR, dataset_name)
        analytical_path = dataset_path(ANALYTICAL_DIR, dataset_name)

        source_columns = read_csv_columns(source_path)
        analytical_columns = read_csv_columns(analytical_path)

        assert_projection(
            dataset_name,
            source_columns,
            analytical_columns,
        )


def test_explicit_source_grain_keys_exist_and_are_unique() -> None:
    """
    Validate the 23 explicit source grain contracts.

    The grain is checked against the cleaned source, matching the
    Phase 16-C architecture. Analytical projections are not required
    to retain the grain key because the historical analytical schema
    intentionally excludes several source identifiers.
    """
    for dataset_name, grain_key in EXPLICIT_GRAIN_KEYS.items():
        source_path = dataset_path(CLEANED_DIR, dataset_name)
        source_columns = read_csv_columns(source_path)
        source_rows = read_csv_rows(source_path)

        assert grain_key in source_columns, (
            f"{dataset_name}: grain key {grain_key!r} "
            "is absent from cleaned source."
        )

        values = [row.get(grain_key, "") for row in source_rows]

        null_or_blank_count = sum(
            1 for value in values if value is None or str(value).strip() == ""
        )

        assert null_or_blank_count == 0, (
            f"{dataset_name}: grain key {grain_key!r} has "
            f"{null_or_blank_count} null/blank values."
        )

        assert len(values) == len(set(values)), (
            f"{dataset_name}: grain key {grain_key!r} "
            "contains duplicate values."
        )


def test_semantic_grain_exceptions_remain_explicit() -> None:
    """
    The three historically documented semantic-grain datasets must remain
    explicit exceptions rather than being assigned invented replacement keys.
    """
    assert set(SEMANTIC_GRAIN_EXCEPTIONS) == {
        "daily_category_metrics",
        "daily_platform_metrics",
        "daily_vendor_metrics",
    }

    for dataset_name in SEMANTIC_GRAIN_EXCEPTIONS:
        source_path = dataset_path(CLEANED_DIR, dataset_name)
        analytical_path = dataset_path(ANALYTICAL_DIR, dataset_name)

        assert source_path.exists()
        assert analytical_path.exists()


def test_daily_vendor_duplicate_behavior_is_preserved() -> None:
    """
    The six complete-row duplicates in daily_vendor_metrics are intentional
    historical behavior and must not be silently deduplicated.
    """
    analytical_path = dataset_path(
        ANALYTICAL_DIR,
        "daily_vendor_metrics",
    )

    rows = read_csv_rows(analytical_path)

    assert duplicate_complete_rows(rows) == EXPECTED_DAILY_VENDOR_DUPLICATES


def test_refresh_evidence_reports_success() -> None:
    """The latest controlled refresh evidence must report PASS."""
    report = load_refresh_report()

    assert report.get("phase") == "16-C"
    assert report.get("operation") == "controlled_analytical_refresh"
    assert report.get("status") == "PASS"
    assert report.get("dataset_count_expected") == 26

    datasets = report.get("datasets")
    assert isinstance(datasets, list)
    assert len(datasets) == 26

    publication = report.get("publication")
    assert isinstance(publication, dict)
    assert publication.get("attempted") is True
    assert publication.get("status") == "PASS"

    # A null failure value is the success representation.
    assert report.get("failure") is None


def test_refresh_evidence_contains_no_failed_dataset() -> None:
    """
    Validate structured refresh evidence instead of searching raw JSON for
    the word 'FAILURE'. The property name 'failure' is valid even when null.
    """
    report = load_refresh_report()

    for dataset_result in report["datasets"]:
        assert isinstance(dataset_result, dict), (
            "Each dataset refresh result must be a JSON object."
        )

        status = str(dataset_result.get("status", "")).upper()

        assert status == "PASS", (
            f"Dataset refresh evidence contains non-PASS status: "
            f"{dataset_result}"
        )


def test_validate_contracts_command_is_read_only_and_passes() -> None:
    """
    Execute the implementation's read-only contract validation.

    This intentionally uses --validate-contracts rather than --refresh.
    The test therefore does not publish or mutate the analytical layer.
    """
    completed = subprocess.run(
        [
            sys.executable,
            str(REFRESH_SCRIPT),
            "--validate-contracts",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    combined_output = (
        completed.stdout
        + "\n"
        + completed.stderr
    )

    assert completed.returncode == 0, (
        "Refresh contract validation failed.\n"
        f"Return code: {completed.returncode}\n"
        f"Output:\n{combined_output}"
    )

    assert "CONTRACT VALIDATION RESULT: 26/26 PASS" in combined_output, (
        "Expected 26/26 contract-validation PASS result was not found.\n"
        f"Output:\n{combined_output}"
    )


def test_source_and_analytical_row_counts_match() -> None:
    """
    Source-to-analytical row preservation is mandatory for the current
    source-only analytical construction boundary.
    """
    for dataset_name in EXPECTED_DATASETS:
        source_path = dataset_path(CLEANED_DIR, dataset_name)
        analytical_path = dataset_path(ANALYTICAL_DIR, dataset_name)

        source_rows = read_csv_rows(source_path)
        analytical_rows = read_csv_rows(analytical_path)

        assert len(source_rows) == len(analytical_rows), (
            f"{dataset_name}: source rows={len(source_rows)}, "
            f"analytical rows={len(analytical_rows)}"
        )