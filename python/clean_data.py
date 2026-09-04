import os
import pandas as pd
import numpy as np

def clean_customers(df):
    print("  Cleaning Customers...")
    df = df.copy()
    df['customer_city'] = df['customer_city'].str.strip()
    df['customer_state'] = df['customer_state'].str.strip().str.upper()
    return df

def clean_geolocation(df):
    print("  Cleaning Geolocation...")
    df = df.copy()
    # Deduplicate rows slightly to save space/time, but keep requested columns
    df = df.drop_duplicates(subset=['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'])
    df['geolocation_city'] = df['geolocation_city'].str.strip()
    df['geolocation_state'] = df['geolocation_state'].str.strip().str.upper()
    return df

def clean_order_items(df):
    print("  Cleaning Order Items...")
    df = df.copy()
    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
    df['freight_value'] = pd.to_numeric(df['freight_value'], errors='coerce').fillna(0.0)
    return df

def clean_payments(df):
    print("  Cleaning Payments...")
    df = df.copy()
    df['payment_sequential'] = pd.to_numeric(df['payment_sequential'], errors='coerce').fillna(1).astype(int)
    df['payment_installments'] = pd.to_numeric(df['payment_installments'], errors='coerce').fillna(1).astype(int)
    df['payment_value'] = pd.to_numeric(df['payment_value'], errors='coerce').fillna(0.0)
    return df

def clean_reviews(df):
    print("  Cleaning Reviews...")
    df = df.copy()
    # Deduplicate by review_id to respect the single-column primary key constraint
    df = df.drop_duplicates(subset=['review_id'])
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], errors='coerce')
    df['review_answer_timestamp'] = pd.to_datetime(df['review_answer_timestamp'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce').fillna(5).astype(int)
    df['review_comment_title'] = df['review_comment_title'].fillna("").str.strip()
    df['review_comment_message'] = df['review_comment_message'].fillna("").str.strip()
    return df

def clean_orders(df):
    print("  Cleaning Orders...")
    df = df.copy()
    date_cols = [
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date', 
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df['order_status'] = df['order_status'].str.strip().str.lower()
    return df

def clean_products(df):
    print("  Cleaning Products...")
    df = df.copy()
    
    # Rename columns to fix spelling from raw data
    df = df.rename(columns={
        'product_name_lenght': 'product_name_length',
        'product_description_lenght': 'product_description_length'
    })
    
    df['product_category_name'] = df['product_category_name'].fillna("missing_category").str.strip()
    
    num_cols = [
        'product_name_length', 'product_description_length', 
        'product_photos_qty', 'product_weight_g', 
        'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df

def clean_sellers(df):
    print("  Cleaning Sellers...")
    df = df.copy()
    df['seller_city'] = df['seller_city'].str.strip()
    df['seller_state'] = df['seller_state'].str.strip().str.upper()
    return df

def clean_translation(df):
    print("  Cleaning Category Translation...")
    df = df.copy()
    df['product_category_name'] = df['product_category_name'].str.strip()
    df['product_category_name_english'] = df['product_category_name_english'].str.strip()
    return df

def run_cleaning_pipeline(raw_dir, processed_dir):
    """
    Executes Olist E-commerce cleaning pipeline.
    Output CSVs are mapped directly to target database table names.
    """
    print("=" * 60)
    print("  Olist E-Commerce - Executing Data Cleaning Pipeline")
    print("=" * 60)
    
    os.makedirs(processed_dir, exist_ok=True)
    
    pipeline_config = {
        "olist_customers_dataset.csv": (clean_customers, "customers_cleaned.csv"),
        "olist_geolocation_dataset.csv": (clean_geolocation, "geolocation_cleaned.csv"),
        "olist_order_items_dataset.csv": (clean_order_items, "order_items_cleaned.csv"),
        "olist_order_payments_dataset.csv": (clean_payments, "payments_cleaned.csv"),
        "olist_order_reviews_dataset.csv": (clean_reviews, "reviews_cleaned.csv"),
        "olist_orders_dataset.csv": (clean_orders, "orders_cleaned.csv"),
        "olist_products_dataset.csv": (clean_products, "products_cleaned.csv"),
        "olist_sellers_dataset.csv": (clean_sellers, "sellers_cleaned.csv"),
        "product_category_name_translation.csv": (clean_translation, "category_translation_cleaned.csv")
    }
    
    for raw_file, (clean_func, processed_file) in pipeline_config.items():
        raw_path = os.path.join(raw_dir, raw_file)
        processed_path = os.path.join(processed_dir, processed_file)
        
        if not os.path.exists(raw_path):
            print(f"  [SKIPPED] Raw file '{raw_file}' does not exist.")
            continue
            
        try:
            if os.path.getsize(raw_path) <= 1:
                print(f"  [SKIPPED] Raw file '{raw_file}' is empty/placeholder.")
                continue
                
            df_raw = pd.read_csv(raw_path)
            if df_raw.empty:
                print(f"  [SKIPPED] Raw file '{raw_file}' has no row data.")
                continue
                
            df_clean = clean_func(df_raw)
            df_clean.to_csv(processed_path, index=False)
            print(f"    -> Saved cleaned version to: {processed_file} (Rows: {len(df_clean)})")
            
        except Exception as e:
            print(f"  Error processing '{raw_file}': {e}")
            
    print("\n" + "=" * 60)
    print("Cleaning Pipeline Completed.")
    print("=" * 60)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    run_cleaning_pipeline(raw_dir, processed_dir)
