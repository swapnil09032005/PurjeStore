
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PurjeStore — Controlled Dashboard Application
#
# Evidence boundaries:
#   Analytical datasets : 26
#   Analytical rows     : 12,148
#   Analytical columns  : 289
#   Approved page/field : 21
#   Approved pages      : 8
#   Final KPIs          : 0
#   Approved joins      : 0
#   Selected ML         : 0
#
# The dashboard reads the validated analytical layer only.
# It never writes to analytical CSVs.
# ============================================================


PROJECT_ROOT = Path(
    r"C:\Users\ASUS\Desktop\PurjeStore"
)

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


KNOWN_LIMITATIONS = [
    "Final KPI activation remains zero.",
    "No approved cross-dataset joins are used.",
    "ML and predictive outputs remain blocked.",
    "The analytical layer is read-only from the dashboard.",
    "Orders does not expose order_id in the approved analytical projection.",
    "Customer-related raw PII is not exposed.",
    "Deferred variants_temp fields remain blocked.",
    "Numeric dtype alone does not establish business meaning.",
]


APPROVED_MAPPING = [{'dataset': 'daily_category_metrics', 'field': 'order_count', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily category-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_category_metrics', 'field': 'units_sold', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily category-level units sold', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_platform_metrics', 'field': 'total_orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily platform-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_platform_metrics', 'field': 'total_product_views', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily platform-level product-view count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'units_sold', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level units sold', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'cancelled_orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level cancelled-order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'payment_transactions', 'field': 'status', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Payment transaction status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'payments', 'field': 'status', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Payment status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'invoices', 'field': 'quantity', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Invoice quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'order_items', 'field': 'quantity', 'page': 'P03 Orders', 'proposed_meaning': 'Order-item quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'product', 'field': 'status', 'page': 'P04 Products / Catalog', 'proposed_meaning': 'Product status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'type', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction type', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'method', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction method', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'status', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'shipment_items', 'field': 'quantity', 'page': 'P06 Fulfillment / Shipping', 'proposed_meaning': 'Shipment-item quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'hub_inventory', 'field': 'quantity', 'page': 'P06 Fulfillment / Shipping', 'proposed_meaning': 'Hub inventory quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'return_request', 'field': 'status', 'page': 'P07 Returns / Exchange', 'proposed_meaning': 'Return-request status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'hub_returns', 'field': 'quantity', 'page': 'P07 Returns / Exchange', 'proposed_meaning': 'Hub-return quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'hub_inventory', 'field': 'quantity', 'page': 'P08 Operations / Inventory', 'proposed_meaning': 'Hub inventory quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'product_views', 'page': 'P08 Operations / Inventory', 'proposed_meaning': 'Daily vendor-level product views', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}]


# ============================================================
# Existing reusable data functions
# ============================================================

@st.cache_data(show_spinner=False)
def discover_analytical_files() -> list[Path]:
    """Discover analytical CSVs without modifying the filesystem."""

    if not ANALYTICAL_ROOT.exists():
        return []

    return sorted(
        path
        for path in ANALYTICAL_ROOT.glob("*.csv")
        if path.is_file()
    )


@st.cache_data(show_spinner=False)
def load_dataset(path_string: str) -> pd.DataFrame:
    """Read one analytical CSV into memory."""

    path = Path(path_string)

    if not path.exists():
        raise FileNotFoundError(
            f"Analytical dataset not found: {path}"
        )

    if path.suffix.lower() != ".csv":
        raise ValueError(
            f"Unsupported analytical source: {path.name}"
        )

    return pd.read_csv(
        path,
        low_memory=False,
    )


@st.cache_data(show_spinner=False)
def load_refresh_report() -> dict[str, Any] | None:
    """Read the actual Phase 16-C refresh report."""

    if not REFRESH_REPORT_PATH.exists():
        return None

    try:

        with REFRESH_REPORT_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:

            report = json.load(handle)

        if not isinstance(report, dict):
            return None

        return report

    except Exception:
        return None


