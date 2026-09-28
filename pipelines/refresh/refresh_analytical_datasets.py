"""
PurjeStore — Controlled Analytical Dataset Refresh
===================================================

Phase 16-C implementation.

Purpose
-------
Refresh the existing 26 validated analytical datasets from the cleaned
source layer without changing their established analytical schemas.

Authoritative architecture
--------------------------
    data/cleaned
        |
        v
    source validation
        |
        +--> physical source-grain validation
        |
        v
    controlled analytical projection
        |
        v
    analytical-output validation
        |
        v
    staging
        |
        v
    read-back validation
        |
        v
    controlled publication
        |
        v
    data/processed/analytical

Important contract distinction
------------------------------
The physical source grain and analytical output schema are separate
contracts.

The source grain key is validated against the cleaned source, but it
is NOT automatically required to exist in the analytical projection.

The 26 current analytical CSV schemas are the preserved analytical
projection baseline established by the completed analytical milestones.

This implementation intentionally does NOT:
    - perform joins
    - aggregate
    - deduplicate
    - invent analytical grains
    - add source identifiers to analytical outputs
    - create KPIs
    - perform ML
    - mutate cleaned source data
    - publish partial refreshes

Failure safety
--------------
A refresh is published only after every dataset passes validation.

If publication fails, the previous analytical state is restored from
the controlled backup created during publication.

CLI
---
    python refresh_analytical_datasets.py --validate-contracts

    python refresh_analytical_datasets.py --refresh
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


import pandas as pd


# =================================================================================================
# 1. PROJECT PATHS
# =================================================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DIR = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
)

ANALYTICAL_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytical"
)

REFRESH_EVIDENCE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "refresh"
)

STAGING_ROOT = (
    REFRESH_EVIDENCE_DIR
    / "staging"
)


# =================================================================================================
# 2. AUTHORITATIVE DATASET CONTRACT REGISTRY
# =================================================================================================
#
# expected_field_count
# --------------------
# This is the established ANALYTICAL OUTPUT field count.
#
# It is deliberately NOT compared with the complete cleaned-source
# field count.
#
# grain_key
# ---------
# This is the established PHYSICAL SOURCE-GRAIN key.
#
# It is validated against the cleaned source independently.
#
# semantic_grain_exception
# -------------------------
# Preserves the three previously established source-record-grain
# semantic exceptions.
#
# expected_duplicate_rows
# -----------------------
# Preserves the validated analytical complete-row duplicate behavior
# from the 5.3-C construction/persistence evidence.
#
# 25 datasets -> 0 duplicate complete rows
# daily_vendor_metrics -> 6 intentionally preserved duplicate rows
#
# =================================================================================================


@dataclass(frozen=True)
class DatasetContract:
    name: str
    expected_field_count: int
    grain_key: Optional[str]
    semantic_grain_exception: bool = False
    expected_duplicate_rows: int = 0


DATASET_CONTRACT_SPECS = (
    ("accounts", 9, "accountId", False, 0),
    ("attribute_values", 4, "id", False, 0),
    ("commission_history", 8, "id", False, 0),
    ("daily_category_metrics", 7, None, True, 0),
    ("daily_platform_metrics", 9, None, True, 0),
    ("daily_vendor_metrics", 11, None, True, 6),
    ("einvoice_records", 12, "id", False, 0),
    ("hub_inventory", 5, "hub_inventory_id", False, 0),
    ("hub_returns", 10, "order_id", False, 0),
    ("invoices", 15, "id", False, 0),
    ("journal_entries", 12, "journalEntryId", False, 0),
    ("notification_logs", 11, "id", False, 0),
    ("order_items", 11, "order_id", False, 0),
    ("orders", 14, "order_id", False, 0),
    ("outbound_packaging", 13, "shipment_id", False, 0),
    ("payment_receipts", 12, "id", False, 0),
    ("payment_transactions", 10, "id", False, 0),
    ("payments", 11, "payment_id", False, 0),
    ("product", 18, "product_id", False, 0),
    ("product_temp", 16, "product_temp_id", False, 0),
    ("return_request", 13, "order_id", False, 0),
    ("shipment_booking", 20, "shipment_booking_id", False, 0),
    ("shipment_items", 4, "shipment_item_id", False, 0),
    ("variants", 14, "id", False, 0),
    ("variants_temp", 13, "id", False, 0),
    ("wallet_transactions", 7, "id", False, 0),
)

CONTRACTS = tuple(
    DatasetContract(
        name=name,
        expected_field_count=field_count,
        grain_key=grain_key,
        semantic_grain_exception=semantic_exception,
        expected_duplicate_rows=expected_duplicate_rows,
    )
    for (
        name,
        field_count,
        grain_key,
        semantic_exception,
        expected_duplicate_rows,
    ) in DATASET_CONTRACT_SPECS
)


# =================================================================================================
# 3. RESULT MODEL
# =================================================================================================


@dataclass
class DatasetRefreshResult:
    dataset: str
    source_path: str
    analytical_path: str
    source_rows: int
    output_rows: int
    source_fields: int
    output_fields: int
    source_grain_key: Optional[str]
    source_grain_nulls: Optional[int]
    source_grain_duplicate_values: Optional[int]
    source_grain_unique_non_null: Optional[bool]
    expected_duplicate_rows: int
    actual_duplicate_rows: int
    status: str
    error: Optional[str] = None


# =================================================================================================
# 4. BASIC HELPERS
# =================================================================================================


def utc_timestamp() -> str:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def source_path_for(contract: DatasetContract) -> Path:
    """Return the cleaned source path for a dataset."""
    return CLEANED_DIR / f"{contract.name}.csv"


def final_path_for(contract: DatasetContract) -> Path:
    """Return the controlled analytical output path."""
    return ANALYTICAL_DIR / f"{contract.name}.csv"


def read_csv(path: Path) -> pd.DataFrame:
    """
    Read a CSV using the same general behavior as the validated
    analytical construction process.
    """
    return pd.read_csv(
        path,
        low_memory=False,
    )


def read_csv_columns(path: Path) -> list[str]:
    """Read only a CSV header."""
    return [
        str(column)
        for column in pd.read_csv(
            path,
            nrows=0,
        ).columns
    ]


def count_complete_row_duplicates(df: pd.DataFrame) -> int:
    """
    Count all rows belonging to a complete-row duplicate group.

    Example:
        A,A,B,B,C -> duplicate-row count = 4

    This matches pandas duplicated(keep=False) semantics.
    """
    if df.empty:
        return 0

    return int(
        df.duplicated(
            keep=False
        ).sum()
    )


def normalized_column_list(columns) -> list[str]:
    """Normalize column labels for deterministic comparison."""
    return [
        str(column).strip()
        for column in columns
    ]


# =================================================================================================
# 5. CONTRACT REGISTRY VALIDATION
# =================================================================================================


def validate_contract_registry() -> None:
    """
    Validate the internal 26-dataset contract registry.

    This checks only contract structure.
    It does not modify any file.
    """

    if len(CONTRACTS) != 26:
        raise ValueError(
            f"Expected 26 dataset contracts, found {len(CONTRACTS)}."
        )

    names = [
        contract.name
        for contract in CONTRACTS
    ]

    if len(set(names)) != len(names):
        raise ValueError(
            "Duplicate dataset names detected in contract registry."
        )

    for contract in CONTRACTS:

        if not contract.name.strip():
            raise ValueError(
                "Contract contains a blank dataset name."
            )

        if contract.expected_field_count <= 0:
            raise ValueError(
                f"{contract.name}: invalid expected analytical "
                f"field count {contract.expected_field_count}."
            )

        if contract.grain_key is not None:
            if not str(contract.grain_key).strip():
                raise ValueError(
                    f"{contract.name}: blank grain key must be represented "
                    "as None."
                )

        if contract.expected_duplicate_rows < 0:
            raise ValueError(
                f"{contract.name}: negative duplicate expectation."
            )

    semantic_exception_count = sum(
        contract.semantic_grain_exception
        for contract in CONTRACTS
    )

    if semantic_exception_count != 3:
        raise ValueError(
            "Expected exactly 3 semantic-grain exceptions, found "
            f"{semantic_exception_count}."
        )

    explicit_grain_count = sum(
        contract.grain_key is not None
        for contract in CONTRACTS
    )

    if explicit_grain_count != 23:
        raise ValueError(
            "Expected exactly 23 explicit source grain keys, found "
            f"{explicit_grain_count}."
        )

    duplicate_exception_count = sum(
        contract.expected_duplicate_rows > 0
        for contract in CONTRACTS
    )

    if duplicate_exception_count != 1:
        raise ValueError(
            "Expected exactly one dataset with a non-zero expected "
            "complete-row duplicate count."
        )

    vendor_contract = next(
        contract
        for contract in CONTRACTS
        if contract.name == "daily_vendor_metrics"
    )

    if vendor_contract.expected_duplicate_rows != 6:
        raise ValueError(
            "daily_vendor_metrics must preserve the validated expectation "
            "of 6 complete-row duplicate rows."
        )


# =================================================================================================
# 6. PROJECTION SCHEMA DISCOVERY
# =================================================================================================
#
# The existing analytical CSVs are the preserved physical baseline.
#
# Their current headers represent the approved analytical projection
# schema that must be reproduced by refresh.
#
# This avoids inventing or reconstructing 289 field names from memory.
#
# The implementation requires the existing validated analytical outputs
# to be present as the schema authority for the current refresh contract.
#
# A refresh therefore cannot silently create a new analytical schema.
#
# =================================================================================================


def projection_columns_for(contract: DatasetContract) -> list[str]:
    """
    Return the preserved analytical projection columns for a dataset.

    The current analytical CSV is the physical baseline produced by the
    already-closed analytical construction milestone.

    The function intentionally does not infer a projection from source
    fields, names, data types, uniqueness, or business semantics.
    """

    analytical_path = final_path_for(contract)

    if not analytical_path.exists():
        raise FileNotFoundError(
            f"{contract.name}: preserved analytical baseline is missing:\n"
            f"{analytical_path}"
        )

    columns = read_csv_columns(
        analytical_path
    )

    columns = normalized_column_list(
        columns
    )

    if not columns:
        raise ValueError(
            f"{contract.name}: analytical baseline contains no columns."
        )

    if len(columns) != contract.expected_field_count:
        raise ValueError(
            f"{contract.name}: analytical baseline contains "
            f"{len(columns)} fields, but the validated contract expects "
            f"{contract.expected_field_count}."
        )

    if len(columns) != len(set(columns)):
        raise ValueError(
            f"{contract.name}: analytical baseline contains duplicate "
            "column names."
        )

    return columns


# =================================================================================================
# 7. SOURCE DISCOVERY
# =================================================================================================


def discover_sources() -> list[tuple[DatasetContract, Path]]:
    """
    Discover all 26 expected cleaned sources.
    """

    discovered = []

    for contract in CONTRACTS:

        path = source_path_for(
            contract
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Missing cleaned source for {contract.name}:\n{path}"
            )

        discovered.append(
            (
                contract,
                path,
            )
        )

    if len(discovered) != 26:
        raise ValueError(
            f"Expected 26 source datasets, found {len(discovered)}."
        )

    return discovered


# =================================================================================================
# 8. SOURCE SCHEMA VALIDATION
# =================================================================================================


def validate_source_schema(
    contract: DatasetContract,
    df: pd.DataFrame,
) -> None:
    """
    Validate the cleaned source against the analytical projection contract.

    IMPORTANT:
    The source field count is NOT required to equal the analytical field
    count.

    The source is allowed to contain additional physical fields.

    Required condition:
        approved analytical projection columns ⊆ source columns
    """

    source_columns = normalized_column_list(
        df.columns
    )

    if len(source_columns) != len(set(source_columns)):
        raise ValueError(
            f"{contract.name}: cleaned source contains duplicate "
            "column names."
        )

    projection_columns = projection_columns_for(
        contract
    )

    missing_projection_columns = [
        column
        for column in projection_columns
        if column not in source_columns
    ]

    if missing_projection_columns:
        raise ValueError(
            f"{contract.name}: analytical projection columns missing "
            f"from cleaned source: "
            f"{missing_projection_columns}"
        )

    if contract.grain_key is not None:

        if contract.grain_key not in source_columns:
            raise ValueError(
                f"{contract.name}: physical source grain key "
                f"'{contract.grain_key}' is absent from cleaned source."
            )

    if contract.grain_key is None:

        if not contract.semantic_grain_exception:
            raise ValueError(
                f"{contract.name}: no grain key is defined and the "
                "contract is not marked as a semantic-grain exception."
            )


# =================================================================================================
# 9. SOURCE-GRAIN VALIDATION
# =================================================================================================


def validate_grain(
    contract: DatasetContract,
    df: pd.DataFrame,
) -> tuple[Optional[int], Optional[int], bool]:
    """
    Validate the physical source grain.

    Returns:
        (
            null_count,
            duplicate_value_count,
            unique_non_null
        )

    The grain key is validated ONLY against the cleaned source.

    It is not required to survive into the analytical projection.
    """

    if contract.grain_key is None:

        if not contract.semantic_grain_exception:
            raise ValueError(
                f"{contract.name}: missing grain key without "
                "semantic-grain exception."
            )

        return (
            None,
            None,
            False,
        )

    grain_key = contract.grain_key

    if grain_key not in df.columns:
        raise ValueError(
            f"{contract.name}: source grain key '{grain_key}' "
            "is absent from source."
        )

    series = df[grain_key]

    null_count = int(
        series.isna().sum()
    )

    non_null = series.dropna()

    if non_null.empty:
        raise ValueError(
            f"{contract.name}: source grain key '{grain_key}' "
            "contains no populated values."
        )

    value_duplicate_count = int(
        non_null.duplicated(
            keep=False
        ).sum()
    )

    unique_non_null = (
        non_null.nunique(
            dropna=True
        )
        == len(non_null)
    )

    if null_count != 0:
        raise ValueError(
            f"{contract.name}: source grain key '{grain_key}' "
            f"contains {null_count} null values."
        )

    if value_duplicate_count != 0:
        raise ValueError(
            f"{contract.name}: source grain key '{grain_key}' "
            f"contains {value_duplicate_count} rows participating "
            "in duplicate grain values."
        )

    if not unique_non_null:
        raise ValueError(
            f"{contract.name}: source grain key '{grain_key}' "
            "is not unique among non-null values."
        )

    return (
        null_count,
        value_duplicate_count,
        bool(unique_non_null),
    )


# =================================================================================================
# 10. SOURCE-ONLY ANALYTICAL CONSTRUCTION
# =================================================================================================


def construct_source_only(
    contract: DatasetContract,
    source_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construct the analytical dataset as a controlled projection of the
    cleaned source.

    No joins.
    No aggregation.
    No deduplication.
    No identifier reintroduction.
    No invented grain.
    """

    projection_columns = projection_columns_for(
        contract
    )

    missing_columns = [
        column
        for column in projection_columns
        if column not in source_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{contract.name}: cannot construct projection because "
            f"columns are missing from source: {missing_columns}"
        )

    output_df = source_df.loc[
        :,
        projection_columns,
    ].copy()

    return output_df


