from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "sales_data.csv"

def test_sample_dataset_exists_and_has_rows():
    assert DATA_PATH.exists()
    data = pd.read_csv(DATA_PATH)
    assert len(data) > 0

def test_required_columns_exist():
    data = pd.read_csv(DATA_PATH)
    required = {
        "order_id", "order_date", "region", "sales_channel", "product",
        "category", "quantity", "unit_price", "discount_pct", "revenue", "cost", "profit"
    }
    assert required.issubset(set(data.columns))

def test_revenue_and_profit_are_numeric():
    data = pd.read_csv(DATA_PATH)
    assert pd.to_numeric(data["revenue"], errors="coerce").notna().all()
    assert pd.to_numeric(data["profit"], errors="coerce").notna().all()

def test_order_ids_are_unique():
    data = pd.read_csv(DATA_PATH)
    assert data["order_id"].is_unique
