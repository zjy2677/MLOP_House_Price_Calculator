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

st.divider()

if st.button("Estimate Price"):
    estimated_price = calculate_price(city, surface, df)
    st.success(f"The estimated price of this house is approximately {data['estimated_price']:.2f} euros")
 
# Anomaly detection module
if st.button("Check Anomaly"):
    result = detect_anomaly(city, actual_price, surface, df)
    if result['status'] == 'anomaly_overprice':
        st.error("This house is overpriced")
    elif result['status'] == 'anomaly_underprice':
        st.warning("This house is underpriced")
    else:
        st.success("This house is in normal price range")
