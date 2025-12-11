import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getEvent } from "../api/events";
import { createOrder } from "../api/orders";

export default function EventDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [event, setEvent] = useState<any>(null);
    const [qty, setQty] = useState(1);

    useEffect(() => {
        if (id) getEvent(id).then(setEvent);
    }, [id]);

    if (!event) {
        return (
            <div className="flex items-center justify-center h-screen text-gray-500">
                Loading...
            </div>
        );
    }

    const handleBuy = async () => {
        const order = await createOrder({
            customer: {
                name: "John Doe",
                email: "john@example.com",
            },
            paymentMethod: "credit_card",
            items: [
                {
                    ticketId: event.id,
                    qty: qty,
                },
            ],
        });

        navigate(`/orders/${order.orderId}`);
    };

    return (
        <div className="flex justify-center p-6">
            <div className="w-full max-w-lg bg-white rounded-xl shadow-md p-6">
                {/* Header */}
                <h1 className="text-3xl font-bold text-gray-900">{event.name}</h1>
                <p className="text-gray-600 mt-1">{event.type}</p>

                {/* Price */}
                <div className="mt-4 text-2xl font-semibold text-blue-600">
                    €{event.price}
                </div>

                {/* Quantity */}
                <div className="mt-6">
                    <label className="block font-medium text-gray-700 mb-1">
                        Quantity
                    </label>
                    <input
                        type="number"
                        min={1}
                        value={qty}
                        onChange={(e) => setQty(Number(e.target.value))}
                        className="w-24 border rounded-lg px-3 py-2 text-gray-800 focus:ring-2 focus:ring-blue-400 focus:outline-none"
                    />
                </div>

                {/* Buttons */}
                <div className="mt-8 flex gap-4">
                    <button
                        onClick={handleBuy}
                        className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg shadow transition"
                    >
                        Buy Ticket
                    </button>

                    <button
                        onClick={() => navigate("/")}
                        className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 rounded-lg transition"
                    >
                        Back Home
                    </button>
                </div>
            </div>
        </div>
    );
}
