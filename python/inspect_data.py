import os
import pandas as pd

def inspect_datasets(raw_data_dir):
    """
    Inspects all raw CSV datasets in the specified directory.
    Prints basic statistics, shapes, columns, missing values, and duplicate rows.
    """
    expected_files = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv"
    ]
    
    print("=" * 60)
    print("  Olist E-Commerce Dataset - Raw Data Inspection Report")
    print("=" * 60)
    
    if not os.path.exists(raw_data_dir):
        print(f"ERROR: Raw data directory '{raw_data_dir}' does not exist.")
        return

    for filename in expected_files:
        filepath = os.path.join(raw_data_dir, filename)
        print(f"\nAnalyzing: {filename}")
        print("-" * len(f"Analyzing: {filename}"))
        
        if not os.path.exists(filepath):
            print("  Status: [MISSING] File not found. Please download from Kaggle.")
            continue
            
        try:
            # Check if file is empty
            if os.path.getsize(filepath) <= 1:
                print("  Status: [EMPTY] File size is 0 or 1 byte.")
                continue
                
            df = pd.read_csv(filepath)
            
            if df.empty:
                print("  Status: [EMPTY HEADER] Contains headers but no row data.")
                print(f"  Columns: {list(df.columns)}")
                continue
                
            print(f"  - Shape (rows, cols): {df.shape}")
            print(f"  - Duplicate Rows   : {df.duplicated().sum()}")
            
            # Print column summary
            print("\n  - Column Breakdown:")
            print(f"    {'Column Name':<35} | {'Dtype':<10} | {'Null Count':<10} | {'Null %':<8}")
            print("    " + "-" * 71)
            for col in df.columns:
                null_count = df[col].isnull().sum()
                null_pct = (null_count / len(df)) * 100
                dtype_str = str(df[col].dtype)
                print(f"    {col:<35} | {dtype_str:<10} | {null_count:<10} | {null_pct:>6.2f}%")
                
            print("\n  - Preview (first 2 rows):")
            print(df.head(2).to_string(index=False, justify='left', max_colwidth=30))
            
        except Exception as e:
            print(f"  Error reading file: {e}")
            
    print("\n" + "=" * 60)
    print("Inspection Completed.")
    print("=" * 60)

if __name__ == "__main__":
    # Standard location relative to python project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    inspect_datasets(raw_dir)
