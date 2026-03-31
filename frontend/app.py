import streamlit as st
import requests
import os

# Backend URL (works locally, can change later for Docker)
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("House Price Prototype")

st.sidebar.title("Instructions")

st.sidebar.markdown("""
### How to use this app
1.Select a city PARIS 01 - PARIS 15
2.Input the Surface Area of the house
3.Input the actual price of the house
4.You can chekc the estimated price and status by clicking the two buttons
""")
# --- Inputs ---
city = st.text_input("City")
surface = st.number_input("Surface (m²)", min_value=1.0, step=1.0)
actual_price = st.number_input("Actual Price", min_value=1.0, step=1000.0)

st.divider()

# --- Price Estimation ---
if st.button("Estimate Price"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/price",
            json={
                "city": city,
                "surface": surface
            }
        )

        if response.status_code == 200:
            data = response.json()
            st.success(f"Estimated Price: {data['estimated_price']:.2f}")
        else:
            st.error(response.json()["detail"])

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")


# --- Anomaly Detection ---
if st.button("Check Anomaly"):
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

            st.write(f"Estimated Price: {data['estimated_price']:.2f}")
            st.write(f"Actual Price: {data['actual_price']:.2f}")
            st.write(f"Status: {data['status']}")

        else:
            st.error(response.json()["detail"])

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")
