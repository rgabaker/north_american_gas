# north_american_gas

A FastAPI + JavaScript interface for running a natural gas distribution optimization and visualizing inputs/outputs.

## Project structure

- `data/input_data.json`: default input dataset (restored) loaded by the API.
- `backend/optimization_module.py`: optimization logic and validation.
- `backend/app.py`: FastAPI server + API routes.
- `static/index.html`: JavaScript dashboard UI.

## Run locally

```bash
pip install fastapi uvicorn pydantic
uvicorn backend.app:app --reload
```

Then open: `http://127.0.0.1:8000`

## Features

- Editable input grid for regional demand, supply capacity, and transport cost.
- Loads default input dataset from `data/input_data.json` via `/api/sample-data`.
- Optimizer API endpoint (`/api/optimize`) backed by `backend/optimization_module.py`.
- Interactive charts (Chart.js) for allocation vs. demand and utilization.
- Output table, summary KPI cards, and explicit run/error status messages.
