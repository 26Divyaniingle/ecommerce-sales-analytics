import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

def get_db_engine():
    """
    Creates a SQLAlchemy database engine using environment variables.
    Defaults to postgresql://postgres:postgres@localhost:5432/ecommerce_olist if not configured.
    """
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "ecommerce_olist")
    
    # URL-encode user and password to handle special characters like '@'
    encoded_user = quote_plus(db_user)
    encoded_password = quote_plus(db_password)
    
    connection_url = f"postgresql://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_url)

def load_data_to_postgres(processed_dir):
    """
    Loads cleaned CSV files into target tables in PostgreSQL, following foreign key hierarchies.
    """
    print("=" * 60)
    print("  Olist E-Commerce - Loading Data to PostgreSQL Database")
    print("=" * 60)
    
    # Mapping of cleaned files to DB tables
    file_to_table_mapping = {
        "customers_cleaned.csv": "customers",
        "products_cleaned.csv": "products",
        "sellers_cleaned.csv": "sellers",
        "category_translation_cleaned.csv": "category_translation",
        "geolocation_cleaned.csv": "geolocation",
        "orders_cleaned.csv": "orders",
        "order_items_cleaned.csv": "order_items",
        "payments_cleaned.csv": "payments",
        "reviews_cleaned.csv": "reviews"
    }
    
    # Strict sequence mapping to prevent FK violation errors during data insertion
    load_sequence = [
        "customers_cleaned.csv",
        "products_cleaned.csv",
        "sellers_cleaned.csv",
        "category_translation_cleaned.csv",
        "geolocation_cleaned.csv",
        "orders_cleaned.csv",
        "order_items_cleaned.csv",
        "payments_cleaned.csv",
        "reviews_cleaned.csv"
    ]
    
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            print("  Successfully connected to the database.")
    except Exception as e:
        print(f"  Database connection failed: {e}")
        print("  Please verify your PostgreSQL database server is running and credentials are correct.")
        return
        
    for filename in load_sequence:
        filepath = os.path.join(processed_dir, filename)
        table_name = file_to_table_mapping.get(filename)
        
        if not os.path.exists(filepath):
            print(f"  [SKIPPED] Cleaned file '{filename}' does not exist.")
            continue
            
        try:
            print(f"  Loading '{filename}' to table '{table_name}'...")
            df = pd.read_csv(filepath)
            if df.empty:
                print(f"    - File is empty, skipping database write.")
                continue
                
            for col in df.columns:
                if 'date' in col or 'timestamp' in col:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=5000
            )
            print(f"    -> Successfully loaded {len(df)} rows into '{table_name}'.")
            
        except Exception as e:
            print(f"  Error loading '{filename}' to database: {e}")
            print("  (Note: Make sure table schema exists. Run 'sql/02_create_tables.sql' first.)")
            
    print("\n" + "=" * 60)
    print("Database Load Completed.")
    print("=" * 60)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, "data", "processed")
    load_data_to_postgres(processed_dir)
