# MLOP – House Price Calculator API

This repository contains a simple **FastAPI-based REST API** for estimating house prices using a transparent, rule-based scoring function.

The project is designed as a learning-oriented backend service and follows basic **MLOps / backend best practices**:
- separation between API layer and business logic
- containerization with Docker
- dependency management via `pyproject.toml`

---

The API exposes an endpoint that:
- accepts house characteristics (size, rooms, location score, energy rating, etc.)
- computes an estimated house price
- returns a detailed price breakdown and a confidence score

This is **not a machine learning model (yet)**.  
It is a deterministic pricing function that can later be replaced or extended with ML.

```text
------------------------------------------
Project structure:
├── app/
│ ├── main.py # FastAPI entrypoint (API layer)
│ └── scoring.py # House price scoring logic
├── Dockerfile
├── pyproject.toml
├── .gitignore
└── README.md



