# backend/order_worker/worker.py
import asyncio
import json
from shared.redis_client import get_redis_client
from shared.models import Order
from typing import Tuple

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

    ok, reason = try_reserve_stock(order)

    if not ok:
        # out of stock (or misconfigured)
        order.status = "failed"
        order.message = "Order failed: insufficient stock"
        if hasattr(order, "failureReason"):
            order.failureReason = reason

        r.set(f"order:{order_id}", order.model_dump_json())
        r.xack(STREAM_KEY, GROUP_NAME, msg_id)
        return

    order.status = "confirmed"
    order.message = "Order confirmed"

    # save updated order
    r.set(f"order:{order_id}", order.model_dump_json())

    r.xack(STREAM_KEY, GROUP_NAME, msg_id)

def try_reserve_stock(order: Order) -> Tuple[bool, str | None]:
   
    # check stock first 
    for item in order.items:
        tid = item.ticketId
        qty = int(item.qty)

        ticket_key = f"ticket:{tid}"
        stock_raw = r.hget(ticket_key, "stock")

        # settle edge cases 
        if stock_raw is None:
            return False, f"No stock information for ticket {tid}"

        stock = int(stock_raw)

        if qty > stock:
            return False, f"Not enough stock for ticket {tid}. Requested {qty}, available {stock}"

    # if sufficnet stock, decrement stock 
    for item in order.items:
        tid = item.ticketId
        qty = int(item.qty)
        ticket_key = f"ticket:{tid}"
        r.hincrby(ticket_key, "stock", -qty)

    return True, None
