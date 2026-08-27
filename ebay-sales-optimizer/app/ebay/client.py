"""Shared HTTP client for eBay REST APIs (Phase 2 implementation).

A thin httpx wrapper that will centralise:
  * base URL selection (production vs sandbox) from config,
  * the Authorization: Bearer header (token from auth.get_access_token),
  * the X-EBAY-C-MARKETPLACE-ID header (EBAY_DE for this account),
  * pagination helpers (offset/limit for REST; page cursors for reports),
  * error handling: 401 -> refresh & retry once; 429 -> respect rate limits with
    backoff; 4xx/5xx -> raise with a redacted, secret-free message,
  * partial-response tolerance: return what parsed and record a note.

The Trading API (GetMyeBaySelling) is XML/SOAP, not REST, so it gets its own
small caller in ``listings.py`` rather than reusing this REST client.

Nothing here logs tokens.
"""

from __future__ import annotations


class EbayApiError(RuntimeError):
    """Raised for non-recoverable eBay API errors (message is secret-free)."""


class EbayClient:
    """Placeholder. Implemented in Phase 2."""

    def __init__(self) -> None:
        raise NotImplementedError("Implemented in Phase 2 — connection & client.")
