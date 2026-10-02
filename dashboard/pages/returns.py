from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P07_PAGE = "P07 Returns / Exchange"


def _render_returns_exchange_evidence() -> None:
    st.subheader("Observed Returns / Exchange Evidence")

    st.caption(
        "This page presents the approved return-request status and "
        "hub-return quantity evidence available in the analytical "
        "layer. The evidence is descriptive and remains at its "
        "source-native analytical grain."
    )

    records = approved_records_for_page(P07_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p07_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "return_request.status and hub_returns.quantity. These "
        "fields support descriptive observation of return-request "
        "status frequencies and hub-return quantity only. The "
        "dashboard does not infer return rates, approval rates, "
        "rejection rates, refund rates, processing-time metrics, "
        "exchange rates, customer return behavior, financial impact, "
        "operational performance rankings, certified return-volume "
        "KPIs, optimization outcomes, or predictive returns/exchange "
        "outcomes from this evidence. Displayed quantity totals are "
        "descriptive observations and are not certified business KPIs."
    )


def render_returns_exchange() -> None:
    render_page_header(
        "Returns / Exchange",
        (
            "Descriptive return-request status and hub-return "
            "quantity evidence from the approved analytical projections."
        ),
    )

    _render_returns_exchange_evidence()
    _render_evidence_boundary()
