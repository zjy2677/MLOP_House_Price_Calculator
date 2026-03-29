from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.scoring import load_benchmark_data, calculate_price
from services.anomaly import detect_anomaly

benchmark_df = load_benchmark_data("../data/city_price_benchmark.csv")

app = FastAPI(title="House Price Backend")

class PriceRequest(BaseModel):
    city: str
    surface: float


class AnomalyRequest(BaseModel):
    city: str
    actual_price: float
    surface: float

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/price")
def get_price(request: PriceRequest):
    try:
        estimated_price = calculate_price(city = request.city, surface = request.surface, benchmark_df = benchmark_df)
        return {
            "city": request.city,
            "surface": request.surface,
            "estimated_price": estimated_price
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/anomaly")
def check_anomaly(request: AnomalyRequest):
    try:
        return detect_anomaly(city = request.city, actual_price = request.actual_price, surface = request.surface,
            benchmark_df = benchmark_df)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
