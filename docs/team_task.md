# Project Overview

This project is a **property price checker prototype**
By far this is just a naive thought and could be changed during development phase

The goal is to help users evaluate a property listing by:
- estimating a fair market price from historical transactions,
- comparing the listing price to that estimate,
- flagging potential anomalies (overpriced or suspiciously cheap listings).

User inputs:
- commune,
- property size (m²),
- number of bedrooms,
- listing price.

Expected backend logic:
- retrieve benchmark `avg_price_m2` for the commune,
- compute `estimated_price = avg_price_m2 × property_size`,
- compute ratio `listing_price / estimated_price`,
- classify listing status:
  - `> 1.3`: overpriced,
  - `< 0.7`: suspiciously cheap,
  - otherwise: within market range.

# Project Architecture

The prototype follows a simple 3-layer architecture:

1. **Frontend (Streamlit)**
   - Collects user input.
   - Sends a request to the backend.
   - Displays estimate and anomaly status.

2. **Backend (FastAPI service)**
   - Exposes analysis API endpoint(s).
   - Loads benchmark dataset.
   - Computes fair price and anomaly label.

3. **Data layer (CSV benchmark)**
   - Stores average price per m² by commune.
   - Provides baseline values for price estimation.

# Repository Structure

Current repository structure (prototype):

```text
.
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── services/
│       ├── anomaly.py
│       └── scoring.py
├── data/
│   ├── city_price_benchmark.csv
│   └── samples.csv
├── docs/
│   ├── team_task.md
│   └── team_tasks.md
├── docker-compose.yml
├── README.md
└── pyproject.toml
```

# Data Pipeline (completed work)

Data source: French **DVF real estate transaction dataset**.

Completed preparation steps:
1. Loaded raw DVF data with pandas.
2. Kept only relevant transactions:
   - property types: `Maison` and `Appartement`,
   - valid surface: `Surface reelle bati > 0`.
3. Computed price per square meter:
   - `price_m2 = Valeur fonciere / Surface reelle bati`.
4. Aggregated by commune:
   - `avg_price_m2 = mean(price_m2) grouped by Commune`.
5. Exported benchmark file to:
   - `data/city_price_benchmark.csv`.

This data preparation work is **already completed** and ready for backend usage.

# Division of Work

## Member A — Frontend
- Build and polish Streamlit interface in `frontend/app.py`.
- Handle input validation and clear result display.
- Connect frontend requests to backend API.

## Member B — Backend
- Implement/complete analysis endpoint in `backend/main.py`.
- Use backend services for pricing and anomaly classification.
- Ensure API response format is stable for frontend integration.

## Member C — Data
- Maintain benchmark dataset quality and updates.
- Verify commune coverage and data consistency.
- Provide sample test inputs and expected outputs for validation.

# Tasks Already Completed

Completed items:
- Initial repository scaffold and Docker setup.
- Core project folders for frontend, backend, data, and docs.
- Data cleaning/preprocessing for DVF transactions.
- Benchmark price calculation per commune.
- Creation of `data/city_price_benchmark.csv`.

# Remaining Tasks

## Frontend
- Build final Streamlit UI flow.
- Connect UI form submission to backend endpoint.
- Improve result presentation (estimated price, ratio, status).

## Backend
- Implement `/analyze` endpoint behavior.
- Load and query benchmark CSV by commune.
- Finalize fair price estimation logic.
- Finalize anomaly detection thresholds and output labels.

## Integration & Validation
- End-to-end connection: frontend ↔ backend.
- Functional tests on representative sample listings.
- Prepare one demo scenario for project presentation.

# Development Milestones

1. **Milestone 1 — Data readiness (Done)**
   - DVF filtering, feature computation, and commune benchmark export completed.

2. **Milestone 2 — Backend analysis service (In progress)**
   - Complete endpoint + pricing/anomaly logic using benchmark data.

3. **Milestone 3 — Frontend and API integration (To do)**
   - Connect Streamlit form to backend and show analysis output.

4. **Milestone 4 — End-to-end validation and demo (To do)**
   - Test full pipeline and finalize demonstration example.


