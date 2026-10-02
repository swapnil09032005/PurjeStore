from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.config import ANALYTICAL_ROOT
from dashboard.data import discover_analytical_files, load_dataset
from dashboard.utils import format_number


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_technical_explorer() -> None:

    render_page_header(
        "Technical Dataset Explorer",
        (
            "Read-only technical exploration of the analytical "
            "layer. Technical field characteristics do not "
            "constitute business-semantic approval."
        ),
    )

    analytical_files = (
        discover_analytical_files()
    )

    if not analytical_files:

        st.error(
            "No analytical CSV files were discovered."
        )

        return

    dataset_names = [
        path.stem
        for path in analytical_files
    ]

    selected_dataset = st.selectbox(
        "Analytical dataset",
        dataset_names,
    )

    selected_path = (
        ANALYTICAL_ROOT
        / f"{selected_dataset}.csv"
    )

    try:

        df = load_dataset(
            str(selected_path)
        )

    except Exception as exc:

        st.error(
            f"Unable to load dataset: {exc}"
        )

        return

    st.markdown(
        "### Dataset overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            format_number(
                len(df)
            ),
        )

    with col2:

        st.metric(
            "Columns",
            format_number(
                len(df.columns)
            ),
        )

    with col3:

        st.metric(
            "Missing cells",
            format_number(
                int(
                    df.isna().sum().sum()
                )
            ),
        )

    st.dataframe(
        df.head(100),
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        "### Technical field profile"
    )

    quality_frame = pd.DataFrame(
        [
            {
                "field": column,
                "dtype": str(
                    df[column].dtype
                ),
                "non_null": int(
                    df[column].notna().sum()
                ),
                "missing": int(
                    df[column].isna().sum()
                ),
                "missing_pct": round(
                    df[column].isna().mean() * 100,
                    2,
                ),
                "unique": int(
                    df[column].nunique(
                        dropna=True
                    )
                ),
            }
            for column in df.columns
        ]
    )

    st.dataframe(
        quality_frame,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "This technical explorer intentionally does not "
        "certify fields as business KPIs or semantic dimensions."
    )
