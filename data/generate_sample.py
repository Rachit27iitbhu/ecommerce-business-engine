import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(rows: int = 10000) -> None:
    """Generates deterministic synthetic transaction data for testing."""
    np.random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    dates = [start_date + timedelta(days=np.random.randint(0, 180)) for _ in range(rows)]
    product_ids = [f"P{str(i).zfill(3)}" for i in np.random.randint(1, 100, rows)]
    customer_ids = [f"C{str(i).zfill(4)}" for i in np.random.randint(1, 1000, rows)]
    
    # Introduce some data quality issues intentionally for the validation engine
    quantities = np.random.randint(1, 10, rows).astype(float)
    quantities[np.random.choice(rows, 10, replace=False)] = -1  # Negative quantities
    quantities[np.random.choice(rows, 10, replace=False)] = np.nan # Missing quantities
    
    prices = np.random.uniform(10.0, 500.0, rows)
    prices[np.random.choice(rows, 5, replace=False)] = -50.0 # Invalid prices

    df = pd.DataFrame({
        "order_id": [f"ORD{str(i).zfill(6)}" for i in range(rows)],
        "order_date": dates,
        "customer_id": customer_ids,
        "product_id": product_ids,
        "quantity": quantities,
        "unit_price": prices
    })
    
    df.to_csv("data/sample_orders.csv", index=False)
    print(f"Generated {rows} rows in data/sample_orders.csv")

if __name__ == "__main__":
    generate_sample_data()