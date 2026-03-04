import pandas as pd

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={"order_id": "jumlah_terjual"}, inplace=True)
    return sum_order_items_df

def create_revenue_by_price_df(df):
    # Mengategorikan harga
    df['price_category'] = pd.cut(df['price'], bins=[0, 50, 150, 500, 10000], labels=['Low (<50)', 'Medium (50-150)', 'High (150-500)', 'Premium (>500)'])
    revenue_by_price = df.groupby('price_category')['price'].sum().reset_index()
    return revenue_by_price

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_unique_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_unique_id": "customer_count"
    }, inplace=True)
    return bystate_df.sort_values(by='customer_count', ascending=False)

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max", # Mengambil tanggal order terakhir
        "order_id": "nunique", # Menghitung jumlah order
        "price": "sum" # Menghitung total revenue yang dihasilkan
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    # Menghitung kapan terakhir pelanggan melakukan transaksi (hari)
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max() + pd.Timedelta(days=1)
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df
