"""SQLAlchemy ORM models for the eBay Sales Optimizer.

Phase 1 scope: schema only. These tables are populated by the read-only sync
scripts in later phases. No model here performs any write operation against
eBay — they only persist data that has already been retrieved.

Design notes
------------
* Every table that stores a daily snapshot carries a unique constraint so that
  running a sync twice does not create duplicate rows (idempotent upserts).
* Metric columns are nullable on purpose. eBay does not always return every
  metric, and the project rule is: never fabricate an unavailable value. A NULL
  means "not reported by the API", which is different from 0.0 ("reported as
  zero"). The analysis engine must treat NULL as "unknown", not as zero.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class Listing(Base):
    """A single active eBay listing for the seller account.

    Sourced from the Trading API ``GetMyeBaySelling`` (ActiveList). ``sku`` and
    several detail fields may be NULL when eBay does not expose them for a given
    listing.
    """

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Natural key from eBay. Unique so upserts can match on it.
    ebay_listing_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    sku: Mapped[str | None] = mapped_column(String(128), index=True)
    title: Mapped[str | None] = mapped_column(String(512))
    category_id: Mapped[str | None] = mapped_column(String(32))
    category_name: Mapped[str | None] = mapped_column(String(256))
    price: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str | None] = mapped_column(String(8))
    quantity: Mapped[int | None] = mapped_column(Integer)
    condition: Mapped[str | None] = mapped_column(String(64))
    listing_status: Mapped[str | None] = mapped_column(String(32))
    listing_start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Item specifics / shipping stored as JSON text (SQLite-friendly). NULL when
    # the API did not return them. Parsed on read where needed.
    item_specifics_json: Mapped[str | None] = mapped_column(Text)
    shipping_cost: Mapped[float | None] = mapped_column(Float)
    shipping_service: Mapped[str | None] = mapped_column(String(128))

    # Sync bookkeeping. first_seen_at is set once; last_seen_at is refreshed on
    # every sync so we can detect listings that dropped out.
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    traffic_daily: Mapped[list["ListingTrafficDaily"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )
    advertising: Mapped[list["AdvertisingPerformance"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )
    analyses: Mapped[list["ListingAnalysis"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )
    changes: Mapped[list["ListingChangeLog"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )


class ListingTrafficDaily(Base):
    """One row per (listing, day) of Analytics API traffic metrics.

    Populated from the Analytics API ``getTrafficReport`` with
    ``dimension=LISTING`` aggregated per day, or ``dimension=DAY`` when pulling a
    single listing's daily series. NULL columns = metric not reported.
    """

    __tablename__ = "listing_traffic_daily"
    __table_args__ = (
        UniqueConstraint("listing_id", "date", name="uq_traffic_listing_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), index=True
    )
    date: Mapped[date] = mapped_column(Date, index=True)

    impressions: Mapped[int | None] = mapped_column(Integer)  # LISTING_IMPRESSION_TOTAL
    views: Mapped[int | None] = mapped_column(Integer)  # LISTING_VIEWS_TOTAL
    ctr: Mapped[float | None] = mapped_column(Float)  # CLICK_THROUGH_RATE (percent)
    transactions: Mapped[int | None] = mapped_column(Integer)  # TRANSACTION
    quantity_sold: Mapped[int | None] = mapped_column(Integer)
    conversion_rate: Mapped[float | None] = mapped_column(Float)  # SALES_CONVERSION_RATE (percent)

    listing: Mapped["Listing"] = relationship(back_populates="traffic_daily")


class AdvertisingPerformance(Base):
    """One row per (listing, day, campaign) of Promoted Listings performance.

    Populated from the Marketing API Promoted Listings *listing report*. ROAS is
    stored as retrieved or computed as attributed_revenue / spend when both are
    present; NULL when spend is zero or data is missing.
    """

    __tablename__ = "advertising_performance"
    __table_args__ = (
        UniqueConstraint(
            "listing_id", "date", "campaign_id", name="uq_ads_listing_date_campaign"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), index=True
    )
    date: Mapped[date] = mapped_column(Date, index=True)

    campaign_id: Mapped[str] = mapped_column(String(64))
    campaign_name: Mapped[str | None] = mapped_column(String(256))
    campaign_type: Mapped[str | None] = mapped_column(String(64))  # CPS / CPC / OFFSITE
    ad_rate: Mapped[float | None] = mapped_column(Float)  # bid percentage
    impressions: Mapped[int | None] = mapped_column(Integer)
    clicks: Mapped[int | None] = mapped_column(Integer)
    spend: Mapped[float | None] = mapped_column(Float)
    attributed_sales: Mapped[int | None] = mapped_column(Integer)
    attributed_revenue: Mapped[float | None] = mapped_column(Float)
    roas: Mapped[float | None] = mapped_column(Float)

    listing: Mapped["Listing"] = relationship(back_populates="advertising")


class ListingAnalysis(Base):
    """Output of the deterministic analysis engine for one listing on one date.

    Regenerated by ``run_analysis.py``. Idempotent per (listing, analysis_date):
    re-running the analysis on the same day replaces the row rather than adding
    a duplicate.
    """

    __tablename__ = "listing_analysis"
    __table_args__ = (
        UniqueConstraint(
            "listing_id", "analysis_date", name="uq_analysis_listing_date"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), index=True
    )
    analysis_date: Mapped[date] = mapped_column(Date, index=True)

    opportunity_score: Mapped[float | None] = mapped_column(Float)  # 0..100
    problem_type: Mapped[str | None] = mapped_column(String(32))  # see classifier enum
    severity: Mapped[str | None] = mapped_column(String(16))  # LOW / MEDIUM / HIGH
    evidence: Mapped[str | None] = mapped_column(Text)  # human-readable, why
    recommendation: Mapped[str | None] = mapped_column(Text)  # what to do
    do_not_do: Mapped[str | None] = mapped_column(Text)  # explicit guardrail

    listing: Mapped["Listing"] = relationship(back_populates="analyses")


class ListingChangeLog(Base):
    """Manual/experiment change journal — prepared for a future write phase.

    Phase 1 is read-only, so nothing populates this automatically. It exists so
    that, once seller-approved changes begin, we can correlate a change with the
    performance movement that follows it (Objective #6).
    """

    __tablename__ = "listing_change_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), index=True
    )
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    change_type: Mapped[str | None] = mapped_column(String(64))  # TITLE / PRICE / ...
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)

    listing: Mapped["Listing"] = relationship(back_populates="changes")


class SyncRun(Base):
    """Audit row for each sync/analysis run.

    Not required by the brief, but cheap and useful: it records what ran, when,
    the eBay marketplace, row counts, and any partial-failure note, without ever
    logging tokens or secrets.
    """

    __tablename__ = "sync_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(32))  # listings / traffic / ads / analysis
    marketplace: Mapped[str | None] = mapped_column(String(16))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ok: Mapped[bool] = mapped_column(Boolean, default=False)
    rows_written: Mapped[int | None] = mapped_column(Integer)
    note: Mapped[str | None] = mapped_column(Text)  # partial-response / limitation notes
