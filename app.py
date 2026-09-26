from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


# =============================================================================
# PURJESTORE — DASHBOARD APPLICATION FOUNDATION
# Major Milestone 8.3
#
# Evidence boundary inherited from Milestones 8.0–8.2:
#   - Streamlit is the primary application framework.
#   - Plotly is used for interactive descriptive visuals.
#   - data/processed/analytical is read-only application input.
#   - No cross-dataset joins are performed.
#   - No final business KPI is invented from numeric-column presence.
#   - No ML / forecasting / recommendation / churn / fraud page is activated.
#   - 5.5-C candidate_measure_register_55c values remain unrecoverable.
#
# This is an evidence-bounded descriptive analytics foundation.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. APPLICATION CONFIGURATION
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="PurjeStore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent
ANALYTICAL_ROOT = PROJECT_ROOT / "data" / "processed" / "analytical"

PAGE_AREAS = [
    "Executive / Overview",
    "Sales / Commercial Analytics",
    "Order Analytics",
    "Product / Catalog Analytics",
    "Customer / Account Analytics",
    "Fulfillment / Shipping Analytics",
    "Returns / Exchange Analytics",
    "Operations / Inventory Analytics",
]

EXCLUDED_AREAS = [
    "ML Predictions",
    "Forecasting",
    "Recommendations",
    "Churn / Retention Prediction",
    "Fraud Detection",
]

KNOWN_LIMITATIONS = {
    "5.5-C measure evidence": (
        "candidate_measure_register_55c values were not recoverable as a "
        "complete 193 × 14 structured register."
    ),
    "notification_logs": "Coverage gap preserved from prior milestones.",
    "orders": "Coverage gap preserved from prior milestones.",
    "variants_temp": "Semantic deferrals preserved from prior milestones.",
    "grain exceptions": "3 known grain exceptions preserved.",
    "identifier/code warnings": "3 known identifier/code warnings preserved.",
    "ML problem selection": "0 ML problems selected in Milestone 6.",
}


# -----------------------------------------------------------------------------
# 2. DATA DISCOVERY / LOADING
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def discover_analytical_files() -> list[Path]:
    """Discover analytical CSVs without modifying the filesystem."""
    if not ANALYTICAL_ROOT.exists():
        return []

    return sorted(
        path
        for path in ANALYTICAL_ROOT.glob("*.csv")
        if path.is_file()
    )


@st.cache_data(show_spinner=False)
def load_dataset(path_string: str) -> pd.DataFrame:
    """Read one analytical CSV into memory without modifying its source."""
    path = Path(path_string)

    if not path.exists():
        raise FileNotFoundError(f"Analytical dataset not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Unsupported analytical source: {path.name}")

    return pd.read_csv(path, low_memory=False)


# -----------------------------------------------------------------------------
# 3. TYPE / DISPLAY HELPERS
# -----------------------------------------------------------------------------

