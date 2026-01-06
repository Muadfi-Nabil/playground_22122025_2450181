import streamlit as st
import numpy as np
import pandas as pd
import math

st.set_page_config("Sistem Pengolah Data Bioaktivitas", layout="wide")

# =========================
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =========================
# FUNGSI REGRESI LINIER
# =========================
def regresi_linier(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)

    a = (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / \
        (n*np.sum(x**2) - (np.sum(x))**2)

    b = (np.sum(y) - a*np.sum(x)) / n
    return a, b

def klasifikasi_ic50(x):
    if x < 50:
        return "Sangat kuat"
    elif x < 100:
        return "Kuat"
    elif x < 150:
        return "Sedang"
    elif x <= 200:
        return "Lemah"
    else:
        return "Sangat lemah / Tidak aktif"

def mortalitas_ke_probit(p):
    tabel = [
        (1,3.72),(5,4.36),(10,4.72),(20,5.16),(30,5.52),
        (40,5.84),(50,5.00),(60,6.16),(70,6.48),(80,6.84),
        (90,7.28),(95,7.64),(99,8.09)
    ]
    for i in range(len(tabel)-1):
        if tabel[i][0] <= p <= tabel[i+1][0]:
            return tabel[i][1]
    return tabel[-1][1]

# =========================
# LOGIN
# =========================
if not st.session_state.login:
    st.title("🔐 Login Sistem Bioaktivitas")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.login = True
            st.success("Login berhasil")
            st.experimental_rerun()
        else:
            st.error("Login gagal")
    st.stop()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "Menu",
    ["Home", "IC50 / EC50", "LC50 (Probit)", "TPC", "Riwayat", "Logout"]
)

# =========================
# HOME
# =========================
if menu == "Home":
    st.title("🧪 Sistem Pengolah Data Bioaktivitas")
    st.markdown("""
    **Fitur Analisis:**
    - IC₅₀ / EC₅₀ (regresi linier)
    - LC₅₀ metode Probit
    - Total Phenolic Content (TPC)
    """)

# =========================
# IC50 / EC50
# =========================
if menu == "IC50 / EC50":
    st.header("IC₅₀ / EC₅₀ (mg/L)")
    n = st.number_input("Jumlah titik data", min_value=3, value=5)

    x, y = [], []
    for i in range(int(n)):
        c1, c2 = st.columns(2)
        x.append(c1.number_input(f"Konsentrasi {i+1} (mg/L)", min_value=0.0))
        y.append(c2.number_input(f"% Efek {i+1}", min_value=0.0, max_value=100.0))

    if st.button("Hitung IC50"):
        a, b = regresi_linier(x, y)

        if a == 0:
            st.error("Regresi tidak valid (gradien = 0)")
            st.stop()

        ic50 = (50 - b) / a
        kategori = klasifikasi_ic50(ic50)

        df = pd.DataFrame({
            "Konsentrasi (mg/L)": x,
            "% Efek": y
        })

        st.line_chart(df.set_index("Konsentrasi (mg/L)"))
        st.success(f"IC₅₀ = {ic50:.4f} mg/L")
        st.info(f"Kategori: {kategori}")

        st.session_state.riwayat.append({
            "Jenis": "IC50",
            "Nilai": round(ic50, 4),
            "Satuan": "mg/L",
            "Kategori": kategori
        })

# =========================
# LC50 PROBIT
# =========================
if menu == "LC50 (Probit)":
    st.header("LC₅₀ Metode Probit")
    n = st.number_input("Jumlah titik data", min_value=3, value=5)

    kons, mati, total = [], [], []
    for i in range(int(n)):
        c1, c2, c3 = st.columns(3)
        kons.append(c1.number_input(f"Konsentrasi {i+1} (mg/L)", min_value=0.001))
        mati.append(c2.number_input(f"Jumlah mati {i+1}", min_value=0, step=1))
        total.append(c3.number_input(f"Total {i+1}", min_value=1))

    if st.button("Proses Probit"):
        persen = []
        for i in range(int(n)):
            p = (mati[i] / total[i]) * 100
            if p == 0:
                p = 0.25
            elif p == 100:
                p = 99.75
            persen.append(p)

        logk = [math.log10(k) for k in kons]
        prob = [mortalitas_ke_probit(p) for p in persen]

        df_probit = pd.DataFrame({
            "Konsentrasi (mg/L)": kons,
            "Log Konsentrasi": logk,
            "Jumlah Mati": mati,
            "Jumlah Total": total,
            "% Mortalitas": persen,
            "Nilai Probit": prob
        })

        st.subheader("Tabel Probit")
        st.table(df_probit.round(4))
        st.line_chart(df_probit.set_index("Log Konsentrasi")["Nilai Probit"])

        a, b = regresi_linier(logk, prob)
        lc50 = 10 ** ((5 - b) / a)

        st.success(f"LC₅₀ = {lc50:.4f} mg/L")

        st.session_state.riwayat.append({
            "Jenis": "LC50",
            "Nilai": round(lc50, 4),
            "Satuan": "mg/L",
            "Kategori": "-"
        })

# =========================
# TPC
# =========================
if menu == "TPC":
    st.header("Total Phenolic Content (mg GAE/g)")
    n = st.number_input("Jumlah titik standar", min_value=3, value=5)

    xs, ys = [], []
    for i in range(int(n)):
        c1, c2 = st.columns(2)
        xs.append(c1.number_input(f"Konsentrasi standar {i+1} (mg/L)"))
        ys.append(c2.number_input(f"Absorbansi {i+1}"))

    if st.button("Buat Kurva Standar"):
        a, b = regresi_linier(xs, ys)
        st.session_state.a = a
        st.session_state.b = b

        df = pd.DataFrame({
            "Konsentrasi (mg/L)": xs,
            "Absorbansi": ys
        })

        st.line_chart(df.set_index("Konsentrasi (mg/L)"))
        st.success(f"Persamaan: A = {a:.4f}C + {b:.4f}")

    if "a" in st.session_state:
        abs_s = st.number_input("Absorbansi sampel")
        vol = st.number_input("Volume (mL)", value=1.0)
        fp = st.number_input("Faktor pengenceran", value=1.0)
        m = st.number_input("Massa sampel (g)", value=1.0)

        if st.button("Hitung TPC"):
            c = ((abs_s - st.session_state.b) / st.session_state.a) / 1000
            tpc = (c * vol * fp) / m
            st.success(f"TPC = {tpc:.4f} mg GAE/g")

            st.session_state.riwayat.append({
                "Jenis": "TPC",
                "Nilai": round(tpc, 4),
                "Satuan": "mg GAE/g",
                "Kategori": "-"
            })

# =========================
# RIWAYAT
# =========================
if menu == "Riwayat":
    if st.session_state.riwayat:
        st.table(pd.DataFrame(st.session_state.riwayat))
    else:
        st.warning("Belum ada data")

# =========================
# LOGOUT
# =========================
if menu == "Logout":
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Anda telah logout")
    st.stop()
