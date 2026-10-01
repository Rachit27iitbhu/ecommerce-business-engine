import pandas as pd
from datetime import timedelta

def analyze_customers(df: pd.DataFrame, reference_date: pd.Timestamp = None) -> pd.DataFrame:
    """Calculates customer lifetime value and segments by recency."""
    if reference_date is None:
        reference_date = pd.to_datetime(df['order_date']).max()
        
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['revenue'] = df['quantity'] * df['unit_price']
    
    customers = df.groupby('customer_id').agg(
        total_orders=('order_id', 'nunique'),
        total_revenue=('revenue', 'sum'),
        last_purchase_date=('order_date', 'max')
    ).reset_index()
    
    customers['average_order_value'] = customers['total_revenue'] / customers['total_orders']
    customers['days_since_last_purchase'] = (reference_date - customers['last_purchase_date']).dt.days
    
    # Deterministic Segmentation
    def segment_customer(days: int) -> str:
        if pd.isna(days):
            return "Unknown"
        if days <= 60:
            return "Active"
        elif days <= 120:
            return "At-risk"
        return "Inactive"
        
    customers['segment'] = customers['days_since_last_purchase'].apply(segment_customer)
    
    return customers