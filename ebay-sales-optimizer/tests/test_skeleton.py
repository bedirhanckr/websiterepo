"""Phase 1 smoke tests: the skeleton imports and the schema builds.

Real behavioural tests (parsers, upserts, classification, opportunity score,
performance-drop, insufficient-data, CTR/conversion/ROAS math) are added
alongside their implementations in Phases 2–4. These early tests just guarantee
the structure is sound and the DB schema is creatable on an in-memory SQLite.
"""

from __future__ import annotations

import os

# Use a throwaway in-memory DB for the schema test; set before importing db.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")


def test_config_masks_secrets() -> None:
    from app.config import REQUIRED_SCOPES, get_settings

    settings = get_settings()
    masked = settings.masked()
    # Secret fields are reported as presence flags, never raw values.
    assert masked["ebay_client_secret"] in {"set", "MISSING"}
    assert masked["ebay_refresh_token"] in {"set", "MISSING"}
    # All required scopes are read-only.
    assert all(s.endswith("readonly") or "readonly" in s for s in REQUIRED_SCOPES)


def test_analysis_rules_yaml_loads() -> None:
    import yaml

    from app.config import get_settings

    with open(get_settings().rules_path, encoding="utf-8") as fh:
        rules = yaml.safe_load(fh)
    assert "opportunity_score" in rules
    assert "fallback" in rules
    assert rules["insufficient_data"]["min_impressions_30d"] >= 0


def test_schema_creates_on_memory_db() -> None:
    from sqlalchemy import create_engine, inspect

    from app.database.models import Base

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    tables = set(inspect(engine).get_table_names())
    assert {
        "listings",
        "listing_traffic_daily",
        "advertising_performance",
        "listing_analysis",
        "listing_change_log",
    } <= tables


def test_problem_type_vocabulary() -> None:
    from app.analysis.classifier import ProblemType

    names = {p.value for p in ProblemType}
    assert names == {
        "VISIBILITY_PROBLEM",
        "CLICK_PROBLEM",
        "CONVERSION_PROBLEM",
        "WINNER",
        "PERFORMANCE_DROP",
        "INSUFFICIENT_DATA",
    }
