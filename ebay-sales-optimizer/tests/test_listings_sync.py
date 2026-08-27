"""Tests for the GetMyeBaySelling parser and the idempotent listing upsert.

These prove step 9 deterministically (double sync => no duplicate rows) without
needing live eBay credentials, by feeding the parser a representative XML page
and upserting the same data twice into an in-memory SQLite DB.
"""

from __future__ import annotations

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.database.models import Base, Listing
from app.database.repository import upsert_listings
from app.ebay.listings import parse_active_list

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<GetMyeBaySellingResponse xmlns="urn:ebay:apis:eBLBaseComponents">
  <Ack>Success</Ack>
  <ActiveList>
    <PaginationResult>
      <TotalNumberOfPages>1</TotalNumberOfPages>
      <TotalNumberOfEntries>2</TotalNumberOfEntries>
    </PaginationResult>
    <ItemArray>
      <Item>
        <ItemID>110111222333</ItemID>
        <SKU>BMW-INT-001</SKU>
        <Title>BMW E90 Interior Trim Clip Set OEM Style</Title>
        <Quantity>10</Quantity>
        <PrimaryCategory>
          <CategoryID>33694</CategoryID>
          <CategoryName>Vehicle Parts</CategoryName>
        </PrimaryCategory>
        <SellingStatus>
          <CurrentPrice currencyID="EUR">14.99</CurrentPrice>
          <QuantitySold>3</QuantitySold>
          <ListingStatus>Active</ListingStatus>
        </SellingStatus>
        <ListingDetails>
          <StartTime>2026-07-01T10:00:00.000Z</StartTime>
        </ListingDetails>
      </Item>
      <Item>
        <ItemID>110444555666</ItemID>
        <Title>Door Handle Cover Set</Title>
        <Quantity>5</Quantity>
        <SellingStatus>
          <CurrentPrice currencyID="EUR">7.50</CurrentPrice>
          <ListingStatus>Active</ListingStatus>
        </SellingStatus>
      </Item>
    </ItemArray>
  </ActiveList>
</GetMyeBaySellingResponse>"""


def _memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_parser_extracts_core_fields() -> None:
    listings, total_pages = parse_active_list(SAMPLE_XML)
    assert total_pages == 1
    assert len(listings) == 2

    a = {x.ebay_listing_id: x for x in listings}
    first = a["110111222333"]
    assert first.sku == "BMW-INT-001"
    assert first.title.startswith("BMW E90")
    assert first.price == 14.99
    assert first.currency == "EUR"
    assert first.quantity == 7  # 10 total - 3 sold = 7 available
    assert first.category_id == "33694"
    assert first.category_name == "Vehicle Parts"
    assert first.listing_status == "Active"
    assert first.listing_start_date.startswith("2026-07-01")
    # Fields GetMyeBaySelling does not return must be None, never fabricated.
    assert first.item_specifics is None
    assert first.shipping_cost is None

    second = a["110444555666"]
    assert second.sku is None
    assert second.quantity == 5  # no QuantitySold => total used as-is


def test_upsert_is_idempotent() -> None:
    listings, _ = parse_active_list(SAMPLE_XML)
    session = _memory_session()

    r1 = upsert_listings(session, listings)
    session.commit()
    assert r1.inserted == 2 and r1.updated == 0

    # Second identical sync: everything is an update, nothing new.
    r2 = upsert_listings(session, listings)
    session.commit()
    assert r2.inserted == 0 and r2.updated == 2

    # The table still holds exactly 2 rows — no duplicates.
    count = session.execute(select(func.count()).select_from(Listing)).scalar_one()
    assert count == 2

    # first_seen_at is stable; last_seen_at advances (>= first_seen_at).
    row = session.execute(
        select(Listing).where(Listing.ebay_listing_id == "110111222333")
    ).scalar_one()
    assert row.last_seen_at >= row.first_seen_at


def test_upsert_updates_changed_price() -> None:
    listings, _ = parse_active_list(SAMPLE_XML)
    session = _memory_session()
    upsert_listings(session, listings)
    session.commit()

    listings[0].price = 12.49  # simulate a price change on the next sync
    upsert_listings(session, listings)
    session.commit()

    row = session.execute(
        select(Listing).where(Listing.ebay_listing_id == listings[0].ebay_listing_id)
    ).scalar_one()
    assert row.price == 12.49
    count = session.execute(select(func.count()).select_from(Listing)).scalar_one()
    assert count == 2  # still no duplicate
