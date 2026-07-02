import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ── Snowflake Connection ───────────────────────────────────
@st.cache_resource
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["SNOWFLAKE_ACCOUNT"],
        user=st.secrets["SNOWFLAKE_USER"],
        password=st.secrets["SNOWFLAKE_PASSWORD"],
        role=st.secrets["SNOWFLAKE_ROLE"],
        warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
        database=st.secrets["SNOWFLAKE_DATABASE"],
        schema=st.secrets["SNOWFLAKE_SCHEMA"],
    )

@st.cache_data(ttl=600)
def load_data():
    conn = get_connection()
    query = "SELECT * FROM SALES_DW.SALES.MART_DASHBOARD"
    df = pd.read_sql(query, conn)
    return df

df = load_data()

# ── Title ──────────────────────────────────────────────────
st.title("📊 Sales Analytics Dashboard")
st.markdown("Built with Python, Snowflake & dbt-style SQL transformations")

# ── KPI Cards ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['SALES'].sum():,.0f}")
col2.metric("Total Orders", f"{df['ORDER_ID'].nunique():,}")
col3.metric("Avg Order Value", f"${df['SALES'].mean():,.2f}")
col4.metric("Total Customers", f"{df['CUSTOMER_ID'].nunique():,}")

st.divider()

# ── Row 1: Monthly Trend + Region ─────────────────────────
c1, c2 = st.columns(2)

with c1:
    monthly = df.groupby(['YEAR', 'MONTH', 'MONTH_NAME'], as_index=False)['SALES'].sum()
    monthly = monthly.sort_values(['YEAR', 'MONTH'])
    monthly['PERIOD'] = monthly['MONTH_NAME'] + " " + monthly['YEAR'].astype(str)
    fig1 = px.line(monthly, x='PERIOD', y='SALES', title="📈 Monthly Sales Trend", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    region = df.groupby('REGION', as_index=False)['SALES'].sum().sort_values('SALES', ascending=False)
    fig2 = px.bar(region, x='REGION', y='SALES', title="🗺️ Region-wise Sales", color='REGION')
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Category + Segment ─────────────────────────────
c3, c4 = st.columns(2)

with c3:
    cat = df.groupby('CATEGORY', as_index=False)['SALES'].sum()
    fig3 = px.pie(cat, names='CATEGORY', values='SALES', title="📦 Category-wise Sales")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    seg = df.groupby('SEGMENT', as_index=False)['SALES'].sum()
    fig4 = px.bar(seg, x='SEGMENT', y='SALES', title="👥 Customer Segment Sales", color='SEGMENT')
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Top Products ───────────────────────────────────
top_products = (
    df.groupby('PRODUCT_NAME', as_index=False)['SALES']
    .sum()
    .sort_values('SALES', ascending=False)
    .head(10)
)
fig5 = px.bar(top_products, x='SALES', y='PRODUCT_NAME', orientation='h',
              title="🏆 Top 10 Products by Sales")
fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig5, use_container_width=True)

# ── Raw Data (optional view) ──────────────────────────────
with st.expander("🔍 View Raw Data"):
    st.dataframe(df.head(100))