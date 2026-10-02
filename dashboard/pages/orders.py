from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P03_PAGE = "P03 Orders"


def _render_order_evidence() -> None:
    st.subheader("Observed Order-Item Evidence")

    st.caption(
        "This page presents the approved order-item quantity evidence "
        "available in the analytical layer. The evidence is descriptive "
        "and remains at its source-native analytical grain."
    )

    records = approved_records_for_page(P03_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p03_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "order_items.quantity. It supports descriptive observation of "
        "order-item quantity only. The dashboard does not infer order "
        "revenue, order value, average order value, conversion rate, "
        "customer order frequency, or order growth KPIs from this field."
    )


def render_orders() -> None:
    render_page_header(
        "Orders",
        (
            "Descriptive order-item quantity evidence from the "
            "approved analytical projection."
        ),
    )

    st.info(
        "The analytical orders projection does not expose order_id, "
        "so individual-order drill-down is not provided."
    )

    _render_order_evidence()
    _render_evidence_boundary()
