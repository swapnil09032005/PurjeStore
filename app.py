from __future__ import annotations

from dashboard.app import run_application_shell
from dashboard.pages.overview import render_executive_overview
from dashboard.pages.commercial import render_commercial_sales
from dashboard.pages.orders import render_orders
from dashboard.pages.products import render_products_catalog
from dashboard.pages.customers import render_customers_accounts
from dashboard.pages.fulfillment import render_fulfillment_shipping
from dashboard.pages.returns import render_returns_exchange
from dashboard.pages.operations import render_operations_inventory
from dashboard.pages.health import render_data_health
from dashboard.pages.explorer import render_technical_explorer

# ============================================================
# PurjeStore — Controlled Dashboard Application
#
# Evidence boundaries:
#   Analytical datasets : 26
#   Analytical rows     : 12,148
#   Analytical columns  : 289
#   Approved page/field : 21
#   Approved pages      : 8
#   Final KPIs          : 0
#   Approved joins      : 0
#   Selected ML         : 0
#
# The dashboard reads the validated analytical layer only.
# It never writes to analytical CSVs.
# ============================================================










APPROVED_MAPPING = [{'dataset': 'daily_category_metrics', 'field': 'order_count', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily category-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_category_metrics', 'field': 'units_sold', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily category-level units sold', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_platform_metrics', 'field': 'total_orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily platform-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_platform_metrics', 'field': 'total_product_views', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily platform-level product-view count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'units_sold', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level units sold', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'cancelled_orders', 'page': 'P01 Executive Overview', 'proposed_meaning': 'Daily vendor-level cancelled-order count', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'payment_transactions', 'field': 'status', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Payment transaction status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'payments', 'field': 'status', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Payment status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'invoices', 'field': 'quantity', 'page': 'P02 Commercial / Sales', 'proposed_meaning': 'Invoice quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'order_items', 'field': 'quantity', 'page': 'P03 Orders', 'proposed_meaning': 'Order-item quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'product', 'field': 'status', 'page': 'P04 Products / Catalog', 'proposed_meaning': 'Product status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'type', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction type', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'method', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction method', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'wallet_transactions', 'field': 'status', 'page': 'P05 Customers / Accounts', 'proposed_meaning': 'Wallet transaction status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'shipment_items', 'field': 'quantity', 'page': 'P06 Fulfillment / Shipping', 'proposed_meaning': 'Shipment-item quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'hub_inventory', 'field': 'quantity', 'page': 'P06 Fulfillment / Shipping', 'proposed_meaning': 'Hub inventory quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'return_request', 'field': 'status', 'page': 'P07 Returns / Exchange', 'proposed_meaning': 'Return-request status', 'aggregation': 'COUNT / FREQUENCY ONLY', 'visualization': 'BAR / TABLE', 'filterable': True, 'reason': 'Explicit categorical/status semantics with observed values suitable for descriptive presentation.'}, {'dataset': 'hub_returns', 'field': 'quantity', 'page': 'P07 Returns / Exchange', 'proposed_meaning': 'Hub-return quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'hub_inventory', 'field': 'quantity', 'page': 'P08 Operations / Inventory', 'proposed_meaning': 'Hub inventory quantity', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}, {'dataset': 'daily_vendor_metrics', 'field': 'product_views', 'page': 'P08 Operations / Inventory', 'proposed_meaning': 'Daily vendor-level product views', 'aggregation': 'COUNT / SUM ONLY WHERE GRAIN SUPPORTS IT', 'visualization': 'BAR / LINE / TABLE', 'filterable': True, 'reason': 'Explicit count/quantity semantics and source-native analytical grain support descriptive use. Not a certified business KPI.'}]


# ============================================================
# Existing reusable data functions
# ============================================================

# ============================================================
# Controlled semantic access
# ============================================================







# ============================================================
# Shared page header
# ============================================================



# ============================================================
# P01 Executive Overview
# ============================================================


# ============================================================
# P02 Commercial / Sales
# ============================================================





# ============================================================
# P04 Products / Catalog
# ============================================================



# ============================================================
# P05 Customers / Accounts
# ============================================================



# ============================================================
# P06 Fulfillment / Shipping
# ============================================================



# ============================================================
# P07 Returns / Exchange
# ============================================================



# ============================================================
# P08 Operations / Inventory
# ============================================================



# ============================================================
# Data & System Health
# ============================================================



# ============================================================
# Technical Dataset Explorer
# ============================================================



# ============================================================
# Application shell
# ============================================================

run_application_shell(
    {
        "P01 Executive Overview": render_executive_overview,
        "P02 Commercial / Sales": render_commercial_sales,
        "P03 Orders": render_orders,
        "P04 Products / Catalog": render_products_catalog,
        "P05 Customers / Accounts": render_customers_accounts,
        "P06 Fulfillment / Shipping": render_fulfillment_shipping,
        "P07 Returns / Exchange": render_returns_exchange,
        "P08 Operations / Inventory": render_operations_inventory,
        "Data & System Health": render_data_health,
        "Technical Dataset Explorer": render_technical_explorer,
    }
)
