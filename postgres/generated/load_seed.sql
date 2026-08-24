\set ON_ERROR_STOP on

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
