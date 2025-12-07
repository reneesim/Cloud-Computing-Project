from fastapi import FastAPI
import asyncio
from .worker import start_order_consumer

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    asyncio.create_task(start_order_consumer())