def is_numeric_series(
    series: pd.Series,
) -> bool:

    return pd.api.types.is_numeric_dtype(
        series
    )


def is_datetime_like_series(
    series: pd.Series,
) -> bool:

    if pd.api.types.is_datetime64_any_dtype(
        series
    ):
        return True

    name = str(
        series.name
    ).lower()

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


def safe_numeric_columns(
    df: pd.DataFrame,
) -> list[str]:

    return [
        column
        for column in df.columns
        if is_numeric_series(
            df[column]
        )
    ]


def safe_categorical_columns(
    df: pd.DataFrame,
) -> list[str]:

    result = []

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

    return [
        column
        for column in df.columns
        if is_datetime_like_series(
            df[column]
        )
    ]


def format_number(
    value: Any,
) -> str:

    if value is None:
        return "—"

    try:

        if (
            isinstance(value, float)
            and math.isnan(value)
        ):
            return "—"

        if isinstance(
            value,
            (int, float),
        ):

            return (
                f"{value:,.2f}"
                .rstrip("0")
                .rstrip(".")
            )

    except Exception:
        pass

    return str(value)


# ============================================================
# Controlled semantic access
# ============================================================

def approved_records_for_page(
    page_name: str,
) -> list[dict[str, Any]]:

    return [
        record
        for record in APPROVED_MAPPING
        if record["page"] == page_name
    ]


def descriptive_summary(
    series: pd.Series,
) -> dict[str, Any]:

    clean = series.dropna()

    return {
        "rows": int(len(series)),
        "non_null": int(clean.shape[0]),
        "missing": int(
            series.isna().sum()
        ),
        "unique": int(
            clean.nunique()
        ),
    }


def safe_display_label(
    record: dict[str, Any],
) -> str:

    meaning = str(
        record.get(
            "proposed_meaning",
            "",
        )
    ).strip()

    if meaning:
        return meaning

    return (
        str(record["field"])
        .replace("_", " ")
        .title()
    )


