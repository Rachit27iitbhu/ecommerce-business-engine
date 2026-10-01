import pandas as pd
from datetime import datetime, timedelta
from analytics.recommendations import generate_recommendations

def test_declining_product_detection():
    # Setup deterministic data
    now = datetime.now()
    dates = []
    quants = []
    
    # Previous period (high sales)
    for i in range(40):
        dates.append(now - timedelta(days=45))
        quants.append(2) # 80 units / 30 days = 2.66 v
        
    # Recent period (low sales)
    for i in range(10):
        dates.append(now - timedelta(days=15))
        quants.append(1) # 10 units / 30 days = 0.33 v
        
    df = pd.DataFrame({
        "order_id": [f"O{i}" for i in range(50)],
        "order_date": dates,
        "customer_id": ["C1"] * 50,
        "product_id": ["P_DECLINE"] * 50,
        "quantity": quants,
        "unit_price": [10.0] * 50
    })
    
    recs = generate_recommendations(df)
    decline_recs = [r for r in recs if r["type"] == "FALLING_DEMAND" and r["entity_id"] == "P_DECLINE"]
    
    assert len(decline_recs) == 1
    assert decline_recs[0]["priority"] == "HIGH"
    assert decline_recs[0]["metric_value"] < -30.0 # Strict decline