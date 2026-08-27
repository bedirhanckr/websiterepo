"""Actionable, guarded recommendations (Phase 4 implementation).

Turns a classification + evidence into a concrete next action AND an explicit
"do NOT do" line. Deterministic mapping — no generative advice.

KEY ADVERTISING RULE (Objective #4), encoded here:
  * High impressions + weak CTR/conversion  ->
        "Fix listing performance (photo/title/price/shipping) BEFORE increasing
         advertising."  do_not_do = "Do not raise Promoted Listings ad rate yet."
  * Strong conversion + low impressions + stock available  ->
        "Increasing visibility may be worth investigating (carefully)."
  * WINNER ->
        "Avoid unnecessary edits. Monitor stock. Scale visibility carefully."
        do_not_do = "Do not change title/price without a controlled test."

Every recommendation separates the three problem classes so advice never
conflates a traffic problem with a click or conversion problem.
"""

from __future__ import annotations


def build_recommendation(*args, **kwargs):  # finalised in Phase 4
    """Return (recommendation, do_not_do) for a classified listing."""
    raise NotImplementedError("Implemented in Phase 4 — recommendations.")
