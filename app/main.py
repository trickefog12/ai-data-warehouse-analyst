import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page Config
st.set_page_config(page_title="AI Data Warehouse Analyst", layout="wide")

st.title("📊 AI Data Warehouse Analyst")
st.markdown("### Smart Inventory & Sales Insights")

# Sidebar for file upload
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload your warehouse CSV", type=["csv"])

# Default file if no upload
DEFAULT_FILE = "warehouse_data.csv"

def load_data(file):
    df = pd.read_csv(file)
    # Data Cleaning: Median Imputation for Units_Sold
    if 'Units_Sold' in df.columns:
        median_val = df['Units_Sold'].median()
        df['Units_Sold'] = df['Units_Sold'].fillna(median_val)
    
    # Logic: Calculate Revenue only for Shipped items
    if all(col in df.columns for col in ['Units_Sold', 'Unit_Price', 'Status']):
        df['Revenue'] = df.apply(
            lambda x: x['Units_Sold'] * x['Unit_Price'] if x['Status'] == 'Shipped' else 0, 
            axis=1
        )
    return df

# Trigger data loading
data_source = uploaded_file if uploaded_file else (DEFAULT_FILE if os.path.exists(DEFAULT_FILE) else None)

if data_source:
    df = load_data(data_source)
    
    # Layout: Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_rev = df['Revenue'].sum()
        st.metric("Total Revenue (Shipped)", f"${total_rev:,.2f}")
    with col2:
        shipped_count = len(df[df['Status'] == 'Shipped'])
        st.metric("Orders Shipped", shipped_count)
    with col3:
        avg_units = df['Units_Sold'].mean()
        st.metric("Avg Units per Order", f"{avg_units:.1f}")

    # Visualizations
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Revenue by Product")
        product_rev = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)
        st.bar_chart(product_rev)

    with c2:
        st.subheader("Order Status Distribution")
        status_counts = df['Status'].value_value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=status_counts.index, y=status_counts.values, ax=ax, palette="viridis")
        st.pyplot(fig)

    # Data Table
    st.markdown("---")
    st.subheader("Raw Data Preview")
    st.dataframe(df)
else:
    st.warning("Please upload a CSV file or ensure warehouse_data.csv exists.")