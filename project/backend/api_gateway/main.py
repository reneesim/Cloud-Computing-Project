import json
import uuid
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import os

# ---------------------------------------------------------------------
# Redis connection
# ---------------------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost") # need to set redis in docker environment
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://129.192.69.172:30080"
        ]
    }
})

# =====================================================================
# Redis Keys Used
# =====================================================================
# tickets list      → "tickets" (list of ticket IDs)
# ticket:{id}       → hash storing ticket fields
# order:{id}        → JSON blob for order object
# =====================================================================


# ---------------------------------------------------------------------
# Helper: Load all tickets from Redis
# ---------------------------------------------------------------------
def load_all_tickets():
    ticket_ids = r.lrange("tickets", 0, -1)
    tickets = []
    for tid in ticket_ids:
        t = r.hgetall(f"ticket:{tid}")
        if t:
            # convert numeric strings back to proper types
            t["price"] = float(t["price"])
            tickets.append(t)
    return tickets


# ---------------------------------------------------------------------
# Helper: Store ticket in Redis
# ---------------------------------------------------------------------
def add_ticket(ticket):
    ticket_id = ticket["id"]
    r.rpush("tickets", ticket_id)
    r.hset(f"ticket:{ticket_id}", mapping=ticket)


# ---------------------------------------------------------------------
# Helper: Bootstrap demo tickets if missing
# ---------------------------------------------------------------------
def bootstrap_tickets():
    if r.llen("tickets") == 0:
        print("Bootstrapping demo tickets...")
        
        add_ticket({
            "id": "t1",
            "name": "Concert",
            "type": "adult",
            "price": "25.00",
            "currency": "EUR",
            "description": "Standard adult ticket",
            "stock": "100"
        })
        add_ticket({
            "id": "t2",
            "name": "Concert",
            "type": "child",
            "price": "12.00",
            "currency": "EUR",
            "description": "Child ticket ages 3–12",
            "stock": "50"
        })

        add_ticket({
            "id": "t3",
            "name": "Concert",
            "type": "vip",
            "price": "60.00",
            "currency": "EUR",
            "description": "VIP ticket with front-row seating",
            "stock": "20"
        })

        add_ticket({
            "id": "t4",
            "name": "Festival Day Pass",
            "type": "adult",
            "price": "40.00",
            "currency": "EUR",
            "description": "One-day access to the music festival",
            "stock": "200"
        })

        add_ticket({
            "id": "t5",
            "name": "Festival Weekend Pass",
            "type": "adult",
            "price": "90.00",
            "currency": "EUR",
            "description": "Full weekend access to all stages and events",
            "stock": "120"
        })

        add_ticket({
            "id": "t6",
            "name": "Theatre Show",
            "type": "balcony",
            "price": "30.00",
            "currency": "EUR",
            "description": "Balcony seat for evening theatre performance",
            "stock": "80"
        })

        add_ticket({
            "id": "t7",
            "name": "Theatre Show",
            "type": "front-row",
            "price": "55.00",
            "currency": "EUR",
            "description": "Front-row premium theatre seat",
            "stock": "40"
        })

        add_ticket({
            "id": "t8",
            "name": "Movie Night",
            "type": "standard",
            "price": "10.00",
            "currency": "EUR",
            "description": "Standard cinema entry ticket",
            "stock": "150"
        })

        add_ticket({
            "id": "t9",
            "name": "Movie Night",
            "type": "student",
            "price": "7.50",
            "currency": "EUR",
            "description": "Discounted ticket for students (ID required)",
            "stock": "70"
        })



bootstrap_tickets()


# ---------------------------------------------------------------------
# Helper: Calculate order totals
# ---------------------------------------------------------------------
def calculate_order_total(items):
    total = 0
    detailed_items = []

    for item in items:
        tid = item["ticketId"]
        qty = int(item["qty"])

        ticket = r.hgetall(f"ticket:{tid}")
        if not ticket:
            return None, f"Invalid ticketId: {tid}"

        unit_price = float(ticket["price"])
        subtotal = unit_price * qty

        detailed_items.append({
            "ticketId": tid,
            "type": ticket["type"],
            "qty": qty,
            "unitPrice": unit_price,
            "total": subtotal
        })

        total += subtotal

    return detailed_items, total


# =====================================================================
# GET /tickets
# =====================================================================
@app.route("/tickets", methods=["GET"])
def get_tickets():
    type_filter = request.args.get("type")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    tickets = load_all_tickets()

    if type_filter:
        tickets = [t for t in tickets if t["type"] == type_filter]

    if min_price:
        tickets = [t for t in tickets if t["price"] >= float(min_price)]

    if max_price:
        tickets = [t for t in tickets if t["price"] <= float(max_price)]

    return jsonify({"tickets": tickets}), 200


# =====================================================================
# GET /orders/{orderId}
# =====================================================================
@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    raw = r.get(f"order:{order_id}")
    if not raw:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(json.loads(raw)), 200


# =====================================================================
# POST /orders
# =====================================================================
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    # Validate required fields
    if "customer" not in data or "items" not in data or "paymentMethod" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    items = data["items"]

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "Items must be a non-empty array"}), 400

    # Calculate totals
    detailed_items, grand_total = calculate_order_total(items)
    if detailed_items is None:
        return jsonify({"error": grand_total}), 400

    order_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow().isoformat() + "Z"

    order = {
        "orderId": order_id,
        "customer": data["customer"],
        "items": detailed_items,
        "grandTotal": grand_total,
        "currency": "EUR",
        "status": "pending",
        "createdAt": now,
        "message": "Order pending confirmation"
    }

    # Store in Redis as JSON
    r.set(f"order:{order_id}", json.dumps(order))

    r.xadd("orders-stream", {"order_id": order_id})


    '''
    response = {
       "orderId": order_id,
        "status": "confirmed",
        "grandTotal": grand_total,
        "currency": "EUR",
        "message": "Order successfully created"
    }
    '''

    return jsonify(order), 201


# =====================================================================
# Root
# =====================================================================
@app.route("/", methods=["GET"])
def root():
    return jsonify({"ok": True, "service": "Ticket Service API (Redis Backend)"})


# =====================================================================
# Entry point
# =====================================================================
if __name__ == "__main__":
    print("Starting Redis-backed Ticket Service on 0.0.0.0:5000")
    #app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=8000)
