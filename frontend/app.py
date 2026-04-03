import streamlit as st
import requests
import os
from pathlib import Path
import pandas as pd
import base64


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

data_path = os.getenv("DATA_PATH")
if not data_path:
    raise RuntimeError("Missing required environment variable: DATA_PATH")
data_path = Path(data_path)
if not data_path.exists():
    raise RuntimeError(f"DATA_PATH does not exist: {data_path}")

background_path = os.getenv("BACKGROUND_IMAGE_PATH")
if not background_path:
    raise RuntimeError("Missing required environment variable: BACKGROUND_IMAGE_PATH")
background_path = Path(background_path)
if not background_path.exists():
    raise RuntimeError(f"BACKGROUND_IMAGE_PATH does not exist: {background_path}")

df = pd.read_csv(data_path)
    
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if Path(background_path).exists():
    base64_img = get_base64(Path(background_path))
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
            linear-gradient(rgba(0,0,0,0.48), rgba(0,0,0,0.48)),
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

st.title("PriceYourHouse")

st.sidebar.title("User's Guide")

st.sidebar.markdown(
    """
### Weclome to PriceYourHouse!

This app will help you check the value of a property
1. You select a city/region of the property
2. You type in the surface area and listed value of the property 
3. Upon clicking the estimate price button, you will get an estimated price of the property
4. Upon clicking the analysis button, you will see a detailed analysis on the listed price of the property
"""
)

# Inputs start from here
cities = sorted(df["Commune"].tolist())
city = st.selectbox("Select City", cities)
surface = st.number_input("Surface (m²)", min_value=1.0)
actual_price = st.number_input("Actual Price", min_value=1.0)

st.divider()

# Estimate price
if st.button("Estimate House Price"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/price",
            json={"city": city, "surface": surface}
        )

        if response.status_code == 200:
            data = response.json()
            st.success(
                f"The estimated price of this house is approximately {data['estimated_price']:.2f} euros"
            )
        else:
            st.error(response.json()["detail"])

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")


# Anomaly detection module
if st.button("Show Pricing Analysis"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/anomaly",
            json={
                "city": city,
                "actual_price": actual_price,
                "surface": surface
            }
        )

        if response.status_code == 200:
            data = response.json()

            estimated_price = data['estimated_price']
            actual_price = data['actual_price']
            ratio = actual_price / estimated_price

            if data['status'] == 'extreme_overprice':
                st.error(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio:.2f} times of our estimation. This has surpassed 1.6 times benchmark so please be careful that this house is extremely overpriced. We strongly do not recommend you to take any actions on this property")

            elif data['status'] == 'anomaly_overprice':
                st.warning(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio:.2f} times of our estimation. This has surpassed 1.3 times benchmark so please be careful that this house is overpriced. We do not recommend you to take actions on this property")

            elif data['status'] == 'extreme_underprice':
                st.error(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio*100:.2f}% of our estimation. This has dropped below 50% benchmark, please be aware that for some reasons this house is abnormally underpriced. We recommend you to be extremely cautious and do further investigations before any of your decisions")

            elif data['status'] == 'anomaly_underprice':
                st.warning(f"The estimated price of this house is {estimated_price:.2f}, the actual price {actual_price:.2f} is {ratio*100:.2f}% of our estimation. This has dropped below 80% benchmark, please be aware that for some reasons this house is underpriced. We recommend you to be cautious when making your decisions")

            else:
                st.success(f"This actual price {actual_price:.2f} is {ratio*100:.2f}% of our estimated price {estimated_price:.2f} and stays in acceptable range of 80% - 130%. We thus conclude that this property is priced normally and you may take your desired actions")
        else:
            st.error(response.json()["detail"])

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")
