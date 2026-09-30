import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.database import get_db

client = TestClient(app)

def test_read_root_and_health():
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["status"] == "active"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"


def test_auth_missing_role_header():
    # Missing x-user-role header returns 401
    response = client.get("/customers")
    assert response.status_code == 401
    assert "Missing required authentication header 'X-User-Role'." in response.json()["detail"]


def test_auth_invalid_role():
    # Role not in VALID_ROLES returns 401
    response = client.post(
        "/customers",
        headers={"x-user-role": "unconfigured_role"},
        json={"customer_id": "C999", "name": "Jane", "email": "j@ex.com", "created_at": "2026-01-01"}
    )
    assert response.status_code == 401
    assert "Invalid or unconfigured role" in response.json()["detail"]


def test_auth_forbidden_role():
    # Valid role but lacks permissions for POST returns 403
    response = client.post(
        "/customers",
        headers={"x-user-role": "viewer"},
        json={"customer_id": "C999", "name": "Jane", "email": "j@ex.com", "created_at": "2026-01-01"}
    )
    assert response.status_code == 403
    assert "lacks required permissions" in response.json()["detail"]


def test_customer_api_endpoints(isolate_test_db_session):
    headers = {"x-user-role": "billing_admin"}

    # Create Customer
    payload = {
        "customer_id": "CUST_API_1",
        "name": "API User",
        "email": "api@example.com",
        "created_at": "2026-01-01"
    }
    create_res = client.post("/customers", json=payload, headers=headers)
    assert create_res.status_code == 201
    assert create_res.json()["customer_id"] == "CUST_API_1"

    # List Customers
    list_res = client.get("/customers", headers=headers)
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1


def test_ticket_api_endpoints(isolate_test_db_session):
    headers = {"x-user-role": "billing_admin"}

    # First seed customer
    client.post(
        "/customers",
        json={"customer_id": "CUST_API_2", "name": "API User 2", "email": "api2@example.com", "created_at": "2026-01-01"},
        headers=headers
    )

    # Create Ticket
    ticket_payload = {
        "ticket_id": "TICK_API_1",
        "customer_id": "CUST_API_2",
        "issue_description": "API Test Issue",
        "status": "open"
    }
    create_res = client.post("/tickets", json=ticket_payload, headers=headers)
    assert create_res.status_code == 201

    # List Tickets
    list_res = client.get("/tickets", headers=headers)
    assert list_res.status_code == 200


def test_order_api_endpoints(isolate_test_db_session):
    headers = {"x-user-role": "billing_admin"}

    # First seed customer
    client.post(
        "/customers",
        json={"customer_id": "CUST_API_3", "name": "API User 3", "email": "api3@example.com", "created_at": "2026-01-01"},
        headers=headers
    )

    # Create Order
    order_payload = {
        "order_id": "ORD_API_1",
        "customer_id": "CUST_API_3",
        "amount": 250.50,
        "status": "paid"
    }
    create_res = client.post("/orders", json=order_payload, headers=headers)
    assert create_res.status_code == 201

    # List Orders
    list_res = client.get("/orders", headers=headers)
    assert list_res.status_code == 200


def test_database_get_db_generator():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    try:
        next(db_gen)
    except StopIteration:
        pass
