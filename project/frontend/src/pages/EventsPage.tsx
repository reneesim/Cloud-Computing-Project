import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getEvents } from "../api/events";

export default function EventsPage() {
    const [events, setEvents] = useState<any[]>([]);

    useEffect(() => {
        getEvents().then(setEvents);
    }, []);

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8 text-gray-900">
                Available Tickets (CHANGED AGAIN)
            </h1>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {events.map((e) => (
                    <div
                        key={e.id}
                        className="p-5 border rounded-2xl shadow-sm hover:shadow-lg transition-shadow bg-white"
                    >
                        <div className="font-semibold text-xl text-gray-800">
                            {e.name}
                        </div>

                        <div className="mt-1 text-gray-600">
                            <span className="font-medium">Type:</span> {e.type}
                        </div>

                        <div className="mt-1 text-gray-600">
                            <span className="font-medium">Price:</span> €{e.price}
                        </div>

                        <Link
                            to={`/events/${e.type}`}
                            className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                        >
                            View Details
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
}