# =================================================================================================
# 11. DATAFRAME VALUE COMPARISON
# =================================================================================================


def assert_projection_values_equal(
    contract: DatasetContract,
    source_df: pd.DataFrame,
    analytical_df: pd.DataFrame,
) -> None:
    """
    Verify that the analytical projection contains exactly the values
    currently present in the cleaned source for the approved projection
    columns.

    This protects against:
        - sorting
        - filtering
        - transformation
        - coercion that changes values
        - row loss
        - row duplication
        - accidental calculation
    """

    projection_columns = projection_columns_for(
        contract
    )

    expected_df = source_df.loc[
        :,
        projection_columns,
    ].reset_index(
        drop=True
    )

    actual_df = analytical_df.loc[
        :,
        projection_columns,
    ].reset_index(
        drop=True
    )

    if expected_df.shape != actual_df.shape:
        raise ValueError(
            f"{contract.name}: projection shape mismatch. "
            f"Expected {expected_df.shape}, "
            f"found {actual_df.shape}."
        )

    try:

        pd.testing.assert_frame_equal(
            expected_df,
            actual_df,
            check_dtype=False,
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )

    except AssertionError as exc:

        raise ValueError(
            f"{contract.name}: analytical baseline values do not exactly "
            "match the current cleaned-source projection."
        ) from exc


