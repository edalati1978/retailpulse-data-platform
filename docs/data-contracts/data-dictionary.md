# RetailPulse Data Dictionary

## TPC-DS

### customer

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per customer record identified by `c_customer_sk`.

**Primary key:** `c_customer_sk`

**Business key:** Not explicitly defined as unique in the official TPC-DS DDL. `c_customer_id` is required (`NOT NULL`) but is not declared as a primary or unique key in the schema.

| Column | Type | Nullable | Description |
|---|---|---|---|
| c_customer_sk | integer | No | Customer surrogate key; primary key. |
| c_customer_id | char(16) | No | Customer identifier provided by TPC-DS. |
| c_current_cdemo_sk | integer | Yes | Reference to current customer demographics. |
| c_current_hdemo_sk | integer | Yes | Reference to current household demographics. |
| c_current_addr_sk | integer | Yes | Reference to current customer address. |
| c_first_shipto_date_sk | integer | Yes | First ship-to date key. |
| c_first_sales_date_sk | integer | Yes | First sales date key. |
| c_salutation | char(10) | Yes | Customer salutation. |
| c_first_name | char(20) | Yes | Customer first name. |
| c_last_name | char(30) | Yes | Customer last name. |
| c_preferred_cust_flag | char(1) | Yes | Preferred-customer flag. |
| c_birth_day | integer | Yes | Birth day. |
| c_birth_month | integer | Yes | Birth month. |
| c_birth_year | integer | Yes | Birth year. |
| c_birth_country | varchar(20) | Yes | Birth country. |
| c_login | char(13) | Yes | Customer login value. |
| c_email_address | char(50) | Yes | Customer email address. |
| c_last_review_date | char(10) | Yes | Last review date value as defined by TPC-DS. |

### inventory

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per item, warehouse, and date combination.

**Primary key:** Composite key: `inv_date_sk`, `inv_item_sk`, `inv_warehouse_sk`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable | Description |
|---|---|---|---|
| inv_date_sk | integer | No | Date key for the inventory record; part of the primary key. |
| inv_item_sk | integer | No | Item key; part of the primary key. |
| inv_warehouse_sk | integer | No | Warehouse key; part of the primary key. |
| inv_quantity_on_hand | integer | Yes | Quantity on hand for the item in the warehouse on the specified date. |

### catalog_returns

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per returned item within a catalog order.

**Primary key:** Composite key: `cr_item_sk`, `cr_order_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| cr_returned_date_sk | integer | Yes |
| cr_returned_time_sk | integer | Yes |
| cr_item_sk | integer | No |
| cr_refunded_customer_sk | integer | Yes |
| cr_refunded_cdemo_sk | integer | Yes |
| cr_refunded_hdemo_sk | integer | Yes |
| cr_refunded_addr_sk | integer | Yes |
| cr_returning_customer_sk | integer | Yes |
| cr_returning_cdemo_sk | integer | Yes |
| cr_returning_hdemo_sk | integer | Yes |
| cr_returning_addr_sk | integer | Yes |
| cr_call_center_sk | integer | Yes |
| cr_catalog_page_sk | integer | Yes |
| cr_ship_mode_sk | integer | Yes |
| cr_warehouse_sk | integer | Yes |
| cr_reason_sk | integer | Yes |
| cr_order_number | integer | No |
| cr_return_quantity | integer | Yes |
| cr_return_amount | decimal(7,2) | Yes |
| cr_return_tax | decimal(7,2) | Yes |
| cr_return_amt_inc_tax | decimal(7,2) | Yes |
| cr_fee | decimal(7,2) | Yes |
| cr_return_ship_cost | decimal(7,2) | Yes |
| cr_refunded_cash | decimal(7,2) | Yes |
| cr_reversed_charge | decimal(7,2) | Yes |
| cr_store_credit | decimal(7,2) | Yes |
| cr_net_loss | decimal(7,2) | Yes |

### web_returns

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per returned item within a web order.

**Primary key:** Composite key: `wr_item_sk`, `wr_order_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| wr_returned_date_sk | integer | Yes |
| wr_returned_time_sk | integer | Yes |
| wr_item_sk | integer | No |
| wr_refunded_customer_sk | integer | Yes |
| wr_refunded_cdemo_sk | integer | Yes |
| wr_refunded_hdemo_sk | integer | Yes |
| wr_refunded_addr_sk | integer | Yes |
| wr_returning_customer_sk | integer | Yes |
| wr_returning_cdemo_sk | integer | Yes |
| wr_returning_hdemo_sk | integer | Yes |
| wr_returning_addr_sk | integer | Yes |
| wr_web_page_sk | integer | Yes |
| wr_reason_sk | integer | Yes |
| wr_order_number | integer | No |
| wr_return_quantity | integer | Yes |
| wr_return_amt | decimal(7,2) | Yes |
| wr_return_tax | decimal(7,2) | Yes |
| wr_return_amt_inc_tax | decimal(7,2) | Yes |
| wr_fee | decimal(7,2) | Yes |
| wr_return_ship_cost | decimal(7,2) | Yes |
| wr_refunded_cash | decimal(7,2) | Yes |
| wr_reversed_charge | decimal(7,2) | Yes |
| wr_account_credit | decimal(7,2) | Yes |
| wr_net_loss | decimal(7,2) | Yes |

