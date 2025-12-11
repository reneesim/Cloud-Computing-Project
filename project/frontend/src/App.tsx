import { BrowserRouter, Routes, Route } from "react-router-dom";
import EventsPage from "./pages/EventsPage";
import EventDetailPage from "./pages/EventDetailPage";
import OrderConfirmationPage from "./pages/OrderConfirmationPage";
import "./App.css"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EventsPage />} />
        <Route path="/events/:id" element={<EventDetailPage />} />
        <Route path="/orders/:id" element={<OrderConfirmationPage />} />
      </Routes>
    </BrowserRouter>
  );
}