from dataclasses import dataclass
from typing import Optional

@dataclass
class Customer:
    """Represents a clean Atlas Ops customer record."""
    customer_id: str
    name: str
    email: str
    created_at: str

@dataclass
class Order:
    """Represents a clean Atlas Ops billing order record."""
    order_id: str
    customer_id: str
    amount: float
    status: str
