from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P04_PAGE = "P04 Products / Catalog"


def _render_product_evidence() -> None:
    st.subheader("Observed Product Status Evidence")

    st.caption(
        "This page presents the approved product status evidence "
        "available in the analytical layer. The evidence is descriptive "
        "and remains at its source-native analytical grain."
    )

    records = approved_records_for_page(P04_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p04_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "product.status. It supports descriptive observation of "
        "product status frequencies only. The dashboard does not "
        "infer product sales, revenue, profitability, inventory "
        "value, product popularity, conversion, rankings, "
        "recommendations, or predictive outcomes from this field."
    )


def render_products_catalog() -> None:
    render_page_header(
        "Products / Catalog",
        (
            "Descriptive product-status evidence from the "
            "approved analytical projection."
        ),
    )

    _render_product_evidence()
    _render_evidence_boundary()