### web_sales

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per sold item within a web order.

**Primary key:** Composite key: `ws_item_sk`, `ws_order_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| ws_sold_date_sk | integer | Yes |
| ws_sold_time_sk | integer | Yes |
| ws_ship_date_sk | integer | Yes |
| ws_item_sk | integer | No |
| ws_bill_customer_sk | integer | Yes |
| ws_bill_cdemo_sk | integer | Yes |
| ws_bill_hdemo_sk | integer | Yes |
| ws_bill_addr_sk | integer | Yes |
| ws_ship_customer_sk | integer | Yes |
| ws_ship_cdemo_sk | integer | Yes |
| ws_ship_hdemo_sk | integer | Yes |
| ws_ship_addr_sk | integer | Yes |
| ws_web_page_sk | integer | Yes |
| ws_web_site_sk | integer | Yes |
| ws_ship_mode_sk | integer | Yes |
| ws_warehouse_sk | integer | Yes |
| ws_promo_sk | integer | Yes |
| ws_order_number | integer | No |
| ws_quantity | integer | Yes |
| ws_wholesale_cost | decimal(7,2) | Yes |
| ws_list_price | decimal(7,2) | Yes |
| ws_sales_price | decimal(7,2) | Yes |
| ws_ext_discount_amt | decimal(7,2) | Yes |
| ws_ext_sales_price | decimal(7,2) | Yes |
| ws_ext_wholesale_cost | decimal(7,2) | Yes |
| ws_ext_list_price | decimal(7,2) | Yes |
| ws_ext_tax | decimal(7,2) | Yes |
| ws_coupon_amt | decimal(7,2) | Yes |
| ws_ext_ship_cost | decimal(7,2) | Yes |
| ws_net_paid | decimal(7,2) | Yes |
| ws_net_paid_inc_tax | decimal(7,2) | Yes |
| ws_net_paid_inc_ship | decimal(7,2) | Yes |
| ws_net_paid_inc_ship_tax | decimal(7,2) | Yes |
| ws_net_profit | decimal(7,2) | Yes |

### catalog_sales

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per sold item within a catalog order.

**Primary key:** Composite key: `cs_item_sk`, `cs_order_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| cs_sold_date_sk | integer | Yes |
| cs_sold_time_sk | integer | Yes |
| cs_ship_date_sk | integer | Yes |
| cs_bill_customer_sk | integer | Yes |
| cs_bill_cdemo_sk | integer | Yes |
| cs_bill_hdemo_sk | integer | Yes |
| cs_bill_addr_sk | integer | Yes |
| cs_ship_customer_sk | integer | Yes |
| cs_ship_cdemo_sk | integer | Yes |
| cs_ship_hdemo_sk | integer | Yes |
| cs_ship_addr_sk | integer | Yes |
| cs_call_center_sk | integer | Yes |
| cs_catalog_page_sk | integer | Yes |
| cs_ship_mode_sk | integer | Yes |
| cs_warehouse_sk | integer | Yes |
| cs_item_sk | integer | No |
| cs_promo_sk | integer | Yes |
| cs_order_number | integer | No |
| cs_quantity | integer | Yes |
| cs_wholesale_cost | decimal(7,2) | Yes |
| cs_list_price | decimal(7,2) | Yes |
| cs_sales_price | decimal(7,2) | Yes |
| cs_ext_discount_amt | decimal(7,2) | Yes |
| cs_ext_sales_price | decimal(7,2) | Yes |
| cs_ext_wholesale_cost | decimal(7,2) | Yes |
| cs_ext_list_price | decimal(7,2) | Yes |
| cs_ext_tax | decimal(7,2) | Yes |
| cs_coupon_amt | decimal(7,2) | Yes |
| cs_ext_ship_cost | decimal(7,2) | Yes |
| cs_net_paid | decimal(7,2) | Yes |
| cs_net_paid_inc_tax | decimal(7,2) | Yes |
| cs_net_paid_inc_ship | decimal(7,2) | Yes |
| cs_net_paid_inc_ship_tax | decimal(7,2) | Yes |
| cs_net_profit | decimal(7,2) | Yes |

