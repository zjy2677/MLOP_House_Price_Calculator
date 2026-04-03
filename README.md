# PriceYourHouse - Product Version
## What It Does and Why It Matters 

The French real estate market is highly fragmented. Individual agencies controlling small regional markets have built invisible walls that block the flow of pricing information. Customers looking for transparent benchmark prices can only resort to random web searches or word-of-mouth, causing both inefficiency and frustration.

PriceYourHouse was born out of this gap. We give each customer a personal experience when answering the questions that actually matter to them: **Am I paying a reasonable price for this house? If not, by how much am I off — and what should I do about it?**


## Product Overview 
Our product prototype encapsulates clear front-end and back-end logic. The minimalistic UI guides users with both user guide in the left panel (visible when clicking on the arrow mark) and the instructional input boxes. After uses input the city, the surface and the asking price that are compliant to the validation constraints, they can choose either to get an instant benchmark price calculation by clicking on the `Estimate house price` button, or jump directly into the price analysis (`Show pricing analysis` button) that compares the price of this selected property with the benchmark price of the house of identical surface in the same region. If our backend algorithm detects an anomaly, the user will be advise to conduct further investigations before purchasing.  

## Known Limitations
* **Prediction model is intentionally naive**. Our estimate is `avg_price_m2 × surface`, which gives a city-level average with no adjustment for property-specific features. Variables like district, floor, number of rooms, property age, or energy rating are not accounted for. This means the model can produce estimates that are plausible at the city level but miss the mark for a specific listing, especially in cities with high intra-city price variance (e.g., Paris arrondissements).
* **City coverage depends on DVF data quality**. Cities are populated from the benchmark dataset via a scrollable dropdown, so users can only select cities that exist in the data. However, if a city is sparsely represented in DVF, its benchmark rate may be statistically unreliable — the system has no mechanism to flag low-confidence estimates or fall back to a regional or departmental average.
* **The anomaly thresholds (−20% / +30%) are heuristics**. They were set manually and have not been validated against historical transaction data. A property flagged as overpriced may simply be premium; a property flagged as normal may still be a poor deal. Users should treat the output as a first filter, not a final verdict.
* **No authentication or rate limiting**. The API is fully open. In a production context, this would need to be addressed before any public-facing deployment.

## What We Did Not Deliver
We want to be transparet to the team maintaining or extending this system by calling out these following issues: 
* **No regression model**. We scoped this project as a rule-based benchmark tool. Training a regression model (e.g., with district, rooms, floor, energy class as features) would significantly improve accuracy.
* **No data refresh pipeline**. The benchmark CSV is static. DVF data is updated annually; there is currently no automated process to re-pull, re-aggregate, and redeploy updated benchmarks.
* **The anomaly recommendation is vague**. When an anomaly is detected, the user is advised to investigate further but is given no actionable next step (e.g., contact information for official valuation bodies or local agencies).

## What Could Be Done In The Future 
* Frontend
   * Migrate the current form-based UI to an LLM-powered chatbot interface, enabling users to ask ad-hoc questions beyond price and anomaly analysis.
   * Make anomaly recommendations more actionable — for example, by surfacing contact information for official departments (notaires, DGFiP) or well-established regional agencies when a pricing anomaly is detected.
   
* Backend
   * Replace the naive estimator with a regression model trained on DVF data, incorporating features such as district, number of rooms, floor level, property age, and energy rating. This would allow property-specific estimates rather than city-wide averages.
   * Introduce automated benchmark refresh: a scheduled job that pulls updated DVF exports, recomputes city averages, and redeploys the updated CSV without manual intervention.
   * Add confidence intervals to estimates, so users understand the reliability of the benchmark for their specific city.

------------------------------------------
# PriceYourHouse - Docker Version

This repository contains a simple **HOUSE PRICE CALCULATOR** for estimating house prices in FRANCE, it also has the ability to identify if , given a surface area(square meter) and its price(euros), the pricing is reasonable.


## Data Source

We use data from DVF of the past years and group by with cities. 
Thus, we were able to calculate a average price estimator of house in euros per squared meter.


```text
Project structure:

├── backend/
│   ├── services/
│   │   ├── anomaly.py
│   │   ├── scoring.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/
│   ├── city_price_benchmark.csv (This is the complete data file)
│   └── sample.csv (This contains test data sample)
│
├── .env.example
├── .gitignore
└── README.md
```
We seperated our repo into the following parts:<br>
(1)**backend**: This will contain a service folder which has scoring.py that calculates the price of the house and a anomaly.py that examine if alarm should be triggered. Main.py is for an entry-point to our backend logic where we run fastAPI service. Dockerfile and requirement.txt contains settings and requirements for running all the backend files.<br>

(2)**frontend**: This folder contains an app.py which defines our UI. Dockerfile and requirements.txt in this folder will ensure all necessary elements used in app.py are installed.<br>

(3)**Data**: Data folder contains a city_price_benchmark which contains average price of house in a specific city. Sample.csv contains a small part of the database for testing purpose only.<br>

(4)**.env.example**: Template of environment in case we need to hide some secrets like API keys.<br>

(5)**.gitignore**: Prevents potential leakage of sensitive data and avoids unnecessary files

------------------------------------------
## Methodology (Backend)

Our backend follows a simple rule-based pipeline powered by the benchmark table in `data/city_price_benchmark.csv`.

### 1) Load city benchmark data
- At startup, the API loads benchmark data from `city_price_benchmark.csv`.
- Each row contains a city (`Commune`) and its average price per square meter (`avg_price_m2`).

### 2) House price estimation logic
For each `price` request (`city`, `surface`):
1. Validate `surface` is numeric and strictly greater than 0.
2. Look up the city in the benchmark table.
3. Compute a baseline estimate:

`estimated_price = surface * avg_price_m2(city)`

This gives a reference value for the input property.

### 3) Anomaly detection logic
For each `anomaly` request (`city`, `surface`, `actual_price`):
1. Recompute the same baseline `estimated_price` using the scoring method above.
2. Build a tolerance interval around the estimate:
   - `lower_bound = 0.8 × estimated_price`
   - `upper_bound = 1.3 × estimated_price`
3. Classify pricing status with simple rules:
   - `actual_price < lower_bound`  → `anomaly_underprice`
   - `actual_price > upper_bound`  → `anomaly_overprice`
   - otherwise                     → `normal`

------------------------------------------
## How to Run (Docker - Codespaces)

Follow these steps to build and run the application using Docker.

---

### 1. Build Docker Images

Build both backend and frontend images:

```bash
docker build -f backend/Dockerfile -t house-backend .
docker build -f frontend/Dockerfile -t house-frontend .
```

---

### 2. Create a Docker Network

Create a shared network so containers can communicate:

```bash
docker network create house-net
```

---

### 3. Prepare Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Make sure your `.env` contains:

```env
DATA_PATH=/app/data/city_price_benchmark.csv
BACKGROUND_IMAGE_PATH=/app/background.png
BACKEND_URL=http://house-backend-container:8000
```

---

### 4. Run the Backend Container

Start the backend service:

```bash
docker run -d \
  --name house-backend-container \
  --network house-net \
  --env-file .env \
  -p 8000:8000 \
  house-backend
```

---

### 5. Run the Frontend Container

Start the frontend service:

```bash
docker run -d \
  --name house-frontend-container \
  --network house-net \
  --env-file .env \
  -p 8501:8501 \
  house-frontend
```

---

## Access the Application

- Frontend: http://localhost:8501  
- Backend API: http://localhost:8000  