def render_approved_record(
    record: dict[str, Any],
    key_prefix: str,
) -> None:

    del key_prefix

    dataset = record["dataset"]
    field = record["field"]

    dataset_path = (
        ANALYTICAL_ROOT
        / f"{dataset}.csv"
    )

    if not dataset_path.exists():

        st.warning(
            f"Analytical dataset '{dataset}' "
            "is currently unavailable."
        )

        return

    df = load_dataset(
        str(dataset_path)
    )

    if field not in df.columns:

        st.warning(
            f"Approved field '{dataset}.{field}' "
            "is currently unavailable."
        )

        return

    series = df[field]

    summary = descriptive_summary(
        series
    )

    label = safe_display_label(
        record
    )

    st.markdown(
        f"### {label}"
    )

    st.caption(
        f"Source: {dataset}.{field}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Observed rows",
            format_number(
                summary["rows"]
            ),
        )

    with col2:

        st.metric(
            "Non-null",
            format_number(
                summary["non_null"]
            ),
        )

    with col3:

        st.metric(
            "Distinct values",
            format_number(
                summary["unique"]
            ),
        )

    if summary["non_null"] == 0:

        st.info(
            "No populated values are currently "
            "available for this approved descriptive field."
        )

        return

    visualization = str(
        record.get(
            "visualization",
            "",
        )
    ).lower()

    if (
        pd.api.types.is_numeric_dtype(series)
        and (
            "bar" in visualization
            or "distribution" in visualization
            or "chart" in visualization
        )
    ):

        chart_df = (
            series
            .value_counts(
                dropna=False
            )
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        chart_df["value"] = (
            chart_df["value"]
            .astype(str)
        )

        fig = px.bar(
            chart_df,
            x="value",
            y="observations",
            title=label,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    elif (
        not pd.api.types.is_numeric_dtype(series)
        and (
            "bar" in visualization
            or "distribution" in visualization
            or "chart" in visualization
        )
    ):

        chart_df = (
            series
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(30)
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        fig = px.bar(
            chart_df,
            x="value",
            y="observations",
            title=label,
        )

        fig.update_layout(
            xaxis_title=label,
            yaxis_title="Observed rows",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    else:

        table_df = (
            series
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(30)
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        st.dataframe(
            table_df,
            width="stretch",
            hide_index=True,
        )

    limitation = str(
        record.get(
            "reason",
            "",
        )
    ).strip()

    if limitation:

        st.caption(
            f"Evidence boundary: {limitation}"
        )


# ============================================================
# Shared page header
# ============================================================

def render_page_header(
    title: str,
    description: str,
) -> None:

    st.title(title)

    st.caption(
        description
    )


# ============================================================
# P01 Executive Overview
# ============================================================

def render_executive_overview() -> None:

    render_page_header(
        "Executive Overview",
        (
            "Evidence-bounded descriptive overview of the "
            "validated analytical layer. Final business KPIs "
            "are not activated."
        ),
    )

    st.info(
        "This page presents approved descriptive observations. "
        "It does not certify revenue, profit, ROI, forecasting, "
        "churn, recommendations, or fraud outputs."
    )

    report = load_refresh_report()

    if report:

        status = str(
            report.get(
                "status",
                "UNKNOWN",
            )
        )

        expected = report.get(
            "dataset_count_expected"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Refresh status",
                status,
            )

        with col2:

            st.metric(
                "Datasets in refresh",
                format_number(
                    expected
                ),
            )

    else:

        st.warning(
            "The latest refresh report is unavailable. "
            "The analytical layer itself remains read-only."
        )

    records = approved_records_for_page(
        "P01 Executive Overview"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p01_{index}",
        )


# ============================================================
# P02 Commercial / Sales
# ============================================================

def render_commercial_sales() -> None:

    render_page_header(
        "Commercial / Sales",
        (
            "Descriptive commercial observations from "
            "evidence-approved analytical fields."
        ),
    )

    st.info(
        "Order, unit, product-view, and related descriptive "
        "fields are shown only where explicitly approved. "
        "Monetary KPI activation remains zero."
    )

    records = approved_records_for_page(
        "P02 Commercial / Sales"
    )

    if not records:

        st.info(
            "No approved descriptive fields are available "
            "for this page."
        )

        return

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p02_{index}",
        )


# ============================================================
# P03 Orders
# ============================================================

def render_orders() -> None:

    render_page_header(
        "Orders",
        (
            "Descriptive order information using only "
            "the approved analytical projection."
        ),
    )

    st.info(
        "The analytical orders projection does not expose "
        "order_id, so individual-order drill-down is not "
        "provided."
    )

    records = approved_records_for_page(
        "P03 Orders"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p03_{index}",
        )


# ============================================================
# P04 Products / Catalog
# ============================================================

def render_products_catalog() -> None:

    render_page_header(
        "Products / Catalog",
        (
            "Descriptive product and catalog observations "
            "from approved analytical fields."
        ),
    )

    st.info(
        "Deferred variants_temp fields such as stock, deleted, "
        "handling_time, and item_length remain unavailable."
    )

    records = approved_records_for_page(
        "P04 Products / Catalog"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p04_{index}",
        )


# ============================================================
# P05 Customers / Accounts
# ============================================================

def render_customers_accounts() -> None:

    render_page_header(
        "Customers / Accounts",
        (
            "Account and customer-related descriptive information "
            "within the evidence-supported analytical boundary."
        ),
    )

    st.warning(
        "The accounts dataset is not treated as a customer master. "
        "Raw customer names, emails, addresses, and other PII are "
        "not exposed by this dashboard."
    )

    records = approved_records_for_page(
        "P05 Customers / Accounts"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p05_{index}",
        )


# ============================================================
# P06 Fulfillment / Shipping
# ============================================================

def render_fulfillment_shipping() -> None:

    render_page_header(
        "Fulfillment / Shipping",
        (
            "Descriptive fulfillment and shipping observations "
            "from approved analytical fields."
        ),
    )

    records = approved_records_for_page(
        "P06 Fulfillment / Shipping"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p06_{index}",
        )


# ============================================================
# P07 Returns / Exchange
# ============================================================

def render_returns_exchange() -> None:

    render_page_header(
        "Returns / Exchange",
        (
            "Descriptive return and exchange observations "
            "from approved analytical fields."
        ),
    )

    records = approved_records_for_page(
        "P07 Returns / Exchange"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p07_{index}",
        )


# ============================================================
# P08 Operations / Inventory
# ============================================================

def render_operations_inventory() -> None:

    render_page_header(
        "Operations / Inventory",
        (
            "Descriptive operational and inventory observations "
            "from approved analytical fields."
        ),
    )

    records = approved_records_for_page(
        "P08 Operations / Inventory"
    )

    for index, record in enumerate(
        records
    ):

        render_approved_record(
            record,
            f"p08_{index}",
        )


# ============================================================
# Data & System Health
# ============================================================

def render_data_health() -> None:

    render_page_header(
        "Data & System Health",
        (
            "Technical health of the validated analytical layer "
            "and the latest controlled refresh."
        ),
    )

    report = load_refresh_report()

    if report is None:

        st.error(
            "The latest refresh report is unavailable."
        )

        st.info(
            "No refresh metadata is being invented. "
            "The dashboard will not fabricate a refresh status."
        )

        return

    status = report.get(
        "status",
        "UNKNOWN",
    )

    started = report.get(
        "started_at_utc",
        "—",
    )

    finished = report.get(
        "finished_at_utc",
        "—",
    )

    expected = report.get(
        "dataset_count_expected",
        "—",
    )

    failure = report.get(
        "failure"
    )

    publication = report.get(
        "publication",
        {},
    )

    if isinstance(
        publication,
        dict,
    ):

        publication_status = publication.get(
            "status",
            "UNKNOWN",
        )

    else:

        publication_status = "UNKNOWN"

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Refresh status",
            str(status),
        )

    with col2:

        st.metric(
            "Expected datasets",
            format_number(expected),
        )

    with col3:

        st.metric(
            "Publication",
            str(publication_status),
        )

    st.markdown(
        "### Refresh timestamps"
    )

    timestamp_df = pd.DataFrame(
        [
            {
                "event": "Started (UTC)",
                "timestamp": started,
            },
            {
                "event": "Finished (UTC)",
                "timestamp": finished,
            },
        ]
    )

    st.dataframe(
        timestamp_df,
        width="stretch",
        hide_index=True,
    )

    if failure is not None:

        st.error(
            "The latest controlled refresh reports a failure. "
            "The previous valid analytical state remains the "
            "dashboard's source boundary."
        )

        st.json(
            failure
        )

    datasets = report.get(
        "datasets",
        [],
    )

    if not isinstance(
        datasets,
        list,
    ):

        datasets = []

    st.markdown(
        "### Dataset validation"
    )

    if not datasets:

        st.info(
            "No dataset-level refresh records are available."
        )

    else:

        health_records = []

        for dataset_record in datasets:

            health_records.append(
                {
                    "dataset": dataset_record.get(
                        "dataset",
                        "—",
                    ),
                    "status": dataset_record.get(
                        "status",
                        "—",
                    ),
                    "source_rows": dataset_record.get(
                        "source_rows",
                        "—",
                    ),
                    "output_rows": dataset_record.get(
                        "output_rows",
                        "—",
                    ),
                    "source_fields": dataset_record.get(
                        "source_fields",
                        "—",
                    ),
                    "output_fields": dataset_record.get(
                        "output_fields",
                        "—",
                    ),
                    "grain_nulls": dataset_record.get(
                        "source_grain_nulls",
                        "—",
                    ),
                    "grain_duplicate_values": dataset_record.get(
                        "source_grain_duplicate_values",
                        "—",
                    ),
                    "expected_duplicate_rows": dataset_record.get(
                        "expected_duplicate_rows",
                        "—",
                    ),
                    "actual_duplicate_rows": dataset_record.get(
                        "actual_duplicate_rows",
                        "—",
                    ),
                    "error": dataset_record.get(
                        "error"
                    ),
                }
            )

        health_df = pd.DataFrame(
            health_records
        )

        st.dataframe(
            health_df,
            width="stretch",
            hide_index=True,
        )

    st.markdown(
        "### Validation boundary"
    )

    st.caption(
        "The current refresh report does not contain "
        "refresh_id, rows_processed, rows_published, "
        "schema_changes, or historical refresh count. "
        "Those values are therefore not displayed."
    )


# ============================================================
# Technical Dataset Explorer
# ============================================================

def render_technical_explorer() -> None:

    render_page_header(
        "Technical Dataset Explorer",
        (
            "Read-only technical exploration of the analytical "
            "layer. Technical field characteristics do not "
            "constitute business-semantic approval."
        ),
    )

    analytical_files = (
        discover_analytical_files()
    )

    if not analytical_files:

        st.error(
            "No analytical CSV files were discovered."
        )

        return

    dataset_names = [
        path.stem
        for path in analytical_files
    ]

    selected_dataset = st.selectbox(
        "Analytical dataset",
        dataset_names,
    )

    selected_path = (
        ANALYTICAL_ROOT
        / f"{selected_dataset}.csv"
    )

    try:

        df = load_dataset(
            str(selected_path)
        )

    except Exception as exc:

        st.error(
            f"Unable to load dataset: {exc}"
        )

        return

    st.markdown(
        "### Dataset overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            format_number(
                len(df)
            ),
        )

    with col2:

        st.metric(
            "Columns",
            format_number(
                len(df.columns)
            ),
        )

    with col3:

        st.metric(
            "Missing cells",
            format_number(
                int(
                    df.isna().sum().sum()
                )
            ),
        )

    st.dataframe(
        df.head(100),
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        "### Technical field profile"
    )

    quality_frame = pd.DataFrame(
        [
            {
                "field": column,
                "dtype": str(
                    df[column].dtype
                ),
                "non_null": int(
                    df[column].notna().sum()
                ),
                "missing": int(
                    df[column].isna().sum()
                ),
                "missing_pct": round(
                    df[column].isna().mean() * 100,
                    2,
                ),
                "unique": int(
                    df[column].nunique(
                        dropna=True
                    )
                ),
            }
            for column in df.columns
        ]
    )

    st.dataframe(
        quality_frame,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "This technical explorer intentionally does not "
        "certify fields as business KPIs or semantic dimensions."
    )


# ============================================================
# Application shell
# ============================================================

st.set_page_config(
    page_title="PurjeStore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.sidebar.title(
    "PurjeStore Analytics"
)

st.sidebar.caption(
    "Evidence-driven analytical decision support"
)

selected_page = st.sidebar.radio(
    "Navigation",
    PAGE_AREAS,
)

st.sidebar.divider()

st.sidebar.subheader(
    "Evidence Boundary"
)

st.sidebar.caption(
    "26 analytical datasets"
)

st.sidebar.caption(
    "21 approved descriptive page/field records"
)

st.sidebar.caption(
    "0 final KPIs"
)

st.sidebar.caption(
    "0 approved joins"
)

st.sidebar.caption(
    "ML blocked"
)

st.sidebar.caption(
    "Analytical layer is read-only"
)


# ============================================================
# Controlled page routing
# ============================================================

if selected_page == "P01 Executive Overview":

    render_executive_overview()

elif selected_page == "P02 Commercial / Sales":

    render_commercial_sales()

elif selected_page == "P03 Orders":

    render_orders()

elif selected_page == "P04 Products / Catalog":

    render_products_catalog()

elif selected_page == "P05 Customers / Accounts":

    render_customers_accounts()

elif selected_page == "P06 Fulfillment / Shipping":

    render_fulfillment_shipping()

elif selected_page == "P07 Returns / Exchange":

    render_returns_exchange()

elif selected_page == "P08 Operations / Inventory":

    render_operations_inventory()

elif selected_page == "Data & System Health":

    render_data_health()

elif selected_page == "Technical Dataset Explorer":

    render_technical_explorer()
