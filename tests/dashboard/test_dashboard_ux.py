from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd

from dashboard.config import ANALYTICAL_ROOT
from dashboard.semantics import (
    approved_records_for_page,
    configure_approved_mapping,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_ROOT = PROJECT_ROOT / "dashboard"
PAGES_ROOT = DASHBOARD_ROOT / "pages"


BUSINESS_PAGE_RENDERERS = {
    "P01 Executive Overview": (
        "overview.py",
        "render_executive_overview",
    ),
    "P02 Commercial / Sales": (
        "commercial.py",
        "render_commercial_sales",
    ),
    "P03 Orders": (
        "orders.py",
        "render_orders",
    ),
    "P04 Products / Catalog": (
        "products.py",
        "render_products_catalog",
    ),
    "P05 Customers / Accounts": (
        "customers.py",
        "render_customers_accounts",
    ),
    "P06 Fulfillment / Shipping": (
        "fulfillment.py",
        "render_fulfillment_shipping",
    ),
    "P07 Returns / Exchange": (
        "returns.py",
        "render_returns_exchange",
    ),
    "P08 Operations / Inventory": (
        "operations.py",
        "render_operations_inventory",
    ),
}


TECHNICAL_PAGE_RENDERERS = {
    "Data & System Health": (
        "health.py",
        "render_data_health",
    ),
    "Technical Dataset Explorer": (
        "explorer.py",
        "render_technical_explorer",
    ),
}


def _read_page_source(filename: str) -> str:
    path = PAGES_ROOT / filename
    return path.read_text(encoding="utf-8-sig")


def _parse_page(filename: str) -> ast.Module:
    path = PAGES_ROOT / filename
    source = path.read_text(encoding="utf-8-sig")
    return ast.parse(source, filename=str(path))


def _function_names(tree: ast.AST) -> set[str]:
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _all_dashboard_page_sources() -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8-sig")
        for path in sorted(PAGES_ROOT.glob("*.py"))
    }


def _configure_authoritative_mapping() -> list[dict]:
    """
    Configure semantics.py from the authoritative root dashboard
    mapping without importing the executable Streamlit entry point.

    The mapping remains owned by app.py. This test reads the literal
    APPROVED_MAPPING assignment from that authoritative source and
    passes the resulting list to the existing semantic adapter.
    """
    source_path = PROJECT_ROOT / "app.py"
    source = source_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(source_path))

    mapping_node = None

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "APPROVED_MAPPING"
                ):
                    mapping_node = node.value
                    break

        if mapping_node is not None:
            break

    assert mapping_node is not None, (
        "Authoritative APPROVED_MAPPING assignment was not found "
        "in root app.py."
    )

    mapping = ast.literal_eval(mapping_node)

    assert isinstance(mapping, list), (
        "Authoritative APPROVED_MAPPING must remain a list."
    )

    assert all(isinstance(record, dict) for record in mapping), (
        "Authoritative APPROVED_MAPPING must contain dictionary records."
    )

    configure_approved_mapping(mapping)

    return mapping


def test_all_business_page_renderers_exist() -> None:
    for page_name, (filename, renderer) in BUSINESS_PAGE_RENDERERS.items():
        path = PAGES_ROOT / filename

        assert path.is_file(), (
            f"{page_name}: expected page module is missing: {path}"
        )

        tree = _parse_page(filename)

        assert renderer in _function_names(tree), (
            f"{page_name}: expected renderer {renderer}() is missing."
        )


def test_all_technical_page_renderers_exist() -> None:
    for page_name, (filename, renderer) in TECHNICAL_PAGE_RENDERERS.items():
        path = PAGES_ROOT / filename

        assert path.is_file(), (
            f"{page_name}: expected technical page module is missing: {path}"
        )

        tree = _parse_page(filename)

        assert renderer in _function_names(tree), (
            f"{page_name}: expected renderer {renderer}() is missing."
        )


def test_business_pages_use_authoritative_semantic_mapping() -> None:
    _configure_authoritative_mapping()

    for page_name, (filename, _renderer) in BUSINESS_PAGE_RENDERERS.items():
        source = _read_page_source(filename)

        assert "approved_records_for_page" in source, (
            f"{page_name}: page must use the authoritative semantic adapter."
        )

        records = approved_records_for_page(page_name)

        assert isinstance(records, list), (
            f"{page_name}: semantic adapter must return a list."
        )

        assert all(isinstance(record, dict) for record in records), (
            f"{page_name}: semantic records must remain dictionaries."
        )


def test_exactly_21_approved_dashboard_records_remain_represented() -> None:
    _configure_authoritative_mapping()

    records = []

    for page_name in BUSINESS_PAGE_RENDERERS:
        records.extend(
            approved_records_for_page(page_name)
        )

    assert len(records) == 21

    identity_records = {
        (
            record.get("page"),
            record.get("dataset"),
            record.get("field"),
        )
        for record in records
    }

    assert len(identity_records) == 21


def test_approved_records_have_required_semantic_contract_fields() -> None:
    _configure_authoritative_mapping()

    required_fields = {
        "page",
        "dataset",
        "field",
        "proposed_meaning",
        "aggregation",
        "visualization",
        "filterable",
        "reason",
    }

    records = []

    for page_name in BUSINESS_PAGE_RENDERERS:
        records.extend(
            approved_records_for_page(page_name)
        )

    assert len(records) == 21

    for record in records:
        missing = required_fields - set(record)

        assert not missing, (
            f"Approved record is missing required fields: {missing}. "
            f"Record={record}"
        )


