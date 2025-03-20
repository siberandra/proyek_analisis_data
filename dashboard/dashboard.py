import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Order", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard E-Commerce |  Analisis Order")




# Membaca dataset
customers_df = pd.read_csv("data/customers_dataset.csv")
orders_df = pd.read_csv("data/orders_dataset.csv")
payments_df = pd.read_csv("data/order_payments_dataset.csv")

# Menggabungkan dataset untuk analisis yang lebih komprehensif
df = orders_df.merge(payments_df, on="order_id", how="left")

# Konversi kolom tanggal ke format datetime
if "order_purchase_timestamp" in df.columns:
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_year"] = df["order_purchase_timestamp"].dt.year
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")

# Sidebar untuk filter tahun
st.sidebar.header("📌 Filter")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=["All"] + sorted(df["order_year"].dropna().unique()))

# Filter data berdasarkan tahun yang dipilih
df_filtered = df if selected_year == "All" else df[df["order_year"] == selected_year]

# 1️⃣ **Grafik Tren Jumlah Pesanan dari Waktu ke Waktu**
if "order_month" in df_filtered.columns:
    st.subheader("📈 Tren Jumlah Pesanan dari Waktu ke Waktu")

    # Menghitung jumlah pesanan per bulan
    order_trend = df_filtered.groupby("order_month").size().reset_index(name="jumlah_pesanan")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(order_trend["order_month"].astype(str), order_trend["jumlah_pesanan"], marker='o', linestyle='-')
    ax.set_xticklabels(order_trend["order_month"].astype(str), rotation=45)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan dari Waktu ke Waktu")
    ax.grid(True)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

# 2️⃣ **Metode Pembayaran Paling Sering Digunakan**
st.subheader("💳 Metode Pembayaran Paling Sering Digunakan")

# Menghitung jumlah transaksi per metode pembayaran
payment_counts = payments_df['payment_type'].value_counts()

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax, color='steelblue')

# Label
ax.set_title("Metode Pembayaran Paling Sering Digunakan")
ax.set_xlabel("Metode Pembayaran")
ax.set_ylabel("Jumlah Transaksi")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

# Tampilkan plot di Streamlit
st.pyplot(fig)

# 3️⃣ **Top 10 Users with Highest Spending**
st.subheader("👑 Top 10 Users with Highest Spending")

# Menghitung total pengeluaran per pelanggan
top_users = df.groupby("customer_id")["payment_value"].sum().reset_index()
top_users = top_users.sort_values(by="payment_value", ascending=False).head(10)

# Visualisasi
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="payment_value", y="customer_id", data=top_users, palette="viridis", ax=ax)

# Label dan judul
ax.set_xlabel("Total Spent (USD)")
ax.set_ylabel("Customer ID")
ax.set_title("Top 10 Users with Highest Spending")
ax.invert_yaxis()  # Supaya pelanggan dengan pengeluaran tertinggi ada di atas

# Tampilkan plot di Streamlit
st.pyplot(fig)

# Copyright
st.sidebar.markdown("📊 ©DBS Dicoding 2025 | Made by **Vicky Chandra**")
