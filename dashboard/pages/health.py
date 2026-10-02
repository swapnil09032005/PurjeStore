from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.header import render_page_header
from dashboard.data import load_refresh_report
from dashboard.utils import format_number


def _render_refresh_summary(report: dict) -> None:
    st.subheader("Current Controlled Refresh")

    status = report.get("status", "UNKNOWN")
    expected = report.get("dataset_count_expected", "-")

    publication = report.get("publication", {})

    if isinstance(publication, dict):
        publication_status = publication.get("status", "UNKNOWN")
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
            "Publication status",
            str(publication_status),
        )


def _render_refresh_timestamps(report: dict) -> None:
    st.subheader("Refresh Timestamps")

    started = report.get("started_at_utc", "-")
    finished = report.get("finished_at_utc", "-")

    timestamp_df = pd.DataFrame(
        [
            {
                "Event": "Started (UTC)",
                "Timestamp": started,
            },
            {
                "Event": "Finished (UTC)",
                "Timestamp": finished,
            },
        ]
    )

    st.dataframe(
        timestamp_df,
        width="stretch",
        hide_index=True,
    )


def _render_refresh_failure(report: dict) -> None:
    failure = report.get("failure")

    if failure is None:
        return

    st.subheader("Refresh Failure")

    st.error(
        "The latest controlled refresh reports a failure. "
        "The previous valid analytical state remains the "
        "dashboard source boundary."
    )

    st.json(failure)


def _render_dataset_validation(report: dict) -> None:
    st.subheader("Dataset Validation")

    datasets = report.get("datasets", [])

    if not isinstance(datasets, list):
        datasets = []

    if not datasets:
        st.info(
            "No dataset-level refresh records are available."
        )
        return

    health_records = []

    for dataset_record in datasets:
        if not isinstance(dataset_record, dict):
            continue

        health_records.append(
            {
                "Dataset": dataset_record.get(
                    "dataset",
                    "-",
                ),
                "Status": dataset_record.get(
                    "status",
                    "-",
                ),
                "Source rows": dataset_record.get(
                    "source_rows",
                    "-",
                ),
                "Output rows": dataset_record.get(
                    "output_rows",
                    "-",
                ),
                "Source fields": dataset_record.get(
                    "source_fields",
                    "-",
                ),
                "Output fields": dataset_record.get(
                    "output_fields",
                    "-",
                ),
                "Grain nulls": dataset_record.get(
                    "source_grain_nulls",
                    "-",
                ),
                "Grain duplicate values": dataset_record.get(
                    "source_grain_duplicate_values",
                    "-",
                ),
                "Expected duplicate rows": dataset_record.get(
                    "expected_duplicate_rows",
                    "-",
                ),
                "Actual duplicate rows": dataset_record.get(
                    "actual_duplicate_rows",
                    "-",
                ),
                "Error": dataset_record.get(
                    "error"
                ),
            }
        )

    if not health_records:
        st.info(
            "No valid dataset-level refresh records are available."
        )
        return

    health_df = pd.DataFrame(health_records)

    st.dataframe(
        health_df,
        width="stretch",
        hide_index=True,
    )


def _render_validation_boundary(report: dict) -> None:
    st.subheader("Validation Boundary")

    st.info(
        "This page reports only technical information contained "
        "in the latest controlled analytical refresh report. "
        "Refresh status and publication status are technical "
        "states, not business KPIs. The dashboard does not "
        "invent refresh identifiers, processed-row metrics, "
        "published-row metrics, schema-change history, or "
        "historical refresh counts when those values are absent "
        "from the report."
    )

    st.caption(
        "The analytical layer remains read-only from the dashboard. "
        "Refresh execution and publication remain owned by the "
        "controlled refresh pipeline."
    )


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

    _render_refresh_summary(report)
    _render_refresh_timestamps(report)
    _render_refresh_failure(report)
    _render_dataset_validation(report)
    _render_validation_boundary(report)