# =================================================================================================
# 12. CONSTRUCTED OUTPUT VALIDATION
# =================================================================================================


def validate_constructed_output(
    contract: DatasetContract,
    source_df: pd.DataFrame,
    output_df: pd.DataFrame,
) -> dict:
    """
    Validate the newly constructed analytical projection before staging.
    """

    projection_columns = projection_columns_for(
        contract
    )

    source_rows = int(
        source_df.shape[0]
    )

    output_rows = int(
        output_df.shape[0]
    )

    if source_rows != output_rows:
        raise ValueError(
            f"{contract.name}: row count changed. "
            f"Source={source_rows}, output={output_rows}."
        )

    actual_columns = normalized_column_list(
        output_df.columns
    )

    if actual_columns != projection_columns:
        raise ValueError(
            f"{contract.name}: analytical output schema/order does not "
            "match the preserved analytical baseline."
        )

    if len(actual_columns) != contract.expected_field_count:
        raise ValueError(
            f"{contract.name}: output contains "
            f"{len(actual_columns)} fields; expected "
            f"{contract.expected_field_count}."
        )

    if len(actual_columns) != len(set(actual_columns)):
        raise ValueError(
            f"{contract.name}: output contains duplicate column names."
        )

    actual_duplicate_rows = count_complete_row_duplicates(
        output_df
    )

    if actual_duplicate_rows != contract.expected_duplicate_rows:
        raise ValueError(
            f"{contract.name}: complete-row duplicate behavior changed. "
            f"Expected {contract.expected_duplicate_rows}, "
            f"found {actual_duplicate_rows}."
        )

    assert_projection_values_equal(
        contract,
        source_df,
        output_df,
    )

    return {
        "dataset": contract.name,
        "source_rows": source_rows,
        "output_rows": output_rows,
        "source_fields": int(source_df.shape[1]),
        "output_fields": int(output_df.shape[1]),
        "expected_duplicate_rows":
            contract.expected_duplicate_rows,
        "actual_duplicate_rows":
            actual_duplicate_rows,
        "projection_columns":
            projection_columns,
    }


