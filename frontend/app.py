import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from backend.services.scoring import calculate_price, load_benchmark_data
from backend.services.anomaly import detect_anomaly


data_path = Path("data/city_price_benchmark.csv")
df = load_benchmark_data(data_path)

st.title("House Price Prototype")

st.sidebar.title("Instructions")

st.sidebar.markdown(
    """
### How to use this app

1. Select a city from the dropdown
2. Input the surface area of the house
3. Input the actual price of the house
4. Click the buttons to check the estimated price and anomaly status
"""
)

# Inputs start from here
cities = sorted(df["Commune"].tolist())
city = st.selectbox("Select City", cities)
surface = st.number_input("Surface (m²)", min_value=1.0)
actual_price = st.number_input("Actual Price", min_value=1.0)
estimated_price = calculate_price(city, surface, df)

st.divider()

if st.button("Estimate house price"):
    st.success(f"The estimated price of this house is approximately {estimated_price:.2f} euros")
 
# Anomaly detection module
if st.button("Show pricing analysis"):
    result = detect_anomaly(city, actual_price, surface, df)
    if result['status'] == 'anomaly_overprice':
        st.error(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} has exceeded 1.3 times of the estimated price, please be careful that this house is overpriced.")
    elif result['status'] == 'anomaly_underprice':
        st.warning(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} has dropped below 80% of the estimated price, this house is underpriced and please be aware.")
    else:
        st.success(f"This actual price {actual_price:.2f} stays in range 80% - 130% of our estimated price {estimated_price:.2f}. The price is considered as noraml")
