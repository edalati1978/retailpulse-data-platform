-- RetailPulse PostgreSQL OLTP sample queries

-- 1. Row counts for the main OLTP tables
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;


-- 2. Sample customer/order join
SELECT
    o.order_number,
    c.customer_number,
    c.first_name,
    c.last_name,
    o.order_status,
    o.order_total,
    o.currency_code
FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id
ORDER BY o.order_id
LIMIT 10;


-- 3. Verify order totals against line-item totals
SELECT
    o.order_number,
    o.order_total,
    SUM(oi.quantity * oi.unit_price) AS calculated_total
FROM orders o
JOIN order_items oi
    ON oi.order_id = o.order_id
GROUP BY
    o.order_id,
    o.order_number,
    o.order_total
ORDER BY o.order_id
LIMIT 10;


-- 4. Products with the lowest current inventory
SELECT
    product_sku,
    product_name,
    quantity_on_hand,
    current_unit_price
FROM inventory
ORDER BY quantity_on_hand ASC
LIMIT 10;