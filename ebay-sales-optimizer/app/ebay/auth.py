"""eBay OAuth (authorization-code grant) — READ-ONLY.

Flow (verified against eBay OAuth docs):
  * Seller-scoped data requires a **user** access token minted via the
    authorization-code grant. A client-credentials token is NOT sufficient.
  * One-time consent: seller opens the authorize URL, approves the read-only
    scopes, and eBay redirects to the RuName with an authorization ``code``.
  * ``exchange_code_for_tokens`` swaps that code for an access token (~2h) and a
    refresh token (~18 months).
  * ``get_access_token`` mints a short-lived access token from the refresh token
    on demand and caches it in memory until shortly before expiry.

Security:
  * Only the refresh token is persisted (in the gitignored .env).
  * Access tokens live in memory only — never written to disk or logged.
  * No token value is ever printed. Callers get expiry metadata, not the token.
"""

from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from urllib.parse import urlencode

import httpx

from app.config import REQUIRED_SCOPES, get_settings


class EbayAuthError(RuntimeError):
    """Raised on OAuth failures. Message is deliberately secret-free."""


def build_authorize_url(state: str = "optimizer") -> str:
    """Build the one-time consent URL for the seller to grant read-only access."""
    settings = get_settings()
    params = {
        "client_id": settings.ebay_client_id,
        "redirect_uri": settings.ebay_ru_name,
        "response_type": "code",
        "scope": " ".join(REQUIRED_SCOPES),
        "state": state,
    }
    return f"{settings.oauth['authorize']}?{urlencode(params)}"


def _basic_auth_header() -> str:
    settings = get_settings()
    raw = f"{settings.ebay_client_id}:{settings.ebay_client_secret}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def _post_token(data: dict[str, str]) -> dict:
    settings = get_settings()
    headers = {
        "Authorization": _basic_auth_header(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        resp = httpx.post(
            settings.oauth["token"], headers=headers, data=data, timeout=30.0
        )
    except httpx.HTTPError as exc:  # network-level
        raise EbayAuthError(f"Token endpoint unreachable: {type(exc).__name__}") from exc

    if resp.status_code != 200:
        # eBay returns an error/desc in JSON; surface those (never the token).
        detail = ""
        try:
            body = resp.json()
            detail = f" ({body.get('error')}: {body.get('error_description')})"
        except Exception:
            pass
        raise EbayAuthError(f"Token request failed: HTTP {resp.status_code}{detail}")
    return resp.json()


@dataclass
class TokenExchangeResult:
    """Non-secret metadata about a successful exchange (no token values)."""

    refresh_token: str  # returned to the caller ONLY so it can be saved to .env
    refresh_token_expires_in: int | None
    access_token_expires_in: int | None


def exchange_code_for_tokens(auth_code: str) -> TokenExchangeResult:
    """Exchange a one-time authorization ``code`` for refresh + access tokens.

    The caller (``check_auth.py --code``) writes the refresh token to .env.
    """
    settings = get_settings()
    payload = _post_token(
        {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": settings.ebay_ru_name,
        }
    )
    refresh = payload.get("refresh_token")
    if not refresh:
        raise EbayAuthError("No refresh_token in exchange response.")
    return TokenExchangeResult(
        refresh_token=refresh,
        refresh_token_expires_in=payload.get("refresh_token_expires_in"),
        access_token_expires_in=payload.get("expires_in"),
    )


# In-memory cache: (access_token, expiry_epoch). Never persisted.
_ACCESS_CACHE: tuple[str, float] | None = None


def get_access_token(force_refresh: bool = False) -> str:
    """Return a valid user access token, minting from the refresh token if needed.

    Cached in memory until 60s before expiry. Raises EbayAuthError if no refresh
    token is configured.
    """
    global _ACCESS_CACHE
    now = time.time()
    if not force_refresh and _ACCESS_CACHE and _ACCESS_CACHE[1] - 60 > now:
        return _ACCESS_CACHE[0]

    settings = get_settings()
    if not settings.ebay_refresh_token:
        raise EbayAuthError(
            "No EBAY_REFRESH_TOKEN configured. Complete the consent flow first "
            "(python scripts/check_auth.py --login, then --code <CODE>)."
        )

    payload = _post_token(
        {
            "grant_type": "refresh_token",
            "refresh_token": settings.ebay_refresh_token,
            "scope": " ".join(REQUIRED_SCOPES),
        }
    )
    token = payload.get("access_token")
    if not token:
        raise EbayAuthError("No access_token in refresh response.")
    expires_in = int(payload.get("expires_in", 7200))
    _ACCESS_CACHE = (token, now + expires_in)
    return token


def access_token_expires_in() -> int | None:
    """Seconds until the cached access token expires, or None if none cached.

    Used by the auth test to report success WITHOUT exposing the token value.
    """
    if _ACCESS_CACHE is None:
        return None
    return max(0, int(_ACCESS_CACHE[1] - time.time()))
