import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getEvents } from "../api/events";


export default function EventsPage() {
    const [events, setEvents] = useState<any[]>([]);


    useEffect(() => {
        getEvents().then(setEvents);
    }, []);


    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Available Tickets</h1>
            <ul className="space-y-2">
                {events.map((e) => (
                    <li key={e.id} className="p-3 border rounded-lg shadow">
                        <div className="font-semibold">{e.name}</div>
                        <div>Type: {e.type}</div>
                        <div>Price: €{e.price}</div>
                        <Link
                            to={`/events/${e.type}`}
                            className="text-blue-600 underline mt-2 inline-block"
                        >
                            View Details
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}