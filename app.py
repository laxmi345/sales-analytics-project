import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide", page_icon="📊")

# ── Load Data (Snowflake with Automatic Local CSV Fallback) ──
@st.cache_data(ttl=600)
def load_data():
    # 1. Try Snowflake connection if secrets are configured
    if "SNOWFLAKE_ACCOUNT" in st.secrets:
        try:
            import snowflake.connector
            conn = snowflake.connector.connect(
                account=st.secrets["SNOWFLAKE_ACCOUNT"],
                user=st.secrets["SNOWFLAKE_USER"],
                password=st.secrets["SNOWFLAKE_PASSWORD"],
                role=st.secrets.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
                warehouse=st.secrets.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
                database=st.secrets.get("SNOWFLAKE_DATABASE", "SALES_DW"),
                schema=st.secrets.get("SNOWFLAKE_SCHEMA", "SALES"),
            )
            query = "SELECT * FROM SALES_DW.SALES.MART_DASHBOARD"
            df = pd.read_sql(query, conn)
            return df, "Snowflake Data Warehouse (Live)"
        except Exception as e:
            st.sidebar.warning(f"Snowflake connection bypassed ({e}). Using local dataset.")

    # 2. Fallback to repository CSV dataset (data/train.csv)
    possible_paths = [
        "data/train.csv",
        "../data/train.csv",
        "train.csv",
        os.path.join(os.path.dirname(__file__), "data", "train.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "train.csv"),
    ]
    csv_file = None
    for p in possible_paths:
        if os.path.exists(p):
            csv_file = p
            break

    if not csv_file:
        raise FileNotFoundError("Could not find data/train.csv dataset file.")

    df = pd.read_csv(csv_file, encoding='latin-1')
    df.drop(columns=['Row ID'], inplace=True, errors='ignore')
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
    df['YEAR'] = df['Order Date'].dt.year
    df['MONTH'] = df['Order Date'].dt.month
    df['MONTH_NAME'] = df['Order Date'].dt.strftime('%B')
    df['QUARTER'] = df['Order Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    df['DAYS_TO_SHIP'] = (df['Ship Date'] - df['Order Date']).dt.days
    df.columns = [c.upper().replace(' ', '_').replace('-', '_') for c in df.columns]
    return df, "Superstore Enterprise Dataset (Cached CSV)"

df, data_source = load_data()

# ── Sidebar Filters ──
st.sidebar.header("🎯 Filter Options")
st.sidebar.caption(f"Connected to: **{data_source}**")

# Year filter
years = sorted(df['YEAR'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + [str(y) for y in years])

# Region filter
regions = sorted(df['REGION'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", ["All"] + regions)

# Category filter
categories = sorted(df['CATEGORY'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['YEAR'] == int(selected_year)]
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['REGION'] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['CATEGORY'] == selected_category]

# ── Header & KPIs ──
st.title("📊 Sales Analytics Executive Dashboard")
st.markdown("End-to-End Analytics Pipeline built with **Python, Snowflake / dbt & Streamlit**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['SALES'].sum():,.2f}")
col2.metric("Total Orders", f"{filtered_df['ORDER_ID'].nunique():,}")
col3.metric("Avg Order Value", f"${(filtered_df['SALES'].mean() if not filtered_df.empty else 0):,.2f}")
col4.metric("Active Customers", f"{filtered_df['CUSTOMER_ID'].nunique():,}")

st.divider()

# ── Row 1: Monthly Trend + Region-wise ──
c1, c2 = st.columns(2)

with c1:
    monthly = filtered_df.groupby(['YEAR', 'MONTH', 'MONTH_NAME'], as_index=False)['SALES'].sum()
    monthly = monthly.sort_values(['YEAR', 'MONTH'])
    monthly['PERIOD'] = monthly['MONTH_NAME'] + " " + monthly['YEAR'].astype(str)
    fig1 = px.line(
        monthly, 
        x='PERIOD', 
        y='SALES', 
        title="📈 Monthly Revenue Trend", 
        markers=True,
        color_discrete_sequence=['#2E86AB']
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    region = filtered_df.groupby('REGION', as_index=False)['SALES'].sum().sort_values('SALES', ascending=False)
    fig2 = px.bar(
        region, 
        x='REGION', 
        y='SALES', 
        title="🌍 Region-wise Sales Distribution", 
        color='REGION',
        text_auto='.2s'
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Category Share + Customer Segments ──
c3, c4 = st.columns(2)

with c3:
    cat = filtered_df.groupby('CATEGORY', as_index=False)['SALES'].sum()
    fig3 = px.pie(
        cat, 
        names='CATEGORY', 
        values='SALES', 
        title="🥧 Category Contribution",
        hole=0.4
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    seg = filtered_df.groupby('SEGMENT', as_index=False)['SALES'].sum()
    fig4 = px.bar(
        seg, 
        x='SEGMENT', 
        y='SALES', 
        title="👥 Sales by Customer Segment", 
        color='SEGMENT',
        text_auto='.2s'
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Top 10 Products ──
top_products = (
    filtered_df.groupby('PRODUCT_NAME', as_index=False)['SALES']
    .sum()
    .sort_values('SALES', ascending=False)
    .head(10)
)
fig5 = px.bar(
    top_products, 
    x='SALES', 
    y='PRODUCT_NAME', 
    orientation='h',
    title="🏆 Top 10 Revenue-Generating Products",
    color='SALES',
    color_continuous_scale='Viridis'
)
fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig5, use_container_width=True)

# ── Raw Data Table ──
with st.expander("🔍 View Raw Filtered Records"):
    st.dataframe(filtered_df.head(150), use_container_width=True)