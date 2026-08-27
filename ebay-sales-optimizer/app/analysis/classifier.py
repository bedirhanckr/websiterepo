"""Deterministic, rules-based listing classifier (Phase 4 implementation).

No LLM decides a classification. Every label below comes from transparent,
testable rules driven by ``config/analysis_rules.yaml``. This module defines the
label vocabulary now so the DB (``ListingAnalysis.problem_type``), the dashboard,
and the tests share one source of truth.

Decision order (implemented in Phase 4), account-relative first, fallback second:
  1. INSUFFICIENT_DATA  — below insufficient_data thresholds, or key metrics NULL.
  2. PERFORMANCE_DROP    — had a real baseline, last 7d materially below prior 7d
                           / 30d baseline.
  3. WINNER              — strong traffic AND strong conversion AND recent sales.
  4. VISIBILITY_PROBLEM  — low impressions & low views & little/no sales.
  5. CLICK_PROBLEM       — decent impressions but weak CTR.
  6. CONVERSION_PROBLEM  — decent views but weak conversion.
  A listing gets exactly one primary label; secondary observations go in evidence.

Guardrail: a NULL metric means "unknown", never 0. Unknown -> INSUFFICIENT_DATA
rather than a forced problem label.
"""

from __future__ import annotations

from enum import StrEnum


class ProblemType(StrEnum):
    VISIBILITY_PROBLEM = "VISIBILITY_PROBLEM"
    CLICK_PROBLEM = "CLICK_PROBLEM"
    CONVERSION_PROBLEM = "CONVERSION_PROBLEM"
    WINNER = "WINNER"
    PERFORMANCE_DROP = "PERFORMANCE_DROP"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class Severity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


def classify_listing(*args, **kwargs):  # signature finalised in Phase 4
    """Classify one listing from its aggregated metrics + account baseline."""
    raise NotImplementedError("Implemented in Phase 4 — classification engine.")
