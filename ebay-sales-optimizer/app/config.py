"""Central configuration, loaded from environment variables (.env).

Uses pydantic-settings so that every value is validated once, in one place, and
secrets never get hard-coded. Nothing here prints or logs a token.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo-relative paths so the tool works regardless of the current directory.
PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "optimizer.db"
DEFAULT_RULES_PATH = PROJECT_ROOT / "config" / "analysis_rules.yaml"

# eBay OAuth environments. The sandbox is useful for wiring auth without
# touching production data; production is required for real seller metrics.
EBAY_OAUTH_ENDPOINTS = {
    "production": {
        "authorize": "https://auth.ebay.com/oauth2/authorize",
        "token": "https://api.ebay.com/identity/v1/oauth2/token",
        "api_base": "https://api.ebay.com",
    },
    "sandbox": {
        "authorize": "https://auth.sandbox.ebay.com/oauth2/authorize",
        "token": "https://api.sandbox.ebay.com/identity/v1/oauth2/token",
        "api_base": "https://api.sandbox.ebay.com",
    },
}

# Legacy Trading API (XML) endpoints — used for complete active-listing coverage.
EBAY_TRADING_ENDPOINTS = {
    "production": "https://api.ebay.com/ws/api.dll",
    "sandbox": "https://api.sandbox.ebay.com/ws/api.dll",
}

# Trading API site IDs. This account sells on eBay Germany (77).
EBAY_SITE_IDS = {
    "EBAY_DE": "77",
    "EBAY_US": "0",
    "EBAY_GB": "3",
    "EBAY_AT": "16",
    "EBAY_FR": "71",
    "EBAY_IT": "101",
    "EBAY_ES": "186",
}

# A recent, valid Trading API schema version.
EBAY_TRADING_COMPAT_LEVEL = "1249"

# OAuth scopes this tool needs. All read-only — Phase 1 performs no writes.
# Verified against eBay's current API docs during Phase 1 research.
REQUIRED_SCOPES = [
    "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
    # Negotiation eligibility. Confirm the exact scope your app is granted;
    # eBay documents sell.negotiation for this family of calls.
    "https://api.ebay.com/oauth/api_scope/sell.negotiation.readonly",
]


class Settings(BaseSettings):
    """Runtime settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- eBay application credentials (from the eBay Developer Portal) ---
    ebay_env: str = Field(default="production")
    ebay_client_id: str = Field(default="")  # a.k.a. App ID
    ebay_client_secret: str = Field(default="")  # a.k.a. Cert ID
    ebay_dev_id: str = Field(default="")  # Dev ID — required by the Trading API
    ebay_ru_name: str = Field(default="")  # OAuth redirect (RuName)

    # User (authorization-code) tokens obtained via check_auth flow.
    ebay_refresh_token: str = Field(default="")

    # --- Marketplace ---
    ebay_marketplace_id: str = Field(default="EBAY_DE")

    # --- Local storage ---
    database_url: str = Field(default=f"sqlite:///{DEFAULT_DB_PATH}")
    rules_path: Path = Field(default=DEFAULT_RULES_PATH)

    @property
    def oauth(self) -> dict[str, str]:
        env = self.ebay_env if self.ebay_env in EBAY_OAUTH_ENDPOINTS else "production"
        return EBAY_OAUTH_ENDPOINTS[env]

    @property
    def trading_endpoint(self) -> str:
        env = self.ebay_env if self.ebay_env in EBAY_TRADING_ENDPOINTS else "production"
        return EBAY_TRADING_ENDPOINTS[env]

    @property
    def site_id(self) -> str:
        return EBAY_SITE_IDS.get(self.ebay_marketplace_id, "77")

    def masked(self) -> dict[str, str]:
        """Return a log-safe view of settings. Never exposes secret values."""

        def mask(value: str) -> str:
            return "set" if value else "MISSING"

        return {
            "ebay_env": self.ebay_env,
            "ebay_marketplace_id": self.ebay_marketplace_id,
            "ebay_client_id": mask(self.ebay_client_id),
            "ebay_client_secret": mask(self.ebay_client_secret),
            "ebay_dev_id": mask(self.ebay_dev_id),
            "ebay_ru_name": mask(self.ebay_ru_name),
            "ebay_refresh_token": mask(self.ebay_refresh_token),
            "database_url": self.database_url,
        }


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
