"""Authentication setup & test — READ-ONLY.

Usage:
  python scripts/check_auth.py            # validate config; if a refresh token
                                          # exists, mint an access token (live
                                          # auth test) — token value never shown.
  python scripts/check_auth.py --login    # print the one-time consent URL.
  python scripts/check_auth.py --code X   # exchange authorization code X for a
                                          # refresh token and save it to .env.

No access or refresh token value is ever printed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REQUIRED_SCOPES, get_settings  # noqa: E402
from app.database.db import init_db  # noqa: E402
from app.ebay.auth import (  # noqa: E402
    EbayAuthError,
    access_token_expires_in,
    build_authorize_url,
    exchange_code_for_tokens,
    get_access_token,
)

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

REQUIRED_APP_CREDS = {
    "EBAY_CLIENT_ID": "ebay_client_id",
    "EBAY_CLIENT_SECRET": "ebay_client_secret",
    "EBAY_DEV_ID": "ebay_dev_id",
    "EBAY_RU_NAME": "ebay_ru_name",
}


def _missing_app_creds() -> list[str]:
    settings = get_settings()
    return [name for name, attr in REQUIRED_APP_CREDS.items() if not getattr(settings, attr)]


def _save_refresh_token(token: str) -> None:
    """Write/replace EBAY_REFRESH_TOKEN in .env without printing the value."""
    lines: list[str] = []
    found = False
    if ENV_PATH.exists():
        lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if line.startswith("EBAY_REFRESH_TOKEN="):
            lines[i] = f"EBAY_REFRESH_TOKEN={token}"
            found = True
            break
    if not found:
        lines.append(f"EBAY_REFRESH_TOKEN={token}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_login() -> int:
    missing = _missing_app_creds()
    if missing:
        print("  ⚠ Cannot build consent URL — missing: " + ", ".join(missing))
        return 1
    print("  Open this URL while logged into the seller account, approve the")
    print("  read-only scopes, then copy the `code` from the redirect URL:\n")
    print("   ", build_authorize_url())
    print("\n  Then run:  python scripts/check_auth.py --code \"<CODE>\"")
    return 0


def cmd_code(auth_code: str) -> int:
    missing = _missing_app_creds()
    if missing:
        print("  ⚠ Missing app credentials: " + ", ".join(missing))
        return 1
    try:
        result = exchange_code_for_tokens(auth_code)
    except EbayAuthError as exc:
        print(f"  ✗ Exchange failed: {exc}")
        return 1
    _save_refresh_token(result.refresh_token)
    print("  ✓ Refresh token obtained and saved to .env (value not shown).")
    if result.refresh_token_expires_in:
        days = result.refresh_token_expires_in // 86400
        print(f"    Refresh token valid for ~{days} days.")
    print("  Next: python scripts/sync_listings.py")
    return 0


def cmd_check() -> int:
    settings = get_settings()
    print("=== eBay Sales Optimizer — auth check (READ-ONLY) ===")
    for key, value in settings.masked().items():
        print(f"  {key:22} : {value}")
    print("\n  Required OAuth scopes (all read-only):")
    for scope in REQUIRED_SCOPES:
        print(f"    - {scope}")

    print("\n  Initialising local database schema ...")
    init_db()
    print(f"  OK — schema ready at: {settings.database_url}")

    missing = _missing_app_creds()
    if missing:
        print("\n  ⚠ Missing app credentials: " + ", ".join(missing))
        print("    Copy .env.example to .env and fill them in, then re-run.")
        return 1

    if not settings.ebay_refresh_token:
        print("\n  No refresh token yet. Start the one-time consent flow:")
        print("    python scripts/check_auth.py --login")
        return 1

    print("\n  Testing authentication (minting a user access token) ...")
    try:
        get_access_token()
    except EbayAuthError as exc:
        print(f"  ✗ Auth test FAILED: {exc}")
        return 1
    ttl = access_token_expires_in()
    print(f"  ✓ Auth OK — access token minted, valid ~{ttl}s (value not shown).")
    print("  Ready: python scripts/sync_listings.py")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--login":
        return cmd_login()
    if len(argv) >= 2 and argv[1] == "--code":
        if len(argv) < 3 or not argv[2].strip():
            print("  Usage: python scripts/check_auth.py --code \"<AUTHORIZATION_CODE>\"")
            return 1
        return cmd_code(argv[2].strip())
    return cmd_check()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
