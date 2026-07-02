import pandas as pd
import os

# ── Paths (hardcoded, no pathlib) ─────────────────────────
RAW  = r"C:\Users\laxmi sahu\OneDrive\Documents\Sales analytics project\data\train.csv"
SAVE = r"C:\Users\laxmi sahu\Downloads\sales_cleaned.csv"
# ── 1. Load ───────────────────────────────────────────────
df = pd.read_csv(RAW, encoding='latin-1')
print(f"✅ Loaded  → {df.shape[0]} rows, {df.shape[1]} cols")

# ── 2. Drop useless columns ───────────────────────────────
df.drop(columns=['Row ID'], inplace=True)

# ── 3. Fix date columns ───────────────────────────────────
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

# ── 4. Handle nulls ───────────────────────────────────────
df['Postal Code'] = df['Postal Code'].fillna(0).astype('Int64')

# ── 5. Fix column name ────────────────────────────────────
df.rename(columns={'Sub-Category': 'Sub_Category'}, inplace=True)

# ── 6. Add calculated columns ─────────────────────────────
df['Year']         = df['Order Date'].dt.year
df['Month']        = df['Order Date'].dt.month
df['Month_Name']   = df['Order Date'].dt.strftime('%B')
df['Quarter']      = df['Order Date'].dt.quarter.map({1:'Q1',2:'Q2',3:'Q3',4:'Q4'})
df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

# ── 7. Clean column names ─────────────────────────────────
df.columns = df.columns.str.strip().str.replace(' ', '_').str.upper()

# ── 8. Data Quality Report ────────────────────────────────
print(f"✅ Cleaned → {df.shape[0]} rows, {df.shape[1]} cols")
print(f"\n📋 Columns:\n{df.columns.tolist()}")
print(f"\n🔍 Null values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\n📊 Sales stats:\n{df['SALES'].describe().round(2)}")
print(f"\n📅 Date range: {df['ORDER_DATE'].min().date()} → {df['ORDER_DATE'].max().date()}")
print(f"\n🗺️  Regions: {df['REGION'].unique().tolist()}")
print(f"📦 Categories: {df['CATEGORY'].unique().tolist()}")

# ── 9. Save ───────────────────────────────────────────────
df.to_csv(SAVE, index=False)
print(f"\n✅ File saved → {SAVE}")