import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from backend.services.scoring import calculate_price, load_benchmark_data
from backend.services.anomaly import detect_anomaly
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
        
background_path = Path(__file__).parent / "background.png"
base64_img = get_base64(background_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
        linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
        url("data:image/png;base64,{base64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

data_path = Path("data/city_price_benchmark.csv")
df = load_benchmark_data(data_path)

st.title("Price a house")

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
ratio = actual_price / estimated_price
st.divider()

if st.button("Estimate house price"):
    st.success(f"The estimated price of this house is approximately {estimated_price:.2f} euros")
 
# Anomaly detection module
if st.button("Show pricing analysis"):
    result = detect_anomaly(city, actual_price, surface, df)
    if result['status'] == 'anomaly_overprice':
        st.error(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio:.2f} times of our estimation. This has surpassed 1.3 times benchmark so please be careful that this house is overpriced. We do not recommend you a purchase action on this property")
    elif result['status'] == 'anomaly_underprice':
        st.warning(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio*100:.2f}% of our estimation. This has dropped below 80% benchmark, please be aware that for some reasons this house is underpriced. We recommend you to be cautious when making your decisions")
    else:
        st.success(f"This actual price {actual_price:.2f} is {ratio*100:.2f}% of our estimated price {estimated_price:.2f} and stays in acceptable range of 80% - 130%. We thus conclude that this property is priced normally and you may take your desired actions")
