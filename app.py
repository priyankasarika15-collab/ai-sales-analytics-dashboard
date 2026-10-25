
from pathlib import Path
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from insights import generate_rule_based_insights


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI-Powered Sales Intelligence")
st.caption(
    "Sales analytics, business insights, interactive charts, and SQL analysis"
)


# --------------------------------------------------
# 2. DATASET CONFIGURATION
# --------------------------------------------------

data_folder = Path(__file__).parent / "data"

test_file = data_folder / "sales_analytics_testing_dataset.csv"
sales_file = data_folder / "sales_data.csv"

required_cols = [
    "order_date",
    "region",
    "category",
    "product",
    "revenue",
    "profit",
]


# --------------------------------------------------
# 3. LOAD AND CLEAN DATA
# --------------------------------------------------

def clean_data(data):
    """Validate and clean the uploaded sales dataset."""

    data = data.copy()

    # Remove extra spaces from column names
    data.columns = data.columns.str.strip()

    # Check required columns
    missing_cols = [
        column
        for column in required_cols
        if column not in data.columns
    ]

    if missing_cols:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_cols)
        )

    # Convert dates and numeric columns
    data["order_date"] = pd.to_datetime(
        data["order_date"], errors="coerce"
    )

    for column in ["revenue", "profit"]:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    # Remove rows with invalid dates or financial values
    data = data.dropna(
        subset=["order_date", "revenue", "profit"]
    )

    # Standardize text fields
    for column in [
        "region",
        "category",
        "product",
        "sales_channel",
        "order_status",
    ]:
        if column in data.columns:
            data[column] = data[column].fillna(
                "Unknown"
            ).astype(str).str.strip()

    return data


# --------------------------------------------------
# 4. SELECT THE DATASET
# --------------------------------------------------

st.sidebar.header("📁 Sales Dataset")

file = st.sidebar.file_uploader(
    "Upload your sales CSV",
    type=["csv"],
)

try:
    if file is not None:
        raw_df = pd.read_csv(file)
        file_name = file.name

    elif test_file.exists():
        raw_df = pd.read_csv(test_file)
        file_name = test_file.name

    elif sales_file.exists():
        raw_df = pd.read_csv(sales_file)
        file_name = sales_file.name

    else:
        st.error(
            "No CSV dataset found. Please upload a sales CSV "
            "using the sidebar."
        )
        st.stop()

    df = clean_data(raw_df)

except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if df.empty:
    st.error("The dataset contains no valid sales records.")
    st.stop()

st.sidebar.success(f"Loaded: {file_name}")
st.sidebar.write(f"Valid records: {len(df):,}")


# --------------------------------------------------
# 5. FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filter Sales")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

dates = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(dates, (tuple, list)):
    if len(dates) == 2:
        start_date, end_date = dates
    else:
        start_date = dates[0]
        end_date = dates[0]
else:
    start_date = dates
    end_date = dates

regions = sorted(df["region"].dropna().unique().tolist())
categories = sorted(df["category"].dropna().unique().tolist())

chosen_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions,
)

chosen_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories,
)

if "sales_channel" in df.columns:
    channels = sorted(
        df["sales_channel"].dropna().unique().tolist()
    )
    chosen_channels = st.sidebar.multiselect(
        "Sales channel",
        channels,
        default=channels,
    )
else:
    chosen_channels = None

if "order_status" in df.columns:
    statuses = sorted(
        df["order_status"].dropna().unique().tolist()
    )

    default_statuses = (
        ["Completed"] if "Completed" in statuses
        else statuses
    )

    chosen_statuses = st.sidebar.multiselect(
        "Order status",
        statuses,
        default=default_statuses,
        help="Completed orders are selected by default.",
    )
else:
    chosen_statuses = None


# --------------------------------------------------
# 6. APPLY FILTERS
# --------------------------------------------------

sales_df = df.copy()

sales_df = sales_df[
    (sales_df["order_date"].dt.date >= start_date)
    & (sales_df["order_date"].dt.date <= end_date)
]

sales_df = sales_df[
    sales_df["region"].isin(chosen_regions)
    & sales_df["category"].isin(chosen_categories)
]

if chosen_channels is not None:
    sales_df = sales_df[
        sales_df["sales_channel"].isin(chosen_channels)
    ]

if chosen_statuses is not None:
    sales_df = sales_df[
        sales_df["order_status"].isin(chosen_statuses)
    ]

if sales_df.empty:
    st.warning(
        "No sales records match these filters. "
        "Try selecting a different date range or filter."
    )
    st.stop()


# --------------------------------------------------
# 7. KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("📌 Sales Performance")

revenue = sales_df["revenue"].sum()
profit = sales_df["profit"].sum()

if "order_id" in sales_df.columns:
    orders = sales_df["order_id"].nunique()
else:
    orders = len(sales_df)

if "quantity" in sales_df.columns:
    quantity = sales_df["quantity"].sum()
else:
    quantity = None

if revenue != 0:
    margin = profit / revenue * 100
else:
    margin = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₹{revenue:,.2f}",
)

col2.metric(
    "Total Profit",
    f"₹{profit:,.2f}",
)

col3.metric(
    "Number of Orders",
    f"{orders:,}",
)

col4.metric(
    "Profit Margin",
    f"{margin:.2f}%",
)

if quantity is not None:
    st.caption(f"Total units sold: {quantity:,.0f}")

st.caption(
    f"Showing {len(sales_df):,} records after applying filters."
)


# --------------------------------------------------
# 8. INTERACTIVE CHARTS
# --------------------------------------------------