# =================================================================================================
# 13. STAGING
# =================================================================================================


def create_staging_directory() -> Path:
    """
    Create a unique staging directory under the controlled refresh
    evidence area.
    """

    REFRESH_EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    STAGING_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    staging_dir = Path(
        tempfile.mkdtemp(
            prefix="refresh_",
            dir=str(STAGING_ROOT),
        )
    )

    return staging_dir


# =================================================================================================
# 14. STAGED OUTPUT WRITING
# =================================================================================================


def write_staged_output(
    contract: DatasetContract,
    output_df: pd.DataFrame,
    staging_dir: Path,
) -> Path:
    """
    Write one validated output to staging.
    """

    staged_path = (
        staging_dir
        / f"{contract.name}.csv"
    )

    output_df.to_csv(
        staged_path,
        index=False,
    )

    if not staged_path.exists():
        raise IOError(
            f"{contract.name}: staged output was not created."
        )

    return staged_path


# =================================================================================================
# 15. READ-BACK VALIDATION
# =================================================================================================


def validate_read_back(
    contract: DatasetContract,
    staged_path: Path,
    expected_df: pd.DataFrame,
) -> bool:
    """
    Re-read the staged CSV and verify that it matches the expected
    analytical output.
    """

    if not staged_path.exists():
        raise FileNotFoundError(
            f"{contract.name}: staged file missing:\n{staged_path}"
        )

    read_back_df = read_csv(
        staged_path
    )

    expected_columns = projection_columns_for(
        contract
    )

    actual_columns = normalized_column_list(
        read_back_df.columns
    )

    if actual_columns != expected_columns:
        raise ValueError(
            f"{contract.name}: staged read-back schema mismatch."
        )

    if len(read_back_df) != len(expected_df):
        raise ValueError(
            f"{contract.name}: staged read-back row count mismatch. "
            f"Expected {len(expected_df)}, "
            f"found {len(read_back_df)}."
        )

    actual_duplicate_rows = count_complete_row_duplicates(
        read_back_df
    )

    if actual_duplicate_rows != contract.expected_duplicate_rows:
        raise ValueError(
            f"{contract.name}: staged read-back duplicate behavior "
            "does not match the contract."
        )

    try:

        pd.testing.assert_frame_equal(
            expected_df.reset_index(drop=True),
            read_back_df.reset_index(drop=True),
            check_dtype=False,
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )

    except AssertionError as exc:

        raise ValueError(
            f"{contract.name}: staged read-back values differ from "
            "the expected analytical output."
        ) from exc

    return True


