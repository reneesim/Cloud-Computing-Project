# backend/workload_service/load_runner.py
import asyncio
import time
import os
import httpx

TARGET_API = os.getenv("TARGET_API", "http://localhost:8000")  # api-gateway URL

_config = {
    "target_rps": 100,      # default requests per second
    "mode": "orders",     # could be "orders" or "tickets" later if you want
}

_is_running = False

_stats = {
    "total_requests": 0,
    "success": 0,
    "failure": 0,
    "avg_latency_ms": 0.0,
    "last_error": None,
}


def get_config() -> dict:
    return _config.copy()


def update_config(new_cfg: dict) -> dict:
    _config.update(new_cfg)
    return get_config()


def get_status() -> dict:
    return {
        "running": _is_running,
        "config": get_config(),
        "stats": _stats.copy(),
    }


def stop_load():
    global _is_running
    _is_running = False


async def _send_one_request(client: httpx.AsyncClient):
    """
    For now, send a POST /orders with some dummy payload.
    This will exercise both api-gateway and worker.
    """
    payload = {
        "customer": {"name": "LoadTester", "email": "load@test.com"},
        "items": [
            {"ticketId": "t1", "qty": 1}
        ],
        "paymentMethod": "credit_card",
    }

    start = time.perf_counter()
    try:
        resp = await client.post(f"{TARGET_API}/orders", json=payload)
        elapsed_ms = (time.perf_counter() - start) * 1000

        _stats["total_requests"] += 1
        if resp.status_code in (200, 201, 202):
            _stats["success"] += 1
        else:
            _stats["failure"] += 1
            _stats["last_error"] = f"HTTP {resp.status_code}: {resp.text[:200]}"

        # simple moving average
        _stats["avg_latency_ms"] = (
            0.9 * _stats["avg_latency_ms"] + 0.1 * elapsed_ms
        )

    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        _stats["total_requests"] += 1
        _stats["failure"] += 1
        _stats["last_error"] = str(e)
        _stats["avg_latency_ms"] = (
            0.9 * _stats["avg_latency_ms"] + 0.1 * elapsed_ms
        )


async def start_load():
    """
    Starts the load generator loop. This should be scheduled as a background task
    from FastAPI (we don't block the request handler).
    """
    global _is_running
    if _is_running:
        return  # already running

    _is_running = True

    async with httpx.AsyncClient(timeout=5.0) as client:
        while _is_running:
            rps = max(_config.get("target_rps", 1), 1)
            delay = 1.0 / rps

            await _send_one_request(client)
            await asyncio.sleep(delay)
