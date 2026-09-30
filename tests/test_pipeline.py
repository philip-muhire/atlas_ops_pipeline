import pytest
from src.models import Customer, Order
from src.pipeline import deduplicate_customers, deduplicate_orders


def test_deduplicate_customers():
    """
    Verify that deduplicate_customers drops duplicate IDs and preserves unique ones.
    """
    raw_customers = [
        Customer("CUST-001", "Jimi Hendrix", "jimi@example.com", "2026-01-01"),
        Customer("CUST-002", "Frida Kahlo", "frida@example.com", "2026-01-02"),
        Customer("CUST-001", "Jimi Hendrix", "jimi@example.com", "2026-01-01"),  # Duplicate
    ]

    # Convert generator output to a list
    result = list(deduplicate_customers(c for c in raw_customers))

    # Assertions
    assert len(result) == 2
    assert result[0].customer_id == "CUST-001"
    assert result[1].customer_id == "CUST-002"


def test_deduplicate_orders():
    """
    Verify that deduplicate_orders drops duplicate order IDs.
    """
    raw_orders = [
        Order("ORD-101", "CUST-001", 150.00, "paid"),
        Order("ORD-101", "CUST-001", 150.00, "paid"),  # Duplicate
        Order("ORD-102", "CUST-002", 89.99, "pending"),
    ]

    result = list(deduplicate_orders(o for o in raw_orders))

    assert len(result) == 2
    assert result[0].order_id == "ORD-101"
    assert result[1].order_id == "ORD-102"
