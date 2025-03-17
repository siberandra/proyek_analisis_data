import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Order", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis Order")

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
st.sidebar.header("Filter")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=["All Dates"] + sorted(df["order_year"].dropna().unique()))

# Filter data berdasarkan tahun yang dipilih
if selected_year != "All Dates":
    df_filtered = df[df["order_year"] == selected_year]
else:
    df_filtered = df

# Grafik Tren Jumlah Pesanan dari Waktu ke Waktu
if "order_month" in df_filtered.columns:
    st.subheader("📈 Tren Jumlah Pesanan dari Waktu ke Waktu")

    # Menghitung jumlah pesanan per bulan
    order_trend = df_filtered.groupby("order_month").size().reset_index(name="jumlah_pesanan")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(order_trend["order_month"].astype(str), order_trend["jumlah_pesanan"], marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    plt.title("Tren Jumlah Pesanan dari Waktu ke Waktu")
    plt.grid(True)

    # Menampilkan plot
    st.pyplot(fig)

# Data transaksi metode pembayaran
payment_methods = ['credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined']
transaction_counts = [77000, 20000, 7000, 3000, 1000]

# Membuat plot
plt.figure(figsize=(8, 6))
sns.barplot(x=payment_methods, y=transaction_counts, color='steelblue')

# Memberi judul dan label
plt.title('Metode Pembayaran Paling Sering Digunakan')
plt.xlabel('Metode Pembayaran')
plt.ylabel('Jumlah Transaksi')

# Rotasi label x agar miring
plt.xticks(rotation=30)

# Menampilkan plot
plt.show()


# Memberi judul dan label
plt.title('Metode Pembayaran Paling Sering Digunakan')
plt.xlabel('Metode Pembayaran')
plt.ylabel('Jumlah Transaksi')

# Rotasi label x agar miring
plt.xticks(rotation=30)

# Menampilkan plot
st.pyplot(plt)
