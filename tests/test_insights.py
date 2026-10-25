
import pandas as pd

from insights import generate_rule_based_insights


def test_empty_data():
    data = pd.DataFrame(
        columns=["revenue", "profit", "region", "product"]
    )

    result = generate_rule_based_insights(data)

    assert len(result) == 1
    assert "No sales data" in result[0]


def test_sales_insights():
    data = pd.DataFrame({
        "revenue": [1000, 500, 800],
        "profit": [200, 100, 160],
        "region": ["North", "South", "North"],
        "product": ["Laptop", "Mouse", "Laptop"],
    })

    result = generate_rule_based_insights(data)

    assert any("North" in item for item in result)
    assert any("Laptop" in item for item in result)
    assert any("profit margin" in item.lower() for item in result)
