"""Listing traffic metrics via the Analytics API (Phase 3 implementation).

VERIFIED during Phase 1 research (eBay Analytics API, getTrafficReport):
  Endpoint : GET /sell/analytics/v1/traffic_report
  Scope    : https://api.ebay.com/oauth/api_scope/sell.analytics.readonly
  Grant    : authorization code (seller-scoped)
  Header   : X-EBAY-C-MARKETPLACE-ID: EBAY_DE

  dimension : LISTING  (one row per listing over the range) or
              DAY      (daily series; use per-listing for daily snapshots)
  metric    (exact enum, case-insensitive):
     CLICK_THROUGH_RATE
     LISTING_IMPRESSION_TOTAL   (= SEARCH_RESULTS_PAGE + STORE)
     LISTING_IMPRESSION_SEARCH_RESULTS_PAGE
     LISTING_IMPRESSION_STORE
     LISTING_VIEWS_TOTAL
     LISTING_VIEWS_SOURCE_*      (direct / off_ebay / other_ebay / search / store)
     SALES_CONVERSION_RATE
     TRANSACTION
     TOTAL_IMPRESSION_TOTAL

  filter    : marketplace_ids:{EBAY_DE} and a date_range, e.g.
              [20240101..20240131]  (Pacific/YYYYMMDD) or ISO-8601 w/ offset.

  LIMITATIONS (must be surfaced, not hidden):
    * Maximum 90 days per request. For 7d and 30d we issue separate ranges.
    * Earliest start date is 2 years before today.
    * Data lags: only trust up to the response's ``lastUpdatedDate``.
    * CTR and SALES_CONVERSION_RATE are returned as percentages.
    * Metrics can be absent for a listing/day; store NULL (unknown), never 0.

Mapping to DB (ListingTrafficDaily):
  impressions     <- LISTING_IMPRESSION_TOTAL
  views           <- LISTING_VIEWS_TOTAL
  ctr             <- CLICK_THROUGH_RATE
  transactions    <- TRANSACTION
  conversion_rate <- SALES_CONVERSION_RATE
  quantity_sold   <- derived from TRANSACTION where a per-qty metric is absent
                     (documented as an approximation when exact qty not exposed)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class TrafficRow:
    """One parsed (listing, day) traffic record (Phase 3)."""

    ebay_listing_id: str
    day: date
    impressions: int | None
    views: int | None
    ctr: float | None
    transactions: int | None
    quantity_sold: int | None
    conversion_rate: float | None


def fetch_traffic_report(start: date, end: date) -> list[TrafficRow]:
    """Pull getTrafficReport for the date range and parse rows. (Phase 3)"""
    raise NotImplementedError("Implemented in Phase 3 — Analytics integration.")
