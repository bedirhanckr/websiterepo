"""Retrieve all active listings and save them to SQLite — READ-ONLY.

Uses Trading API GetMyeBaySelling. Idempotent: re-running does not create
duplicate rows (upsert on ebay_listing_id). Performs NO write to eBay.

Run:  python scripts/sync_listings.py
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import get_settings  # noqa: E402
from app.database.db import init_db, session_scope  # noqa: E402
from app.database.models import Listing, SyncRun  # noqa: E402
from app.database.repository import upsert_listings  # noqa: E402
from app.ebay.auth import EbayAuthError  # noqa: E402
from app.ebay.client import EbayApiError  # noqa: E402
from app.ebay.listings import fetch_active_listings  # noqa: E402


def _fmt_price(price: float | None, currency: str | None) -> str:
    if price is None:
        return "n/a"
    return f"{price:.2f} {currency or ''}".strip()


def main() -> int:
    settings = get_settings()
    print(f"=== Active-listing sync (READ-ONLY) — marketplace {settings.ebay_marketplace_id} ===")
    init_db()

    if not settings.ebay_refresh_token:
        print("\n  ⚠ No EBAY_REFRESH_TOKEN configured — cannot reach eBay.")
        print("    Run:  python scripts/check_auth.py --login")
        print("    then: python scripts/check_auth.py --code \"<AUTHORIZATION_CODE>\"")
        return 2

    started = datetime.now(timezone.utc)
    try:
        print("  Fetching active listings from eBay ...")
        parsed = fetch_active_listings()
    except (EbayAuthError, EbayApiError) as exc:
        print(f"\n  ✗ eBay error: {exc}")
        with session_scope() as s:
            s.add(SyncRun(kind="listings", marketplace=settings.ebay_marketplace_id,
                          started_at=started, finished_at=datetime.now(timezone.utc),
                          ok=False, rows_written=0, note=str(exc)))
        return 1

    with session_scope() as session:
        result = upsert_listings(session, parsed)
        session.add(
            SyncRun(
                kind="listings",
                marketplace=settings.ebay_marketplace_id,
                started_at=started,
                finished_at=datetime.now(timezone.utc),
                ok=True,
                rows_written=result.total,
                note=f"inserted={result.inserted} updated={result.updated}",
            )
        )

    print(
        f"\n  Retrieved {len(parsed)} active listing(s). "
        f"Inserted {result.inserted}, updated {result.updated} (no duplicates)."
    )

    # Print the fields the seller asked for, read back from the DB.
    print("\n  ID | Title | Price | Qty")
    print("  " + "-" * 68)
    with session_scope() as session:
        rows = session.query(Listing).order_by(Listing.ebay_listing_id).all()
        for r in rows:
            title = (r.title or "")[:48]
            print(f"  {r.ebay_listing_id} | {title} | {_fmt_price(r.price, r.currency)} | {r.quantity if r.quantity is not None else 'n/a'}")
        print(f"\n  Total listings in database: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
