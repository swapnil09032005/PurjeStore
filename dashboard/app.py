from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from .config import (
    PAGE_AREAS,
    STREAMLIT_INITIAL_SIDEBAR_STATE,
    STREAMLIT_LAYOUT,
    STREAMLIT_PAGE_ICON,
    STREAMLIT_PAGE_TITLE,
)


def run_application_shell(
    page_renderers: dict[str, Callable[[], None]],
) -> None:
    """
    Run the PurjeStore Streamlit application shell.

    Page implementations and APPROVED_MAPPING remain owned by app.py
    during this controlled extraction stage.
    """
    st.set_page_config(
        page_title=STREAMLIT_PAGE_TITLE,
        page_icon=STREAMLIT_PAGE_ICON,
        layout=STREAMLIT_LAYOUT,
        initial_sidebar_state=STREAMLIT_INITIAL_SIDEBAR_STATE,
    )

    st.sidebar.title(
        "PurjeStore Analytics"
    )

    st.sidebar.caption(
        "Evidence-driven analytical decision support"
    )

    selected_page = st.sidebar.radio(
        "Navigation",
        PAGE_AREAS,
    )

    st.sidebar.divider()

    st.sidebar.subheader(
        "Evidence Boundary"
    )

    st.sidebar.caption(
        "26 analytical datasets"
    )

    st.sidebar.caption(
        "21 approved descriptive page/field records"
    )

    st.sidebar.caption(
        "0 final KPIs"
    )

    st.sidebar.caption(
        "0 approved joins"
    )

    st.sidebar.caption(
        "ML blocked"
    )

    st.sidebar.caption(
        "Analytical layer is read-only"
    )

    renderer = page_renderers.get(selected_page)

    if renderer is None:
        st.error(
            f"No renderer is registered for dashboard page: {selected_page}"
        )
        return

    renderer()