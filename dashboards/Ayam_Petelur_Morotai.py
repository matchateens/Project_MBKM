import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
import graphviz
import matplotlib.ticker as ticker

# Fungsi untuk memuat data
def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

def main():
    # Memuat data
    df = load_data("data/data_ayam.csv")
    
    # Filter data untuk wilayah Morotai
    morotai_data = df[df['wilayah'] == 'Kabupaten Pulau Morotai'].copy()

    # Tab untuk menampilkan analisis
    tabs = st.tabs([
        "Analisis Peluang Pasar Ternak Ayam di Morotai", 
        "Analisis Detail Pasar Ternak Ayam di Morotai", 
        "Analisis Profitabilitas Detail Ternak Ayam di Morotai", 
        "Analisis dan Rencana Implementasi", 
        "Analisis Peluang Pasar Peternakan Ayam di Pulau Morotai", 
        "Kesimpulan Utama"
    ])

    # Tab 1: Analisis Peluang Pasar Ternak Ayam di Morotai
    with tabs[0]:
        st.header("Analisis Peluang Pasar Ternak Ayam di Morotai")
        
        # Trend Produksi dan Harga
        st.subheader("Trend Produksi dan Harga Tahunan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=morotai_data, x='tahun', y='produksi_pertahun', marker='o', color='blue', label='Produksi (kg)', ax=ax)
        sns.lineplot(data=morotai_data, x='tahun', y='harga', marker='o', color='orange', label='Harga (Rp/kg)', ax=ax)
        ax.set_title("Trend Produksi dan Harga Tahunan", fontsize=16)
        ax.set_xlabel("Tahun", fontsize=12)
        ax.set_ylabel("Produksi (kg) / Harga (Rp/kg)", fontsize=12)
        ax.grid(True)
        st.pyplot(fig)
        
        # Distribusi Permintaan
        st.subheader("Distribusi Permintaan Ayam")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=morotai_data, x='permintaan_ayam', palette='cool', hue='permintaan_ayam', legend=False, ax=ax)
        ax.set_title("Distribusi Permintaan Ayam", fontsize=16)
        ax.set_xlabel("Kategori Permintaan", fontsize=12)
        ax.set_ylabel("Jumlah Kasus", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)
        
        # Posisi Kompetitif
        st.subheader("Posisi Kompetitif Antar Wilayah")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='wilayah', y='produksi_pertahun', hue='wilayah', palette='viridis', legend=False, ax=ax)
        ax.set_title("Perbandingan Produksi Antar Wilayah", fontsize=16)
        ax.set_xlabel("Wilayah", fontsize=12)
        ax.set_ylabel("Produksi Pertahun (kg)", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)
        
        # Kesimpulan
        st.markdown("""
        **Kesimpulan:**
        - Produksi ayam di Morotai menunjukkan tren yang fluktuatif, dengan peningkatan signifikan pada tahun 2024.
        - Permintaan pasar didominasi oleh kategori "sedang", menunjukkan potensi peningkatan melalui strategi pemasaran.
        - Morotai memiliki posisi kompetitif yang cukup baik, tetapi perlu meningkatkan produksi untuk bersaing dengan wilayah lain.
        """)

    # Tab 2: Analisis Detail Pasar Ternak Ayam di Morotai
    with tabs[1]:
        st.header("Analisis Detail Pasar Ternak Ayam di Morotai")
        
        # Contoh analisis detail pasar
        st.subheader("Distribusi Harga per Kategori Permintaan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=morotai_data, x='permintaan_ayam', y='harga', hue='permintaan_ayam', palette='cool', legend=False, ax=ax)
        ax.set_title("Distribusi Harga per Kategori Permintaan", fontsize=16)
        ax.set_xlabel("Kategori Permintaan", fontsize=12)
        ax.set_ylabel("Harga (Rp/kg)", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Harga ayam cenderung lebih tinggi di wilayah dengan permintaan tinggi.
        - Wilayah dengan permintaan rendah memiliki variasi harga yang lebih besar.
        """)

    # Tab 3: Analisis Profitabilitas Detail Ternak Ayam di Morotai
    with tabs[2]:
        st.header("Analisis Profitabilitas Detail Ternak Ayam di Morotai")
        
        # Contoh analisis profitabilitas
        st.subheader("Profitabilitas per Tahun")
        morotai_data['profit'] = morotai_data['harga'] * morotai_data['produksi_pertahun']
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=morotai_data, x='tahun', y='profit', marker='o', color='green', ax=ax)
        ax.set_title("Profitabilitas per Tahun", fontsize=16)
        ax.set_xlabel("Tahun", fontsize=12)
        ax.set_ylabel("Profit (Rp)", fontsize=12)
        ax.grid(True)
        st.pyplot(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Profitabilitas meningkat signifikan pada tahun 2024.
        - Peningkatan profitabilitas disebabkan oleh peningkatan produksi dan harga.
        """)

    # Tab 4: Analisis dan Rencana Implementasi
    with tabs[3]:
        st.header("Analisis dan Rencana Implementasi")
        
        # Contoh analisis dan rencana implementasi
        st.subheader("Rencana Implementasi")
        st.write("""
        - **Peningkatan Kapasitas Produksi:** Investasi dalam teknologi dan infrastruktur untuk meningkatkan produksi.
        - **Pemasaran yang Lebih Agresif:** Meningkatkan promosi untuk menarik lebih banyak konsumen.
        - **Manajemen Risiko:** Mengurangi risiko fluktuasi harga dengan diversifikasi produk.
        """)

    # Tab 5: Analisis Peluang Pasar Peternakan Ayam di Pulau Morotai
    with tabs[4]:
        st.header("Analisis Peluang Pasar Peternakan Ayam di Pulau Morotai")
        
        # Contoh analisis peluang pasar
        st.subheader("Peluang Pasar Berdasarkan Permintaan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=morotai_data, x='permintaan_ayam', y='produksi_pertahun', hue='permintaan_ayam', palette='cool', legend=False, ax=ax)
        ax.set_title("Peluang Pasar Berdasarkan Permintaan", fontsize=16)
        ax.set_xlabel("Kategori Permintaan", fontsize=12)
        ax.set_ylabel("Produksi Pertahun (kg)", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Peluang pasar terbesar ada di wilayah dengan permintaan tinggi.
        - Wilayah dengan permintaan sedang memiliki potensi untuk ditingkatkan melalui strategi pemasaran.
        """)

    # Tab 6: Kesimpulan Utama
    with tabs[5]:
        st.header("Kesimpulan Utama")
        
        # Contoh kesimpulan utama
        st.markdown("""
        **Kesimpulan Utama:**
        - Produksi ayam di Morotai memiliki potensi besar untuk dikembangkan.
        - Peningkatan produksi dan pemasaran dapat meningkatkan profitabilitas.
        - Manajemen risiko dan diversifikasi produk diperlukan untuk mengurangi fluktuasi harga.
        """)

# Panggil fungsi main() untuk menjalankan dashboard
if __name__ == "__main__":
    main()
