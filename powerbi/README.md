# Power BI Dashboard Setup Guide

This directory contains the Power BI setup guide and workbook file (`ecommerce_dashboard.pbix`) for visualizing the Olist E-Commerce sales dataset.

---

## Prerequisites
1. **Power BI Desktop** (Windows).
2. **PostgreSQL Connector / Npgsql Provider**: Power BI uses the native PostgreSQL driver or may prompt you to install Npgsql.
3. Ensure your PostgreSQL instance is running and the database `ecommerce_olist` has been populated using `python/load_postgres.py` and `sql/05_views.sql`.

---

## Connection Steps
1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **More...** $\rightarrow$ select **PostgreSQL database**.
3. Enter Connection Settings:
   - **Server**: `localhost` (or server IP)
   - **Database**: `ecommerce_olist`
   - **Data Connectivity Mode**: **Import** (Recommended for fast report interactivity)
4. Authenticate using database credentials:
   - **User name**: `postgres` (or your configured user)
   - **Password**: your database password
5. In the **Navigator** pane, select the analytical reporting views (created by `sql/05_views.sql`):
   - `vw_monthly_sales`
   - `vw_category_sales`
   - `vw_state_sales`
   - `vw_payment_analysis`
   - `vw_delivery_performance`
   - `vw_customer_lifetime_value`
   - `vw_seller_performance`
   - `vw_product_performance`
6. Click **Load**.

---

## Pre-Built Analytical Dashboard Tabs

### 1. Executive Sales Overview
- **KPI Cards**: Total Revenue, Total Orders, Average Order Value (AOV).
- **Line Chart**: Monthly Revenue & Order Volume Trends (`month` vs. `total_revenue` / `total_orders` from `vw_monthly_sales`).
- **Donut Chart**: Payment Method Distribution (`revenue` by `payment_type` from `vw_payment_analysis`).

### 2. Geographic & Demographics Analysis
- **Filled Map / Shape Map**: Sales distribution across Brazilian states (`total_spending` & `total_unique_customers` by `customer_state` from `vw_state_sales`).
- **Bar Chart**: Top Customer Cities by Lifetime Value from `vw_customer_lifetime_value`.

### 3. Product & Category Performance
- **Bar Chart**: Revenue by Product Category in English (`total_sales_revenue` by `category_english` from `vw_category_sales`).
- **Table / Matrix**: Top performing products by total sales count (`orders_count` and `revenue` from `vw_product_performance`).

### 4. Operations & Logistics Performance
- **Bar/Column Chart**: On-Time vs. Late vs. Undelivered Breakdown (`delivery_status` count from `vw_delivery_performance`).
- **Scatter Plot**: Seller Performance (`orders_handled` vs. `total_sales` from `vw_seller_performance`).
