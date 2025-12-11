import axios from "axios";
import { API_BASE } from "./apiConfig";

export const createOrder = async (payload: any) => {
const res = await axios.post(`${API_BASE}/orders`, payload);
return res.data;
};


export const getOrder = async (id: string) => {
const res = await axios.get(`${API_BASE}/orders/${id}`);
return res.data;
};