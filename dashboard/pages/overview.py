from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.config import ANALYTICAL_ROOT
from dashboard.data import load_dataset, load_refresh_report
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page
from dashboard.utils import format_number


P01_PAGE = "P01 Executive Overview"

P01_DATASETS = (
    "daily_category_metrics",
    "daily_platform_metrics",
    "daily_vendor_metrics",
)


def _render_current_evidence_summary() -> None:
    st.subheader("Current Evidence Summary")

    st.caption(
        "This page provides an orientation view of the evidence currently "
        "approved for descriptive dashboard use. The summary describes "
        "analytical coverage and system refresh state; it is not a business KPI view."
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
                format_number(expected),
            )

    else:
        st.warning(
            "The latest refresh report is unavailable. "
            "The analytical layer itself remains read-only."
        )


def _render_analytical_coverage() -> None:
    st.subheader("Analytical Coverage")

    st.caption(
        "The approved P01 evidence currently comes from three analytical "
        "datasets. Row and field counts describe dataset coverage only."
    )

    columns = st.columns(len(P01_DATASETS))

    for column, dataset_name in zip(
        columns,
        P01_DATASETS,
    ):
        path = ANALYTICAL_ROOT / f"{dataset_name}.csv"

        with column:
            st.markdown(f"**{dataset_name}**")

            if not path.exists():
                st.warning(
                    "Dataset is currently unavailable."
                )
                continue

            try:
                dataset = load_dataset(
                    str(path)
                )
            except (
                OSError,
                ValueError,
                FileNotFoundError,
            ) as exc:
                st.warning(
                    f"Dataset could not be loaded: {exc}"
                )
                continue

            st.metric(
                "Rows",
                format_number(
                    len(dataset)
                ),
            )

            st.caption(
                f"{format_number(len(dataset.columns))} available fields"
            )


def _render_descriptive_evidence() -> None:
    st.subheader("Descriptive Evidence")

    st.caption(
        "The records below are the exact approved P01 descriptive evidence. "
        "Values are rendered from the validated analytical layer without "
        "cross-dataset joins or additional business inference."
    )

    records = approved_records_for_page(
        P01_PAGE
    )

    for index, record in enumerate(
        records
    ):
        render_approved_record(
            record,
            f"p01_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "This page is an Executive Overview of available analytical evidence, "
        "not an Executive KPI Dashboard. No final business KPIs, approved "
        "cross-dataset joins, predictive outputs, or unsupported business "
        "interpretations are activated. Revenue, profit, ROI, forecasting, "
        "churn, recommendations, and fraud outputs are not certified by this dashboard."
    )


def render_executive_overview() -> None:
    render_page_header(
        "Executive Overview",
        (
            "Evidence-bounded orientation view of the validated analytical "
            "layer and the descriptive evidence currently approved for PurjeStore."
        ),
    )

    _render_current_evidence_summary()

    _render_analytical_coverage()

    _render_descriptive_evidence()

    _render_evidence_boundary()
