from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_orders() -> None:
    render_page_header(
        "Orders",
        "Descriptive order information using only the approved analytical projection.",
    )

    st.info(
        "The analytical orders projection does not expose order_id, so individual-order drill-down is not provided."
    )

    records = approved_records_for_page("P03 Orders")

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p03_{index}",
        )