### store_sales

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per sold item within a store transaction identified by a ticket number.

**Primary key:** Composite key: `ss_item_sk`, `ss_ticket_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| ss_sold_date_sk | integer | Yes |
| ss_sold_time_sk | integer | Yes |
| ss_item_sk | integer | No |
| ss_customer_sk | integer | Yes |
| ss_cdemo_sk | integer | Yes |
| ss_hdemo_sk | integer | Yes |
| ss_addr_sk | integer | Yes |
| ss_store_sk | integer | Yes |
| ss_promo_sk | integer | Yes |
| ss_ticket_number | integer | No |
| ss_quantity | integer | Yes |
| ss_wholesale_cost | decimal(7,2) | Yes |
| ss_list_price | decimal(7,2) | Yes |
| ss_sales_price | decimal(7,2) | Yes |
| ss_ext_discount_amt | decimal(7,2) | Yes |
| ss_ext_sales_price | decimal(7,2) | Yes |
| ss_ext_wholesale_cost | decimal(7,2) | Yes |
| ss_ext_list_price | decimal(7,2) | Yes |
| ss_ext_tax | decimal(7,2) | Yes |
| ss_coupon_amt | decimal(7,2) | Yes |
| ss_net_paid | decimal(7,2) | Yes |
| ss_net_paid_inc_tax | decimal(7,2) | Yes |
| ss_net_profit | decimal(7,2) | Yes |

### store_returns

**Source:** TPC-DS Tools v4.0.0 official schema (`tpcds.sql`)

**Grain:** One row per returned item within a store transaction identified by a ticket number.

**Primary key:** Composite key: `sr_item_sk`, `sr_ticket_number`

**Business key:** Not separately defined in the official TPC-DS DDL.

| Column | Type | Nullable |
|---|---|---|
| sr_returned_date_sk | integer | Yes |
| sr_return_time_sk | integer | Yes |
| sr_item_sk | integer | No |
| sr_customer_sk | integer | Yes |
| sr_cdemo_sk | integer | Yes |
| sr_hdemo_sk | integer | Yes |
| sr_addr_sk | integer | Yes |
| sr_store_sk | integer | Yes |
| sr_reason_sk | integer | Yes |
| sr_ticket_number | integer | No |
| sr_return_quantity | integer | Yes |
| sr_return_amt | decimal(7,2) | Yes |
| sr_return_tax | decimal(7,2) | Yes |
| sr_return_amt_inc_tax | decimal(7,2) | Yes |
| sr_fee | decimal(7,2) | Yes |
| sr_return_ship_cost | decimal(7,2) | Yes |
| sr_refunded_cash | decimal(7,2) | Yes |
| sr_reversed_charge | decimal(7,2) | Yes |
| sr_store_credit | decimal(7,2) | Yes |
| sr_net_loss | decimal(7,2) | Yes |
