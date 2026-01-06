import streamlit as st
import numpy as np
import pandas as pd
import math

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Penentuan Nilai Probit",
    layout="wide"
)

# =====================================================
# BACKGROUND & UI
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,
        rgba(210,240,220,0.55),
        rgba(200,230,255,0.55)
    );
    background-attachment: fixed;
}
.block-container {
    background: rgba(255,255,255,0.88);
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
}
.logo {
    font-size: 72px;
    text-align: center;
}
.app-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #2f5d50;
}
.subtitle {
    text-align: center;
    color: #4f6f68;
}
.stButton > button {
    background: linear-gradient(90deg,#4CAF50,#66BB6A);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "login" not in st.session_state:
    st.session_state.login = False
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =====================================================
# PROBIT TABLE (FINNEY)
# =====================================================
PROBIT_TABLE = {
    1:{0:2.67,1:2.95,2:3.12,3:3.25,4:3.36,5:3.45,6:3.52,7:3.58,8:3.59,9:3.66},
    10:{0:3.72,1:3.77,2:3.82,3:3.87,4:3.92,5:3.96,6:4.01,7:4.05,8:4.08,9:4.12},
    20:{0:4.16,1:4.19,2:4.23,3:4.26,4:4.29,5:4.33,6:4.36,7:4.39,8:4.42,9:4.45},
    30:{0:4.48,1:4.50,2:4.53,3:4.56,4:4.59,5:4.61,6:4.64,7:4.67,8:4.69,9:4.72},
    40:{0:4.75,1:4.77,2:4.80,3:4.82,4:4.85,5:4.87,6:4.90,7:4.92,8:4.95,9:4.97},
    50:{0:5.00,1:5.03,2:5.05,3:5.08,4:5.10,5:5.13,6:5.15,7:5.18,8:5.20,9:5.23},
    60:{0:5.25,1:5.28,2:5.31,3:5.33,4:5.36,5:5.39,6:5.41,7:5.44,8:5.47,9:5.50},
    70:{0:5.52,1:5.55,2:5.58,3:5.61,4:5.64,5:5.67,6:5.71,7:5.74,8:5.77,9:5.81},
    80:{0:5.84,1:5.88,2:5.92,3:5.95,4:5.99,5:6.04,6:6.08,7:6.13,8:6.18,9:6.23},
    90:{0:6.28,1:6.34,2:6.41,3:6.48,4:6.55,5:6.63,6:6.71,7:6.80,8:6.89,9:6.98},
    99:{0:7.33,1:7.37,2:7.41,3:7.46,4:7.51,5:7.58,6:7.65,7:7.72,8:7.88,9:8.09}
}

# =====================================================
# FUNGSI
# =====================================================
def mortalitas_ke_probit(p):
    if p <= 0: p = 1
    if p >= 100: p = 99
    p = int(round(p))
    puluhan = int(p//10*10)
    satuan = int(p%10)
    if puluhan == 0:
        puluhan = 1
    return PROBIT_TABLE[puluhan][satuan]

def regresi_linier(x, y):
    x, y = np.array(x,float), np.array(y,float)
    n = len(x)
    a = (n*np.sum(x*y)-np.sum(x)*np.sum(y))/(n*np.sum(x**2)-(np.sum(x))**2)
    b = (np.sum(y)-a*np.sum(x))/n
    return a, b

def korelasi(x,y):
    x, y = np.array(x,float), np.array(y,float)
    n = len(x)
    r = (n*np.sum(x*y)-np.sum(x)*np.sum(y))/np.sqrt(
        (n*np.sum(x**2)-(np.sum(x))**2)*(n*np.sum(y**2)-(np.sum(y))**2)
    )
    return r, r**2

def klasifikasi_ic50(x):
    if x < 50: return "Sangat kuat"
    elif x < 100: return "Kuat"
    elif x < 150: return "Sedang"
    elif x <= 200: return "Lemah"
    else: return "Sangat lemah / Tidak aktif"

# =====================================================
# LOGIN
# =====================================================
if not st.session_state.login:
    st.markdown('<div class="logo">🧪🌿</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-title">50 Test</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistem Analisis Bioaktivitas</div>', unsafe_allow_html=True)

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "anafi" and p == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Username atau password salah")
    st.stop()

# =====================================================
# MENU
# =====================================================
menu = st.sidebar.radio(
    "Menu",
    ["Home","LC50 Probit","IC50 / EC50","TPC","Riwayat","Logout"]
)

# =====================================================
# HOME
# =====================================================
if menu == "Home":
    st.markdown('<div class="logo">🌱🔬</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-title">Silakan Olah Data Anda</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">LC₅₀ • IC₅₀ • EC₅₀ • TPC</div>', unsafe_allow_html=True)

# =====================================================
# LC50 PROBIT
# =====================================================
if menu == "LC50 Probit":
    st.header("Penentuan Nilai Probit")
    n = st.number_input("Jumlah data", min_value=3, value=5)

    kons, mati, total = [], [], []
    for i in range(int(n)):
        c1,c2,c3 = st.columns(3)
        kons.append(c1.number_input(f"Konsentrasi {i+1}", min_value=0.001))
        mati.append(c2.number_input(f"Jumlah mati {i+1}", min_value=0))
        total.append(c3.number_input(f"Total {i+1}", min_value=1))

    if st.button("Hitung LC50"):
        persen = [(mati[i]/total[i])*100 for i in range(int(n))]
        logk = [math.log10(k) for k in kons]
        prob = [mortalitas_ke_probit(p) for p in persen]

        df = pd.DataFrame({
            "Log Konsentrasi": logk,
            "Probit": prob
        })
        st.line_chart(df.set_index("Log Konsentrasi"))

        a,b = regresi_linier(logk, prob)
        lc50 = 10 ** ((5 - b)/a)
        st.success(f"LC₅₀ = {lc50:.4f}")

# =====================================================
# IC50 / EC50 + GRAFIK + REGRESI
# =====================================================
if menu == "IC50 / EC50":
    st.header("IC₅₀ / EC₅₀")
    n = st.number_input("Jumlah titik", min_value=3, value=5)

    x, y = [], []
    for i in range(int(n)):
        c1, c2 = st.columns(2)
        x.append(c1.number_input(f"Konsentrasi {i+1}"))
        y.append(c2.number_input(f"% Efek {i+1}", 0.0, 100.0))

    if st.button("Hitung IC50 / EC50"):
        # =========================
        # REGRESI & KORELASI
        # =========================
        a, b = regresi_linier(x, y)
        r, r2 = korelasi(x, y)
        ic50 = (50 - b) / a

        # =========================
        # DATA GRAFIK
        # =========================
        df = pd.DataFrame({
            "Konsentrasi": x,
            "% Efek": y
        }).sort_values("Konsentrasi")

        x_reg = np.linspace(min(x), max(x), 100)
        y_reg = a * x_reg + b

        df_reg = pd.DataFrame({
            "Konsentrasi": x_reg,
            "Regresi": y_reg
        })

        # =========================
        # GRAFIK
        # =========================
        st.subheader("Grafik IC₅₀ / EC₅₀")
        st.line_chart(df.set_index("Konsentrasi"))
        st.line_chart(df_reg.set_index("Konsentrasi"))

        # =========================
        # OUTPUT NUMERIK 
        # =========================
        st.success(f"IC₅₀ / EC₅₀ = {ic50:.4f}")
        st.info(f"Persamaan regresi: y = {a:.4f}x + {b:.4f}")
        st.info(f"Koefisien korelasi (r) = {r:.4f}")
        st.info(f"Koefisien determinasi (R²) = {r2:.4f}")
        st.info(f"Kategori aktivitas: {klasifikasi_ic50(ic50)}")

# =====================================================
# TPC
# =====================================================
if menu == "TPC":
    st.header("Total Phenolic Content (TPC)")
    n = st.number_input("Jumlah standar", min_value=3, value=5)

    xs,ys = [],[]
    for i in range(int(n)):
        c1,c2 = st.columns(2)
        xs.append(c1.number_input(f"Konsentrasi {i+1}"))
        ys.append(c2.number_input(f"Absorbansi {i+1}"))

    if st.button("Persamaan Regresi"):
        a,b = regresi_linier(xs,ys)
        st.session_state.a = a
        st.session_state.b = b
        st.success(f"A = {a:.4f}C + {b:.4f}")

    if "a" in st.session_state:
        abs_s = st.number_input("Absorbansi sampel")
        vol = st.number_input("Volume (mL)")
        fp = st.number_input("Faktor pengenceran")
        m = st.number_input("Massa (g)")

        if st.button("Hitung TPC"):
            c = ((abs_s-st.session_state.b)/st.session_state.a)/1000
            tpc = (c*vol*fp)/m
            st.success(f"TPC = {tpc:.4f} mg GAE/g")

# =====================================================
# KURVA REGRESI — TPC
# =====================================================
if menu == "TPC" and st.session_state.get("login", False):

    if st.button("Tampilkan Kurva Standar TPC"):
        if len(xs) > 1:

            df_plot = pd.DataFrame({
                "Konsentrasi": xs,
                "Absorbansi": ys
            })

            line = alt.Chart(df_plot).mark_line().encode(
                x="Konsentrasi",
                y="Absorbansi"
            )

            scatter = alt.Chart(df_plot).mark_point(size=80).encode(
                x="Konsentrasi",
                y="Absorbansi"
            )

            st.subheader("Kurva Standar TPC")
            st.altair_chart(line + scatter, use_container_width=True)
            

# =====================================================
# RIWAYAT & LOGOUT
# =====================================================
if menu == "Logout":
    st.session_state.clear()
    st.success("Logout berhasil")
    st.stop()
