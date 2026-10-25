# AI-Powered Sales Analytics Dashboard

A beginner-friendly Data Analyst portfolio project built with Python, Pandas, SQLite/SQL, Plotly, Streamlit, and an optional Gemini API integration.

## Features

- Synthetic sales dataset with 600 order records.
- Data cleaning for dates, numeric columns, duplicate order IDs, and missing key values.
- KPI cards: revenue, profit, orders, units sold, and profit margin.
- Date, region, and category filters.
- Interactive monthly, regional, product, and sales-channel charts.
- SQL analysis tables and reusable SQL examples.
- Optional AI-generated observations and recommendations based on aggregate metrics.
- Download filtered records as CSV.
- Basic automated data tests.

## Important note about the data

The included dataset is synthetic and is intended for learning and demonstration. Do not present the sample values as real company results. For a job portfolio, explain how you would validate findings against a real business dataset.

## Requirements

- Python 3.11 or newer recommended.
- VS Code (recommended).
- Internet connection only for installing packages and using the Gemini API.

## Setup on Windows (VS Code)

Open the VS Code terminal in this project folder.

### 1. Create a virtual environment

```powershell
py -m venv .venv
```

### 2. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt in VS Code instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Enable AI insights (optional)

1. Create an API key in Google AI Studio: https://aistudio.google.com/app/apikey
2. Copy `.env.example` to a new file named `.env`.
3. Put the key after `GEMINI_API_KEY=` in `.env`.
4. Restart Streamlit and click **Generate AI insights**.

Example `.env`:

```text
GEMINI_API_KEY=your_key_goes_here
```

Keep `.env` private. Do not commit it to GitHub, include it in screenshots, or paste your key into public chats. Free-tier access and model availability are subject to Google's current terms, quotas, and pricing: https://ai.google.dev/gemini-api/docs/pricing

The app sends only summary metrics (aggregated values and top performers) to the AI model, not the full row-level dataset. AI output may still be incorrect; verify it against the dashboard and SQL results.

## SQL queries

See `sql_queries.sql` for:
- Overall KPIs
- Monthly revenue and profit
- Product performance
- Regional performance
- Sales-channel mix
- Negative-profit products
- Average order value

The Streamlit app creates `data/sales.db` automatically and loads the table named `sales`.

## Run tests

```powershell
pytest -q
```

## Folder structure

```text
ai_sales_analytics_project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── sql_queries.sql
├── data/
│   ├── sales_data.csv
│   └── generate_sample_data.py
└── tests/
    └── test_data.py
```

## Suggested analysis questions

1. Which product has the highest revenue?
2. Which region generates the highest revenue and profit?
3. Which month performs best in the selected period?
4. Which sales channel contributes the most revenue?
5. Which products have low profit compared with revenue?
6. What business recommendations can be supported by the data?

## How to publish to GitHub

Create an empty repository on GitHub, then run these commands from the project folder:

```powershell
git init
git add .
git status
git commit -m "Build AI-powered sales analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-sales-analytics-dashboard.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL GitHub provides. Never add `.env` or the generated `data/sales.db` file to Git.

## Portfolio description

**AI-Powered Sales Analytics Dashboard** — Developed an interactive sales analytics application using Python, Pandas, SQLite, SQL, Plotly, and Streamlit. Cleaned and analyzed 600 synthetic order records, created KPI metrics and interactive visualizations, and integrated an optional Gemini API feature to generate concise business insights from aggregated metrics. Added reusable SQL queries, CSV export, and automated data validation tests.

## Limitations and next improvements

- The sample dataset is synthetic.
- The app does not forecast future sales yet.
- The AI feature needs an API key and internet access.
- Add a proper data dictionary and business definitions when using a real dataset.
- Potential extensions: Power BI dashboard, sales forecasting, unit tests for calculations, and deployment to Streamlit Community Cloud.
