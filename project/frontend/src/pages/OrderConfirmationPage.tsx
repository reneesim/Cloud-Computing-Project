import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getOrder } from "../api/orders";


export default function OrderConfirmationPage() {
    const { id } = useParams();
    const [order, setOrder] = useState<any>(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (id) getOrder(id).then(setOrder);
    }, [id]);


    if (!order) return <div>Loading...</div>;


    return (
        <div className="p-4">
            <h1 className="text-xl font-bold">Order Confirmation</h1>
            <p className="mt-2">Order ID: {order.orderId}</p>
            <p>Status: {order.status}</p>
            <p>Total: €{order.grandTotal}</p>


            <h2 className="mt-4 font-semibold">Items:</h2>
            <ul>
                {order.items.map((item: any) => (
                    <li key={item.id}>
                        {item.name} x {item.quantity} — €{item.total}
                    </li>
                ))}
            </ul>

            <button
                onClick={() => navigate("/")}
                className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg"
            >
                Back to Home
            </button>
        </div>
    );
}