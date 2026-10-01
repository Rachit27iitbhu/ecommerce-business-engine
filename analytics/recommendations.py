import pandas as pd
from typing import List, Dict, Any
from analytics.products import analyze_products

def generate_recommendations(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generates deterministic business recommendations based on historical data."""
    recommendations = []
    
    # 1. Product Velocity Rules
    prod_df = analyze_products(df)
    
    # Filter out low-volume noise (e.g., must have sold at least 1 unit/day previously)
    sig_drops = prod_df[(prod_df['prev_velocity'] >= 1.0) & (prod_df['velocity_change_pct'] <= -30.0)]
    
    for _, row in sig_drops.iterrows():
        recommendations.append({
            "priority": "HIGH",
            "type": "FALLING_DEMAND",
            "entity_id": row['product_id'],
            "title": f"Product {row['product_id']} demand declining",
            "description": "Review pricing, visibility, and inventory strategy.",
            "metric": "velocity_change_pct",
            "metric_value": round(row['velocity_change_pct'], 1),
            "evidence": f"Previous velocity: {row['prev_velocity']:.1f} units/day. Recent: {row['recent_velocity']:.1f} units/day."
        })

    sig_growth = prod_df[(prod_df['recent_velocity'] >= 1.0) & (prod_df['velocity_change_pct'] >= 40.0)]
    
    for _, row in sig_growth.iterrows():
        recommendations.append({
            "priority": "MEDIUM",
            "type": "GROWING_OPPORTUNITY",
            "entity_id": row['product_id'],
            "title": f"Product {row['product_id']} demand surging",
            "description": "Investigate inventory availability and expansion opportunity.",
            "metric": "velocity_change_pct",
            "metric_value": round(row['velocity_change_pct'], 1),
            "evidence": f"Velocity increased from {row['prev_velocity']:.1f} to {row['recent_velocity']:.1f} units/day."
        })

    # 2. Revenue Concentration Risk
    total_revenue = prod_df['total_revenue'].sum()
    top_10_pct_count = max(1, int(len(prod_df) * 0.10))
    top_products = prod_df.nlargest(top_10_pct_count, 'total_revenue')
    top_revenue = top_products['total_revenue'].sum()
    
    concentration_pct = (top_revenue / total_revenue) * 100 if total_revenue > 0 else 0
    if concentration_pct > 50.0:
        recommendations.append({
            "priority": "HIGH",
            "type": "REVENUE_CONCENTRATION",
            "entity_id": "GLOBAL",
            "title": "High Revenue Concentration",
            "description": "Monitor concentration risk and protect high-value products.",
            "metric": "revenue_concentration_pct",
            "metric_value": round(concentration_pct, 1),
            "evidence": f"Top 10% of products ({top_10_pct_count} items) generate {concentration_pct:.1f}% of total revenue."
        })
        
    # 3. Customer Inactivity (Simplified inline for brevity)
    df['order_date'] = pd.to_datetime(df['order_date'])
    ref_date = df['order_date'].max()
    cust_last_purchase = df.groupby('customer_id')['order_date'].max()
    days_since = (ref_date - cust_last_purchase).dt.days
    
    inactive = days_since[(days_since > 60) & (days_since <= 90)]
    for cust_id, days in inactive.items():
        recommendations.append({
            "priority": "MEDIUM",
            "type": "CUSTOMER_INACTIVITY",
            "entity_id": cust_id,
            "title": f"Customer {cust_id} at risk of churn",
            "description": "Consider a targeted retention campaign.",
            "metric": "days_since_last_purchase",
            "metric_value": int(days),
            "evidence": f"No purchase for {days} days."
        })
        
    return recommendations