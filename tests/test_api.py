import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_viewer_cannot_mutate_customer():
    response = client.post(
        "/customers",
        json={"customer_id": "cust_101", "name": "Jane Doe", "email": "jane@example.com"},
        headers={"x-user-role": "viewer"}
    )
    assert response.status_code == 403

def test_support_agent_cannot_create_customer():
    response = client.post(
        "/customers",
        json={"customer_id": "cust_102", "name": "Mark Smith", "email": "mark@example.com"},
        headers={"x-user-role": "support_agent"}
    )
    assert response.status_code == 403

def test_billing_admin_can_create_customer():
    response = client.post(
        "/customers",
        json={"customer_id": "cust_1000", "name": "Alice Admin", "email": "alice@example.com"},
        headers={"x-user-role": "billing_admin"}
    )
    assert response.status_code == 201
    assert response.json()["customer_id"] == "cust_1000"

def test_support_agent_can_create_ticket():
    # Ensure customer exists first
    client.post(
        "/customers",
        json={"customer_id": "cust_2000", "name": "Bob Support", "email": "bob@example.com"},
        headers={"x-user-role": "billing_admin"}
    )
    
    response = client.post(
        "/tickets",
        json={"ticket_id": "t_100", "customer_id": "cust_2000", "issue_description": "API latency"},
        headers={"x-user-role": "support_agent"}
    )
    assert response.status_code == 201
    assert response.json()["ticket_id"] == "t_100"

def test_list_customers_serialization_and_pagination(client):
    """Verify that GET /customers correctly serializes ORM models and applies pagination."""
    # 1. Seed two customers directly into the test database via the API
    admin_headers = {"X-User-Role": "billing_admin"}
    client.post(
        "/customers",
        json={"customer_id": "cust_101", "name": "Alice", "email": "alice@example.com"},
        headers=admin_headers,
    )
    client.post(
        "/customers",
        json={"customer_id": "cust_102", "name": "Bob", "email": "bob@example.com"},
        headers=admin_headers,
    )

    # 2. Query endpoint as a viewer with pagination (limit=1)
    viewer_headers = {"X-User-Role": "viewer"}
    response = client.get("/customers?skip=0&limit=1", headers=viewer_headers)

    # 3. Assert response structure and serialization
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["skip"] == 0
    assert data["limit"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["customer_id"] == "cust_101"
    assert "created_at" in data["items"][0]


def test_list_customers_unauthorized(client):
    """Verify that GET /customers returns 401 when given invalid roles."""
    # Roles not in ['billing_admin', 'support_agent', 'viewer'] should be rejected
    response = client.get("/customers", headers={"X-User-Role": "unauthorized_role"})
    assert response.status_code == 401

def test_list_customers_missing_role_header(client):
    """Verify that GET /customers returns 401 when the role header is missing entirely."""
    response = client.get("/customers")
    assert response.status_code == 401

def test_viewer_cannot_create_customer(client):
    """Verify that a valid 'viewer' role is forbidden (403) from mutating customer data."""
    headers = {"X-User-Role": "viewer"}
    payload = {"customer_id": "cust_99", "name": "Eve", "email": "eve@example.com"}
    response = client.post("/customers", json=payload, headers=headers)
    assert response.status_code == 403
