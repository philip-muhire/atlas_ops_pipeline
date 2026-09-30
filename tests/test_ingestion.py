import json
from pathlib import Path
import pytest
from src.ingestion import parse_crm_csv, parse_billing_json

def test_parse_crm_csv_success(tmp_path: Path):
    csv_file = tmp_path / "crm_valid.csv"
    csv_file.write_text(
        "customer_id,name,email,created_at\n"
        "CUST_001, john doe , JOHN@EXAMPLE.COM ,2026-01-01\n"
        "CUST_002,jane smith,jane@example.com,2026-01-02\n"
    )
    customers = list(parse_crm_csv(csv_file))
    assert len(customers) == 2
    assert customers[0].customer_id == "CUST_001"
    assert customers[0].name == "John Doe"
    assert customers[0].email == "john@example.com"
    assert customers[1].name == "Jane Smith"

def test_parse_crm_csv_invalid_rows_and_missing_file(tmp_path: Path):
    # Missing file path
    missing_file = tmp_path / "non_existent.csv"
    assert list(parse_crm_csv(missing_file)) == []

    # Corrupted / invalid rows
    corrupt_file = tmp_path / "crm_corrupt.csv"
    corrupt_file.write_text(
        "customer_id,name,email,created_at\n"
        ",No ID,noid@example.com,2026-01-01\n"          # Missing cust_id
        "CUST_002,,noname@example.com,2026-01-01\n"       # Missing name
        "CUST_003,Bad Email,bademail.com,2026-01-01\n"    # Missing @ in email
        "CUST_004,Invalid Date,ok@ex.com,invalid_date\n"  # "invalid" in created_at
    )
    customers = list(parse_crm_csv(corrupt_file))
    assert len(customers) == 0

def test_parse_billing_json_success(tmp_path: Path):
    json_file = tmp_path / "billing_valid.json"
    data = [
        {"order_id": "ORD_001", "customer_id": "CUST_001", "amount": "150.50", "status": "PAID"},
        {"order_id": "ORD_002", "customer_id": "CUST_002", "amount": 99.0, "status": "pending"}
    ]
    json_file.write_text(json.dumps(data))

    orders = list(parse_billing_json(json_file))
    assert len(orders) == 2
    assert orders[0].order_id == "ORD_001"
    assert orders[0].amount == 150.50
    assert orders[0].status == "paid"
    assert orders[1].status == "pending"

def test_parse_billing_json_invalid_and_missing_file(tmp_path: Path):
    # Missing file path
    missing_file = tmp_path / "missing.json"
    assert list(parse_billing_json(missing_file)) == []

    # Syntax error in JSON
    bad_json_file = tmp_path / "malformed.json"
    bad_json_file.write_text("{ unclosed_json: ")
    assert list(parse_billing_json(bad_json_file)) == []

    # Validation filters (bad amount types, non-positive amounts, illegal statuses)
    records_file = tmp_path / "billing_invalid.json"
    invalid_data = [
        {"order_id": "O1", "customer_id": "C1", "amount": "not_a_number", "status": "paid"},
        {"order_id": "O2", "customer_id": "C2", "amount": -10.0, "status": "paid"},
        {"order_id": "O3", "customer_id": "C3", "amount": 0, "status": "paid"},
        {"order_id": "O4", "customer_id": "C4", "amount": 50.0, "status": "invalid_status"}
    ]
    records_file.write_text(json.dumps(invalid_data))
    orders = list(parse_billing_json(records_file))
    assert len(orders) == 0
