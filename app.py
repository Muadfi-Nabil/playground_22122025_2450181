import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bioassay Analyzer", layout="centered")

st.title("🧪 Bioassay Data Analyzer")
st.caption("IC50 | EC50 | LC50 | Total Phenolic Content")

menu = st.sidebar.selectbox(
    "Pilih Jenis Analisis",
    ["IC50 / EC50 / LC50", "Total Phenolic Content"]
)

# =====================================================
# IC50 / EC50 / LC50
# =====================================================
if menu == "IC50 / EC50 / LC50":
    st.subheader("📊 Analisis IC50 / EC50 / LC50")

    file = st.file_uploader("Upload file CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write("📁 Data yang diunggah")
        st.dataframe(df)

        x = df.iloc[:, 0].values  # Konsentrasi
        y = df.iloc[:, 1].values  # Respon (%)

        target = 50
        ic50 = np.interp(target, y, x)

        st.success(f"🎯 Nilai IC50 / EC50 / LC50 = **{ic50:.2f}**")

        # ===== Grafik =====
        fig, ax = plt.subplots()
        ax.plot(x, y, 'o-', label="Data Eksperimen")
        ax.axhline(50, linestyle='--', label="50% Respon")
        ax.axvline(ic50, linestyle='--', label=f"IC50 = {ic50:.2f}")
        ax.set_xlabel("Konsentrasi")
        ax.set_ylabel("Respon (%)")
        ax.set_title("Kurva IC50 / EC50 / LC50")
        ax.legend()

        st.pyplot(fig)

        # ===== Interpretasi =====
        if ic50 < 50:
            st.info("🔬 Aktivitas **SANGAT KUAT**")
        elif ic50 < 100:
            st.info("🔬 Aktivitas **KUAT**")
        else:
            st.info("🔬 Aktivitas **LEMAH**")

# =====================================================
# TOTAL PHENOLIC CONTENT
# =====================================================
if menu == "Total Phenolic Content":
    st.subheader("🌿 Total Phenolic Content (TPC)")

    file = st.file_uploader("Upload data kurva standar (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write("📁 Data Kurva Standar")
        st.dataframe(df)

        x = df.iloc[:, 0].values  # Konsentrasi standar
        y = df.iloc[:, 1].values  # Absorbansi

        # Regresi linier
        a, b = np.polyfit(x, y, 1)

        st.write(f"📐 Persamaan regresi: **y = {a:.4f}x + {b:.4f}**")

        Abs_sample = st.number_input("Absorbansi Sampel", value=0.500)
        V = st.number_input("Volume ekstrak (mL)", value=10.0)
        m = st.number_input("Berat sampel (g)", value=0.1)

        C = (Abs_sample - b) / a
        TPC = (C * V) / m

        st.success(f"🌿 TPC = **{TPC:.2f} mg GAE/g sampel**")

        # ===== Grafik =====
        fig, ax = plt.subplots()
        ax.scatter(x, y, label="Data Standar")
        ax.plot(x, a * x + b, label="Regresi Linier")
        ax.set_xlabel("Konsentrasi Asam Galat (ppm)")
        ax.set_ylabel("Absorbansi")
        ax.set_title("Kurva Standar Total Fenolik")
        ax.legend()

        st.pyplot(fig)
