import pandas as pd
from typing import Dict, Any

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates overall business KPIs from transaction data."""
    if df.empty:
        return {
            "total_revenue": 0.0, "total_orders": 0, "total_units": 0,
            "average_order_value": 0.0, "unique_customers": 0, "unique_products": 0
        }

    # Ensure correct types
    df['revenue'] = df['quantity'] * df['unit_price']
    
    total_revenue = float(df['revenue'].sum())
    total_orders = int(df['order_id'].nunique())
    total_units = int(df['quantity'].sum())
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_units": total_units,
        "average_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0,
        "unique_customers": int(df['customer_id'].nunique()),
        "unique_products": int(df['product_id'].nunique())
    }