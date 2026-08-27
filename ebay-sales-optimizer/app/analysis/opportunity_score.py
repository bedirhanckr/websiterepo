"""Opportunity Score 0..100 (Phase 4 implementation).

GOAL: prioritise listings where an intervention likely yields the most economic
upside — NOT simply the worst listing. Deterministic and documented; weights in
``config/analysis_rules.yaml`` under ``opportunity_score``.

Formula (implemented in Phase 4), each component normalised to 0..1 then weighted:

  score = 100 * (
      w_unrealised_traffic * unrealised_traffic
    + w_conversion_gap     * conversion_gap
    + w_ctr_gap            * ctr_gap
    + w_performance_drop   * performance_drop
    + w_revenue_at_stake   * revenue_at_stake
  )

  where, using account-relative percentiles where possible:
    unrealised_traffic : high impressions/views but ~zero sales  (biggest lever)
    conversion_gap     : good traffic, conversion below account norm
    ctr_gap            : good impressions, CTR below account norm
    performance_drop   : magnitude of recent decline from a real baseline
    revenue_at_stake   : min(1, price * available_qty / revenue_reference_eur)

DEMAND GATE (the "20 impressions, 1 view" rule): if trailing-30d impressions are
below ``demand_floor_impressions_30d``, the final score is capped at
``low_demand_cap``. A listing with almost no demand can never dominate the queue
just because its ratios look bad on tiny numbers.
"""

from __future__ import annotations


def compute_opportunity_score(*args, **kwargs) -> float:  # finalised in Phase 4
    """Return a 0..100 opportunity score for one listing."""
    raise NotImplementedError("Implemented in Phase 4 — opportunity score.")
