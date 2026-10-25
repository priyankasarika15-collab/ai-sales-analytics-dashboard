"""Regenerate the synthetic sample dataset with a fixed random seed."""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_PATH = BASE_DIR / "data" / "sales_data.csv"
rng = np.random.default_rng(42)
n = 600
dates = pd.to_datetime(rng.choice(pd.date_range("2025-01-01", "2025-12-31", freq="D"), size=n))
products = {
    "Laptop Stand": ("Accessories", 900, 1450),
    "Wireless Mouse": ("Accessories", 350, 650),
    "Notebook Pack": ("Stationery", 80, 160),
    "Office Chair": ("Furniture", 3200, 5200),
    "Desk Lamp": ("Furniture", 650, 1100),
    "Water Bottle": ("Lifestyle", 250, 480),
    "Backpack": ("Lifestyle", 850, 1450),
    "Keyboard": ("Accessories", 700, 1250),
}
regions = ["North", "South", "East", "West", "Central"]
channels = ["Online", "Retail", "Partner"]
rows = []
for i in range(n):
    product = rng.choice(list(products.keys()))
    category, low, high = products[product]
    quantity = int(rng.integers(1, 6))
    unit_price = round(float(rng.uniform(low, high)), 2)
    unit_cost = round(unit_price * float(rng.uniform(0.52, 0.82)), 2)
    discount_pct = float(rng.choice([0, 0.05, 0.10, 0.15], p=[0.45, 0.25, 0.20, 0.10]))
    revenue = round(quantity * unit_price * (1 - discount_pct), 2)
    cost = round(quantity * unit_cost, 2)
    rows.append({
        "order_id": f"ORD-{i+1:04d}",
        "order_date": pd.Timestamp(dates[i]).strftime("%Y-%m-%d"),
        "region": str(rng.choice(regions)),
        "sales_channel": str(rng.choice(channels)),
        "product": product,
        "category": category,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_pct": discount_pct,
        "revenue": revenue,
        "cost": cost,
        "profit": round(revenue - cost, 2),
    })
pd.DataFrame(rows).to_csv(OUT_PATH, index=False)
print(f"Created {OUT_PATH} with {n} rows")
