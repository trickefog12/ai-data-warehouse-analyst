# app/main.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import subprocess
import sys
import os

# === CONFIGURATION === #
st.set_page_config(page_title="Warehouse Analytics Dashboard", layout="wide")
DATA_FILENAME = "warehouse_data.csv"
GENERATE_SCRIPT = "generate_data.py"


# === DATA LOADING LOGIC === #
@st.cache_data
def load_data(file_obj=None):
    """Load data from uploaded file or fallback to local CSV."""
    if file_obj:
        df = pd.read_csv(file_obj)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df

    # Fallback path logic
    root = Path(__file__).resolve().parent.parent
    data_path = root / DATA_FILENAME
    gen_script = root / GENERATE_SCRIPT

    # If CSV exists, load it
    if data_path.exists():
        df = pd.read_csv(data_path)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df

    # Else try to generate it
    elif gen_script.exists():
        try:
            subprocess.run([sys.executable, str(gen_script)], check=True)
            if data_path.exists():
                df = pd.read_csv(data_path)
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                return df
        except Exception as e:
            st.error(f"Failed to generate {DATA_FILENAME}: {e}")
    
    st.warning("No data available. Please upload a file.")
    return pd.DataFrame()


# === CLEANING & TRANSFORMATIONS === #
def process_data(df):
    # Fill missing Units_Sold with median
    if 'Units_Sold' in df.columns:
        median_val = df['Units_Sold'].median()
        df['Units_Sold'] = df['Units_Sold'].fillna(median_val)

    # Compute Revenue only for Shipped items
    if all(col in df.columns for col in ['Units_Sold', 'Unit_Price', 'Status']):
        df['Revenue'] = np.where(
            df['Status'] == 'Shipped',
            df['Units_Sold'] * df['Unit_Price'],
            0
        )
    return df


# === UI STARTS HERE === #
st.title("📊 Warehouse Analytics Dashboard")
st.markdown("""
> Interactive business intelligence tool for warehouse inventory tracking and revenue insights.
""")

# Load data
uploaded_file = st.sidebar.file_uploader("📁 Upload your warehouse CSV", type=["csv"])
df_raw = load_data(uploaded_file)

if df_raw.empty:
    st.stop()

df = process_data(df_raw.copy())

# Sidebar Filters
st.sidebar.header("🔍 Filters")
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
selected_dates = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Ensure tuple
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    (df["Date"] >= pd.Timestamp(start_date)) &
    (df["Date"] <= pd.Timestamp(end_date))
]

# Product Filter
selected_products = st.sidebar.multiselect(
    "📦 Products",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)
filtered_df = filtered_df[filtered_df["Product"].isin(selected_products)]

# Status Filter
selected_status = st.sidebar.multiselect(
    "🏷️ Order Status",
    options=df["Status"].unique(),
    default=df["Status"].unique()
)
filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]

# === METRICS === #
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    total_rev = filtered_df["Revenue"].sum()
    st.metric("💰 Total Revenue (Shipped)", f"${total_rev:,.2f}")
with col2:
    shipped_orders = len(filtered_df[filtered_df["Status"] == "Shipped"])
    st.metric("📦 Orders Shipped", shipped_orders)
with col3:
    avg_units = filtered_df["Units_Sold"].mean()
    st.metric("📉 Avg Units per Order", f"{avg_units:.1f}")

# === CHARTS === #
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Revenue by Product")
    rev_by_product = filtered_df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    st.bar_chart(rev_by_product)

with c2:
    st.subheader("📊 Order Status Distribution")
    status_counts = filtered_df["Status"].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=status_counts.index, y=status_counts.values, palette="viridis", ax=ax)
    ax.set_ylabel("Count")
    ax.set_xlabel("Status")
    st.pyplot(fig)

# === TABLE === #
st.markdown("---")
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

# Download Button
st.download_button(
    label="📥 Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_warehouse_data.csv",
    mime="text/csv"
)