def is_numeric_series(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def is_datetime_like_series(series: pd.Series) -> bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    name = str(series.name).lower()

    temporal_tokens = (
        "date",
        "time",
        "timestamp",
        "created",
        "updated",
        "modified",
        "deleted",
        "at",
    )

    return any(token in name for token in temporal_tokens)


def safe_numeric_columns(df: pd.DataFrame) -> list[str]:
    return [
        column
        for column in df.columns
        if is_numeric_series(df[column])
    ]


def safe_categorical_columns(df: pd.DataFrame) -> list[str]:
    result = []

    for column in df.columns:
        series = df[column]
        dtype = series.dtype

        if (
            pd.api.types.is_object_dtype(dtype)
            or pd.api.types.is_string_dtype(dtype)
            or isinstance(dtype, pd.CategoricalDtype)
            or pd.api.types.is_bool_dtype(dtype)
        ):
            result.append(column)

    return result


def safe_temporal_columns(df: pd.DataFrame) -> list[str]:
    return [
        column
        for column in df.columns
        if is_datetime_like_series(df[column])
    ]


def format_number(value: Any) -> str:
    if value is None:
        return "—"

    try:
        if isinstance(value, float) and math.isnan(value):
            return "—"

        if isinstance(value, (int, float)):
            return f"{value:,.2f}".rstrip("0").rstrip(".")

    except Exception:
        pass

    return str(value)


# -----------------------------------------------------------------------------
# 4. HEADER
# -----------------------------------------------------------------------------

st.title("PurjeStore Intelligent E-Commerce Analytics")

st.caption(
    "Evidence-bounded interactive analytics foundation • "
    "Major Milestone 8.3"
)

st.info(
    "This dashboard currently provides dataset-specific descriptive exploration. "
    "Final business KPIs and cross-dataset metrics are not approved because "
    "the authoritative 5.5-C measure register values were not recoverable as "
    "a complete structured register."
)


# -----------------------------------------------------------------------------
# 5. NAVIGATION
# -----------------------------------------------------------------------------

st.sidebar.header("Navigation")

selected_area = st.sidebar.radio(
    "Dashboard area",
    PAGE_AREAS,
    index=0,
)

st.sidebar.divider()

st.sidebar.subheader("Evidence Boundary")

st.sidebar.caption("Approved final business KPIs: 0")
st.sidebar.caption("Approved cross-dataset joins: 0")
st.sidebar.caption("Selected ML problems: 0")
st.sidebar.caption("Source analytical datasets: read-only")

st.sidebar.divider()

st.sidebar.subheader("Excluded from current scope")

for excluded in EXCLUDED_AREAS:
    st.sidebar.caption(f"• {excluded}")


# -----------------------------------------------------------------------------
# 6. SOURCE DISCOVERY
# -----------------------------------------------------------------------------

analytical_files = discover_analytical_files()

if not analytical_files:
    st.error(
        "No analytical CSV datasets were found under "
        "`data/processed/analytical`."
    )
    st.stop()

dataset_names = [path.stem for path in analytical_files]

dataset_lookup = {
    path.stem: path
    for path in analytical_files
}


# -----------------------------------------------------------------------------
# 7. DATASET SELECTION
# -----------------------------------------------------------------------------

st.header(selected_area)

st.caption(
    "Each analytical dataset is explored independently. "
    "Selecting a dataset does not authorize a join with another dataset."
)

selected_dataset = st.selectbox(
    "Select an analytical dataset",
    dataset_names,
    index=0,
)

selected_path = dataset_lookup[selected_dataset]


# -----------------------------------------------------------------------------
# 8. LOAD DATASET
# -----------------------------------------------------------------------------

try:
    df = load_dataset(str(selected_path))
except Exception as exc:
    st.error(f"Unable to load `{selected_dataset}`: {exc}")
    st.stop()


# -----------------------------------------------------------------------------
# 9. DATASET PROFILE
# -----------------------------------------------------------------------------

numeric_columns = safe_numeric_columns(df)
categorical_columns = safe_categorical_columns(df)
temporal_columns = safe_temporal_columns(df)

duplicate_rows = int(df.duplicated().sum())
missing_cells = int(df.isna().sum().sum())
total_cells = int(df.shape[0] * df.shape[1])

missing_pct = (
    (missing_cells / total_cells) * 100
    if total_cells
    else 0.0
)

metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

with metric_col_1:
    st.metric("Rows", f"{len(df):,}")

with metric_col_2:
    st.metric("Columns", f"{len(df.columns):,}")

with metric_col_3:
    st.metric("Missing cells", f"{missing_cells:,}")

with metric_col_4:
    st.metric("Complete-row duplicates", f"{duplicate_rows:,}")

st.caption(
    f"Dataset-level missingness: {missing_pct:.2f}% • "
    f"Numeric fields: {len(numeric_columns)} • "
    f"Categorical/string fields: {len(categorical_columns)} • "
    f"Temporal-signal fields: {len(temporal_columns)}"
)


# -----------------------------------------------------------------------------
# 10. EVIDENCE STATUS
# -----------------------------------------------------------------------------

with st.expander("Evidence and scope status", expanded=False):

    st.warning(
        "Numeric fields shown below are observable dataset fields. "
        "They are NOT automatically approved business KPIs."
    )

    for limitation, detail in KNOWN_LIMITATIONS.items():
        st.markdown(f"**{limitation}:** {detail}")

    st.markdown(
        "**Join control:** No cross-dataset join is performed by this application."
    )

    st.markdown(
        "**ML control:** No prediction, forecasting, recommendation, churn, "
        "retention, or fraud model output is displayed."
    )


# -----------------------------------------------------------------------------
# 11. COLUMN-LEVEL EXPLORATION
# -----------------------------------------------------------------------------

st.subheader("Dataset Exploration")

if not len(df.columns):
    st.warning("This analytical dataset contains no columns.")
    st.stop()

selected_columns = st.multiselect(
    "Columns to inspect",
    options=list(df.columns),
    default=list(df.columns[: min(8, len(df.columns))]),
)

if selected_columns:

    preview_rows = st.slider(
        "Preview rows",
        min_value=5,
        max_value=min(100, max(5, len(df))),
        value=min(20, max(5, len(df))),
        step=5,
    )

    st.dataframe(
        df[selected_columns].head(preview_rows),
        width="stretch",
        hide_index=True,
    )

else:
    st.caption("Select one or more columns to display a preview.")


# -----------------------------------------------------------------------------
# 12. NUMERIC DESCRIPTIVE ANALYSIS
# -----------------------------------------------------------------------------

st.subheader("Descriptive Numeric Analysis")

if not numeric_columns:

    st.caption("No numeric columns are available in this dataset.")

else:

    selected_numeric = st.selectbox(
        "Numeric field",
        numeric_columns,
    )

    numeric_series = pd.to_numeric(
        df[selected_numeric],
        errors="coerce",
    )

    valid_numeric = numeric_series.dropna()

    stat_col_1, stat_col_2, stat_col_3, stat_col_4 = st.columns(4)

    with stat_col_1:
        st.metric("Non-null values", f"{valid_numeric.size:,}")

    with stat_col_2:
        st.metric(
            "Missing values",
            f"{numeric_series.isna().sum():,}",
        )

    with stat_col_3:
        st.metric(
            "Minimum",
            format_number(valid_numeric.min())
            if not valid_numeric.empty
            else "—",
        )

    with stat_col_4:
        st.metric(
            "Maximum",
            format_number(valid_numeric.max())
            if not valid_numeric.empty
            else "—",
        )

    if not valid_numeric.empty:

        summary = pd.DataFrame(
            {
                "Statistic": [
                    "Count",
                    "Mean",
                    "Median",
                    "Std. deviation",
                    "Minimum",
                    "25th percentile",
                    "75th percentile",
                    "Maximum",
                ],
                "Value": [
                    valid_numeric.count(),
                    valid_numeric.mean(),
                    valid_numeric.median(),
                    valid_numeric.std(),
                    valid_numeric.min(),
                    valid_numeric.quantile(0.25),
                    valid_numeric.quantile(0.75),
                    valid_numeric.max(),
                ],
            }
        )

        st.dataframe(
            summary,
            width="stretch",
            hide_index=True,
        )

        chart_type = st.selectbox(
            "Numeric visualization",
            [
                "Histogram",
                "Box plot",
            ],
        )

        if chart_type == "Histogram":

            fig = px.histogram(
                df,
                x=selected_numeric,
                title=f"Distribution of {selected_numeric}",
                marginal="box",
            )

        else:

            fig = px.box(
                df,
                y=selected_numeric,
                points="outliers",
                title=f"Distribution of {selected_numeric}",
            )

        fig.update_layout(
            height=480,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )


# -----------------------------------------------------------------------------
# 13. CATEGORICAL DESCRIPTIVE ANALYSIS
# -----------------------------------------------------------------------------

st.subheader("Categorical / Dimension Exploration")

if not categorical_columns:

    st.caption(
        "No categorical/string fields are available in this dataset."
    )

else:

    selected_category = st.selectbox(
        "Categorical field",
        categorical_columns,
    )

    category_counts = (
        df[selected_category]
        .astype("string")
        .fillna("<NULL>")
        .value_counts(dropna=False)
        .head(30)
        .rename_axis(selected_category)
        .reset_index(name="row_count")
    )

    st.dataframe(
        category_counts,
        width="stretch",
        hide_index=True,
    )

    if not category_counts.empty:

        category_chart = px.bar(
            category_counts,
            x="row_count",
            y=selected_category,
            orientation="h",
            title=f"Top observed values — {selected_category}",
        )

        category_chart.update_layout(
            height=max(
                420,
                min(900, 250 + len(category_counts) * 20),
            ),
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            category_chart,
            width="stretch",
        )


# -----------------------------------------------------------------------------
# 14. TEMPORAL-SIGNAL EXPLORATION
# -----------------------------------------------------------------------------

st.subheader("Temporal-Signal Exploration")

if not temporal_columns:

    st.caption(
        "No temporal-signal fields were identified by the current "
        "conservative field-name/type detection."
    )

else:

    selected_temporal = st.selectbox(
        "Temporal-signal field",
        temporal_columns,
    )

    parsed_temporal = pd.to_datetime(
        df[selected_temporal],
        errors="coerce",
    )

    temporal_valid = parsed_temporal.dropna()

    if temporal_valid.empty:

        st.warning(
            f"`{selected_temporal}` could not be parsed into usable "
            "datetime values under the current conservative parser."
        )

    else:

        temporal_frame = pd.DataFrame(
            {"timestamp": temporal_valid}
        )

        temporal_frame["date"] = (
            temporal_frame["timestamp"].dt.floor("D")
        )

        daily_counts = (
            temporal_frame
            .groupby("date", dropna=False)
            .size()
            .reset_index(name="row_count")
        )

        temporal_fig = px.line(
            daily_counts,
            x="date",
            y="row_count",
            markers=True,
            title=(
                f"Observed row count over time — "
                f"{selected_temporal}"
            ),
        )

        temporal_fig.update_layout(
            height=480,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            temporal_fig,
            width="stretch",
        )

        st.caption(
            "This is an observed row-count visualization. "
            "It is not a forecast or business trend claim."
        )


# -----------------------------------------------------------------------------
# 15. DATA QUALITY SNAPSHOT
# -----------------------------------------------------------------------------

st.subheader("Dataset Quality Snapshot")

quality_frame = pd.DataFrame(
    {
        "column": df.columns,
        "dtype": [
            str(df[column].dtype)
            for column in df.columns
        ],
        "non_null_count": [
            int(df[column].notna().sum())
            for column in df.columns
        ],
        "missing_count": [
            int(df[column].isna().sum())
            for column in df.columns
        ],
        "missing_pct": [
            round(float(df[column].isna().mean() * 100), 2)
            for column in df.columns
        ],
        "unique_count": [
            int(df[column].nunique(dropna=True))
            for column in df.columns
        ],
    }
)

st.dataframe(
    quality_frame,
    width="stretch",
    hide_index=True,
)


# -----------------------------------------------------------------------------
# 16. ANALYTICAL BOUNDARY
# -----------------------------------------------------------------------------

st.divider()

st.subheader("Current Analytical Boundary")

boundary_col_1, boundary_col_2 = st.columns(2)

with boundary_col_1:

    st.markdown("### Currently available")

    st.markdown(
        """
        - Dataset-specific descriptive exploration
        - Numeric distributions
        - Categorical value distributions
        - Temporal-signal exploration
        - Dataset quality inspection
        - Interactive dataset/field selection
        - Plotly visual exploration
        """
    )

with boundary_col_2:

    st.markdown("### Not activated")

    st.markdown(
        """
        - Final business KPI certification
        - Cross-dataset joins
        - Revenue/profit/ROI claims without evidence
        - Forecasting
        - ML predictions
        - Recommendations
        - Churn/retention prediction
        - Fraud detection
        """
    )

st.caption(
    "PurjeStore • Evidence-bounded dashboard foundation • "
    "Major Milestone 8.3"
)