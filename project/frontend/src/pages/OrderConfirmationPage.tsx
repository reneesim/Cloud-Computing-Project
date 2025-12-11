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

    if (!order) {
        return (
            <div className="flex items-center justify-center h-screen text-gray-500">
                Loading...
            </div>
        );
    }

    return (
        <div className="flex justify-center p-6">
            <div className="w-full max-w-lg bg-white rounded-xl shadow-md p-6">
                {/* Header */}
                <h1 className="text-3xl font-bold text-gray-900">
                    Order Confirmed
                </h1>
                <p className="text-gray-600 mt-1">
                    Thank you for your purchase!
                </p>

                {/* Order Summary */}
                <div className="mt-6">
                    <div className="bg-gray-100 rounded-lg p-4">
                        <p className="text-sm text-gray-700">
                            <span className="font-semibold">Order ID:</span>{" "}
                            {order.orderId}
                        </p>
                        <p className="text-sm text-gray-700">
                            <span className="font-semibold">Status:</span>{" "}
                            {order.status}
                        </p>
                        <p className="text-lg font-semibold text-blue-600 mt-2">
                            Total: €{order.grandTotal}
                        </p>
                    </div>
                </div>

                {/* Items */}
                <h2 className="mt-6 text-xl font-semibold">Items</h2>
                <ul className="mt-3 space-y-2">
                    {order.items.map((item: any) => (
                        <li
                            key={item.id}
                            className="flex justify-between bg-gray-50 p-3 rounded-lg border"
                        >
                            <span className="font-medium">
                                {item.name} × {item.quantity}
                            </span>
                            <span className="font-semibold">€{item.total}</span>
                        </li>
                    ))}
                </ul>

                {/* Button */}
                <button
                    onClick={() => navigate("/")}
                    className="w-full mt-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow transition"
                >
                    Back to Home
                </button>
            </div>
        </div>
    );
}
