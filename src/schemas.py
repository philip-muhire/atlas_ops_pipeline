from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Generic, TypeVar

# Declare a generic type variable
T = TypeVar("T")

# Generic Paginated Envelope Schema
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)

# Customer Schemas
class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    email: EmailStr

class CustomerResponse(CustomerCreate):
    created_at: str
    model_config = ConfigDict(from_attributes=True)

# Support Ticket Schemas
class TicketCreate(BaseModel):
    ticket_id: str
    customer_id: str
    issue_description: str

class TicketResponse(TicketCreate):
    status: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)

# Order Schemas
class OrderCreate(BaseModel):
    order_id: str
    customer_id: str
    amount: float

class OrderResponse(OrderCreate):
    status: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)
