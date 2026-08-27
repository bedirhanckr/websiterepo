"""Buyer-interest eligibility via the Negotiation API (later phase, READ ONLY).

VERIFIED during Phase 1 research (eBay Negotiation API):
  Endpoint : POST /sell/negotiation/v1/find_eligible_items
  Header   : X-EBAY-C-MARKETPLACE-ID: EBAY_DE
  Purpose  : returns listings that have buyers who added the item to their
             Watch list or cart — i.e. listings ELIGIBLE for a seller-initiated
             offer. This is a strong "latent demand" signal for the optimizer.

  STRICT SCOPE FOR THIS PROJECT:
    * We call ONLY find_eligible_items (read).
    * We NEVER call sendOfferToInterestedBuyers (that is a write / buyer-facing
      action) — it is intentionally not implemented anywhere in this codebase.

  LIMITATIONS:
    * Returns eligibility, not counts of watchers per listing.
    * Confirm the exact granted scope for your keyset; eBay documents the
      sell.negotiation family for these calls (some references also cite
      sell.inventory). Resolve at implementation against your app's scopes.
"""

from __future__ import annotations


def fetch_eligible_listing_ids() -> set[str]:
    """Return the set of eBay listing IDs eligible for seller offers. (Later)"""
    raise NotImplementedError(
        "Implemented after Analytics — negotiation eligibility (read-only)."
    )
