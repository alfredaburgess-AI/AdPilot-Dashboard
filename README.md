# AdPilot AI — Analytics Dashboard

A professional multi-file **Streamlit** application for ad-campaign analytics,
AI-powered recommendations, and budget simulation.

## Quick Start

```bash
# 1 — Install dependencies
pip install -r requirements.txt

# 2 — Launch the dashboard
streamlit run main.py
```

The app opens at **http://localhost:8501**.

## Project Structure

```
adpilot-ai-dashboard/
├── main.py            # Streamlit UI — the dashboard entry point
├── data.py            # Simulated campaign, budget & trend data
├── engine.py          # AI recommendation & scoring engine
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Features

| Feature | Description |
|---|---|
| **KPI Cards** | Real-time ROAS, CTR, conversion rate, and spend with sparklines |
| **Campaign Table** | Searchable, filterable, sortable list of all campaigns |
| **ROAS Comparison** | Horizontal bar chart ranking campaigns by ROAS |
| **Budget Simulator** | Interactive sliders to model spend reallocation |
| **AI Analysis** | One-click analysis generates prioritized recommendations |
| **Forecasting** | Projected revenue uplift from optimization actions |
| **CSV Export** | Download campaign data as a CSV file |
| **New Campaign** | Add campaigns via an in-app dialog form |