st.divider()
st.subheader("📈 Sales Dashboard")

month_df = sales_df.copy()
month_df["month"] = (
    month_df["order_date"].dt.to_period("M").astype(str)
)

month_sales = (
    month_df.groupby("month", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    .sort_values("month")
)

region_sales = (
    sales_df.groupby("region", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    .sort_values("revenue", ascending=False)
)

product_sales = (
    sales_df.groupby("product", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    .sort_values("revenue", ascending=False)
)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("**Monthly Revenue Trend**")

    month_chart = px.line(
        month_sales,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue by Month",
    )

    month_chart.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
    )

    st.plotly_chart(
        month_chart,
        use_container_width=True,
    )

with chart2:
    st.markdown("**Revenue by Region**")

    region_chart = px.bar(
        region_sales,
        x="region",
        y="revenue",
        color="region",
        title="Regional Revenue",
    )

    region_chart.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue (₹)",
        showlegend=False,
    )

    st.plotly_chart(
        region_chart,
        use_container_width=True,
    )

chart3, chart4 = st.columns(2)

with chart3:
    st.markdown("**Top Products by Revenue**")

    top_products = product_sales.head(10)

    product_chart = px.bar(
        top_products,
        x="revenue",
        y="product",
        orientation="h",
        title="Top 10 Products",
    )

    product_chart.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Product",
        yaxis={"categoryorder": "total ascending"},
    )

    st.plotly_chart(
        product_chart,
        use_container_width=True,
    )

with chart4:
    if "sales_channel" in sales_df.columns:
        st.markdown("**Revenue by Sales Channel**")

        channel_sales = (
            sales_df.groupby("sales_channel", as_index=False)
            ["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )

        channel_chart = px.pie(
            channel_sales,
            names="sales_channel",
            values="revenue",
            title="Sales Channel Distribution",
        )

        st.plotly_chart(
            channel_chart,
            use_container_width=True,
        )
    else:
        st.info(
            "Add a sales_channel column to display "
            "the channel distribution chart."
        )


# --------------------------------------------------
# 9. RULE-BASED BUSINESS INSIGHTS
# --------------------------------------------------

st.divider()
st.subheader("💡 Rule-Based Sales Insights")

st.write(
    "These insights are generated from the currently "
    "filtered dataset using Python rules."
)

try:
    insights = generate_rule_based_insights(sales_df)

    for insight in insights:
        st.markdown(f"- {insight}")

except Exception as error:
    st.warning(f"Unable to generate insights: {error}")


# --------------------------------------------------
# 10. SQL ANALYSIS
# --------------------------------------------------

st.divider()
st.subheader("🗄️ SQL Sales Analysis")

st.write(
    "Explore your filtered sales data using SQLite queries."
)

with sqlite3.connect(":memory:") as connection:
    sales_df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Regional Analysis",
            "Product Analysis",
            "Monthly Analysis",
            "Custom SQL",
        ]
    )

    with tab1:
        st.markdown("**Revenue and profit by region**")

        query = """
            SELECT
                region,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(profit), 2) AS total_profit
            FROM sales
            GROUP BY region
            ORDER BY total_revenue DESC
        """

        result = pd.read_sql_query(query, connection)
        st.dataframe(result, use_container_width=True)

    with tab2:
        st.markdown("**Top 10 products by revenue**")

        query = """
            SELECT
                product,
                SUM(quantity) AS units_sold,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(profit), 2) AS total_profit
            FROM sales
            GROUP BY product
            ORDER BY total_revenue DESC
            LIMIT 10
        """

        if "quantity" in sales_df.columns:
            result = pd.read_sql_query(query, connection)
        else:
            query = """
                SELECT
                    product,
                    ROUND(SUM(revenue), 2) AS total_revenue,
                    ROUND(SUM(profit), 2) AS total_profit
                FROM sales
                GROUP BY product
                ORDER BY total_revenue DESC
                LIMIT 10
            """
            result = pd.read_sql_query(query, connection)

        st.dataframe(result, use_container_width=True)

    with tab3:
        st.markdown("**Revenue by month**")

        query = """
            SELECT
                strftime('%Y-%m', order_date) AS month,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(profit), 2) AS total_profit
            FROM sales
            GROUP BY month
            ORDER BY month
        """

        result = pd.read_sql_query(query, connection)
        st.dataframe(result, use_container_width=True)

    with tab4:
        st.markdown("**Run a read-only SQL query**")

        query = st.text_area(
            "SQL query",
            value=(
                "SELECT region, SUM(revenue) AS total_revenue "
                "FROM sales GROUP BY region "
                "ORDER BY total_revenue DESC"
            ),
            height=120,
        )

        if st.button("Run SQL Query"):
            # Permit only SELECT statements for this demo.
            if not query.strip().lower().startswith("select"):
                st.error("Only SELECT queries are allowed.")
            else:
                try:
                    result = pd.read_sql_query(
                        query,
                        connection,
                    )
                    st.dataframe(
                        result,
                        use_container_width=True,
                    )
                except Exception as error:
                    st.error(f"SQL error: {error}")


# --------------------------------------------------
# 11. DATA PREVIEW AND DOWNLOAD
# --------------------------------------------------

st.divider()
st.subheader("📋 Filtered Sales Data")

with st.expander("View data records"):
    st.dataframe(
        sales_df,
        use_container_width=True,
        hide_index=True,
    )

csv_data = sales_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Sales CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)

st.caption(
    "Portfolio project using sample sales data. "
    "Business metrics depend on the selected filters and order statuses."
)
