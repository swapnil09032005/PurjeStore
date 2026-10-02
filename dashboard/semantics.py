from __future__ import annotations

from typing import Any


_APPROVED_MAPPING: list[dict[str, Any]] | None = None


def configure_approved_mapping(
    mapping: list[dict[str, Any]],
) -> None:
    """
    Configure the authoritative dashboard semantic mapping.

    The root app.py remains the sole owner of APPROVED_MAPPING.
    This module stores only a reference to that existing mapping.

    app.py is intentionally NOT imported here because it is the
    executable Streamlit entry point.
    """
    if not isinstance(mapping, list):
        raise RuntimeError(
            "APPROVED_MAPPING must remain a list of mapping records."
        )

    if not all(
        isinstance(record, dict)
        for record in mapping
    ):
        raise RuntimeError(
            "APPROVED_MAPPING must contain dictionary mapping records."
        )

    global _APPROVED_MAPPING

    _APPROVED_MAPPING = mapping


def approved_mapping() -> list[dict[str, Any]]:
    """
    Return the authoritative configured dashboard mapping.

    This is read-only access. The semantic layer does not own,
    reconstruct, or duplicate the mapping.
    """
    if _APPROVED_MAPPING is None:
        raise RuntimeError(
            "APPROVED_MAPPING has not been configured by the "
            "root dashboard entry point."
        )

    return _APPROVED_MAPPING


def approved_records_for_page(
    page_name: str,
) -> list[dict[str, Any]]:
    """
    Return approved semantic records for the requested dashboard page.
    """
    return [
        record
        for record in approved_mapping()
        if record.get("page") == page_name
    ]


def safe_display_label(
    record: dict[str, Any],
) -> str:
    """
    Return the approved semantic meaning when available.

    If no proposed meaning exists, derive a safe display label
    from the field name without changing the underlying contract.
    """
    proposed_meaning = record.get(
        "proposed_meaning"
    )

    if proposed_meaning:
        return str(proposed_meaning)

    field_name = str(
        record.get(
            "field",
            "",
        )
    )

    if not field_name:
        return ""

    return (
        field_name
        .replace("_", " ")
        .strip()
        .title()
    )