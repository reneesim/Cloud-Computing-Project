# backend/shared/models.py
from pydantic import BaseModel, EmailStr
from typing import List

class OrderItem(BaseModel):
    ticketId: str
    qty: int
    type: str | None = None
    unitPrice: float | None = None
    total: float | None = None

class Customer(BaseModel):
    name: str
    email: EmailStr

class Order(BaseModel):
    orderId: str
    customer: Customer
    items: List[OrderItem]
    grandTotal: float
    currency: str
    status: str
    createdAt: str
    message: str | None = None
    failureReason: str | None = None
