from analytics.kpis import calculate_kpis

def test_calculate_kpis(sample_df):
    kpis = calculate_kpis(sample_df)
    
    # Total Rev = (2*50) + (1*100) + (1*50) + (5*20) + (1*50) = 100 + 100 + 50 + 100 + 50 = 400
    assert kpis["total_revenue"] == 400.0
    assert kpis["total_orders"] == 4 # O1, O2, O3, O4
    assert kpis["total_units"] == 10
    assert kpis["average_order_value"] == 100.0 # 400 / 4
    assert kpis["unique_customers"] == 4
    assert kpis["unique_products"] == 3