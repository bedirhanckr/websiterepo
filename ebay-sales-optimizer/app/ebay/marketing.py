"""Promoted Listings / advertising data via the Marketing API (later phase).

VERIFIED during Phase 1 research (eBay Marketing API):
  Scope   : https://api.ebay.com/oauth/api_scope/sell.marketing.readonly
  Header  : X-EBAY-C-MARKETPLACE-ID: EBAY_DE

  Campaigns:
    GET /sell/marketing/v1/ad_campaign            (getCampaigns)
    -> campaign_id, campaign name, funding model / strategy:
         General  = Cost Per Sale  (CPS)
         Priority = Cost Per Click (CPC)
         Promoted Offsite
  Performance reports (async: create task, then download):
    POST /sell/marketing/v1/ad_report_task        (createReportTask)
    GET  /sell/marketing/v1/ad_report_task/{id}
    Report types include a per-listing daily report with impressions, clicks,
    spend/cost, attributed sales and attributed revenue (used to derive ROAS).

  LIMITATIONS:
    * Advertising data exists ONLY if the seller runs Promoted Listings on
      EBAY_DE. If there are no campaigns, this returns empty — the tool must
      report "no advertising data", not fabricate any.
    * Reports are asynchronous (task create -> poll -> download).
    * Exact metric column names vary by report type; resolved at implementation
      via getReportMetadataForReportType rather than assumed from memory.
    * ROAS = attributed_revenue / spend, computed only when spend > 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class AdRow:
    """One parsed (listing, day, campaign) advertising record (later phase)."""

    ebay_listing_id: str
    day: date
    campaign_id: str
    campaign_name: str | None
    campaign_type: str | None
    ad_rate: float | None
    impressions: int | None
    clicks: int | None
    spend: float | None
    attributed_sales: int | None
    attributed_revenue: float | None
    roas: float | None


def fetch_campaigns() -> list[dict]:
    """List Promoted Listings campaigns. (Later phase)"""
    raise NotImplementedError("Implemented after Analytics — advertising sync.")


def fetch_ad_performance(start: date, end: date) -> list[AdRow]:
    """Retrieve per-listing advertising performance. (Later phase)"""
    raise NotImplementedError("Implemented after Analytics — advertising sync.")
