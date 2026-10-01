import pandas as pd
from analytics.customers import analyze_customers

def test_customer_segmentation(sample_df):
    ref_date = pd.to_datetime(sample_df['order_date']).max()
    customers = analyze_customers(sample_df, reference_date=ref_date)
    
    c1 = customers[customers['customer_id'] == 'C1'].iloc[0]
    c3 = customers[customers['customer_id'] == 'C3'].iloc[0]
    c4 = customers[customers['customer_id'] == 'C4'].iloc[0]
    
    assert c1['total_revenue'] == 200.0
    assert c1['segment'] == 'Active'      # 0 days from ref
    assert c3['segment'] == 'At-risk'     # 90 days from ref
    assert c4['segment'] == 'Inactive'    # 140 days from ref