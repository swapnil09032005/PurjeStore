"""
PurjeStore Dashboard Approved-Record Renderer

This module owns the reusable presentation of one evidence-approved
analytical field.

Responsibilities:
- Load the approved analytical dataset field.
- Present descriptive field observations.
- Render the existing numeric/categorical Plotly views.
- Render the existing frequency-table fallback.
- Display the existing evidence boundary.

This module must NOT contain:
- Semantic approval decisions
- New KPI definitions
- Dataset construction
- Joins
- ML/predictive logic
- Source-data mutation
- Analytical file writes
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from .config import ANALYTICAL_ROOT
from .data import load_dataset
from .semantics import safe_display_label
from .utils import descriptive_summary, format_number


def render_approved_record(
    record: dict,
    key_prefix: str,
) -> None:
    """
    Render one evidence-approved analytical field.

    The implementation intentionally preserves the existing dashboard
    behavior during the architecture refactor.
    """

    del key_prefix

    dataset = record["dataset"]
    field = record["field"]

    dataset_path = (
        ANALYTICAL_ROOT
        / f"{dataset}.csv"
    )

    if not dataset_path.exists():

        st.warning(
            f"Analytical dataset '{dataset}' "
            "is currently unavailable."
        )

        return

    df = load_dataset(
        str(dataset_path)
    )

    if field not in df.columns:

        st.warning(
            f"Approved field '{dataset}.{field}' "
            "is currently unavailable."
        )

        return

    series = df[field]

    summary = descriptive_summary(
        series
    )

    label = safe_display_label(
        record
    )

    st.markdown(
        f"### {label}"
    )

    st.caption(
        f"Source: {dataset}.{field}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Observed rows",
            format_number(
                summary["rows"]
            ),
        )

    with col2:

        st.metric(
            "Non-null",
            format_number(
                summary["non_null"]
            ),
        )

    with col3:

        st.metric(
            "Distinct values",
            format_number(
                summary["unique"]
            ),
        )

    if summary["non_null"] == 0:

        st.info(
            "No populated values are currently "
            "available for this approved descriptive field."
        )

        return

    visualization = str(
        record.get(
            "visualization",
            "",
        )
    ).lower()

    if (
        pd.api.types.is_numeric_dtype(series)
        and (
            "bar" in visualization
            or "distribution" in visualization
            or "chart" in visualization
        )
    ):

        chart_df = (
            series
            .value_counts(
                dropna=False
            )
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        chart_df["value"] = (
            chart_df["value"]
            .astype(str)
        )

        fig = px.bar(
            chart_df,
            x="value",
            y="observations",
            title=label,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    elif (
        not pd.api.types.is_numeric_dtype(series)
        and (
            "bar" in visualization
            or "distribution" in visualization
            or "chart" in visualization
        )
    ):

        chart_df = (
            series
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(30)
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        fig = px.bar(
            chart_df,
            x="value",
            y="observations",
            title=label,
        )

        fig.update_layout(
            xaxis_title=label,
            yaxis_title="Observed rows",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    else:

        table_df = (
            series
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(30)
            .rename_axis(
                "value"
            )
            .reset_index(
                name="observations"
            )
        )

        st.dataframe(
            table_df,
            width="stretch",
            hide_index=True,
        )

    limitation = str(
        record.get(
            "reason",
            "",
        )
    ).strip()

    if limitation:

        st.caption(
            f"Evidence boundary: {limitation}"
        )