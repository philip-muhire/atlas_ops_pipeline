import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.services import OperationsService
from src.schemas import CustomerCreate, TicketCreate, OrderCreate

def test_operations_service_customer_lifecycle(isolate_test_db_session: Session):
    service = OperationsService(isolate_test_db_session)

    # Create Customer
    cust_dto = CustomerCreate(
        customer_id="CUST_100",
        name="Alice Smith",
        email="alice@example.com",
        created_at="2026-01-01"
    )
    cust = service.create_customer(cust_dto)
    assert cust.customer_id == "CUST_100"

    # Listing Customers
    customers, total = service.list_customers(skip=0, limit=10)
    assert total == 1
    assert customers[0].customer_id == "CUST_100"

    # Duplicate Customer Creation Error (400)
    with pytest.raises(HTTPException) as exc_info:
        service.create_customer(cust_dto)
    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


def test_operations_service_ticket_lifecycle(isolate_test_db_session: Session):
    service = OperationsService(isolate_test_db_session)

    # Ticket creation fails if customer doesn't exist (404)
    ticket_dto = TicketCreate(
        ticket_id="TICK_001",
        customer_id="NON_EXISTENT",
        issue_description="Login Error",
        status="open"
    )
    with pytest.raises(HTTPException) as exc_info:
        service.create_ticket(ticket_dto)
    assert exc_info.value.status_code == 404

    # Create valid customer then attach ticket
    cust_dto = CustomerCreate(
        customer_id="CUST_200",
        name="Bob Jones",
        email="bob@example.com",
        created_at="2026-01-01"
    )
    service.create_customer(cust_dto)

    ticket_dto.customer_id = "CUST_200"
    ticket = service.create_ticket(ticket_dto)
    assert ticket.ticket_id == "TICK_001"

    tickets, total = service.list_tickets(skip=0, limit=10)
    assert total == 1
    assert tickets[0].ticket_id == "TICK_001"


def test_operations_service_order_lifecycle(isolate_test_db_session: Session):
    service = OperationsService(isolate_test_db_session)

    # Order creation fails if customer doesn't exist (404)
    order_dto = OrderCreate(
        order_id="ORD_001",
        customer_id="NON_EXISTENT",
        amount=150.00,
        status="paid"
    )
    with pytest.raises(HTTPException) as exc_info:
        service.create_order(order_dto)
    assert exc_info.value.status_code == 404

    # Create valid customer then attach order
    cust_dto = CustomerCreate(
        customer_id="CUST_300",
        name="Charlie Brown",
        email="charlie@example.com",
        created_at="2026-01-01"
    )
    service.create_customer(cust_dto)

    order_dto.customer_id = "CUST_300"
    order = service.create_order(order_dto)
    assert order.order_id == "ORD_001"

    orders, total = service.list_orders(skip=0, limit=10)
    assert total == 1
    assert orders[0].order_id == "ORD_001"
