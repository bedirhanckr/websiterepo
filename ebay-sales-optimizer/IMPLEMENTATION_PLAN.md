# eBay Sales Optimizer — Implementation Plan (Phase 1)

A lightweight, **read-only**, data-driven optimization tool for the eBay Germany
seller account **[zbdesign-de](https://www.ebay.de/usr/zbdesign-de)** (marketplace
`EBAY_DE`). Small catalogue → deliberately an MVP, not a platform.

> **Phase 1 safety rule:** everything is READ-ONLY. No listing edit, no price /
> quantity / title / item-specific change, no advertising change, no buyer
> offers, no end/relist/migrate. Any write capability is a separate, explicitly
> approved future phase. The one buyer-facing write eBay offers here
> (`sendOfferToInterestedBuyers`) is intentionally **not implemented anywhere**.

---

## 1. The 7 questions this tool answers

| # | Question | Backing data | Where |
|---|----------|--------------|-------|
| 1 | Which listings have a **visibility** problem? | Analytics impressions/views | classifier |
| 2 | Which have a **CTR** problem? | Analytics impressions vs CTR | classifier |
| 3 | Which have a **conversion** problem? | Analytics views vs conversion | classifier |
| 4 | Which should **NOT** get more ads? | impressions + CTR/conv + ROAS | recommendations |
| 5 | Which are **winners** to protect? | traffic + conversion + sales | classifier |
| 6 | Which **changes** improved performance? | `listing_change_log` + traffic history | (future write phase) |
| 7 | Which products to **prioritize** next? | Opportunity Score 0–100 | opportunity_score |

---

## 2. eBay APIs used (verified against current docs, Phase 1)

All seller-scoped data requires an **authorization-code** user token (not a
client-credentials token) and the `X-EBAY-C-MARKETPLACE-ID: EBAY_DE` header.

### 2.1 Active listings — **Trading API `GetMyeBaySelling` (ActiveList)**
- **Why not the Sell Inventory API:** `getInventoryItems` only returns items
  created/migrated through the Inventory model. Listings created in the eBay web
  UI (typical for an existing seller) are **invisible** to it. `GetMyeBaySelling`
  returns *all* active listings, so it is the reliable source for completeness.
- Trade-off: Trading API is legacy **XML** (not REST/JSON). Accepted — coverage
  beats elegance. Limit 25,000 items (irrelevant here); 300 calls / 15 s.
- Fields parsed: ItemID, SKU, Title, PrimaryCategory (ID+Name), price+currency,
  Quantity, ConditionDisplayName, status, StartTime, item specifics, shipping.
- Auth: uses the same user token; Trading also needs the app's dev/cert/app IDs.

### 2.2 Performance — **Sell Analytics API `getTrafficReport`**
- `GET /sell/analytics/v1/traffic_report`
- Scope: `sell.analytics.readonly`
- `dimension`: `LISTING` (per-listing totals) or `DAY` (daily series).
- `metric` enum (verified): `LISTING_IMPRESSION_TOTAL`, `LISTING_VIEWS_TOTAL`,
  `CLICK_THROUGH_RATE`, `SALES_CONVERSION_RATE`, `TRANSACTION` (+ the granular
  `*_SEARCH_RESULTS_PAGE`, `*_STORE`, `LISTING_VIEWS_SOURCE_*`, `TOTAL_IMPRESSION_TOTAL`).
- `filter`: `marketplace_ids:{EBAY_DE}` + a `date_range` (`[YYYYMMDD..YYYYMMDD]`
  Pacific, or ISO-8601 with offset).
- We pull **two windows**: last 7 days and last 30 days; and per-listing **daily**
  series (`dimension=DAY`) to store daily snapshots and detect drops.

### 2.3 Advertising — **Sell Marketing API (Promoted Listings)**
- Scope: `sell.marketing.readonly`
- `getCampaigns` → campaign id/name/strategy (General=CPS, Priority=CPC, Offsite).
- Async report task (`createReportTask` → poll → download) → per-listing daily
  impressions, clicks, spend, attributed sales, attributed revenue. ROAS derived
  as `attributed_revenue / spend` when `spend > 0`.

### 2.4 Buyer interest — **Sell Negotiation API `findEligibleItems`** (read only)
- `POST /sell/negotiation/v1/find_eligible_items`
- Returns listings with buyers who watch-listed or carted the item → a
  latent-demand signal. **We never call `sendOfferToInterestedBuyers`.**

---

## 3. Known limitations (surfaced, never hidden)

- **Analytics:** max **90 days** per request; earliest start = **2 years** ago;
  data lags — trust only up to the response's `lastUpdatedDate`; CTR and
  conversion are **percentages**; per-listing daily backfill only exists from the
  first sync onward for anything the API no longer serves.
