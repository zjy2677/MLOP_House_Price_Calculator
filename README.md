# Real Estate Analysis Prototype (Startup Week-1 Scaffold)

## 1) Project Overview
This repository is a **starter engineering foundation** for a student startup prototype in real estate analytics.

**Product vision (future):**
- property search support
- fair-price estimation
- anomaly detection (overpriced / suspiciously cheap)
- risk explanation for buyers

**Current scope (this scaffold):**
- working local architecture with **Streamlit + FastAPI + PostgreSQL + Docker Compose**
- minimal end-to-end flow from UI to API
- baseline service stubs with TODO ownership for a 3-person team

> This is intentionally **not a finished product**. Major logic is left for the team to build manually.

---

## 2) What Is Already Built
### Scaffolded by this starter repo
- Dockerized multi-service setup (`frontend`, `api`, `db`).
- Streamlit form that sends property input to backend.
- FastAPI endpoint `POST /api/v1/analyze` with baseline response.
- Service-layer modules for pricing, anomaly label, and risk text.
- PostgreSQL schema initialization script.
- Sample CSV data for baseline experiments.
- Team docs for architecture and milestones.

### Intentionally incomplete
- robust pricing model and calibration
- statistical anomaly detection
- persistence from API endpoint to DB tables
- historical comps retrieval/query APIs
- UI polish and charts
- test coverage and CI

---

## 3) Architecture
Simple request path:

`User -> Streamlit Frontend -> FastAPI API -> Services -> PostgreSQL`

### Components
- **Frontend (`frontend/`)**: collects property details, displays basic results.
- **API (`api/`)**: validates request, orchestrates baseline analysis pipeline.
- **Service layer (`api/services/`)**: placeholder business logic modules.
- **Database (`database/init.sql`)**: starter tables (`properties`, `analyses`).
- **Data (`data/sample_properties.csv`)**: seed-like dataset for experiments.

---

## 4) How to Run Locally
### Prerequisites
- Docker + Docker Compose
- (Optional) Python 3.11 for local non-container tests

### Setup
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Build and start everything:
   ```bash
   docker compose up --build
   ```
3. Open apps:
   - Frontend (Streamlit): http://localhost:8501
   - API docs (Swagger): http://localhost:8000/docs
   - API health: http://localhost:8000/health

### Database inspection
Use psql through the DB container:
```bash
docker exec -it realestate-db psql -U realestate_user -d realestate
```
Then run:
```sql
\dt
SELECT * FROM properties;
SELECT * FROM analyses;
```

---

## 5) Team Division for 3 People (Startup-Style)

## Person 1 — Frontend / Product Flow
**Owns user journey and UX clarity.**

### Start with files
- `frontend/app.py`
- `docs/architecture.md`

### Concrete next tasks
- Improve layout (sections, cards, visual hierarchy).
- Add frontend input validation and friendly error states.
- Add comparison visuals (e.g., listing vs fair price bar/chart).
- Show “confidence / warning badges” based on API response.

### Dependencies
- Depends on Person 2 for stable API contract.
- Works with Person 3 to present risk/anomaly explanations clearly.

### Definition of Done
- New user can run app and understand result in < 30 seconds.
- Validation prevents obvious bad input.
- UI communicates uncertainty and caveats.

---

## Person 2 — Backend / API / Data Flow
**Owns interfaces, orchestration, and persistence.**

### Start with files
- `api/main.py`
- `api/routes/analysis.py`
- `api/services/db.py`
- `database/init.sql`

### Concrete next tasks
- Persist each request/response in `properties` + `analyses` tables.
- Add endpoint(s) to fetch recent analyses.
- Introduce repository/service boundaries (without overengineering).
- Add backend tests for route contracts and error handling.

### Dependencies
- Needs Person 3 data logic for improved analysis outputs.
- Provides Person 1 with stable response schemas.

### Definition of Done
- API stores analysis history reliably.
- API contract is documented and versioned.
- Core endpoints covered by basic tests.

---

## Person 3 — Data / Analytics / Detection Logic
**Owns baseline models and reasoning quality.**

### Start with files
- `api/services/pricing.py`
- `api/services/anomaly.py`
- `api/services/risk.py`
- `data/sample_properties.csv`

### Concrete next tasks
- Build baseline price-per-m² logic by district/city from CSV.
- Replace hard thresholds with simple data-derived anomaly method.
- Improve risk explanation with factor-level reasoning.
- Create evaluation scenarios and expected outputs.

### Dependencies
- Needs Person 2 integration path for loading data/persisting outcomes.
- Coordinates with Person 1 for how insights should appear in UI.

### Definition of Done
- Baseline pricing outperforms naive fixed-rule version.
- Anomaly logic is consistent on curated test cases.
- Explanations map to measurable factors.

---

## 6) Suggested Milestones
- **Milestone 1:** environment runs locally (`docker compose up --build`)
- **Milestone 2:** frontend submits to API and displays baseline output
- **Milestone 3:** pricing baseline calibrated on sample data
- **Milestone 4:** anomaly detection logic improved and tested
- **Milestone 5:** DB persistence integrated in API
- **Milestone 6:** demo polish + documentation + dry run

(See `docs/milestones.md` for details.)

---

## 7) Collaboration Rules
- Use **feature branches** (`feat/frontend-validation`, `feat/api-persistence`, etc.).
- Keep PRs small and reviewable.
- Agree naming conventions for payload fields early.
- Document assumptions inside code and PR descriptions.
- Re-run containers frequently after each merged change.
- Avoid breaking API contracts without team alignment.

---

## 8) What Must Be Built Manually by Students
The following is intentionally left for your team:
- robust price estimation approach and calibration
- anomaly detection based on actual market distributions
- DB read/write workflows in production-style service boundaries
- proper tests (unit + API integration)
- richer frontend visualizations and decision support
- edge-case handling and business rule definition

**If these are not implemented by the team, the prototype remains only a scaffold.**

---

## 9) Future Improvements (After Course MVP)
- Better models (linear/GBM/regression with explainability)
- Real listing ingestion pipelines
- Caching for repeated analyses
- Monitoring (request metrics, latency, error rates)
- Service decomposition (pricing/anomaly as separate services)
- Scale improvements (async workers, queueing, model serving)

---

## Quick Reference: Important Files
- Frontend app: `frontend/app.py`
- API entrypoint: `api/main.py`
- Main API route: `api/routes/analysis.py`
- Pricing/anomaly/risk logic: `api/services/`
- DB schema: `database/init.sql`
- Sample data: `data/sample_properties.csv`
- Architecture notes: `docs/architecture.md`
- Milestone plan: `docs/milestones.md`

