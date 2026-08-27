"""Active-listing retrieval (Phase 2 implementation).

CHOSEN SOURCE — Trading API ``GetMyeBaySelling`` (ActiveList):
  Verified during Phase 1 research. Rationale for a small seller:
    * Returns ALL currently active listings for the authenticated seller,
      including legacy listings created through the eBay web UI. This is the
      decisive point: the Sell **Inventory API** (``getInventoryItems``) only
      returns items created/migrated through the Inventory model, so listings
      made in the eBay UI are typically invisible to it. For an existing seller
      we cannot assume everything was created via the Inventory API.
    * Simple for small catalogues; 25,000-item cap is irrelevant here.
    * Rate limit is generous (300 calls / 15s per seller).

  Trade-off: Trading API is XML over HTTPS (legacy), not REST/JSON. We accept
  that because completeness beats elegance for this objective.

Fields we parse per listing (mark unavailable, never fabricate, if absent):
  ItemID, SKU, Title, PrimaryCategory (ID + Name), price + currency, Quantity,
  ConditionDisplayName, listing status, StartTime, item specifics, shipping.

Fallback/augmentation (optional, later): the Sell **Inventory API**
(``sell.inventory.readonly``) and the Browse API can enrich specifics for
Inventory-model items. Not required for the MVP.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParsedListing:
    """Normalised listing record produced by the parser (Phase 2)."""

    ebay_listing_id: str
    sku: str | None
    title: str | None
    category_id: str | None
    category_name: str | None
    price: float | None
    currency: str | None
    quantity: int | None
    condition: str | None
    listing_status: str | None
    listing_start_date: str | None
    item_specifics: dict | None
    shipping_cost: float | None
    shipping_service: str | None


def fetch_active_listings() -> list[ParsedListing]:
    """Fetch + parse all active listings via GetMyeBaySelling. (Phase 2)"""
    raise NotImplementedError("Implemented in Phase 2 — listing sync.")
