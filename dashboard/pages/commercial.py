from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P02_PAGE = "P02 Commercial / Sales"


def _render_current_commercial_evidence() -> None:
    st.subheader("Current Commercial Evidence")

    st.caption(
        "This page presents the descriptive commercial evidence currently "
        "approved from the analytical layer. Payment status is shown as "
        "categorical evidence, while invoice quantity is shown as an "
        "observed quantity distribution."
    )

    records = approved_records_for_page(P02_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    evidence = {
        (
            record.get("dataset"),
            record.get("field"),
        ): record
        for record in records
    }

    payment_transaction_status = evidence.get(
        ("payment_transactions", "status")
    )
    payment_status = evidence.get(
        ("payments", "status")
    )
    invoice_quantity = evidence.get(
        ("invoices", "quantity")
    )

    columns = st.columns(3)

    with columns[0]:
        st.markdown("**Payment transaction status**")
        if payment_transaction_status is not None:
            st.caption("`payment_transactions.status`")
            st.caption("Categorical distribution")
        else:
            st.warning("Approved evidence is unavailable.")

    with columns[1]:
        st.markdown("**Payment status**")
        if payment_status is not None:
            st.caption("`payments.status`")
            st.caption("Categorical distribution")
        else:
            st.warning("Approved evidence is unavailable.")

    with columns[2]:
        st.markdown("**Invoice quantity**")
        if invoice_quantity is not None:
            st.caption("`invoices.quantity`")
            st.caption("Observed quantity distribution")
        else:
            st.warning("Approved evidence is unavailable.")


def _render_approved_evidence() -> None:
    st.subheader("Observed Evidence")

    st.caption(
        "The following records are rendered from the exact approved "
        "semantic mapping. No cross-dataset joins or additional business "
        "measures are created by this page."
    )

    records = approved_records_for_page(P02_PAGE)

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p02_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "This page is descriptive rather than a certified sales KPI view. "
        "The approved evidence consists only of payment transaction status, "
        "payment status, and invoice quantity. Revenue, gross sales, net "
        "sales, profit, margin, ROI, and payment success rate as a certified "
        "KPI are not activated. The dashboard does not infer business impact "
        "from these observations."
    )


def render_commercial_sales() -> None:
    render_page_header(
        "Commercial / Sales",
        (
            "Descriptive commercial evidence from payment status and "
            "invoice quantity fields approved for dashboard presentation."
        ),
    )

    _render_current_commercial_evidence()

    _render_approved_evidence()

    _render_evidence_boundary()
