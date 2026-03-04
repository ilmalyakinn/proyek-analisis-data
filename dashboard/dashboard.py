import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import function as func
from PIL import Image

sns.set(style='dark')

# ==============================================================================
# READ & PREPARE DATA
# ==============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    
    # Casting datetime columns
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])
        
    # Sort by date
    df.sort_values(by="order_purchase_timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

all_df = load_data()


# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    
    # Mengambil minimum dan maksimum tanggal dari dataset
    min_date = all_df["order_purchase_timestamp"].dt.date.min()
    max_date = all_df["order_purchase_timestamp"].dt.date.max()
    
    # Input rentang tanggal dari user
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Tanggal Input Users
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]


# ==============================================================================
# PREPARE DATAFRAME
# ==============================================================================
# Data Ekstrak Dari function.py sebelumnya
daily_orders_df = func.create_daily_orders_df(main_df)
sum_order_items_df = func.create_sum_order_items_df(main_df)
revenue_by_price_df = func.create_revenue_by_price_df(main_df)
bystate_df = func.create_bystate_df(main_df)
rfm_df = func.create_rfm_df(main_df)


# ==============================================================================
# DASHBOARD MAIN PAGE/BODY
# ==============================================================================

st.header('E-Commerce Public Dataset Dashboard 🛒')

# ----- Tren Penjualan Harian -----
st.subheader('Order Tertinggi Harian')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Order", value=total_orders)

with col2:
    total_revenue = daily_orders_df.revenue.sum()
    st.metric("Total Revenue ($)", value=f"{total_revenue:,.2f}")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


# ----- PERTANYAAN BISNIS 1 -----
st.subheader("Pertanyaan 1: Performa Penjualan & Revenue Kategori")

col1, col2 = st.columns(2)

# Sub-plot 1: Top 5 Kategori
with col1:
    st.write("#### Top 5 Kategori Produk Paling Laris")
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="jumlah_terjual", 
        y="product_category_name_english",
        data=sum_order_items_df.head(5),
        palette=colors,
        ax=ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

# Sub-plot 2: Revenue By Price
with col2:
    st.write("#### Pendapatan (Revenue) By Rentang Harga")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="price_category", 
        y="price", 
        data=revenue_by_price_df, 
        palette="magma", 
        ax=ax
    )
    ax.set_ylabel("Total Pendapatan", fontsize=20)
    ax.set_xlabel("Rentang Harga", fontsize=20)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)


# ----- PERTANYAAN BISNIS 2 & 3 -----
col3, col4 = st.columns(2)

with col3:
    # PERTANYAAN BISNIS 2: Total Pengeluaran
    st.subheader("Pertanyaan 2: Pengeluaran Per Pelanggan")
    avg_spend = round(main_df.groupby('customer_unique_id')['price'].sum().mean(), 2)
    st.metric(label="Rata-rata Pengeluaran Per Pelanggan", value=f"${avg_spend:,.2f}")
    
    st.write("Distribusi (Capped < $1000):")
    # visualisasi distribusi seperti yang dilakukan di notebook
    customer_spend = main_df.groupby('customer_unique_id')['price'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter under 1000 untuk tampilan yang lbh bagus
    filtered_spend = customer_spend[customer_spend['price'] < 1000]
    
    sns.histplot(filtered_spend['price'], bins=50, kde=True, color='blue', ax=ax)
    ax.axvline(avg_spend, color='red', linestyle='dashed', linewidth=2, label=f"Mean: ${avg_spend}")
    ax.set_xlabel('Total Spend ($)')
    ax.set_ylabel('Freekuensi')
    ax.legend()
    st.pyplot(fig)
    

with col4:
    # PERTANYAAN BISNIS 3: State Terbanyak
    st.subheader("Pertanyaan 3: Geografi Pelanggan (Top 5 State)")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors2 = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        x="customer_count", 
        y="customer_state", 
        data=bystate_df.head(5), 
        palette=colors2, 
        ax=ax
    )
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)


# ----- RFM ANALYSIS Lanjutan -----
st.subheader("Best Customer Based on RFM Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = round(rfm_df.monetary.mean(), 2)
    st.metric("Average Monetary ($)", value=f"${avg_frequency:,.2f}")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='x', rotation=45, labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='x', rotation=45, labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='x', rotation=45, labelsize=30)
ax[2].tick_params(axis='y', labelsize=30)

st.pyplot(fig)

st.caption("Copyright © Ilmal Yakin Nurahman - 2026")