# =================================================================================================
# 16. CONTROLLED PUBLICATION
# =================================================================================================


def publish_staged_outputs(
    staging_dir: Path,
    successful_contracts: list[DatasetContract],
) -> None:
    """
    Publish the complete validated staging set.

    A backup of the current analytical state is created first.

    If any publication step fails, the previous analytical state is
    restored.
    """

    ANALYTICAL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup_dir = Path(
        tempfile.mkdtemp(
            prefix="analytical_backup_",
            dir=str(REFRESH_EVIDENCE_DIR),
        )
    )

    existing_files = {}

    try:

        # -----------------------------------------------------------------------------------------
        # 16.1 Backup current analytical state
        # -----------------------------------------------------------------------------------------

        for contract in successful_contracts:

            final_path = final_path_for(
                contract
            )

            backup_path = (
                backup_dir
                / final_path.name
            )

            if final_path.exists():

                shutil.copy2(
                    final_path,
                    backup_path,
                )

                existing_files[
                    final_path.name
                ] = True

            else:

                existing_files[
                    final_path.name
                ] = False

        # -----------------------------------------------------------------------------------------
        # 16.2 Publish every validated staged file
        # -----------------------------------------------------------------------------------------

        for contract in successful_contracts:

            staged_path = (
                staging_dir
                / f"{contract.name}.csv"
            )

            final_path = final_path_for(
                contract
            )

            if not staged_path.exists():
                raise FileNotFoundError(
                    f"Missing staged output for {contract.name}."
                )

            os.replace(
                staged_path,
                final_path,
            )

        # -----------------------------------------------------------------------------------------
        # 16.3 Verify published files
        # -----------------------------------------------------------------------------------------

        for contract in successful_contracts:

            final_path = final_path_for(
                contract
            )

            if not final_path.exists():
                raise FileNotFoundError(
                    f"Published output missing for {contract.name}."
                )

    except Exception:

        # -----------------------------------------------------------------------------------------
        # 16.4 Restore previous valid state
        # -----------------------------------------------------------------------------------------

        for contract in successful_contracts:

            final_path = final_path_for(
                contract
            )

            backup_path = (
                backup_dir
                / final_path.name
            )

            had_previous_file = existing_files.get(
                final_path.name,
                False,
            )

            try:

                if backup_path.exists():

                    shutil.copy2(
                        backup_path,
                        final_path,
                    )

                elif not had_previous_file and final_path.exists():

                    final_path.unlink()

            except Exception:
                # Preserve the original publication exception.
                pass

        raise

    finally:

        shutil.rmtree(
            backup_dir,
            ignore_errors=True,
        )


