from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.optimization_module import load_default_input_data, optimize_gas_distribution


class OptimizeRequest(BaseModel):
    regions: list[dict]


app = FastAPI(title="North American Gas Optimizer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/sample-data")
def sample_data() -> dict:
    try:
        return load_default_input_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="Missing data/input_data.json") from exc


@app.post("/api/optimize")
def optimize(payload: OptimizeRequest) -> dict:
    try:
        return optimize_gas_distribution(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