- **A metric that is not returned is stored as NULL = "unknown", never 0.** The
  analysis engine treats unknown as `INSUFFICIENT_DATA`, not as a problem.
- **Quantity sold** is not always a distinct Analytics metric; where only
  `TRANSACTION` is available it is used as an approximation and labelled as such.
- **Advertising** data exists only if Promoted Listings campaigns run on EBAY_DE;
  otherwise the tool reports "no advertising data" rather than inventing any.
- **Small catalogue** → account-relative thresholds are only trusted once
  `min_listings_for_relative` is met; otherwise conservative absolute fallbacks
  (in `config/analysis_rules.yaml`) apply.
- **Trading API is XML** and has its own quirks vs the REST Sell APIs.
- No OEM number or vehicle-compatibility fact is ever invented; the audit only
  *flags* implausible part numbers for human verification.

---

## 4. Database schema (SQLite via SQLAlchemy)

Idempotent by design — unique constraints make a double-sync a no-op.

- **listings** — one row per active listing (natural key `ebay_listing_id`,
  unique). `first_seen_at` / `last_seen_at` track lifecycle. Item specifics &
  shipping stored as JSON/columns; NULL where eBay doesn't expose them.
- **listing_traffic_daily** — `UNIQUE(listing_id, date)`. impressions, views,
  ctr, transactions, quantity_sold, conversion_rate (all nullable).
- **advertising_performance** — `UNIQUE(listing_id, date, campaign_id)`. campaign
  meta, ad_rate, impressions, clicks, spend, attributed_sales/revenue, roas.
- **listing_analysis** — `UNIQUE(listing_id, analysis_date)`. opportunity_score,
  problem_type, severity, evidence, recommendation, do_not_do.
- **listing_change_log** — journal for the *future* write/experiment phase
  (Objective #6). **Not auto-populated in Phase 1.**
- **sync_runs** — per-run audit (kind, marketplace, counts, notes). No secrets.

---

## 5. Analysis design (deterministic, no LLM classification)

- **Classifier** labels each listing as exactly one of: `INSUFFICIENT_DATA`,
  `PERFORMANCE_DROP`, `WINNER`, `VISIBILITY_PROBLEM`, `CLICK_PROBLEM`,
  `CONVERSION_PROBLEM` — decided in that priority order, account-relative first,
  absolute fallback second. Rules + thresholds live in
  `config/analysis_rules.yaml`, not in code.
- **Opportunity Score (0–100)** prioritises *economic upside*, not the worst
  listing. Weighted mix of unrealised traffic, conversion gap, CTR gap,
  performance drop and revenue-at-stake, with a **demand gate** so tiny-demand
  listings (e.g. 20 impressions, 1 view) can't dominate the queue.
- **Advertising guardrail:** high impressions + weak CTR/conversion →
  *"fix the listing before spending more."* Strong conversion + low impressions +
  stock → visibility increase *worth investigating*. Never an automatic
  "raise ad rate."
- **Listing audit:** warnings only (missing SKU/specifics, short title, repeated
  keywords, suspicious OEM/reference format, duplicate part numbers, suspicious
  price change, zero stock, malformed data).

---

## 6. Phased roadmap

- **Phase 1 (this) — DONE:** directory inspected; APIs & scopes verified;
  implementation plan; project skeleton; SQLAlchemy models; `.env.example`;
  README setup. Runnable: `check_auth.py` (config + schema), smoke tests green.
- **Phase 2:** OAuth (auth-code + refresh), live connection test, listing sync,
  tests. Read-only.
- **Phase 3:** Analytics integration → real traffic metrics (7d, 30d, daily
  snapshots), stored, tested.
- **Phase 4:** deterministic classifier + opportunity score + recommendations +
  audit; then the Streamlit dashboard. Advertising & negotiation reads folded in.
- **Future (approval-gated):** any write capability + `listing_change_log`
  population for change→impact analysis (Objective #6).

---

## 7. Project layout

```
ebay-sales-optimizer/
├── app/
│   ├── config.py                # env-driven settings (pydantic), scopes, endpoints
│   ├── ebay/                    # auth, client, listings, analytics, marketing, negotiation
│   ├── analysis/                # classifier, opportunity_score, recommendations, listing_audit
│   └── database/                # db.py (engine/session), models.py (schema)
├── config/analysis_rules.yaml   # ALL thresholds & scoring weights (documented)
├── dashboard/app.py             # Streamlit (Phase 4)
├── scripts/                     # check_auth, sync_listings, sync_traffic, sync_ads, run_analysis
├── tests/                       # smoke tests now; behavioural tests per phase
├── .env.example                 # copy to .env; secrets never committed
├── requirements.txt
└── README.md
```
