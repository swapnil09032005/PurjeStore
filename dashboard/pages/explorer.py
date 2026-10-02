from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.config import ANALYTICAL_ROOT
from dashboard.data import discover_analytical_files, load_dataset
from dashboard.utils import format_number


PREVIEW_ROW_LIMIT = 100


def _render_dataset_summary(df: pd.DataFrame) -> None:
    st.subheader("Technical Dataset Summary")

    missing_cells = int(df.isna().sum().sum())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            format_number(len(df)),
        )

    with col2:
        st.metric(
            "Columns",
            format_number(len(df.columns)),
        )

    with col3:
        st.metric(
            "Missing cells",
            format_number(missing_cells),
        )

    st.caption(
        "These values describe the selected analytical dataset "
        "technically. They do not represent business KPIs."
    )


def _render_dataset_preview(
    df: pd.DataFrame,
    dataset_name: str,
) -> None:
    st.subheader("Read-only Data Preview")

    preview = df.head(PREVIEW_ROW_LIMIT)

    st.caption(
        f"Showing up to {PREVIEW_ROW_LIMIT} rows from "
        f"the selected analytical dataset: {dataset_name}."
    )

    st.dataframe(
        preview,
        width="stretch",
        hide_index=True,
    )

    if len(df) > PREVIEW_ROW_LIMIT:
        st.info(
            f"The dataset contains {format_number(len(df))} rows. "
            f"Only the first {PREVIEW_ROW_LIMIT} rows are shown "
            "in this technical preview."
        )


def _build_field_profile(
    df: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Field": column,
                "Data type": str(df[column].dtype),
                "Non-null": int(df[column].notna().sum()),
                "Missing": int(df[column].isna().sum()),
                "Missing %": round(
                    df[column].isna().mean() * 100,
                    2,
                ),
                "Unique values": int(
                    df[column].nunique(
                        dropna=True,
                    )
                ),
            }
            for column in df.columns
        ]
    )


def _render_field_profile(
    df: pd.DataFrame,
) -> None:
    st.subheader("Technical Field Profile")

    profile_df = _build_field_profile(df)

    st.caption(
        "Field-level characteristics are technical observations "
        "only. Data type, missingness, and cardinality do not "
        "approve a field for business interpretation."
    )

    st.dataframe(
        profile_df,
        width="stretch",
        hide_index=True,
    )


def _render_semantic_boundary() -> None:
    st.subheader("Technical Interpretation Boundary")

    st.info(
        "This explorer is a read-only technical inspection tool. "
        "Technical field characteristics do not constitute "
        "business-semantic approval, KPI approval, dimension "
        "approval, join approval, or analytical-model approval. "
        "Business meaning remains governed by the project's "
        "validated semantic evidence and analytical contracts."
    )


def _render_dataset_error(
    dataset_name: str,
    exc: Exception,
) -> None:
    st.error(
        f"Unable to load analytical dataset '{dataset_name}'."
    )

    st.caption(
        "The dashboard did not modify or reconstruct the dataset."
    )

    st.exception(exc)


def render_technical_explorer() -> None:
    render_page_header(
        "Technical Dataset Explorer",
        (
            "Read-only technical exploration of the analytical "
            "layer. Technical field characteristics do not "
            "constitute business-semantic approval."
        ),
    )

    st.info(
        "Use this page to inspect the technical structure and "
        "quality characteristics of one analytical dataset at a "
        "time. This page does not certify business meaning."
    )

    analytical_files = discover_analytical_files()

    if not analytical_files:
        st.error(
            "No analytical CSV files were discovered."
        )

        st.info(
            "The technical explorer cannot display a dataset "
            "until an analytical CSV is available."
        )

        return

    dataset_names = [
        path.stem
        for path in analytical_files
    ]

    selected_dataset = st.selectbox(
        "Select analytical dataset",
        dataset_names,
        help=(
            "Select one validated analytical CSV for "
            "read-only technical inspection."
        ),
    )

    st.caption(
        f"Selected dataset: `{selected_dataset}.csv`"
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
        _render_dataset_error(
            selected_dataset,
            exc,
        )
        return

    _render_dataset_summary(df)
    _render_dataset_preview(
        df,
        selected_dataset,
    )
    _render_field_profile(df)
    _render_semantic_boundary()