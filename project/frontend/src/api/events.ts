import axios from "axios";
import { API_BASE } from "./apiConfig";


export const getEvents = async () => {
const res = await axios.get(`${API_BASE}/tickets`);
return res.data.tickets;
};


export const getEvent = async (id: string) => {
const res = await axios.get(`${API_BASE}/tickets?type=${id}`);
return res.data.tickets[0];
};