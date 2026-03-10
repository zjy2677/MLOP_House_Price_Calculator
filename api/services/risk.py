from api.models.schemas import PropertyInput


def explain_risk(*, payload: PropertyInput, anomaly: str, market_gap_pct: float) -> str:
    """Starter risk messaging with explicit placeholders for richer reasoning."""
    parts = []

    if anomaly == "overpriced":
        parts.append("Listing appears significantly above baseline fair value.")
    elif anomaly == "suspiciously_cheap":
        parts.append("Listing appears significantly below baseline fair value.")
    else:
        parts.append("Listing is close to baseline fair value.")

    if payload.energy_rating.upper() in {"E", "F", "G"}:
        parts.append("Low energy rating may increase long-term renovation costs.")

    if payload.year_built < 1970:
        parts.append("Older property may carry higher maintenance or compliance risk.")

    parts.append(f"Current baseline gap is {market_gap_pct:.1f}%.")
    parts.append("TODO (Person 2 + Person 3): attach explainable factors from real market comps.")

    return " ".join(parts)
