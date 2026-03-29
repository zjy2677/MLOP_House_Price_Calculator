import os
from services.scoring import load_benchmark_data, calculate_price

benchmark_df = load_benchmark_data("/data/city_price_benchmark.csv")

@app.post("/price")
def get_price(ville: str, surface: float):
  price = calculate_price(ville, surface, benchmark_df)
  return {"estimated_price": price}
