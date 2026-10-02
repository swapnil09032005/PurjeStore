from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_customers_accounts() -> None:
    render_page_header(
        "Customers / Accounts",
        "Account and customer-related descriptive information within the evidence-supported analytical boundary.",
    )

    st.warning(
        "The accounts dataset is not treated as a customer master. Raw customer names, emails, addresses, and other PII are not exposed by this dashboard."
    )

    records = approved_records_for_page("P05 Customers / Accounts")

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p05_{index}",
        )
