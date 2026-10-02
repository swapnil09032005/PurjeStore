from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


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