def test_business_pages_do_not_directly_read_analytical_csv_files() -> None:
    forbidden_patterns = (
        ".read_csv(",
        "pd.read_csv(",
        "Path.read_text(",
    )

    for page_name, (filename, _renderer) in BUSINESS_PAGE_RENDERERS.items():
        source = _read_page_source(filename)

        violations = [
            pattern
            for pattern in forbidden_patterns
            if pattern in source
        ]

        assert not violations, (
            f"{page_name}: direct analytical/source reads detected: "
            f"{violations}"
        )


def test_business_pages_do_not_introduce_joins_or_analytical_writes() -> None:
    forbidden_patterns = {
        "pd.merge(": "join",
        ".merge(": "join",
        "pd.concat(": "concatenation",
        ".to_csv(": "write",
        ".to_excel(": "write",
        ".to_parquet(": "write",
        ".to_sql(": "write",
        "predict(": "prediction",
        "Pipeline(": "ML pipeline",
    }

    for page_name, (filename, _renderer) in BUSINESS_PAGE_RENDERERS.items():
        source = _read_page_source(filename)

        violations = [
            f"{pattern} ({meaning})"
            for pattern, meaning in forbidden_patterns.items()
            if pattern in source
        ]

        assert not violations, (
            f"{page_name}: forbidden analytical/ML operations detected: "
            f"{violations}"
        )


def test_technical_pages_remain_separate_from_business_semantic_mapping() -> None:
    for page_name, (filename, _renderer) in TECHNICAL_PAGE_RENDERERS.items():
        source = _read_page_source(filename)

        assert "render_page_header" in source, (
            f"{page_name}: expected shared page-header architecture."
        )

        assert "approved_records_for_page" not in source, (
            f"{page_name}: technical page must not render business "
            "semantic records directly."
        )


def test_explorer_remains_read_only_and_uses_data_access_layer() -> None:
    source = _read_page_source("explorer.py")

    assert "discover_analytical_files" in source
    assert "load_dataset" in source
    assert "ANALYTICAL_ROOT" in source

    forbidden_patterns = (
        ".to_csv(",
        ".to_excel(",
        ".to_parquet(",
        ".to_sql(",
        "pd.merge(",
        ".merge(",
        "pd.concat(",
        "predict(",
        "Pipeline(",
        "fit(",
    )

    violations = [
        pattern
        for pattern in forbidden_patterns
        if pattern in source
    ]

    assert not violations, (
        "Technical Dataset Explorer contains forbidden write/join/ML "
        f"operations: {violations}"
    )


def test_health_remains_connected_to_refresh_report_architecture() -> None:
    source = _read_page_source("health.py")

    assert "load_refresh_report" in source, (
        "Data & System Health must use the existing refresh-report "
        "architecture."
    )

    assert "refresh" in source.lower()


def test_analytical_baseline_remains_readable_and_source_native() -> None:
    files = sorted(
        ANALYTICAL_ROOT.glob("*.csv")
    )

    assert len(files) == 26

    total_rows = 0
    total_columns = 0

    for path in files:
        df = pd.read_csv(path)

        total_rows += len(df)
        total_columns += len(df.columns)

    assert total_rows == 12_148
    assert total_columns == 289


def test_dashboard_page_modules_compile_as_valid_python() -> None:
    for path in sorted(PAGES_ROOT.glob("*.py")):
        if path.name == "__init__.py":
            continue

        tree = _parse_page(path.name)

        assert isinstance(tree, ast.Module)


def test_dashboard_pages_do_not_contain_executable_ml_operations() -> None:
    """
    Detect actual ML imports/calls rather than words appearing in
    evidence-boundary text such as "forecasting is not supported".
    """

    sources = _all_dashboard_page_sources()

    for filename, source in sources.items():
        tree = ast.parse(
            source,
            filename=str(PAGES_ROOT / filename),
        )

        executable_ml_calls = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    call_name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    call_name = node.func.id
                else:
                    continue

                if call_name in {
                    "fit",
                    "predict",
                    "predict_proba",
                }:
                    executable_ml_calls.append(call_name)

            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.lower().startswith(
                        "sklearn"
                    ):
                        executable_ml_calls.append(
                            f"import {alias.name}"
                        )

            if isinstance(node, ast.ImportFrom):
                module = (node.module or "").lower()

                if module.startswith("sklearn"):
                    executable_ml_calls.append(
                        f"from {node.module}"
                    )

        assert not executable_ml_calls, (
            f"{filename}: executable ML operations detected: "
            f"{executable_ml_calls}"
        )


def test_business_page_record_counts_match_approved_mapping() -> None:
    _configure_authoritative_mapping()

    expected_counts = {
        "P01 Executive Overview": 7,
        "P02 Commercial / Sales": 3,
        "P03 Orders": 1,
        "P04 Products / Catalog": 1,
        "P05 Customers / Accounts": 3,
        "P06 Fulfillment / Shipping": 2,
        "P07 Returns / Exchange": 2,
        "P08 Operations / Inventory": 2,
    }

    for page_name, expected in expected_counts.items():
        actual = len(
            approved_records_for_page(page_name)
        )

        assert actual == expected, (
            f"{page_name}: expected {expected} approved records, "
            f"found {actual}."
        )