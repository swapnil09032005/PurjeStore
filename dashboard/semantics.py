"""
PurjeStore Dashboard Semantic Access

This module is a narrow adapter around the existing executable dashboard
semantic mapping.

Authoritative semantic boundaries remain in:
    docs/analytical/DASHBOARD_DATA_MAPPING_AND_SEMANTIC_CONTRACT.md

During the behavior-preserving dashboard refactor, the existing
APPROVED_MAPPING in app.py remains the executable mapping source.

Responsibilities:
- Expose the existing APPROVED_MAPPING.
- Filter approved records by dashboard page.
- Produce the existing controlled display-label behavior.

This module must NOT:
- Redefine APPROVED_MAPPING.
- Add or remove approved fields.
- Approve new KPIs.
- Create joins.
- Create analytical datasets.
- Add ML logic.
- Infer business meaning from data types.
- Change semantic approval decisions.
"""

from __future__ import annotations

from typing import Any


def _load_existing_mapping() -> list[dict[str, Any]]:
    """
    Load the existing executable APPROVED_MAPPING from app.py.

    The import is intentionally deferred until the function is called so
    this adapter does not execute the Streamlit application during module
    import.

    Returns
    -------
    list[dict[str, Any]]
        Existing approved dashboard mapping records.

    Raises
    ------
    RuntimeError
        If the existing mapping cannot be imported or is not a list.
    """
    try:
        from app import APPROVED_MAPPING
    except Exception as exc:
        raise RuntimeError(
            "Unable to load the existing APPROVED_MAPPING from app.py."
        ) from exc

    if not isinstance(APPROVED_MAPPING, list):
        raise RuntimeError(
            "app.APPROVED_MAPPING must remain a list of mapping records."
        )

    return APPROVED_MAPPING


def approved_mapping() -> list[dict[str, Any]]:
    """
    Return the existing executable approved dashboard mapping.

    No records are created, modified, filtered, or reordered here.

    Returns
    -------
    list[dict[str, Any]]
        Existing APPROVED_MAPPING records.
    """
    return _load_existing_mapping()


def approved_records_for_page(page_name: str) -> list[dict[str, Any]]:
    """
    Return existing approved mapping records for one dashboard page.

    Parameters
    ----------
    page_name:
        Exact dashboard page name.

    Returns
    -------
    list[dict[str, Any]]
        Approved records whose ``page`` equals ``page_name``.
    """
    return [
        record
        for record in approved_mapping()
        if record.get("page") == page_name
    ]


def safe_display_label(record: dict[str, Any]) -> str:
    """
    Preserve the existing controlled dashboard display-label behavior.

    ``proposed_meaning`` remains the preferred label. If it is absent or
    empty, the analytical field name is converted into a readable title.

    Parameters
    ----------
    record:
        Existing approved mapping record.

    Returns
    -------
    str
        Controlled display label.
    """
    proposed_meaning = record.get("proposed_meaning")

    if proposed_meaning:
        return str(proposed_meaning)

    field_name = str(record.get("field", ""))

    if not field_name:
        return ""

    return field_name.replace("_", " ").strip().title()