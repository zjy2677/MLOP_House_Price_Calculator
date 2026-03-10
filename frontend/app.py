import os

import requests
import streamlit as st

st.set_page_config(page_title="Real Estate Prototype", layout="wide")
st.title("🏠 Real Estate Analysis Prototype")
st.caption("Week-1 scaffold: UI + API wiring + baseline analytics")

api_base_url = os.getenv("API_BASE_URL", "http://api:8000")

with st.form("analysis_form"):
    st.subheader("Property Input")

    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", value="Lisbon")
        district = st.text_input("District", value="Alvalade")
        area_m2 = st.number_input("Area (m²)", min_value=10.0, value=90.0, step=1.0)
        rooms = st.number_input("Rooms", min_value=1, max_value=20, value=3, step=1)

    with col2:
        year_built = st.number_input("Year Built", min_value=1800, max_value=2100, value=2005, step=1)
        energy_rating = st.selectbox("Energy Rating", ["A", "B", "C", "D", "E", "F", "G"], index=2)
        listing_price_eur = st.number_input(
            "Listing Price (EUR)", min_value=10000.0, value=350000.0, step=1000.0
        )

    submit = st.form_submit_button("Run Baseline Analysis")

if submit:
    payload = {
        "city": city,
        "district": district,
        "area_m2": area_m2,
        "rooms": rooms,
        "year_built": year_built,
        "energy_rating": energy_rating,
        "listing_price_eur": listing_price_eur,
    }

    try:
        response = requests.post(f"{api_base_url}/api/v1/analyze", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        st.success("Analysis completed")
        c1, c2, c3 = st.columns(3)
        c1.metric("Estimated Fair Price", f"€ {data['fair_price_eur']:,.0f}")
        c2.metric("Market Gap", f"{data['market_gap_pct']}%")
        c3.metric("Anomaly Label", data["anomaly_label"])

        st.subheader("Risk Explanation")
        st.write(data["risk_explanation"])

        st.subheader("Implementation Notes")
        for note in data["notes"]:
            st.write(f"- {note}")

        st.info("TODO (Person 1): Improve layout, charts, and decision-support UX.")

    except requests.RequestException as exc:
        st.error(f"Could not connect to API ({api_base_url}): {exc}")
