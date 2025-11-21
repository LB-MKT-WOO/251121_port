"""Configuration constants for the performance dashboard."""

import os

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/13cgCbIF_R4ubaNyIKdW0YY3VUZM0TUozRR3GyZ6vl8A/edit?gid=965675010"
SHEET_NAME = "raw(META,UAC,Twitter)"
CREDENTIALS_FILE = os.path.join(os.path.expanduser('~'), 'access_file', 'python-project-389308-bccaee8d3d37.json')

# Data schema
DIMENSIONS = ["source", "campaign_name", "creative_name", "sub_campaign_name"]
DATE_COL = "Date"
METRICS = [
    "impressions", "clicks", "installs", "cost",
    "create_account_7d", "deposit_1d", "deposit_30d",
    "initial_offering_30d", "integration_account_7d", "signup_7d",
    "trade_buy_1d", "trade_buy_7d",
    "deposit_revenue_1d", "deposit_revenue_30d", "initial_offering_revenue_30d"
]
REQUIRED_COLS = [DATE_COL] + DIMENSIONS + METRICS

# Product dates file
PRODUCT_DATES_FILE = os.path.join("configs", "product_dates.json")

