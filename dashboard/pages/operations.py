from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
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