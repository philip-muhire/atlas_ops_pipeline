import csv
import json
from pathlib import Path

# Path object pointing to our data/directory
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# --- 1. Create messy CRM CSV data ---
# Notice: Row 3 is a duplicate of Row 1 (with extra spaces). Row 4 is completely corrupted.
crm_data =[
    ["customer_id", "name", "email", "created_at"],
    ["CUST-001", "Jimi Hendrix", "jimi@example.com", "2026-01-15"],
    ["CUST-002", "Frida Kahlo", "frida@example.com", "2026-02-01"],
    ["CUST-001", "Jimi Hendrix ", "jimi@example.com", "2026-01-15"],
    ["CUST-003", "", "corrupted_email", "invalid-date"]
]

csv_file_path = data_dir / "crm_export.csv"
with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(crm_data)

print(f"Created: {csv_file_path}")

# --- 2. Create messy Billing JSON data ---
# Notice: ORD-103 has a negative amount and an unknown status.
billing_data = [
    {"order_id": "ORD-101", "customer_id": "CUST-001", "amount": 199.99, "status": "paid"},
    {"order_id": "ORD-102", "customer_id": "CUST-002", "amount": 49.99, "status": "pending"},
    {"order_id": "ORD-103", "customer_id": "CUST-999", "amount": -50.00, "status": "unknown"}
]

json_file_path = data_dir / "billing_export.json"
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(billing_data, f, indent=2)

print(f"Created: {json_file_path}")
