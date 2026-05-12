from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RegionInput:
    region: str
    demand: float
    supply_capacity: float
    transport_cost: float



def _validate_payload(payload: dict[str, Any]) -> list[RegionInput]:
    if "regions" not in payload or not isinstance(payload["regions"], list):
        raise ValueError("Payload must contain a 'regions' list.")

    parsed: list[RegionInput] = []
    for row in payload["regions"]:
        region = str(row.get("region", "")).strip()
        if not region:
            raise ValueError("Every row must include a region name.")

        try:
            demand = float(row.get("demand", 0))
            supply_capacity = float(row.get("supply_capacity", 0))
            transport_cost = float(row.get("transport_cost", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid numeric value for region {region}.") from exc

        if demand < 0 or supply_capacity < 0 or transport_cost < 0:
            raise ValueError(f"Values must be non-negative for region {region}.")

        parsed.append(
            RegionInput(
                region=region,
                demand=demand,
                supply_capacity=supply_capacity,
                transport_cost=transport_cost,
            )
        )

    return parsed



def optimize_gas_distribution(payload: dict[str, Any]) -> dict[str, Any]:
    """Simple cost-minimizing allocator.

    The allocator greedily fills regional demand from lowest transport cost
    regions first, subject to each region's supply capacity.
    """
    regions = _validate_payload(payload)

    total_demand = sum(r.demand for r in regions)
    total_capacity = sum(r.supply_capacity for r in regions)

    demand_remaining = total_demand
    allocations: list[dict[str, Any]] = []

    for region in sorted(regions, key=lambda r: r.transport_cost):
        shipped = min(region.supply_capacity, demand_remaining)
        demand_remaining -= shipped
        utilization = (shipped / region.supply_capacity * 100) if region.supply_capacity else 0.0
        allocations.append(
            {
                "region": region.region,
                "demand": round(region.demand, 2),
                "supply_capacity": round(region.supply_capacity, 2),
                "transport_cost": round(region.transport_cost, 2),
                "allocation": round(shipped, 2),
                "utilization_pct": round(utilization, 2),
                "unmet_demand": round(max(region.demand - shipped, 0), 2),
            }
        )

    total_shipped = sum(a["allocation"] for a in allocations)
    weighted_cost = sum(a["allocation"] * a["transport_cost"] for a in allocations)

    summary = {
        "total_demand": round(total_demand, 2),
        "total_capacity": round(total_capacity, 2),
        "total_shipped": round(total_shipped, 2),
        "unmet_demand": round(max(total_demand - total_shipped, 0), 2),
        "average_transport_cost": round(weighted_cost / total_shipped, 4) if total_shipped else 0,
        "total_transport_cost": round(weighted_cost, 2),
    }

    return {
        "summary": summary,
        "allocations": allocations,
    }


SAMPLE_DATA = {
    "regions": [
        {"region": "Alberta", "demand": 160, "supply_capacity": 180, "transport_cost": 1.8},
        {"region": "British Columbia", "demand": 95, "supply_capacity": 110, "transport_cost": 2.3},
        {"region": "Midwest", "demand": 210, "supply_capacity": 190, "transport_cost": 1.5},
        {"region": "Northeast", "demand": 170, "supply_capacity": 120, "transport_cost": 2.9},
        {"region": "Gulf Coast", "demand": 140, "supply_capacity": 220, "transport_cost": 1.2},
    ]
}
