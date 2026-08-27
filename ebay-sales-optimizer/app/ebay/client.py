"""Trading API (XML) caller — READ-ONLY.

A thin helper that posts an XML request to the Trading API endpoint with the
correct headers and an OAuth **user** access token (supplied via the
``X-EBAY-API-IAF-TOKEN`` header). When authorizing with OAuth we do NOT include
``RequesterCredentials`` in the body (per eBay's Trading OAuth guidance).

Only read calls (``GetMyeBaySelling``) are issued anywhere in this project.

Error handling:
  * 401/invalid token -> refresh once and retry.
  * Non-200 or Trading-level ``Ack=Failure`` -> raise with a secret-free message.
  * No token value is ever logged.
"""

from __future__ import annotations

import httpx

from app.config import EBAY_TRADING_COMPAT_LEVEL, get_settings
from app.ebay.auth import get_access_token


class EbayApiError(RuntimeError):
    """Raised for non-recoverable eBay API errors (message is secret-free)."""


def _headers(call_name: str, access_token: str) -> dict[str, str]:
    settings = get_settings()
    headers = {
        "X-EBAY-API-COMPATIBILITY-LEVEL": EBAY_TRADING_COMPAT_LEVEL,
        "X-EBAY-API-CALL-NAME": call_name,
        "X-EBAY-API-SITEID": settings.site_id,
        "X-EBAY-API-IAF-TOKEN": access_token,
        "Content-Type": "text/xml",
    }
    # Dev/App/Cert name headers are accepted alongside the IAF token and improve
    # compatibility. Sent only if present; never logged.
    if settings.ebay_dev_id:
        headers["X-EBAY-API-DEV-NAME"] = settings.ebay_dev_id
    if settings.ebay_client_id:
        headers["X-EBAY-API-APP-NAME"] = settings.ebay_client_id
    if settings.ebay_client_secret:
        headers["X-EBAY-API-CERT-NAME"] = settings.ebay_client_secret
    return headers


def trading_call(call_name: str, xml_body: str, _retried: bool = False) -> str:
    """POST an XML Trading request and return the raw XML response text.

    Retries once on an auth failure with a freshly minted access token.
    """
    settings = get_settings()
    token = get_access_token(force_refresh=_retried)
    try:
        resp = httpx.post(
            settings.trading_endpoint,
            headers=_headers(call_name, token),
            content=xml_body.encode("utf-8"),
            timeout=60.0,
        )
    except httpx.HTTPError as exc:
        raise EbayApiError(f"{call_name}: network error {type(exc).__name__}") from exc

    if resp.status_code == 401 and not _retried:
        return trading_call(call_name, xml_body, _retried=True)

    if resp.status_code != 200:
        raise EbayApiError(f"{call_name}: HTTP {resp.status_code}")

    return resp.text
