from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P06_PAGE = "P06 Fulfillment / Shipping"


def _render_fulfillment_shipping_evidence() -> None:
    st.subheader("Observed Fulfillment / Shipping Evidence")

    st.caption(
        "This page presents the approved shipment-item quantity and "
        "hub inventory quantity evidence available in the analytical "
        "layer. The evidence is descriptive and remains at its "
        "source-native analytical grain."
    )

    records = approved_records_for_page(P06_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p06_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "shipment_items.quantity and hub_inventory.quantity. These "
        "fields support descriptive quantity observation only. "
        "The dashboard does not infer delivery time, shipping time, "
        "SLA performance, carrier performance, shipping cost, "
        "delivery success rate, fulfillment rate, inventory value, "
        "stockout rate, inventory turnover, shipment revenue, "
        "hub or warehouse performance rankings, optimization "
        "outcomes, or predictive fulfillment/shipping outcomes "
        "from this evidence. The displayed quantity totals are "
        "descriptive observations and are not certified business KPIs."
    )


def render_fulfillment_shipping() -> None:
    render_page_header(
        "Fulfillment / Shipping",
        (
            "Descriptive shipment-item quantity and hub inventory "
            "quantity evidence from the approved analytical projections."
        ),
    )

    _render_fulfillment_shipping_evidence()
    _render_evidence_boundary()
