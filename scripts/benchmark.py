import time
import pandas as pd
from analytics.recommendations import generate_recommendations

def run_benchmark():
    try:
        df = pd.read_csv("data/sample_orders.csv")
    except FileNotFoundError:
        print("Run `python data/generate_sample.py` first.")
        return
        
    start_time = time.perf_counter()
    recs = generate_recommendations(df)
    duration = time.perf_counter() - start_time
    
    print("\n--- Benchmark Results ---")
    print(f"Rows processed: {len(df)}")
    print(f"Products: {df['product_id'].nunique()}")
    print(f"Customers: {df['customer_id'].nunique()}")
    print(f"Recommendations generated: {len(recs)}")
    print(f"Processing time: {duration:.4f} seconds\n")

if __name__ == "__main__":
    run_benchmark()