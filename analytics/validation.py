import pandas as pd
from typing import List, Dict, Any

def validate_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Identifies data quality warnings without altering the dataset."""
    warnings = []
    
    missing = df.isnull().sum()
    for col, count in missing[missing > 0].items():
        warnings.append({"type": "missing_values", "field": col, "count": int(count)})
        
    duplicates = df['order_id'].duplicated().sum()
    if duplicates > 0:
        warnings.append({"type": "duplicate_orders", "field": "order_id", "count": int(duplicates)})
        
    negative_qty = (df['quantity'] <= 0).sum()
    if negative_qty > 0:
        warnings.append({"type": "invalid_quantity", "field": "quantity", "count": int(negative_qty)})
        
    negative_price = (df['unit_price'] < 0).sum()
    if negative_price > 0:
        warnings.append({"type": "invalid_price", "field": "unit_price", "count": int(negative_price)})
        
    return warnings