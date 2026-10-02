from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_fulfillment_shipping() -> None:
    render_page_header(
        "Fulfillment / Shipping",
        "Descriptive fulfillment and shipping observations from approved analytical fields.",
    )

    records = approved_records_for_page("P06 Fulfillment / Shipping")

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p06_{index}",
        )
