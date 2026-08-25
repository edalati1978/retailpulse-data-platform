-- RetailPulse PostgreSQL OLTP update scenarios

-- 1. Customer change
UPDATE customers
SET
    email = 'updated.customer22@example.com',
    updated_at = CURRENT_TIMESTAMP
WHERE customer_number = 'CUST-00000022';


-- 2. Order status change
UPDATE orders
SET
    order_status = 'delivered',
    updated_at = CURRENT_TIMESTAMP
WHERE order_number = 'ORD-0000000003';


-- 3. Inventory change
UPDATE inventory
SET
    quantity_on_hand = quantity_on_hand - 1,
    updated_at = CURRENT_TIMESTAMP
WHERE product_sku = 'SKU-00000013'
  AND quantity_on_hand > 0;