import logging
from typing import Generator, List, Set
from src.models import Customer, Order

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def deduplicate_customers(customers: Generator[Customer, None, None]
) -> Generator[Customer, None, None]:
    """
    Takes a generator of Customer objects and yields only unique customers
    based on customer_id. Drops duplicate occurrences.
    """

    seen_ids: Set[str] = set()

    for cust in customers:
        if cust.customer_id in seen_ids:
            logging.warning(
                f"Duplicate customer detected and dropped: ID={cust.customer_id} ({cust.name})"
            )
            continue

        seen_ids.add(cust.customer_id)
        yield cust


def deduplicate_orders(orders: Generator[Order, None, None]
) -> Generator[Order, None, None]:
    """
    Takes a generator of Order objects and yields only unique orders
    based on order_id. Drops duplicate occurrences.
    """

    seen_ids: Set[str] = set()

    for order in orders:
        if order.order_id in seen_ids:
            logging.warning(
                f"Duplicate order detected and dropped. ID={order.order_id}"
            )
            continue

        seen_ids.add(order.order_id)
        yield order
