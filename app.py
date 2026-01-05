# =============================================
# FUTURISTIC IC50 / LC50 / EC50 ANALYSIS WEB APP
# Streamlit-based Scientific Software
# =============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import hashlib

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="BioAssay Analyzer",
    page_icon="🧬",
    layout="wide"
)

# -------------------------------
# SIMPLE AUTH SYSTEM
# -------------------------------
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "researcher": hashlib.sha256("lab456".encode()).hexdigest()
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def login():
    st.markdown("## 🔐 Login Sistem")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in USERS and hashlib.sha256(pwd.encode()).hexdigest() == USERS[user]:
            st.session_state.authenticated = True
            st.success("Login berhasil")
        else:
            st.error("Username atau password salah")


if not st.session_state.authenticated:
    login()
    st.stop()

# -------------------------------
# HEADER UI
# -------------------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#00FFD1;'>🧬 BioAssay Futuristic Analyzer</h1>
    <p style='text-align:center;color:gray;'>IC50 • LC50 • EC50 Data Processing Software</p>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Analisis")
    assay_type = st.selectbox("Jenis Analisis", ["IC50", "LC50", "EC50"])
    response_type = st.selectbox("Tipe Respon", ["% Inhibisi", "% Mortalitas", "% Efek"])
    st.markdown("---")
    st.markdown("📈 Model: Regresi Linier")

# -------------------------------
# DATA INPUT
# -------------------------------
st.markdown("## 📥 Input Data")

uploaded = st.file_uploader("Upload data (CSV)", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.DataFrame({
        "Konsentrasi": [1, 5, 10, 25, 50, 100],
        "Respon": [5, 12, 28, 55, 72, 90]
    })

st.dataframe(df, use_container_width=True)

# -------------------------------
# REGRESSION & CALCULATION
# -------------------------------
X = df[["Konsentrasi"]].values
Y = df["Respon"].values

model = LinearRegression()
model.fit(X, Y)

slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, Y)

# IC50 / LC50 / EC50 calculation
TARGET = 50
value_50 = (TARGET - intercept) / slope

# -------------------------------
# RESULTS
# -------------------------------
st.markdown("## 📊 Hasil Analisis")

col1, col2, col3 = st.columns(3)
col1.metric("Slope", f"{slope:.4f}")
col2.metric("Intercept", f"{intercept:.4f}")
col3.metric("R²", f"{r2:.4f}")

st.success(f"🎯 Nilai {assay_type} = {value_50:.3f}")

# -------------------------------
# PLOT
# -------------------------------
st.markdown("## 📈 Kurva Regresi")

x_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_line = model.predict(x_line)

fig, ax = plt.subplots()
ax.scatter(X, Y)
ax.plot(x_line, y_line)
ax.axhline(50)
ax.axvline(value_50)
ax.set_xlabel("Konsentrasi")
ax.set_ylabel(response_type)
ax.set_title(f"Kurva Regresi {assay_type}")

st.pyplot(fig)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>Developed for Scientific & Pharmaceutical Data Analysis</p>",
    unsafe_allow_html=True
)
