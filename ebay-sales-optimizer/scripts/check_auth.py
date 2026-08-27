"""Config & environment smoke test (runnable in Phase 1).

Phase 1 behaviour (no network): validates that credentials are present, prints a
SECRET-FREE summary, initialises the local SQLite schema, and prints the consent
URL you would open to grant read-only access. It never prints token values.

Phase 2 will extend this to actually mint an access token from the refresh token
and call a trivial endpoint to confirm live connectivity.

Run:  python scripts/check_auth.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running as `python scripts/check_auth.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REQUIRED_SCOPES, get_settings  # noqa: E402
from app.database.db import init_db  # noqa: E402
from app.ebay.auth import build_authorize_url  # noqa: E402


def main() -> int:
    settings = get_settings()

    print("=== eBay Sales Optimizer — config check (READ-ONLY, Phase 1) ===")
    for key, value in settings.masked().items():
        print(f"  {key:22} : {value}")

    print("\n  Required OAuth scopes (all read-only):")
    for scope in REQUIRED_SCOPES:
        print(f"    - {scope}")

    missing = [
        name
        for name, val in {
            "EBAY_CLIENT_ID": settings.ebay_client_id,
            "EBAY_CLIENT_SECRET": settings.ebay_client_secret,
            "EBAY_RU_NAME": settings.ebay_ru_name,
        }.items()
        if not val
    ]

    print("\n  Initialising local database schema ...")
    init_db()
    print(f"  OK — schema ready at: {settings.database_url}")

    if missing:
        print("\n  ⚠ Missing app credentials: " + ", ".join(missing))
        print("    Fill them in .env (copy from .env.example), then re-run.")
        print("    Live token exchange arrives in Phase 2.")
        return 1

    print("\n  App credentials present. One-time consent URL:")
    print("   ", build_authorize_url())
    if not settings.ebay_refresh_token:
        print("\n  ⚠ No refresh token yet — complete the consent flow (Phase 2).")
    print("\n  Phase 1 check complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
