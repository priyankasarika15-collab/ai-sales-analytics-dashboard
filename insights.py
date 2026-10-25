
import pandas as pd


def generate_rule_based_insights(data: pd.DataFrame) -> list[str]:
    """Generate business insights from the currently filtered sales data."""

    if data.empty:
        return ["No sales data is available for the selected filters."]

    insights = []

    # 1. Overall performance
    total_revenue = data["revenue"].sum()
    total_profit = data["profit"].sum()

    insights.append(
        f"Total revenue is ₹{total_revenue:,.2f}, "
        f"with total profit of ₹{total_profit:,.2f}."
    )

    # 2. Highest-revenue region
    region_sales = data.groupby("region")["revenue"].sum()

    if not region_sales.empty:
        best_region = region_sales.idxmax()
        insights.append(
            f"{best_region} is the highest-revenue region, "
            f"generating ₹{region_sales.max():,.2f}."
        )

    # 3. Highest-revenue product
    product_sales = data.groupby("product")["revenue"].sum()

    if not product_sales.empty:
        best_product = product_sales.idxmax()
        insights.append(
            f"{best_product} is the highest-revenue product, "
            f"generating ₹{product_sales.max():,.2f}."
        )

    # 4. Profit margin
    if total_revenue > 0:
        margin = (total_profit / total_revenue) * 100
        insights.append(
            f"The overall profit margin is {margin:.2f}%."
        )
    else:
        insights.append(
            "Profit margin cannot be calculated because revenue is zero or negative."
        )

    # 5. Business recommendation based on the data
    if not region_sales.empty and len(region_sales) > 1:
        lowest_region = region_sales.idxmin()
        insights.append(
            f"Review sales and customer demand in {lowest_region}, "
            "the lowest-revenue region, to identify improvement opportunities."
        )

    return insights
    