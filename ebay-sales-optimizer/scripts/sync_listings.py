"""CLI entry point — implemented in Phase 2 — active-listing sync (Trading API GetMyeBaySelling).

READ-ONLY. This script only retrieves data and writes it to the local SQLite
database. It performs no write operation against eBay. Idempotent: re-running
must not create duplicate rows (enforced by unique constraints + upserts).

Run:  python scripts/sync_listings.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main() -> int:
    print("sync_listings: implemented in Phase 2 — active-listing sync (Trading API GetMyeBaySelling).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
