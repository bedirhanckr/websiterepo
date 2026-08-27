"""Database write helpers (local SQLite only — never writes to eBay).

The listing upsert is idempotent: it matches on the natural key
``ebay_listing_id``, inserts new rows once, and updates existing rows in place.
Running a sync twice therefore does not create duplicate rows.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Listing
from app.ebay.listings import ParsedListing


@dataclass
class UpsertResult:
    inserted: int
    updated: int

    @property
    def total(self) -> int:
        return self.inserted + self.updated


def _parse_start_date(value: str | None) -> datetime | None:
    if not value:
        return None
    # eBay returns ISO-8601 with a trailing Z (UTC).
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def upsert_listings(session: Session, parsed: list[ParsedListing]) -> UpsertResult:
    """Insert or update listings by ``ebay_listing_id``. Idempotent."""
    now = datetime.now(timezone.utc)
    inserted = 0
    updated = 0

    for p in parsed:
        existing = session.execute(
            select(Listing).where(Listing.ebay_listing_id == p.ebay_listing_id)
        ).scalar_one_or_none()

        specifics_json = (
            json.dumps(p.item_specifics, ensure_ascii=False)
            if p.item_specifics is not None
            else None
        )
        start_date = _parse_start_date(p.listing_start_date)

        if existing is None:
            session.add(
                Listing(
                    ebay_listing_id=p.ebay_listing_id,
                    sku=p.sku,
                    title=p.title,
                    category_id=p.category_id,
                    category_name=p.category_name,
                    price=p.price,
                    currency=p.currency,
                    quantity=p.quantity,
                    condition=p.condition,
                    listing_status=p.listing_status,
                    listing_start_date=start_date,
                    item_specifics_json=specifics_json,
                    shipping_cost=p.shipping_cost,
                    shipping_service=p.shipping_service,
                    first_seen_at=now,
                    last_seen_at=now,
                )
            )
            inserted += 1
        else:
            existing.sku = p.sku
            existing.title = p.title
            existing.category_id = p.category_id
            existing.category_name = p.category_name
            existing.price = p.price
            existing.currency = p.currency
            existing.quantity = p.quantity
            existing.condition = p.condition
            existing.listing_status = p.listing_status
            if start_date is not None:
                existing.listing_start_date = start_date
            if specifics_json is not None:
                existing.item_specifics_json = specifics_json
            if p.shipping_cost is not None:
                existing.shipping_cost = p.shipping_cost
            if p.shipping_service is not None:
                existing.shipping_service = p.shipping_service
            existing.last_seen_at = now
            updated += 1

    return UpsertResult(inserted=inserted, updated=updated)
