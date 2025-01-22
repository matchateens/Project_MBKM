import streamlit as st
import pandas as pd

# Import semua dashboard
from dashboards.Ayam_Petelur_Morotai import main as ayam_dashboard
from dashboards.Cengkeh_Morotai import main as cengkeh_dashboard
from dashboards.Kakao_Morotai import main as kakao_dashboard
from dashboards.Padi_Morotai import main as padi_dashboard
from dashboards.Pisang_Morotai import main as pisang_dashboard


# Judul aplikasi
st.title("🌿 Dashboard Analisis Pertanian Pulau Morotai")

# Sidebar untuk navigasi
st.sidebar.title("📂 Menu Dashboard")
dashboard_options = [
    "Analisis Ayam Petelur",
    "Analisis Cengkeh",
    "Analisis Kakao",
    "Analisis Pisang",
    "Analisis Padi"
]
selected_dashboard = st.sidebar.selectbox("Pilih Dashboard", dashboard_options)

# Menampilkan dashboard yang dipilih
if selected_dashboard == "Analisis Ayam Petelur":
    st.header("🐔 Analisis Ayam Petelur di Pulau Morotai")
    ayam_dashboard()

elif selected_dashboard == "Analisis Cengkeh":
    st.header("🌿 Analisis Cengkeh di Pulau Morotai")
    cengkeh_dashboard()

elif selected_dashboard == "Analisis Kakao":
    st.header("🍫 Analisis Kakao di Pulau Morotai")
    kakao_dashboard()

elif selected_dashboard == "Analisis Pisang":
    st.header("🍌 Analisis Pisang di Pulau Morotai")
    pisang_dashboard()

elif selected_dashboard == "Analisis Padi":
    st.header("🌾 Analisis Padi di Pulau Morotai")
    padi_dashboard()

# Catatan tambahan
st.sidebar.markdown("---")
st.sidebar.markdown("**Catatan:**")
st.sidebar.markdown("""
- Pilih dashboard dari menu di atas untuk melihat analisis spesifik.
- Setiap dashboard menyediakan analisis produksi, permintaan pasar, dan rekomendasi strategis.
""")
