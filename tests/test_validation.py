import pandas as pd
from analytics.validation import validate_data

def test_data_validation():
    df = pd.DataFrame({
        "order_id": ["O1", "O1", "O2", "O3"],
        "order_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "customer_id": ["C1", "C2", "C3", "C4"],
        "product_id": ["P1", "P2", "P3", "P4"],
        "quantity": [1.0, -2.0, None, 5.0],
        "unit_price": [10.0, 20.0, -5.0, 15.0]
    })
    
    warnings = validate_data(df)
    warning_types = [w["type"] for w in warnings]
    
    assert "missing_values" in warning_types
    assert "duplicate_orders" in warning_types
    assert "invalid_quantity" in warning_types
    assert "invalid_price" in warning_types