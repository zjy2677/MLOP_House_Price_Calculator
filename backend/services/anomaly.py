from services.scoring import calculate_price
def detect_anomaly(ville: str, actual_price, surface: float, df):
  '''
  To detect whether there's anomaly existed, we compare it to our estimation using the following rules:
  (1) actual price > 1.3 * estimated price -> anomaly overpriced
  (2) actual price < 0.8 * estimated price -> anomaly underpriced 
  (3) o.w. we consider it to be normal
  '''
  # Two checkers for values and types
  if not isinstance(actual_price,(int,float)):
    raise TypeError("Actual price must be a numeric value")
  if actual_price <= 0:
    raise ValueError("Actual price must be greater than 0")
    
  if not isinstance(actual_price,(int,float)):
    raise TypeError("Actual price must be a numeric value")
  if surface <= 0:
    raise ValueError("Surface area must be greater than 0")

  estimated_price = calculate_price(city, surface, df)
  lower_bound = 0.8 * estimated_price
  upper_bound - 1.3 * estimated_price
  
  if actual_price < lower_bound:
        anomaly_type = "anomaly_underprice"
  elif actual_price > upper_bound:
        anomaly_type = "anomaly_overprice"
  else:
        anomaly_type = "normal"
  return {
        "city": city,
        "surface": surface,
        "actual_price": actual_price,
        "estimated_price": estimated_price,
        "status": anomaly_type
    }

  
