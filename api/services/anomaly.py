def detect_anomaly(*, listing_price: float, fair_price: float) -> str:
    """Very simple anomaly rule.

    TODO (Person 3): replace with distribution-based detection (z-score / IQR / model residuals).
    """
    ratio = listing_price / fair_price
    if ratio >= 1.2:
        return "overpriced"
    if ratio <= 0.8:
        return "suspiciously_cheap"
    return "normal_range"
