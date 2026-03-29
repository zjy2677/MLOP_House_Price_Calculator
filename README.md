# MLOP – House Price Calculator (FRANCE)

This repository contains a simple **HOUSE PRICE CALCULATOR** for estimating house prices in FRANCE.

The project is designed as a learning-oriented backend service and follows basic **MLOps / backend best practices**:
- Region: Whole France 
- Goal: Given a house in any city in France, we want an instant but primary inspection of it and have a general understanding of its price

------------------------------------------
# Data Source

We use data from DVF of the past years and group by with cities. 
Thus, we were able to calculate a average price estimator of house in euros/ m^2


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



