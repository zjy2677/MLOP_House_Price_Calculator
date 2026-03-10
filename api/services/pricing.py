from api.models.schemas import PropertyInput


def estimate_price(payload: PropertyInput) -> float:
    """Baseline pricing heuristic for demo purposes.

    TODO (Person 3): Replace this with a data-driven baseline from CSV/database comparables.
    """
    base = 40000
    area_component = payload.area_m2 * 2500
    rooms_component = payload.rooms * 12000

    age = max(0, 2026 - payload.year_built)
    age_discount = min(age * 0.002, 0.25)

    energy_factor = {
        "A": 1.05,
        "B": 1.03,
        "C": 1.0,
        "D": 0.97,
        "E": 0.93,
        "F": 0.9,
        "G": 0.86,
    }.get(payload.energy_rating.upper(), 0.95)

    pre = base + area_component + rooms_component
    estimate = pre * (1 - age_discount) * energy_factor

    return estimate
