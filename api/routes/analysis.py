from fastapi import APIRouter

from api.models.schemas import PropertyInput, PropertyAnalysisResponse
from api.services.anomaly import detect_anomaly
from api.services.pricing import estimate_price
from api.services.risk import explain_risk

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=PropertyAnalysisResponse)
def analyze_property(payload: PropertyInput) -> PropertyAnalysisResponse:
    """Minimal orchestration endpoint for the project demo pipeline."""
    fair_price = estimate_price(payload)
    market_gap_pct = ((payload.listing_price_eur - fair_price) / fair_price) * 100

    anomaly = detect_anomaly(listing_price=payload.listing_price_eur, fair_price=fair_price)
    risk = explain_risk(payload=payload, anomaly=anomaly, market_gap_pct=market_gap_pct)

    return PropertyAnalysisResponse(
        input=payload,
        fair_price_eur=round(fair_price, 2),
        market_gap_pct=round(market_gap_pct, 2),
        anomaly_label=anomaly,
        risk_explanation=risk,
        notes=[
            "Baseline heuristic only. Replace with data-backed logic.",
            "TODO (Person 2): persist analysis requests to PostgreSQL.",
            "TODO (Person 3): calibrate model against historical comparables.",
        ],
    )
