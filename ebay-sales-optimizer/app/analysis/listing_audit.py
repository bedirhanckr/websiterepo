"""Listing data-quality audit (Phase 4 implementation). Warnings only.

Produces warnings for the seller to review. It NEVER edits a listing and NEVER
invents OEM numbers or vehicle-compatibility facts. Thresholds live in
``config/analysis_rules.yaml`` under ``audit``.

Checks (from the brief; automotive/BMW focus for ZB Design):
  * missing SKU
  * missing item specifics
  * very short title (< audit.min_title_length)
  * repeated keyword tokens (> audit.max_keyword_repeat)
  * suspicious OEM/reference numbers (implausible length/format — flagged for
    HUMAN verification; the tool does not assert correctness of any part number)
  * duplicate/inconsistent part numbers across listings
  * suspicious price change between syncs (> audit.suspicious_price_change_ratio)
  * zero inventory
  * malformed / unparseable data

Output is a list of structured warnings {listing_id, code, message, severity}.
"""

from __future__ import annotations


def audit_listings(*args, **kwargs):  # finalised in Phase 4
    """Return a list of data-quality warnings across the catalogue."""
    raise NotImplementedError("Implemented in Phase 4 — listing audit.")
