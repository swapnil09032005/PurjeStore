from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.data import load_refresh_report
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page
from dashboard.utils import format_number


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
