import pandas as pd
import numpy as np
from datetime import timedelta

def analyze_products(df: pd.DataFrame, reference_date: pd.Timestamp = None) -> pd.DataFrame:
    """Calculates product performance and sales velocity."""
    if reference_date is None:
        reference_date = pd.to_datetime(df['order_date']).max()
        
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['revenue'] = df['quantity'] * df['unit_price']
    
    # Time splits
    recent_cutoff = reference_date - timedelta(days=30)
    prev_cutoff = recent_cutoff - timedelta(days=30)
    
    recent_df = df[df['order_date'] > recent_cutoff]
    prev_df = df[(df['order_date'] <= recent_cutoff) & (df['order_date'] > prev_cutoff)]
    
    # Aggregations
    overall = df.groupby('product_id').agg(
        total_revenue=('revenue', 'sum'),
        total_units=('quantity', 'sum'),
        total_orders=('order_id', 'nunique')
    )
    
    recent_velocity = recent_df.groupby('product_id')['quantity'].sum() / 30.0
    prev_velocity = prev_df.groupby('product_id')['quantity'].sum() / 30.0
    
    overall['recent_velocity'] = recent_velocity
    overall['prev_velocity'] = prev_velocity
    
    # Fill NaN velocities with 0 for accurate math
    overall = overall.fillna({'recent_velocity': 0, 'prev_velocity': 0})
    
    overall['velocity_change_pct'] = np.where(
        overall['prev_velocity'] > 0,
        ((overall['recent_velocity'] - overall['prev_velocity']) / overall['prev_velocity']) * 100,
        0
    )
    
    return overall.reset_index()