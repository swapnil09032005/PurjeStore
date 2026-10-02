from __future__ import annotations

import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.record_renderer import render_approved_record
from dashboard.semantics import approved_records_for_page


P05_PAGE = "P05 Customers / Accounts"


def _render_wallet_transaction_evidence() -> None:
    st.subheader("Observed Wallet Transaction Evidence")

    st.caption(
        "This page presents the approved wallet transaction evidence "
        "available in the analytical layer. The evidence is descriptive "
        "and remains at its source-native analytical grain."
    )

    records = approved_records_for_page(P05_PAGE)

    if not records:
        st.info(
            "No approved descriptive evidence is currently available "
            "for this page."
        )
        return

    for index, record in enumerate(records):
        render_approved_record(
            record,
            f"p05_{index}",
        )


def _render_evidence_boundary() -> None:
    st.subheader("Evidence Boundary")

    st.info(
        "The approved evidence for this page is limited to "
        "wallet_transactions.type, wallet_transactions.method, and "
        "wallet_transactions.status. These fields support descriptive "
        "frequency observation only. The dashboard does not infer "
        "customer counts, customer value, wallet balances, spending, "
        "revenue, profitability, customer lifetime value, customer "
        "segmentation, customer behavior, transaction amount KPIs, "
        "or predictive outcomes from this evidence. The accounts "
        "dataset is not automatically treated as a customer master, "
        "and raw customer identity or PII is not exposed."
    )


def render_customers_accounts() -> None:
    render_page_header(
        "Customers / Accounts",
        (
            "Descriptive wallet transaction evidence from the "
            "approved analytical projection."
        ),
    )

    st.info(
        "This page does not provide individual customer or account "
        "drill-down. The approved analytical evidence does not "
        "establish a customer-master view."
    )

    _render_wallet_transaction_evidence()
    _render_evidence_boundary()