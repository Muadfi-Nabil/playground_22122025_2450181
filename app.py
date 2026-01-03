import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bioassay Analyzer", layout="centered")

st.title("🧪 Bioassay Data Analyzer")
st.write("IC50 | EC50 | LC50 | Total Phenolic Content")

menu = st.sidebar.selectbox(
    "Pilih Analisis",
    ["IC50 / EC50 / LC50", "Total Phenolic Content"]
)

# ================= IC50 / EC50 / LC50 =================
if menu == "IC50 / EC50 / LC50":
    st.subheader("📊 Analisis IC50 / EC50 / LC50")

    file = st.file_uploader("Upload file CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values

        target = 50

        ic50 = np.interp(target, y, x)

        st.success(f"🎯 Nilai IC50 / EC50 / LC50 = **{ic50:.2f}**")

        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o')
        ax.axhline(50, linestyle='--')
        ax.axvline(ic50, linestyle='--')
        ax.set_xlabel("Konsentrasi")
        ax.set_ylabel("Respon (%)")
        ax.set_title("Kurva Bioassay")

        st.pyplot(fig)

        if ic50 < 50:
            st.info("🔬 Aktivitas **SANGAT KUAT**")
        elif ic50 < 100:
            st.info("🔬 Aktivitas **KUAT**")
        else:
            st.info("🔬 Aktivitas **LEMAH**")

# ================= TPC =================
if menu == "Total Phenolic Content":
    st.subheader("🌿 Total Phenolic Content (TPC)")

    file = st.file_uploader("Upload data kurva standar (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values

        coef = np.polyfit(x, y, 1)
        a, b = coef

        st.write(f"📈 Persamaan regresi: **y = {a:.4f}x + {b:.4f}**")

        Abs_sample = st.number_input("Absorbansi Sampel", value=0.500)
        V = st.number_input("Volume ekstrak (mL)", value=10.0)
        m = st.number_input("Berat sampel (g)", value=0.1)

        C = (Abs_sample - b) / a
        TPC = (C * V) / m

        st.success(f"🌿 TPC = **{TPC:.2f} mg GAE/g sampel**")

        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.plot(x, a*x + b)
        ax.set_xlabel("Konsentrasi (ppm)")
        ax.set_ylabel("Absorbansi")
        ax.set_title("Kurva Standar Asam Galat")

        st.pyplot(fig)
