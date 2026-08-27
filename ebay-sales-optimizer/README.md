# eBay Sales Optimizer (MVP, read-only)

A small, local, data-driven tool to help the eBay Germany seller account
**[zbdesign-de](https://www.ebay.de/usr/zbdesign-de)** (marketplace `EBAY_DE`)
find and prioritise listing-performance problems — visibility, click-through and
conversion — and know **which listings to leave alone**.

> **Phase 1 is strictly READ-ONLY.** It never edits listings, prices, quantities,
> item specifics, advertising, or sends buyer offers. See
> [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) for the full design, verified
> API details, limitations, and the phased roadmap.

## What Phase 1 delivers

- Project skeleton, config, and the SQLite/SQLAlchemy database schema.
- Verified eBay API + OAuth-scope plan (Analytics, Trading, Marketing, Negotiation).
- A runnable config/auth smoke test and green unit tests.
- The analysis rules & thresholds file (`config/analysis_rules.yaml`).

Data sync (Phase 2–3), the deterministic classifier + Opportunity Score
(Phase 4), and the Streamlit dashboard (Phase 4) follow in later phases.

## Tech stack

Python 3.12+ (works on 3.11) · SQLite · SQLAlchemy · Pydantic · httpx ·
Streamlit · pytest · python-dotenv. No Redis, no queue, no microservices — by design.

---

## Setup

```bash
cd ebay-sales-optimizer
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
cp .env.example .env                                # then fill in credentials
python scripts/check_auth.py                        # validates config, builds DB
```

`check_auth.py` prints a **secret-free** summary, creates the local SQLite
schema, and (once app credentials are set) prints the one-time consent URL. It
never prints token values.

Run the tests:

```bash
pytest -q
```

---

## eBay credentials & OAuth — step by step

### 1. Create an eBay developer account
1. Go to the **eBay Developers Program** (`developer.ebay.com`) and register
   (you can sign in with your eBay seller account).
2. Under **My Account → Application Keysets**, create a **Production** keyset.
   You will get:
   - **App ID (Client ID)** → `EBAY_CLIENT_ID`
   - **Cert ID (Client Secret)** → `EBAY_CLIENT_SECRET`
   - **Dev ID** (needed later for Trading API calls)

### 2. Create an OAuth redirect (RuName)
In the keyset, add a **User Token / OAuth** redirect and note its **RuName**
→ `EBAY_RU_NAME`. This is where eBay returns the authorization code.

### 3. Required OAuth scopes (all READ-ONLY)
This tool requests only read scopes:

| Scope | Used for |
|-------|----------|
| `sell.analytics.readonly` | traffic report (impressions, views, CTR, conversion, transactions) |
| `sell.inventory.readonly` | optional item-specifics enrichment |
| `sell.marketing.readonly` | Promoted Listings campaigns & performance |
| `sell.negotiation.readonly` | buyer-interest eligibility (read only) |

> Confirm your keyset is granted the negotiation scope; eBay documents the
> `sell.negotiation` family for `findEligibleItems`. Active-listing retrieval
> uses the **Trading API** with the same user token plus your Dev/App/Cert IDs.

### 4. Authorize (grant consent) — one time
1. Put `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_RU_NAME`,
   `EBAY_MARKETPLACE_ID=EBAY_DE` in `.env`.
2. Run `python scripts/check_auth.py` and open the printed **consent URL** in a
   browser while logged into the seller account; approve the read-only scopes.
3. eBay redirects to your RuName with an authorization `code`.
4. **Phase 2** exchanges that code for an **access token** (~2 h) and a
   **refresh token** (~18 months). Only the refresh token is saved, to `.env` as
   `EBAY_REFRESH_TOKEN`. Access tokens stay in memory and are refreshed on demand.

### 5. Test authentication
- **Phase 1:** `python scripts/check_auth.py` confirms your config is complete
  and the database builds.
- **Phase 2:** the same command will additionally mint a live access token and
  call a trivial endpoint to confirm connectivity.

---

## Security

- Secrets live only in `.env`, which is **gitignored** — never commit it.
- Access and refresh tokens are **never printed** to logs or the console; config
  summaries show only `set` / `MISSING`.
- The local SQLite DB (`data/`) is gitignored.

## Commands (available as phases land)

```bash
python scripts/check_auth.py       # Phase 1: config + DB smoke test
python scripts/sync_listings.py    # Phase 2: active listings (Trading API)
python scripts/sync_traffic.py     # Phase 3: traffic (Analytics API)
python scripts/sync_ads.py         # later:   advertising (Marketing API)
python scripts/run_analysis.py     # Phase 4: classify + opportunity score
streamlit run dashboard/app.py     # Phase 4: dashboard (read-only)
```
