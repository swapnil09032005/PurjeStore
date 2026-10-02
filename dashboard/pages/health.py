from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.data import load_refresh_report
from dashboard.utils import format_number


@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def render_data_health() -> None:

    render_page_header(
        "Data & System Health",
        (
            "Technical health of the validated analytical layer "
            "and the latest controlled refresh."
        ),
    )

    report = load_refresh_report()

    if report is None:

        st.error(
            "The latest refresh report is unavailable."
        )

        st.info(
            "No refresh metadata is being invented. "
            "The dashboard will not fabricate a refresh status."
        )

        return

    status = report.get(
        "status",
        "UNKNOWN",
    )

    started = report.get(
        "started_at_utc",
        "—",
    )

    finished = report.get(
        "finished_at_utc",
        "—",
    )

    expected = report.get(
        "dataset_count_expected",
        "—",
    )

    failure = report.get(
        "failure"
    )

    publication = report.get(
        "publication",
        {},
    )

    if isinstance(
        publication,
        dict,
    ):

        publication_status = publication.get(
            "status",
            "UNKNOWN",
        )

    else:

        publication_status = "UNKNOWN"

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Refresh status",
            str(status),
        )

    with col2:

        st.metric(
            "Expected datasets",
            format_number(expected),
        )

    with col3:

        st.metric(
            "Publication",
            str(publication_status),
        )

    st.markdown(
        "### Refresh timestamps"
    )

    timestamp_df = pd.DataFrame(
        [
            {
                "event": "Started (UTC)",
                "timestamp": started,
            },
            {
                "event": "Finished (UTC)",
                "timestamp": finished,
            },
        ]
    )

    st.dataframe(
        timestamp_df,
        width="stretch",
        hide_index=True,
    )

    if failure is not None:

        st.error(
            "The latest controlled refresh reports a failure. "
            "The previous valid analytical state remains the "
            "dashboard's source boundary."
        )

        st.json(
            failure
        )

    datasets = report.get(
        "datasets",
        [],
    )

    if not isinstance(
        datasets,
        list,
    ):

        datasets = []

    st.markdown(
        "### Dataset validation"
    )

    if not datasets:

        st.info(
            "No dataset-level refresh records are available."
        )

    else:

        health_records = []

        for dataset_record in datasets:

            health_records.append(
                {
                    "dataset": dataset_record.get(
                        "dataset",
                        "—",
                    ),
                    "status": dataset_record.get(
                        "status",
                        "—",
                    ),
                    "source_rows": dataset_record.get(
                        "source_rows",
                        "—",
                    ),
                    "output_rows": dataset_record.get(
                        "output_rows",
                        "—",
                    ),
                    "source_fields": dataset_record.get(
                        "source_fields",
                        "—",
                    ),
                    "output_fields": dataset_record.get(
                        "output_fields",
                        "—",
                    ),
                    "grain_nulls": dataset_record.get(
                        "source_grain_nulls",
                        "—",
                    ),
                    "grain_duplicate_values": dataset_record.get(
                        "source_grain_duplicate_values",
                        "—",
                    ),
                    "expected_duplicate_rows": dataset_record.get(
                        "expected_duplicate_rows",
                        "—",
                    ),
                    "actual_duplicate_rows": dataset_record.get(
                        "actual_duplicate_rows",
                        "—",
                    ),
                    "error": dataset_record.get(
                        "error"
                    ),
                }
            )

        health_df = pd.DataFrame(
            health_records
        )

        st.dataframe(
            health_df,
            width="stretch",
            hide_index=True,
        )

    st.markdown(
        "### Validation boundary"
    )

    st.caption(
        "The current refresh report does not contain "
        "refresh_id, rows_processed, rows_published, "
        "schema_changes, or historical refresh count. "
        "Those values are therefore not displayed."
    )