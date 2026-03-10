from typing import List

from pydantic import BaseModel, Field


class PropertyInput(BaseModel):
    city: str = Field(..., min_length=2, max_length=80)
    district: str = Field(..., min_length=2, max_length=80)
    area_m2: float = Field(..., gt=10, le=1200)
    rooms: int = Field(..., ge=1, le=20)
    year_built: int = Field(..., ge=1800, le=2100)
    energy_rating: str = Field(..., description="A-G")
    listing_price_eur: float = Field(..., gt=10000)


class PropertyAnalysisResponse(BaseModel):
    input: PropertyInput
    fair_price_eur: float
    market_gap_pct: float
    anomaly_label: str
    risk_explanation: str
    notes: List[str]
