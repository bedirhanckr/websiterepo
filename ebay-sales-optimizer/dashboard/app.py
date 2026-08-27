"""Streamlit dashboard (Phase 4 implementation).

Planned views (all READ-ONLY over the local SQLite DB):
  * Store overview  — active listings, total impressions/views, avg CTR,
    transactions, quantity sold, avg conversion, revenue, ad spend, ad revenue
    (each shown as "unavailable" when the source metric is NULL).
  * Top Opportunities — sortable table (listing id, title, price, impressions,
    views, CTR, transactions, conversion, opportunity score, problem type,
    severity), sorted by opportunity score descending by default.
  * Listing detail — basic info, 7d & 30d performance, trend over time,
    advertising performance, classification, evidence, recommendation, and the
    explicit "what NOT to do" guardrail.

Run:  streamlit run dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import streamlit as st
except ModuleNotFoundError:  # keep import-safe before deps are installed
    st = None


def main() -> None:
    if st is None:
        print("Install requirements first: pip install -r requirements.txt")
        return
    st.set_page_config(page_title="eBay Sales Optimizer", layout="wide")
    st.title("eBay Sales Optimizer — ZB Design (EBAY_DE)")
    st.info(
        "Phase 1 skeleton. Store overview, Top Opportunities and Listing detail "
        "views are implemented in Phase 4, after data sync (Phase 2–3). "
        "This dashboard is strictly read-only."
    )


if __name__ == "__main__":
    main()
else:  # `streamlit run` executes the module top-to-bottom
    main()
