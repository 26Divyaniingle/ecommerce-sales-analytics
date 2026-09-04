# E-Commerce Sales Analytics & ETL Pipeline

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow?logo=powerbi)
![Data Source](https://img.shields.io/badge/Data_Source-Olist_Kaggle-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end data engineering and business intelligence project built on the **Brazilian E-Commerce Public Dataset by Olist** (~100k orders from 2016 to 2018).

This repository provides an automated data pipeline that ingests raw transactional CSVs, cleans and standardizes them using Python (`pandas`), loads them into a PostgreSQL relational database with foreign key constraints, builds optimized database views and indexes, and connects to a Power BI dashboard for executive reporting.

---

## 🏗️ Architecture & Data Flow

```text
[ Raw Kaggle Datasets (9 CSVs) ]
               │
               ▼
[ Python Cleaning Pipeline (pandas) ]
  • Date parsing & type casting
  • Text standardization & deduplication
  • Null value resolution & schema alignment
               │
               ▼
[ Cleaned Data Output (data/processed/) ]
               │
               ▼
[ PostgreSQL Relational Database (SQLAlchemy) ]
  • Relational Schema (PKs & FKs)
  • B-Tree Indexes on Join Keys
  • 8 Analytical Views
               │
               ▼
[ Power BI Executive Dashboard ]
  • Sales & Revenue Trends
  • Regional & Category Performance
  • Logistics & Seller Metrics
```

---

## 📂 Project Structure

```text
ecommerce-sales-analytics/
├── data/
│   ├── raw/                  # Raw Olist CSV files (Download from Kaggle)
│   └── processed/            # Cleaned CSV files produced by python/clean_data.py
│
├── sql/
│   ├── 01_create_database.sql     # Database initialization script
│   ├── 02_create_tables.sql       # Relational table schemas with PK & FK constraints
│   ├── 03_load_data.sql           # SQL COPY command template (Alternative loader)
│   ├── 04_indexes.sql             # B-tree performance index definitions
│   ├── 05_views.sql               # Pre-built analytical views for Power BI & SQL reporting
│   └── 06_analysis_queries.sql    # Business intelligence & analytical queries
│
├── python/
│   ├── inspect_data.py       # Inspect shape, missing values & data types
│   ├── clean_data.py         # Standardizes types, sanitizes strings & exports cleaned CSVs
│   └── load_postgres.py      # Automated SQLAlchemy database ingestion script
│
├── powerbi/
│   ├── ecommerce_dashboard.pbix   # Power BI Dashboard file template
│   └── README.md                  # Detailed Power BI connection & visualization guide
│
├── .env.example              # Template for environment configuration
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusion rules
└── README.md                 # Project documentation (this file)
```

---

## ⚙️ Prerequisites & Setup

### Requirements
- **Python 3.9+**
- **PostgreSQL 12+**
- **Power BI Desktop** (Optional, for dashboard visualization)
- **Git**

---

## 🚀 Step-by-Step Execution Guide

### Step 1: Clone Repository & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/26Divyaniingle/ecommerce-sales-analytics.git
cd ecommerce-sales-analytics

# Create & activate virtual environment
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

### Step 2: Download Kaggle Dataset

1. Visit the Kaggle page: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Download and unzip the archive files into `data/raw/`:
   - `olist_customers_dataset.csv`
   - `olist_geolocation_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `product_category_name_translation.csv`

---

### Step 3: Run Data Cleaning Pipeline

Inspect raw datasets and process them through the Python cleaning pipeline:

```bash
# Inspect raw data dimensions and missing values
python python/inspect_data.py

# Run cleaning and transformation pipeline
python python/clean_data.py
```
*Cleaned datasets will be exported to `data/processed/`.*

---

### Step 4: Configure Database Connection

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL credentials:

```env
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_olist
```

---

### Step 5: Initialize PostgreSQL Database & Schemas

Run the database and table creation SQL scripts using `psql`:

```bash
# 1. Create target database 'ecommerce_olist'
psql -U postgres -f sql/01_create_database.sql

# 2. Build table schemas with constraints
psql -U postgres -d ecommerce_olist -f sql/02_create_tables.sql
```

---

### Step 6: Ingest Data into PostgreSQL

Populate PostgreSQL database tables from the cleaned CSV files:

```bash
python python/load_postgres.py
```

---

### Step 7: Create Performance Indexes & Analytical Views

Optimize query execution speeds and build analytical reporting views:

```bash
# Create B-Tree indexes on join and lookup columns
psql -U postgres -d ecommerce_olist -f sql/04_indexes.sql

# Build reporting views
psql -U postgres -d ecommerce_olist -f sql/05_views.sql
```

---

### Step 8: Analytical SQL Queries

Execute ready-to-use business intelligence queries in PostgreSQL:

```bash
psql -U postgres -d ecommerce_olist -f sql/06_analysis_queries.sql
```

#### Key Metrics Tracked:
- **Monthly Revenue Growth & Order Count**
- **Top Product Categories (English translated)**
- **Customer Lifetime Value (CLV)**
- **Delivery On-Time vs. Late Rates**
- **Payment Method Breakdowns (Credit Card, Boleto, Voucher)**
- **Seller Sales Performance & Rating Correlations**

---

## 📊 Analytical Views Reference

| View Name | Description | Key Columns |
| :--- | :--- | :--- |
| `vw_monthly_sales` | Aggregate monthly revenue & order counts | `month`, `total_orders`, `total_revenue` |
| `vw_category_sales` | Revenue by product category in English | `category_english`, `total_orders`, `total_sales_revenue` |
| `vw_state_sales` | Spending & customer volume per Brazilian state | `customer_state`, `total_unique_customers`, `total_spending` |
| `vw_payment_analysis` | Transaction counts and revenue by payment type | `payment_type`, `transactions`, `revenue` |
| `vw_delivery_performance` | Actual vs. estimated delivery days & status | `order_id`, `actual_delivery_days`, `delivery_status` |
| `vw_customer_lifetime_value` | Cumulative spending per unique customer | `customer_unique_id`, `total_orders`, `lifetime_value` |
| `vw_seller_performance` | Revenue & average price per seller | `seller_id`, `orders_handled`, `total_sales` |
| `vw_product_performance` | Order volume and revenue per product | `product_id`, `orders_count`, `revenue` |

---

## 📈 Power BI Integration

Connect Power BI Desktop to PostgreSQL using the steps outlined in [powerbi/README.md](file:///c:/Users/Divya/ecommerce-sales-analytics/powerbi/README.md):
1. Open Power BI $\rightarrow$ Get Data $\rightarrow$ PostgreSQL database.
2. Server: `localhost`, Database: `ecommerce_olist`.
3. Select pre-built views (`vw_monthly_sales`, `vw_category_sales`, `vw_state_sales`, etc.).
4. Explore executive dashboard visuals!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
