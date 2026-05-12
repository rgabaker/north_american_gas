# north_american_gas

A FastAPI + JavaScript interface for running a natural gas distribution optimization and visualizing inputs/outputs.

## Run locally

```bash
pip install fastapi uvicorn pydantic
uvicorn backend.app:app --reload
```

Then open: `http://127.0.0.1:8000`

## Features

- Editable input grid for regional demand, supply capacity, and transport cost.
- Optimizer API endpoint (`/api/optimize`) backed by `backend/optimization_module.py`.
- Interactive charts (Chart.js) for allocation vs. demand and utilization.
- Output table and summary KPI cards.