# =================================================================================================
# 17. REFRESH EVIDENCE
# =================================================================================================


def write_refresh_report(
    report: dict,
) -> Path:
    """
    Write the refresh report only after refresh processing has completed.
    """

    REFRESH_EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        REFRESH_EVIDENCE_DIR
        / "latest_refresh_report.json"
    )

    with report_path.open(
        "w",
        encoding="utf-8",
    ) as handle:

        json.dump(
            report,
            handle,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    return report_path


# =================================================================================================
# 18. REFRESH EXECUTION
# =================================================================================================


def refresh_all() -> dict:
    """
    Execute the complete controlled refresh.

    Nothing is published until every dataset has:
        - source schema validation
        - source-grain validation
        - source-only projection
        - analytical output validation
        - staging write
        - staging read-back validation
    """

    validate_contract_registry()

    started_at = utc_timestamp()

    report = {
        "phase": "16-C",
        "operation": "controlled_analytical_refresh",
        "started_at_utc": started_at,
        "status": "RUNNING",
        "dataset_count_expected": 26,
        "datasets": [],
        "publication": {
            "attempted": False,
            "status": "NOT_ATTEMPTED",
        },
        "failure": None,
    }

    staging_dir = None

    successful_contracts = []

    try:

        # -----------------------------------------------------------------------------------------
        # 18.1 Discover sources
        # -----------------------------------------------------------------------------------------

        discovered = discover_sources()

        if len(discovered) != 26:
            raise ValueError(
                f"Expected 26 discovered datasets, found {len(discovered)}."
            )

        # -----------------------------------------------------------------------------------------
        # 18.2 Create staging
        # -----------------------------------------------------------------------------------------

        staging_dir = create_staging_directory()

        # -----------------------------------------------------------------------------------------
        # 18.3 Validate and construct every dataset
        # -----------------------------------------------------------------------------------------

        for index, (contract, source_path) in enumerate(
            discovered,
            start=1,
        ):

            print(
                f"[{index:02d}/26] {contract.name}"
            )

            try:

                # -------------------------------------------------------------------------------
                # Read source
                # -------------------------------------------------------------------------------

                source_df = read_csv(
                    source_path
                )

                # -------------------------------------------------------------------------------
                # Source schema
                # -------------------------------------------------------------------------------

                validate_source_schema(
                    contract,
                    source_df,
                )

                # -------------------------------------------------------------------------------
                # Source physical grain
                # -------------------------------------------------------------------------------

                (
                    source_grain_nulls,
                    source_grain_duplicate_values,
                    source_grain_unique_non_null,
                ) = validate_grain(
                    contract,
                    source_df,
                )

                # -------------------------------------------------------------------------------
                # Controlled projection
                # -------------------------------------------------------------------------------

                output_df = construct_source_only(
                    contract,
                    source_df,
                )

                # -------------------------------------------------------------------------------
                # Output validation
                # -------------------------------------------------------------------------------

                validation = validate_constructed_output(
                    contract,
                    source_df,
                    output_df,
                )

                # -------------------------------------------------------------------------------
                # Stage
                # -------------------------------------------------------------------------------

                staged_path = write_staged_output(
                    contract,
                    output_df,
                    staging_dir,
                )

                # -------------------------------------------------------------------------------
                # Read-back
                # -------------------------------------------------------------------------------

                validate_read_back(
                    contract,
                    staged_path,
                    output_df,
                )

                successful_contracts.append(
                    contract
                )

                result = DatasetRefreshResult(
                    dataset=contract.name,
                    source_path=str(source_path),
                    analytical_path=str(
                        final_path_for(contract)
                    ),
                    source_rows=int(
                        source_df.shape[0]
                    ),
                    output_rows=int(
                        output_df.shape[0]
                    ),
                    source_fields=int(
                        source_df.shape[1]
                    ),
                    output_fields=int(
                        output_df.shape[1]
                    ),
                    source_grain_key=contract.grain_key,
                    source_grain_nulls=source_grain_nulls,
                    source_grain_duplicate_values=
                        source_grain_duplicate_values,
                    source_grain_unique_non_null=
                        source_grain_unique_non_null,
                    expected_duplicate_rows=
                        contract.expected_duplicate_rows,
                    actual_duplicate_rows=
                        validation[
                            "actual_duplicate_rows"
                        ],
                    status="PASS",
                    error=None,
                )

                report["datasets"].append(
                    asdict(result)
                )

                print(
                    "    [PASS] source schema"
                )

                print(
                    "    [PASS] source grain"
                )

                print(
                    "    [PASS] source-only analytical projection"
                )

                print(
                    "    [PASS] analytical output validation"
                )

                print(
                    "    [PASS] staging"
                )

                print(
                    "    [PASS] read-back"
                )

            except Exception as exc:

                result = DatasetRefreshResult(
                    dataset=contract.name,
                    source_path=str(source_path),
                    analytical_path=str(
                        final_path_for(contract)
                    ),
                    source_rows=0,
                    output_rows=0,
                    source_fields=0,
                    output_fields=0,
                    source_grain_key=contract.grain_key,
                    source_grain_nulls=None,
                    source_grain_duplicate_values=None,
                    source_grain_unique_non_null=None,
                    expected_duplicate_rows=
                        contract.expected_duplicate_rows,
                    actual_duplicate_rows=0,
                    status="FAIL",
                    error=str(exc),
                )

                report["datasets"].append(
                    asdict(result)
                )

                raise RuntimeError(
                    f"{contract.name}: refresh validation failed: {exc}"
                ) from exc

        # -----------------------------------------------------------------------------------------
        # 18.4 Publication gate
        # -----------------------------------------------------------------------------------------

        if len(successful_contracts) != 26:
            raise RuntimeError(
                "Publication gate failed: "
                f"{len(successful_contracts)}/26 datasets passed."
            )

        report["publication"]["attempted"] = True

        # -----------------------------------------------------------------------------------------
        # 18.5 Controlled publication
        # -----------------------------------------------------------------------------------------

        publish_staged_outputs(
            staging_dir,
            successful_contracts,
        )

        report["publication"]["status"] = "PASS"

        report["status"] = "PASS"

        # -----------------------------------------------------------------------------------------
        # 18.6 Final publication verification
        # -----------------------------------------------------------------------------------------

        for contract in successful_contracts:

            final_path = final_path_for(
                contract
            )

            if not final_path.exists():
                raise RuntimeError(
                    f"{contract.name}: final analytical output missing "
                    "after publication."
                )

            published_df = read_csv(
                final_path
            )

            projection_columns = projection_columns_for(
                contract
            )

            if normalized_column_list(
                published_df.columns
            ) != projection_columns:
                raise RuntimeError(
                    f"{contract.name}: published schema differs from "
                    "validated projection schema."
                )

        report["finished_at_utc"] = utc_timestamp()

        report_path = write_refresh_report(
            report
        )

        report["report_path"] = str(
            report_path
        )

        # Write the report one final time so report_path itself is included.
        report_path = write_refresh_report(
            report
        )

        print_summary(
            report
        )

        return report

    except Exception as exc:

        report["status"] = "FAIL"

        report["failure"] = {
            "error": str(exc),
        }

        report["finished_at_utc"] = utc_timestamp()

        # Failure evidence is intentionally written because the failure
        # itself is an important refresh-control result.
        try:
            report_path = write_refresh_report(
                report
            )

            report["report_path"] = str(
                report_path
            )

        except Exception:
            pass

        # Remove any remaining staging files.
        if staging_dir is not None:

            shutil.rmtree(
                staging_dir,
                ignore_errors=True,
            )

        print_summary(
            report
        )

        raise

    finally:

        if staging_dir is not None:

            shutil.rmtree(
                staging_dir,
                ignore_errors=True,
            )


# =================================================================================================
# 19. SUMMARY
# =================================================================================================


def print_summary(
    report: dict,
) -> None:
    """Print a concise structured refresh summary."""

    print()
    print("=" * 100)
    print("PURJESTORE PHASE 16-C REFRESH SUMMARY")
    print("=" * 100)

    print(
        f"Status              : {report.get('status')}"
    )

    print(
        f"Datasets expected   : {report.get('dataset_count_expected')}"
    )

    dataset_records = report.get(
        "datasets",
        [],
    )

    passed = sum(
        record.get("status") == "PASS"
        for record in dataset_records
    )

    failed = sum(
        record.get("status") == "FAIL"
        for record in dataset_records
    )

    print(
        f"Datasets passed     : {passed}"
    )

    print(
        f"Datasets failed     : {failed}"
    )

    publication = report.get(
        "publication",
        {},
    )

    print(
        f"Publication attempted: "
        f"{publication.get('attempted')}"
    )

    print(
        f"Publication status  : "
        f"{publication.get('status')}"
    )

    if report.get("failure"):

        print(
            f"Failure             : "
            f"{report['failure'].get('error')}"
        )

    if report.get("report_path"):

        print(
            f"Evidence report     : "
            f"{report['report_path']}"
        )

    print("=" * 100)


# =================================================================================================
# 20. CONTRACT VALIDATION MODE
# =================================================================================================


def validate_contracts_only() -> int:
    """
    Read-only validation mode.

    It verifies:
        - 26 contracts
        - preserved analytical baselines
        - projection schemas
        - source availability
        - source schema compatibility
        - physical source grain
        - analytical baseline integrity

    It does NOT:
        - construct outputs
        - stage outputs
        - publish outputs
        - write refresh reports
    """

    validate_contract_registry()

    print("=" * 100)
    print("PURJESTORE PHASE 16-C — CONTRACT VALIDATION")
    print("=" * 100)

    discovered = discover_sources()

    passed = 0

    for index, (contract, source_path) in enumerate(
        discovered,
        start=1,
    ):

        print(
            f"[{index:02d}/26] {contract.name}"
        )

        source_df = read_csv(
            source_path
        )

        projection_columns = projection_columns_for(
            contract
        )

        validate_source_schema(
            contract,
            source_df,
        )

        (
            grain_nulls,
            grain_duplicates,
            grain_unique,
        ) = validate_grain(
            contract,
            source_df,
        )

        baseline_df = read_csv(
            final_path_for(contract)
        )

        # Baseline analytical schema
        if normalized_column_list(
            baseline_df.columns
        ) != projection_columns:
            raise ValueError(
                f"{contract.name}: analytical baseline schema "
                "does not match the projection contract."
            )

        # Baseline field count
        if len(baseline_df.columns) != contract.expected_field_count:
            raise ValueError(
                f"{contract.name}: analytical baseline field count "
                "does not match contract."
            )

        # Baseline row count
        if len(baseline_df) != len(source_df):
            raise ValueError(
                f"{contract.name}: analytical baseline row count "
                "does not match cleaned source."
            )

        # Baseline duplicate behavior
        actual_duplicates = count_complete_row_duplicates(
            baseline_df
        )

        if actual_duplicates != contract.expected_duplicate_rows:
            raise ValueError(
                f"{contract.name}: analytical baseline duplicate "
                f"behavior changed. Expected "
                f"{contract.expected_duplicate_rows}, "
                f"found {actual_duplicates}."
            )

        # Baseline values must still equal current source projection
        assert_projection_values_equal(
            contract,
            source_df,
            baseline_df,
        )

        print(
            f"    [PASS] source fields={len(source_df.columns)}"
        )

        print(
            f"    [PASS] analytical fields="
            f"{len(baseline_df.columns)}"
        )

        print(
            f"    [PASS] rows={len(source_df)}"
        )

        if contract.grain_key is not None:

            print(
                f"    [PASS] source grain={contract.grain_key}"
            )

            print(
                f"    [PASS] source grain nulls={grain_nulls}"
            )

            print(
                f"    [PASS] source grain duplicate rows="
                f"{grain_duplicates}"
            )

        else:

            print(
                "    [PASS] semantic-grain exception preserved"
            )

        print(
            f"    [PASS] expected complete-row duplicates="
            f"{contract.expected_duplicate_rows}"
        )

        print(
            "    [PASS] analytical projection matches "
            "current cleaned source"
        )

        passed += 1

    print()
    print("=" * 100)
    print(
        f"CONTRACT VALIDATION RESULT: "
        f"{passed}/26 PASS"
    )
    print("=" * 100)

    if passed != 26:
        return 1

    return 0


# =================================================================================================
# 21. CLI
# =================================================================================================


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "PurjeStore controlled analytical dataset refresh."
        )
    )

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        "--validate-contracts",
        action="store_true",
        help=(
            "Run read-only contract/source/baseline validation."
        ),
    )

    group.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "Execute the controlled analytical refresh."
        ),
    )

    return parser


def main() -> int:
    """CLI entry point."""

    parser = build_argument_parser()

    args = parser.parse_args()

    try:

        if args.validate_contracts:

            return validate_contracts_only()

        if args.refresh:

            refresh_all()

            return 0

        return 1

    except KeyboardInterrupt:

        print(
            "\nOperation cancelled by user."
        )

        return 130

    except Exception as exc:

        print(
            "\nPHASE 16-C ERROR:"
        )

        print(
            str(exc)
        )

        return 1


# =================================================================================================
# 22. SCRIPT ENTRY
# =================================================================================================


if __name__ == "__main__":
    raise SystemExit(
        main()
    )