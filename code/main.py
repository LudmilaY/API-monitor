from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import date
from enum import Enum

from calculate_utils import (
    max_power_per_day,
    medium_temperature_per_day,
    plant_generation_per_range,
    inverter_generation_per_range,
)

app = FastAPI(title="API de Usinas Fotovoltaicas")

class MetricType(str, Enum):
    max_power = "max_power"
    medium_temperature = "medium_temperature"
    plant_generation = "plant_generation"
    inverter_generation = "inverter_generation"

@app.get("/search-metrics")
def search_metric(
    tipo: MetricType,
    data_start: date,
    data_end: date,
    inverter_id: Optional[int] = None,
    plant_id: Optional[int] = None
):
    if tipo == MetricType.max_power:
        if not inverter_id:
            raise HTTPException(status_code=400, detail="inverter_id is a constraint to maximum power metric.")
        return [
            {"data": str(d), "max_power": p}
            for d, p in max_power_per_day(inverter_id, data_start, data_end)
        ]

    elif tipo == MetricType.medium_temperature:
        if not inverter_id:
            raise HTTPException(status_code=400, detail="inverter_id is a constraint to medium temperature metric.")
        return [
            {"data": str(d), "medium_temperature": t}
            for d, t in medium_temperature_per_day(inverter_id, data_start, data_end)
        ]

    elif tipo == MetricType.plant_generation:
        if not plant_id:
            raise HTTPException(status_code=400, detail="plant_id is a constraint to plant generation metric.")
        return [
            {"data": str(d), "total_energy": e}
            for d, e in plant_generation_per_range(plant_id, data_start, data_end)
        ]

    elif tipo == MetricType.inverter_generation:
        if not inverter_id:
            raise HTTPException(status_code=400, detail="inverter_id is a constraint to inverter generation metric.")
        return [
            {"data": str(d), "total_energy": e}
            for d, e in inverter_generation_per_range(inverter_id, data_start, data_end)
        ]

    else:
        raise HTTPException(status_code=400, detail="Invalid metric type")
