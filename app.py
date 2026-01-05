# app.py
# Web App Streamlit: Sistem Pengolah Data IC50, LC50, EC50, dan Total Phenolic Content (TPC)
# Input DATA MANUAL (tanpa upload file)

import streamlit as st
import numpy as np



st.set_page_config(page_title="Pengolah Data Bioaktivitas", layout="wide")

st.title("🧪 Sistem Pengolah Data IC₅₀, LC₅₀, EC₅₀ & Total Phenolic Content (Input Manual)")

menu = st.sidebar.selectbox(
    "Pilih Jenis Analisis",
    ["IC50 / LC50 / EC50", "Total Phenolic Content (TPC)"]
)

# ==========================
# FUNGSI
# ==========================

def hitung_x50(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    # regresi linier manual (metode kuadrat terkecil)
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - a * sum_x) / n

    x50 = (50 - b) / a
    return x50, a, b

# ==========================
# IC50 / LC50 / EC50
# ==========================
if menu == "IC50 / LC50 / EC50":
    st.header("📊 Perhitungan IC₅₀ / LC₅₀ / EC₅₀ (Input Manual)")

    st.markdown("Masukkan **konsentrasi** dan **% efek** (inhibisi / mortalitas / respon)")

    n = st.number_input("Jumlah titik data", min_value=3, value=5)

    konsentrasi = []
    efek = []

    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            konsentrasi.append(st.number_input(f"Konsentrasi ke-{i+1}", key=f"x{i}"))
        with col2:
            efek.append(st.number_input(f"% Efek ke-{i+1}", key=f"y{i}"))

    if st.button("Hitung X50"):
        x50, a, b = hitung_x50(konsentrasi, efek)
        st.subheader("Hasil")
        st.write(f"Persamaan regresi: y = {a:.4f}x + {b:.4f}")
        st.success(f"Nilai IC₅₀ / LC₅₀ / EC₅₀ = {x50:.4f}")

# ==========================
# TOTAL PHENOLIC CONTENT
# ==========================
if menu == "Total Phenolic Content (TPC)":
    st.header("🧫 Perhitungan Total Phenolic Content (TPC) – Input Manual")

    st.markdown("Masukkan data **kurva standar asam galat**")

    n_std = st.number_input("Jumlah titik standar", min_value=3, value=5)

    kons_std = []
    abs_std = []

    for i in range(int(n_std)):
        col1, col2 = st.columns(2)
        with col1:
            kons_std.append(st.number_input(f"Konsentrasi standar ke-{i+1}", key=f"xs{i}"))
        with col2:
            abs_std.append(st.number_input(f"Absorbansi ke-{i+1}", key=f"ys{i}"))

    slope, intercept, r, p, se = linregress(kons_std, abs_std)

    st.subheader("Persamaan Kurva Standar")
    st.write(f"y = {slope:.4f}x + {intercept:.4f}")
    st.write(f"R² = {r**2:.4f}")

    st.subheader("Data Sampel")
    abs_sample = st.number_input("Absorbansi Sampel")
    dilution = st.number_input("Faktor Pengenceran", value=1.0)

    if st.button("Hitung TPC"):
        konsen = (abs_sample - intercept) / slope
        tpc = konsen * dilution
        st.success(f"Total Phenolic Content = {tpc:.4f} mg GAE/g")
