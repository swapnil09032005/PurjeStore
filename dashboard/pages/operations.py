from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P08_PAGE = "P08 Operations / Inventory"


def _render_operations_inventory_evidence() -> None:
    st.subheader("Observed Operations / Inventory Evidence")

    st.caption(
        "This page presents the approved hub inventory quantity and "
        "daily vendor-level product-view evidence available in the "
        "analytical layer. The evidence is descriptive and remains "
        "at its source-native analytical grain."
    )

    records = approved_records_for_page(P08_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p08_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "hub_inventory.quantity and daily_vendor_metrics.product_views. "
        "These fields support descriptive observation only within "
        "their source-native analytical grains. The dashboard does "
        "not infer inventory value, stockout rates, inventory "
        "turnover, stock availability or performance, vendor "
        "performance rankings, vendor optimization, sales, revenue, "
        "profitability, conversion, ROI, forecasting, prediction, "
        "recommendations, customer behavior, or certified operational "
        "KPIs from this evidence. Displayed quantity and product-view "
        "totals are descriptive observations and are not certified "
        "business KPIs."
    )


def render_operations_inventory() -> None:
    render_page_header(
        "Operations / Inventory",
        (
            "Descriptive hub inventory quantity and daily vendor-level "
            "product-view evidence from the approved analytical "
            "projections."
        ),
    )

    _render_operations_inventory_evidence()
    _render_evidence_boundary()
