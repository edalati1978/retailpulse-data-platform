from __future__ import annotations

import argparse
import csv
import random
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

DEFAULT_SEED = 42
DEFAULT_CUSTOMERS = 100
DEFAULT_PRODUCTS = 50
DEFAULT_ORDERS = 500

ORDER_STATUSES = (
    "pending",
    "paid",
    "shipped",
    "delivered",
    "cancelled",
)

MONEY_STEP = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_STEP, rounding=ROUND_HALF_UP)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic synthetic PostgreSQL OLTP seed data."
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--customers", type=int, default=DEFAULT_CUSTOMERS)
    parser.add_argument("--products", type=int, default=DEFAULT_PRODUCTS)
    parser.add_argument("--orders", type=int, default=DEFAULT_ORDERS)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).with_name("generated"),
    )
    return parser.parse_args()


def validate_counts(customers: int, products: int, orders: int) -> None:
    if customers < 1:
        raise ValueError("customers must be at least 1")
    if products < 1:
        raise ValueError("products must be at least 1")
    if orders < 1:
        raise ValueError("orders must be at least 1")


def generate_customers(
    writer: csv.writer,
    customer_count: int,
    base_time: datetime,
) -> None:
    for customer_id in range(1, customer_count + 1):
        created_at = base_time + timedelta(seconds=customer_id)

        writer.writerow(
            [
                customer_id,
                f"CUST-{customer_id:08d}",
                f"First{customer_id:08d}",
                f"Last{customer_id:08d}",
                f"customer{customer_id:08d}@example.com",
                created_at.isoformat(),
                created_at.isoformat(),
            ]
        )


def generate_inventory(
    writer: csv.writer,
    product_count: int,
    rng: random.Random,
    base_time: datetime,
) -> list[Decimal]:
    prices: list[Decimal] = [Decimal("0.00")] * (product_count + 1)

    for product_id in range(1, product_count + 1):
        quantity_on_hand = rng.randint(0, 500)

        raw_price = Decimal(rng.randint(499, 49999)) / Decimal(100)
        current_unit_price = money(raw_price)
        prices[product_id] = current_unit_price

        created_at = base_time + timedelta(minutes=product_id)

        writer.writerow(
            [
                f"SKU-{product_id:08d}",
                f"Product-{product_id:08d}",
                quantity_on_hand,
                current_unit_price,
                created_at.isoformat(),
                created_at.isoformat(),
            ]
        )

    return prices


def generate_orders_and_items(
    orders_writer: csv.writer,
    items_writer: csv.writer,
    order_count: int,
    customer_count: int,
    product_count: int,
    prices: list[Decimal],
    rng: random.Random,
    base_time: datetime,
) -> int:
    order_item_id = 1

    for order_id in range(1, order_count + 1):
        customer_id = rng.randint(1, customer_count)
        order_status = rng.choice(ORDER_STATUSES)
        item_count = rng.randint(1, min(5, product_count))

        product_ids = rng.sample(range(1, product_count + 1), item_count)

        created_at = base_time + timedelta(minutes=order_id)
        line_items: list[tuple[int, int, Decimal]] = []
        order_total = Decimal("0.00")

        for product_id in product_ids:
            quantity = rng.randint(1, 5)
            unit_price = prices[product_id]

            line_items.append((product_id, quantity, unit_price))
            order_total += unit_price * quantity

        order_total = money(order_total)

        orders_writer.writerow(
            [
                order_id,
                f"ORD-{order_id:010d}",
                customer_id,
                order_status,
                order_total,
                "USD",
                created_at.isoformat(),
                created_at.isoformat(),
            ]
        )

        for product_id, quantity, unit_price in line_items:
            items_writer.writerow(
                [
                    order_item_id,
                    order_id,
                    f"SKU-{product_id:08d}",
                    quantity,
                    unit_price,
                    created_at.isoformat(),
                ]
            )
            order_item_id += 1

    return order_item_id - 1


