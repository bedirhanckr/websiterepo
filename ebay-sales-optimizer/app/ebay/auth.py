"""eBay OAuth (Phase 2 implementation).

Verified flow (eBay OAuth docs):
  * User data (traffic, listings, ads, negotiation) requires the
    **authorization code grant** — an application/client-credentials token is
    NOT sufficient for seller-scoped data.
  * One-time consent: redirect the seller to the authorize endpoint with the
    required scopes; eBay returns an authorization code to the RuName redirect.
  * Exchange the code for an access token (~2h) + refresh token (~18 months).
  * Thereafter, mint short-lived access tokens from the refresh token as needed.

Security rules (enforced when implemented):
  * Access tokens are held in memory only, never written to disk or logs.
  * Only the refresh token is persisted, and only in the gitignored .env.
  * ``mask``-style logging only — no token value ever appears in output.

Phase 1 provides the scope list and the authorize-URL builder helper so the
README instructions are executable; token exchange lands in Phase 2.
"""

from __future__ import annotations

from urllib.parse import urlencode

from app.config import REQUIRED_SCOPES, get_settings


def build_authorize_url(state: str = "optimizer") -> str:
    """Build the consent URL the seller opens once to grant read-only access.

    Implemented in Phase 1 because it is needed to document/test the auth setup.
    """
    settings = get_settings()
    params = {
        "client_id": settings.ebay_client_id,
        "redirect_uri": settings.ebay_ru_name,
        "response_type": "code",
        "scope": " ".join(REQUIRED_SCOPES),
        "state": state,
    }
    return f"{settings.oauth['authorize']}?{urlencode(params)}"


def exchange_code_for_tokens(auth_code: str) -> dict:
    """Exchange an authorization code for access + refresh tokens. (Phase 2)"""
    raise NotImplementedError("Implemented in Phase 2 — authentication.")


def get_access_token() -> str:
    """Return a valid short-lived access token, refreshing if needed. (Phase 2)"""
    raise NotImplementedError("Implemented in Phase 2 — authentication.")
