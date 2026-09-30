import csv
import json
import logging
from pathlib import Path
from typing import Generator
from src.models import Customer, Order

# Set up logging format: [Time] - [Level] - [Message]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_crm_csv(file_path: Path) -> Generator[Customer, None, None]:
    """
    Reads a CRM CSV export line-by-line, sanitizes input, ignores corrupted rows,
    and yields clean Customer objects.
    """
    if not file_path.exists():
        logging.error(f"File not found at path: {file_path}")
        return

    with open(file_path, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        
        for line_num, row in enumerate(reader, start=2):  # start=2 because line 1 is header
            # 1. Sanitize raw string values
            cust_id = row.get("customer_id", "").strip()
            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            created_at = row.get("created_at", "").strip()

            # 2. Validate input boundary
            if not cust_id or not name or "@" not in email or "invalid" in created_at:
                logging.warning(f"Line {line_num}: Skipping invalid CRM row: {row}")
                continue  # Skip bad row and move to the next one

            # 3. Clean up formatting
            clean_name = name.title()
            clean_email = email.lower()

            # 4. Stream back a clean Customer instance
            yield Customer(
                customer_id=cust_id,
                name=clean_name,
                email=clean_email,
                created_at=created_at
            )


def parse_billing_json(file_path: Path) -> Generator[Order, None, None]:
    """
    Reads a Billing JSON export, validates record schema, rejects invalid orders,
    and yields clean Order objects.
    """
    if not file_path.exists():
        logging.error(f"File not found at path: {file_path}")
        return

    with open(file_path, mode="r", encoding="utf-8") as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON file {file_path}: {e}")
            return

    for idx, item in enumerate(records):
        order_id = item.get("order_id", "").strip()
        cust_id = item.get("customer_id", "").strip()
        raw_amount = item.get("amount", 0.0)
        status = item.get("status", "").strip().lower()

        try:
            amount = float(raw_amount)
        except (ValueError, TypeError):
            logging.warning(f"Record {idx}: Invalid amount '{raw_amount}'. Skipping.")
            continue

        # Reject records with invalid state or negative/zero amounts
        if amount <= 0 or status not in ["paid", "pending", "failed"]:
            logging.warning(f"Record {idx}: Rejecting invalid billing order: {item}")
            continue

        yield Order(
            order_id=order_id,
            customer_id=cust_id,
            amount=amount,
            status=status
        )
