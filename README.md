# MLOP – House Price Calculator (FRANCE)

This repository contains a simple **HOUSE PRICE CALCULATOR** for estimating house prices in FRANCE, it also has the ability to identify that ,given a surface area(m^2) and its price(euros), the pricing is reasonable.

The project is designed as a learning-oriented backend service to 
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

We seperated our repo into the following parts:
(1)backend: This will contains a service folder which has scoring.py that calculates the
            overall score of the house and a anomaly.py that examine if alarm should be triggered.
            Main.py is for an entry-point to our backend logic where we run fastAPI service.
            Dockerfile and requirement.txt contains settings and requirements for running all the backend files.
(2)frontend: This folder contains an app.py which defines our UI. Dockerfile and requirements.txt in this folder
             will ensure all necessary elements used in app.py are installed.
(3)Data: Data folder contains a city_price_benchmark which contains average price of house in a specific city. Sample.csv contains a small part of the database for testing purpose only.
(4).env.example: Template of environment in case we need to hide some secrets like API keys.
(5).gitignore: Prevents potential leakage of sensitive data and avoids unnecessary files


