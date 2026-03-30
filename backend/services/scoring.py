import pandas as pd

def load_benchmark_data(file_path:str):
  # This function is for loading data store inside /data
  df = pd.read_csv(file_path)
  return df
  
def get_avg_price(city: str, benchmark_df: pd.DataFrame) -> float:
  # This function is for retrieving the avg price stored in the database 
  # given the name of the city
  result = benchmark_df[benchmark_df["Commune"] == city]

  # This is for preparing the case of input mismatch and user's ivalid input 
  if result.empty:
    raise ValueError(f"Invalid input for column city:{city}")
  return float(result["avg_price_m2"].values[0])

  
def calculate_price(city: str, surface: float, benchmark_df: pd.DataFrame) -> float:
  # Caculate the theoretical average price simply using p = surface * avg_price/m^2
  # Check the surface area is indeed a numeric value not like abc
  if not isinstance(surface, (int, float)):
    raise TypeError("Surface area must be a numeric value")
  # Prevent user invalid input for surface area less than or equal to 0
  if surface <= 0:
    raise ValueError("Surface area should be greater than 0")
  return get_avg_price(city,benchmark_df) * surface 
  
