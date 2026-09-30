from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey
from src.database import Base

class CustomerModel(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())

class TicketModel(Base):
    __tablename__ = "support_tickets"

    ticket_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    issue_description = Column(String, nullable=False)
    status = Column(String, default="open")
    created_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())

class OrderModel(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
