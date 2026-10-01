import pytest
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def sample_df():
    """Provides a deterministic dataset for all analytics tests."""
    now = datetime.now()
    return pd.DataFrame({
        "order_id": ["O1", "O1", "O2", "O3", "O4"],
        "order_date": [
            now - timedelta(days=10),
            now - timedelta(days=10),
            now - timedelta(days=45),
            now - timedelta(days=100),
            now - timedelta(days=150)
        ],
        "customer_id": ["C1", "C1", "C2", "C3", "C4"],
        "product_id": ["P1", "P2", "P1", "P3", "P1"],
        "quantity": [2.0, 1.0, 1.0, 5.0, 1.0],
        "unit_price": [50.0, 100.0, 50.0, 20.0, 50.0]
    })