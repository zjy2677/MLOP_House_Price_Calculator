# Architecture (Starter)

## Target flow
User -> Streamlit Frontend -> FastAPI API -> Service Layer -> PostgreSQL

## Current scaffold
- `frontend/app.py`: sends property payload to `POST /api/v1/analyze`
- `api/routes/analysis.py`: orchestrates pricing + anomaly + risk functions
- `api/services/*`: baseline-only heuristics
- `database/init.sql`: starter schema

## Intentional gaps
- no persistence in analysis endpoint yet
- no robust comparables retrieval
- no model training/inference pipeline
- no auth, no production hardening

## Why this architecture
- Clear ownership across 3 team members
- Easy to run locally with Docker Compose
- Simple extension path to split services later
