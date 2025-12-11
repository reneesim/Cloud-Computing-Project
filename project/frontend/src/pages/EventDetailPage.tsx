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


    if (!event) return <div>Loading...</div>;


    const handleBuy = async () => {
        const order = await createOrder({
            customer: {
                name: "John Doe",
                email: "john@example.com"
            },
            paymentMethod: "credit_card",
            items: [
                {
                    ticketId: event.id,
                    qty: qty
                }
            ]
        });
        navigate(`/orders/${order.orderId}`);
    };


    return (
        <div className="p-4">
            <h1 className="text-2xl font-semibold">{event.name}</h1>
            <p className="mt-2 text-gray-700">Type: {event.type}</p>
            <p className="text-gray-700">Price: €{event.price}</p>


            <div className="mt-4">
                <label className="mr-2 font-semibold">Quantity:</label>
                <input
                    type="number"
                    value={qty}
                    min={1}
                    onChange={(e) => setQty(Number(e.target.value))}
                    className="border px-2 py-1"
                />
            </div>


            <button
                onClick={handleBuy}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg"
            >
                Buy
            </button>
        </div>
    );
}