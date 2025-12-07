# backend/order_worker/worker.py
import asyncio
import json
from shared.redis_client import get_redis_client
from shared.models import Order

STREAM_KEY = "orders-stream"
GROUP_NAME = "order-workers"
CONSUMER_NAME = "worker-1"

r = get_redis_client()

async def start_order_consumer():
    # create consumer group if it doesn't exist
    try:
        r.xgroup_create(STREAM_KEY, GROUP_NAME, id="$", mkstream=True)
    except Exception:
        pass

    while True:
        resp = r.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={STREAM_KEY: '>'},
            count=10,
            block=5000,
        )

        if not resp:
            await asyncio.sleep(0.1)
            continue

        for _stream, messages in resp:
            for msg_id, fields in messages:
                await process_order_message(msg_id, fields)

async def process_order_message(msg_id: str, fields: dict):
    order_id = fields.get("order_id")
    if not order_id:
        r.xack(STREAM_KEY, GROUP_NAME, msg_id)
        return

    raw = r.get(f"order:{order_id}")
    if not raw:
        r.xack(STREAM_KEY, GROUP_NAME, msg_id)
        return

    order = Order.model_validate_json(raw)

    # simulate processing
    order.status = "confirmed"

    # save updated order
    r.set(f"order:{order_id}", order.model_dump_json())

    r.xack(STREAM_KEY, GROUP_NAME, msg_id)
