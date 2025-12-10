# backend/workload_service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

from .load_runner import (
    start_load,
    stop_load,
    get_status,
    get_config,
    update_config,
)

app = FastAPI(title="Workload Generator Service")


class WorkloadConfig(BaseModel):
    target_rps: int = 5
    mode: str = "orders"


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/config", response_model=WorkloadConfig)
async def read_config():
    cfg = get_config()
    return WorkloadConfig(**cfg)


@app.put("/config", response_model=WorkloadConfig)
async def set_config(new_cfg: WorkloadConfig):
    updated = update_config(new_cfg.model_dict())
    return WorkloadConfig(**updated)


@app.post("/start")
async def start():
    # fire-and-forget background task
    asyncio.create_task(start_load())
    return {"status": "started"}


@app.post("/stop")
async def stop():
    stop_load()
    return {"status": "stopped"}


@app.get("/status")
async def status():
    return get_status()
