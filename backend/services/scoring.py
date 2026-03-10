from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriceBreakdown:
    estimated_price: float
    base: float
    area_component: float
    rooms_component: float
    location_component: float
    age_component: float
    features_component: float
    energy_component: float
    confidence: float


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def score_house_price(
    *,
    area_m2: float,
    bedrooms: int,
    bathrooms: int,
    location_score: float,
    year_built: int,
    has_garage: bool,
    has_garden: bool,
    energy_rating: str,
    current_year: int = 2026,
) -> PriceBreakdown:
    """
    A transparent rule-based price estimator.

    Inputs:
      - area_m2: total size in square meters (e.g., 75)
      - bedrooms, bathrooms: integers
      - location_score: 0..10 (0 = weak, 10 = premium)
      - year_built: e.g., 1998
      - has_garage, has_garden: booleans
      - energy_rating: A, B, C, D, E, F, or G
      - current_year: used to compute age (defaults to 2026)

    Output:
      - PriceBreakdown with estimated_price + components + a rough confidence.
    """

    # --- Base assumptions (tune these for your market) ---
    # Think of these as "global knobs" you can calibrate later.
    BASE_PRICE = 50_000.0
    EUR_PER_M2 = 3_200.0
    EUR_PER_BEDROOM = 12_000.0
    EUR_PER_BATHROOM = 8_000.0
    EUR_PER_LOCATION_POINT = 18_000.0  # per point on 0..10 scale

    # Age effect: older homes slightly discounted, but cap the effect.
    age = max(0, current_year - year_built)
    # -0.35% per year, capped between -30% and +5% (new builds can get slight boost)
    age_multiplier = 1.0 - (0.0035 * age)
    age_multiplier = _clamp(age_multiplier, 0.70, 1.05)

    # Features
    features_component = 0.0
    if has_garage:
        features_component += 15_000.0
    if has_garden:
        features_component += 20_000.0

    # Energy rating premium/penalty
    energy_map = {
        "A": 1.06,
        "B": 1.03,
        "C": 1.01,
        "D": 1.00,
        "E": 0.97,
        "F": 0.94,
        "G": 0.90,
    }
    energy_rating = energy_rating.strip().upper()
    if energy_rating not in energy_map:
        raise ValueError("energy_rating must be one of A, B, C, D, E, F, G")

    energy_multiplier = energy_map[energy_rating]

    # --- Components ---
    base = BASE_PRICE
    area_component = area_m2 * EUR_PER_M2
    rooms_component = (bedrooms * EUR_PER_BEDROOM) + (bathrooms * EUR_PER_BATHROOM)
    location_component = _clamp(location_score, 0.0, 10.0) * EUR_PER_LOCATION_POINT

    # Combine then apply multipliers
    pre_mult = base + area_component + rooms_component + location_component + features_component
    estimated = pre_mult * age_multiplier * energy_multiplier

    # Rough “confidence” heuristic (0..1)
    # More complete “typical” inputs => higher confidence.
    confidence = 0.55
    if 20 <= area_m2 <= 250:
        confidence += 0.10
    if 0 <= location_score <= 10:
        confidence += 0.10
    if 1900 <= year_built <= current_year:
        confidence += 0.10
    if energy_rating in {"A", "B", "C", "D", "E", "F", "G"}:
        confidence += 0.05
    confidence = _clamp(confidence, 0.0, 0.95)

    # For transparency, store age & energy impacts as components (approx)
    # We keep these as “multiplicative effects” represented in the breakdown:
    # Not perfect accounting, but helpful.
    age_component = pre_mult * (age_multiplier - 1.0)
    energy_component = (pre_mult + age_component) * (energy_multiplier - 1.0)

    return PriceBreakdown(
        estimated_price=round(estimated, 2),
        base=round(base, 2),
        area_component=round(area_component, 2),
        rooms_component=round(rooms_component, 2),
        location_component=round(location_component, 2),
        age_component=round(age_component, 2),
        features_component=round(features_component, 2),
        energy_component=round(energy_component, 2),
        confidence=round(confidence, 2),
    )

