from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_products_catalog() -> None:
    render_page_header(
        "Products / Catalog",
        "Descriptive product and catalog observations from approved analytical fields.",
    )

    st.info(
        "Deferred variants_temp fields such as stock, deleted, handling_time, and item_length remain unavailable."
    )

    records = approved_records_for_page("P04 Products / Catalog")

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p04_{index}",
        )