def write_load_sql(output_dir: Path) -> None:
    load_sql = """\\set ON_ERROR_STOP on

BEGIN;

TRUNCATE TABLE order_items, orders, inventory, customers RESTART IDENTITY CASCADE;

COPY customers (
    customer_id,
    customer_number,
    first_name,
    last_name,
    email,
    created_at,
    updated_at
) FROM '/seed/customers.csv' WITH (FORMAT csv, HEADER true);

COPY inventory (
    product_sku,
    product_name,
    quantity_on_hand,
    current_unit_price,
    created_at,
    updated_at
) FROM '/seed/inventory.csv' WITH (FORMAT csv, HEADER true);

COPY orders (
    order_id,
    order_number,
    customer_id,
    order_status,
    order_total,
    currency_code,
    created_at,
    updated_at
) FROM '/seed/orders.csv' WITH (FORMAT csv, HEADER true);

COPY order_items (
    order_item_id,
    order_id,
    product_sku,
    quantity,
    unit_price,
    created_at
) FROM '/seed/order_items.csv' WITH (FORMAT csv, HEADER true);

SELECT setval(
    pg_get_serial_sequence('customers', 'customer_id'),
    COALESCE((SELECT MAX(customer_id) FROM customers), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('orders', 'order_id'),
    COALESCE((SELECT MAX(order_id) FROM orders), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('order_items', 'order_item_id'),
    COALESCE((SELECT MAX(order_item_id) FROM order_items), 1),
    true
);

COMMIT;
"""
    (output_dir / "load_seed.sql").write_text(load_sql, encoding="utf-8")


def main() -> None:
    args = parse_args()
    validate_counts(args.customers, args.products, args.orders)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    base_time = datetime(2026, 8, 1, 0, 0, tzinfo=UTC)

    customers_path = output_dir / "customers.csv"
    inventory_path = output_dir / "inventory.csv"
    orders_path = output_dir / "orders.csv"
    order_items_path = output_dir / "order_items.csv"

    with (
        customers_path.open("w", newline="", encoding="utf-8") as customers_file,
        inventory_path.open("w", newline="", encoding="utf-8") as inventory_file,
        orders_path.open("w", newline="", encoding="utf-8") as orders_file,
        order_items_path.open("w", newline="", encoding="utf-8") as order_items_file,
    ):
        customers_writer = csv.writer(customers_file)
        inventory_writer = csv.writer(inventory_file)
        orders_writer = csv.writer(orders_file)
        items_writer = csv.writer(order_items_file)

        customers_writer.writerow(
            [
                "customer_id",
                "customer_number",
                "first_name",
                "last_name",
                "email",
                "created_at",
                "updated_at",
            ]
        )

        inventory_writer.writerow(
            [
                "product_sku",
                "product_name",
                "quantity_on_hand",
                "current_unit_price",
                "created_at",
                "updated_at",
            ]
        )

        orders_writer.writerow(
            [
                "order_id",
                "order_number",
                "customer_id",
                "order_status",
                "order_total",
                "currency_code",
                "created_at",
                "updated_at",
            ]
        )

        items_writer.writerow(
            [
                "order_item_id",
                "order_id",
                "product_sku",
                "quantity",
                "unit_price",
                "created_at",
            ]
        )

        generate_customers(
            customers_writer,
            args.customers,
            base_time,
        )

        prices = generate_inventory(
            inventory_writer,
            args.products,
            rng,
            base_time,
        )

        item_count = generate_orders_and_items(
            orders_writer,
            items_writer,
            args.orders,
            args.customers,
            args.products,
            prices,
            rng,
            base_time,
        )

    write_load_sql(output_dir)

    print(
        "Generated deterministic OLTP seed data:\n"
        f"  customers:   {args.customers}\n"
        f"  products:    {args.products}\n"
        f"  orders:      {args.orders}\n"
        f"  order_items: {item_count}\n"
        f"  seed:        {args.seed}\n"
        f"  output:      {output_dir}"
    )


if __name__ == "__main__":
    main()

