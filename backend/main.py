from fastapi import FastAPI
from services.scoring import load_benchmark_data, calculate_price
from services.anomaly import detect_anomaly 

benchmark_df = load_benchmark_data("../data/city_price_benchmark.csv")

@app.post("/price")
def get_price(ville: str, surface: float):
  price = calculate_price(ville, surface, benchmark_df)
  return {"estimated_price": price}

@app.post("/anomaly")
def check_anomaly(city: str, actual_price: float, surface: float):
    return detect_anomaly(city, actual_price, surface, benchmark_df)
