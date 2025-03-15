import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Order", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis Order")

# Membaca dataset langsung dari file
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

# Menampilkan preview data
st.subheader("📂 DataFrame Preview")
st.dataframe(df.head())

# Menampilkan summary statistik
st.subheader("📊 Summary Statistics")
st.write(df.describe())

# Grafik 1: Histogram jumlah order per bulan
if "order_month" in df.columns:
    st.subheader("📆 Order Distribution Per Month")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["order_month"].astype(str), bins=20, kde=True, ax=ax, color="blue")
    plt.xticks(rotation=45)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Order")
    ax.set_title("Distribusi Order per Bulan")
    st.pyplot(fig)

# Grafik 2: Bar Chart jumlah order berdasarkan status
if "order_status" in df.columns:
    st.subheader("📦 Order Status Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=df["order_status"], palette="viridis", ax=ax)
    ax.set_xlabel("Status Order")
    ax.set_ylabel("Jumlah Order")
    ax.set_title("Distribusi Status Order")
    st.pyplot(fig)

# Grafik 3: Line Chart jumlah order per tahun menggunakan Plotly
if "order_year" in df.columns:
    st.subheader("📈 Jumlah Order per Tahun (Plotly)")
    order_per_year = df.groupby("order_year").size().reset_index(name="count")
    fig = px.line(order_per_year, x="order_year", y="count", markers=True, title="Tren Order per Tahun")
    st.plotly_chart(fig)
