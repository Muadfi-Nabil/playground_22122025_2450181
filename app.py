import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

st.set_page_config(page_title="Advanced Bioassay Analyzer", layout="wide")

st.title("🧪 Advanced Bioassay & Phenolic Analyzer")
st.write("IC50 | EC50 | LC50 (4PL) + Total Phenolic Content")

menu = st.sidebar.selectbox(
    "Pilih Analisis",
    ["IC50 / EC50 / LC50 (4PL)", "Total Phenolic Content (TPC)"]
)

# =========================
# 4PL FUNCTION
# =========================
def four_pl(x, a, b, c, d):
    return d + (a - d) / (1 + (x / c)**b)

# =========================
# IC50 / EC50 / LC50
# =========================
if menu == "IC50 / EC50 / LC50 (4PL)":
    st.subheader("📊 IC50 / EC50 / LC50 – Model Logistik 4 Parameter")

    file = st.file_uploader("Upload data bioassay (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        x = df["Concentration"].values
        y = df["Response"].values

        log_x = np.log10(x)

        p0 = [min(y), 1, np.median(x), max(y)]

        params, _ = curve_fit(four_pl, x, y, p0=p0, maxfev=10000)
        a, b, c, d = params

        y_pred = four_pl(x, *params)
        r2 = r2_score(y, y_pred)

        st.success(f"🎯 IC50 / EC50 / LC50 = **{c:.3f}**")
        st.write(f"📈 R² = **{r2:.4f}**")

        st.markdown("### 🔍 Parameter Model")
        st.write(f"- a (min response) = {a:.2f}")
        st.write(f"- b (Hill slope) = {b:.2f}")
        st.write(f"- c (IC50/EC50/LC50) = {c:.3f}")
        st.write(f"- d (max response) = {d:.2f}")

        fig, ax = plt.subplots()
        x_fit = np.logspace(np.log10(min(x)), np.log10(max(x)), 100)
        y_fit = four_pl(x_fit, *params)

        ax.scatter(x, y, label="Data Eksperimen")
        ax.plot(x_fit, y_fit, label="Kurva 4PL")
        ax.axhline(50, linestyle="--")
        ax.axvline(c, linestyle="--")

        ax.set_xscale("log")
        ax.set_xlabel("Konsentrasi (log)")
        ax.set_ylabel("Respon (%)")
        ax.set_title("Kurva IC50 / EC50 / LC50 (4PL)")
        ax.legend()

        st.pyplot(fig)

        if c < 50:
            st.info("🔬 Aktivitas **SANGAT KUAT**")
        elif c < 100:
            st.info("🔬 Aktivitas **KUAT**")
        else:
            st.info("🔬 Aktivitas **LEMAH**")

# =========================
# TPC
# =========================
if menu == "Total Phenolic Content (TPC)":
    st.subheader("🌿 Total Phenolic Content (Metode Folin–Ciocalteu)")

    file = st.file_uploader("Upload kurva standar asam galat (CSV)", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        x = df["Concentration"].values
        y = df["Absorbance"].values

        coef = np.polyfit(x, y, 1)
        a, b = coef

        y_pred = a*x + b
        r2 = r2_score(y, y_pred)

        st.write(f"📈 Persamaan: **y = {a:.5f}x + {b:.5f}**")
        st.write(f"📊 R² = **{r2:.4f}**")

        Abs_sample = st.number_input("Absorbansi Sampel", value=0.500)
        V = st.number_input("Volume ekstrak (mL)", value=10.0)
        DF = st.number_input("Faktor pengenceran", value=1.0)
        m = st.number_input("Berat sampel (g)", value=0.1)

        C = (Abs_sample - b) / a
        TPC = (C * V * DF) / m

        st.success(f"🌿 TPC = **{TPC:.2f} mg GAE/g sampel**")

        fig, ax = plt.subplots()
        ax.scatter(x, y, label="Data Standar")
        ax.plot(x, y_pred, label="Regresi Linier")
        ax.set_xlabel("Konsentrasi Asam Galat (ppm)")
        ax.set_ylabel("Absorbansi")
        ax.set_title("Kurva Standar Asam Galat")
        ax.legend()

        st.pyplot(fig)
