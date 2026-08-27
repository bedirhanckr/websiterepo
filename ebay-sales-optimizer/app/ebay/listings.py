"""Active-listing retrieval via Trading API ``GetMyeBaySelling`` — READ-ONLY.

Rationale for the Trading API over the Sell Inventory API is documented in
IMPLEMENTATION_PLAN.md: ``getInventoryItems`` only returns Inventory-model items,
so listings created in the eBay web UI would be missed. ``GetMyeBaySelling``
returns *all* active listings for the authenticated seller.

Many detail fields (item specifics, shipping, category name, start time) are not
returned by GetMyeBaySelling. Per the project rule, those are stored as NULL
("unavailable"), never fabricated. The core fields the seller asked for — item
id, title, price, quantity, SKU — are present.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass

from app.ebay.client import EbayApiError, trading_call

_CALL = "GetMyeBaySelling"


@dataclass
class ParsedListing:
    """Normalised active-listing record."""

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


# ---- namespace-agnostic XML helpers ----------------------------------------
def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _find(elem: ET.Element | None, name: str) -> ET.Element | None:
    if elem is None:
        return None
    for child in elem:
        if _local(child.tag) == name:
            return child
    return None


def _find_deep(elem: ET.Element | None, path: list[str]) -> ET.Element | None:
    cur = elem
    for name in path:
        cur = _find(cur, name)
        if cur is None:
            return None
    return cur


def _findall(elem: ET.Element | None, name: str) -> list[ET.Element]:
    if elem is None:
        return []
    return [c for c in elem if _local(c.tag) == name]


def _text(elem: ET.Element | None) -> str | None:
    if elem is None or elem.text is None:
        return None
    val = elem.text.strip()
    return val or None


def _to_float(elem: ET.Element | None) -> float | None:
    t = _text(elem)
    if t is None:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _to_int(elem: ET.Element | None) -> int | None:
    t = _text(elem)
    if t is None:
        return None
    try:
        return int(t)
    except ValueError:
        return None


# ---- request building -------------------------------------------------------
def build_request(page_number: int, entries_per_page: int) -> str:
    """Build a GetMyeBaySelling ActiveList request (OAuth: no RequesterCredentials)."""
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">'
        "<ActiveList>"
        "<Sort>TimeLeft</Sort>"
        "<Pagination>"
        f"<EntriesPerPage>{entries_per_page}</EntriesPerPage>"
        f"<PageNumber>{page_number}</PageNumber>"
        "</Pagination>"
        "</ActiveList>"
        "<DetailLevel>ReturnAll</DetailLevel>"
        "</GetMyeBaySellingRequest>"
    )


# ---- response parsing -------------------------------------------------------
def _parse_item(item: ET.Element) -> ParsedListing | None:
    ebay_id = _text(_find(item, "ItemID"))
    if not ebay_id:
        return None  # cannot key without an ItemID

    selling_status = _find(item, "SellingStatus")

    # Price: prefer current price, then BuyItNow, then StartPrice.
    # NB: an ElementTree leaf element is falsy (truthiness = child count), so we
    # must test each candidate with `is not None`, never with `or`.
    price_elem = _find(selling_status, "CurrentPrice")
    if price_elem is None:
        price_elem = _find(item, "BuyItNowPrice")
    if price_elem is None:
        price_elem = _find(item, "StartPrice")
    price = _to_float(price_elem)
    currency = price_elem.get("currencyID") if price_elem is not None else None

    # Quantity available = total Quantity - QuantitySold (when both present).
    total_qty = _to_int(_find(item, "Quantity"))
    qty_sold = _to_int(_find(selling_status, "QuantitySold"))
    if total_qty is not None and qty_sold is not None:
        quantity = max(0, total_qty - qty_sold)
    else:
        quantity = total_qty

    primary_cat = _find(item, "PrimaryCategory")

    return ParsedListing(
        ebay_listing_id=ebay_id,
        sku=_text(_find(item, "SKU")),
        title=_text(_find(item, "Title")),
        category_id=_text(_find(primary_cat, "CategoryID")),
        category_name=_text(_find(primary_cat, "CategoryName")),
        price=price,
        currency=currency,
        quantity=quantity,
        condition=_text(_find(item, "ConditionDisplayName")),
        listing_status=_text(_find(selling_status, "ListingStatus")),
        listing_start_date=_text(_find_deep(item, ["ListingDetails", "StartTime"])),
        item_specifics=None,  # not returned by GetMyeBaySelling
        shipping_cost=None,  # not returned by GetMyeBaySelling
        shipping_service=None,  # not returned by GetMyeBaySelling
    )


def parse_active_list(xml_text: str) -> tuple[list[ParsedListing], int]:
    """Parse one GetMyeBaySelling response page.

    Returns (listings, total_pages). Raises EbayApiError on Ack=Failure.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise EbayApiError(f"{_CALL}: malformed XML response ({exc})") from exc

    ack = _text(_find(root, "Ack")) or "Unknown"
    if ack == "Failure":
        msgs = [
            _text(_find(e, "LongMessage")) or _text(_find(e, "ShortMessage")) or "?"
            for e in _findall(root, "Errors")
        ]
        detail = "; ".join(m for m in msgs if m) or "unspecified error"
        raise EbayApiError(f"{_CALL}: Ack=Failure — {detail}")

    active_list = _find(root, "ActiveList")
    total_pages = _to_int(_find_deep(active_list, ["PaginationResult", "TotalNumberOfPages"])) or 1

    item_array = _find(active_list, "ItemArray")
    listings: list[ParsedListing] = []
    for item in _findall(item_array, "Item"):
        parsed = _parse_item(item)
        if parsed is not None:
            listings.append(parsed)
    return listings, total_pages


def fetch_active_listings(entries_per_page: int = 100) -> list[ParsedListing]:
    """Fetch and parse ALL active listings, following pagination. READ-ONLY."""
    page = 1
    first_xml = trading_call(_CALL, build_request(page, entries_per_page))
    listings, total_pages = parse_active_list(first_xml)

    while page < total_pages:
        page += 1
        xml_text = trading_call(_CALL, build_request(page, entries_per_page))
        more, _ = parse_active_list(xml_text)
        listings.extend(more)

    # De-duplicate defensively by ItemID (a listing shouldn't appear twice, but
    # pagination boundaries can occasionally overlap).
    seen: dict[str, ParsedListing] = {}
    for listing in listings:
        seen[listing.ebay_listing_id] = listing
    return list(seen.values())
