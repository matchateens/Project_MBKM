import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import graphviz
import matplotlib.ticker as ticker  # Import ticker untuk FixedLocator

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/matchateens/repo/branch/data/data_cengekeh.csv")
    return data

def main():
    # Memuat data
    data = load_data()

    # Mengubah data kategorikal menjadi numerik untuk analisis korelasi
    label_encoder = LabelEncoder()
    data['curah_hujan_encoded'] = label_encoder.fit_transform(data['curah_hujan'])
    data['permintaan_pasar_encoded'] = label_encoder.fit_transform(data['permintaan_pasar'])

    # Tab untuk menampilkan analisis
    tabs = st.tabs([
        "Analisis Data Produksi dan Permintaan Cengkeh", 
        "Analisis Data Cengkeh", 
        "Analisis Risiko dan Rekomendasi Implementasi", 
        "Analisis Peluang Pasar Cengkeh di Pulau Morotai", 
        "Kesimpulan Utama"
    ])

    # Tab 1: Analisis Data Produksi dan Permintaan Cengkeh
    with tabs[0]:
        st.header("Analisis Data Produksi dan Permintaan Cengkeh")
        
        # Trend Produksi per Tahun
        st.subheader("Trend Produksi per Tahun")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data, x='tahun', y='produksi_pertahun', hue='wilayah', marker='o', ax=ax)
        ax.set_title("Trend Produksi Cengkeh per Tahun")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Produksi (kg)")
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Produksi cengkeh di Pulau Morotai menunjukkan fluktuasi dari tahun ke tahun.
        - Puncak produksi terjadi pada tahun 2022, sementara produksi terendah terjadi pada tahun 2023.
        - Tren produksi cenderung menurun setelah tahun 2022, menunjukkan perlunya intervensi untuk meningkatkan produktivitas.
        """)
        
        # Wilayah dengan Produksi Tertinggi
        st.subheader("Wilayah dengan Produksi Tertinggi")
        production_by_region = data.groupby('wilayah')['produksi_pertahun'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=production_by_region.index, y=production_by_region.values, hue=production_by_region.index, palette='viridis', legend=False, ax=ax)
        ax.set_title("Produksi Cengkeh per Wilayah")
        ax.set_xlabel("Wilayah")
        ax.set_ylabel("Total Produksi (kg)")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(production_by_region.index))))  # Atur posisi tick
        ax.set_xticklabels(production_by_region.index, rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Kabupaten Pulau Talibu memiliki produksi tertinggi dibandingkan wilayah lainnya.
        - Wilayah lain seperti Halmahera Tengah dan Halmahera Barat juga menunjukkan produksi yang signifikan.
        """)
        
        # Pengaruh Curah Hujan terhadap Produksi
        st.subheader("Pengaruh Curah Hujan terhadap Produksi")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=data, x='curah_hujan_encoded', y='produksi_pertahun', hue='wilayah', ax=ax)
        ax.set_title("Pengaruh Curah Hujan terhadap Produksi Cengkeh")
        ax.set_xlabel("Curah Hujan (Encoded)")
        ax.set_ylabel("Produksi (kg)")
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Curah hujan sedang cenderung menghasilkan produksi yang lebih tinggi.
        - Curah hujan rendah dan tinggi memiliki dampak negatif terhadap produksi cengkeh.
        """)
        
        # Analisis Permintaan Pasar
        st.subheader("Analisis Permintaan Pasar")
        demand_counts = data['permintaan_pasar'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=demand_counts.index, y=demand_counts.values, hue=demand_counts.index, palette='cool', legend=False, ax=ax)
        ax.set_title("Distribusi Permintaan Pasar")
        ax.set_xlabel("Kategori Permintaan")
        ax.set_ylabel("Jumlah Kasus")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(demand_counts.index))))  # Atur posisi tick
        ax.set_xticklabels(demand_counts.index, rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Permintaan pasar tinggi mendominasi, diikuti oleh permintaan rendah dan sedang.
        - Permintaan pasar tinggi memiliki jumlah kasus yang lebih sedikit, menunjukkan potensi untuk meningkatkan permintaan melalui pemasaran yang tepat.
        """)
        
        # Harga per Wilayah
        st.subheader("Harga per Wilayah")
        price_by_region = data.groupby('wilayah')['harga'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=price_by_region.index, y=price_by_region.values, hue=price_by_region.index, palette='magma', legend=False, ax=ax)
        ax.set_title("Harga Rata-Rata Cengkeh per Wilayah")
        ax.set_xlabel("Wilayah")
        ax.set_ylabel("Harga (Rp/kg)")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(price_by_region.index))))  # Atur posisi tick
        ax.set_xticklabels(price_by_region.index, rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Harga cengkeh bervariasi antar wilayah, dengan Kabupaten Halmahera Timur memiliki harga tertinggi.
        - Harga terendah ditemukan di Kabupaten Halmahera Selatan, yang mungkin disebabkan oleh volume produksi yang lebih tinggi.
        """)
        
        # Analisis Korelasi
        st.subheader("Analisis Korelasi")
        correlation_matrix = data[['produksi_pertahun', 'curah_hujan_encoded', 'harga', 'permintaan_pasar_encoded']].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Korelasi antara Produksi, Curah Hujan, Harga, dan Permintaan Pasar")
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Korelasi antara produksi dan harga sangat lemah, menunjukkan bahwa peningkatan produksi tidak secara langsung memengaruhi harga.
        - Curah hujan memiliki korelasi positif yang lemah dengan produksi, menunjukkan bahwa curah hujan sedang dapat meningkatkan produksi.
        """)
        
        # Wilayah Paling Potensial
        st.subheader("Wilayah Paling Potensial")
        potential_regions = data.groupby('wilayah')['produksi_pertahun'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=potential_regions.index, y=potential_regions.values, hue=potential_regions.index, palette='plasma', legend=False, ax=ax)
        ax.set_title("Wilayah dengan Potensi Produksi Tertinggi")
        ax.set_xlabel("Wilayah")
        ax.set_ylabel("Rata-Rata Produksi (kg)")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(potential_regions.index))))  # Atur posisi tick
        ax.set_xticklabels(potential_regions.index, rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)  # Menutup plot untuk menghindari kebocoran memori
        st.markdown("""
        **Kesimpulan:**
        - Kabupaten Halmahera Utara memiliki potensi produksi tertinggi, diikuti oleh Pulau Morotai dan Halmahera Barat.
        - Wilayah-wilayah ini memiliki rata-rata produksi yang tinggi, menunjukkan potensi untuk pengembangan lebih lanjut.
        """)

    # Tab 2: Analisis Data Cengkeh
    with tabs[1]:
        st.header("Analisis Data Cengkeh")
        
        # Contoh analisis data cengkeh
        st.subheader("Distribusi Produksi per Wilayah")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data, x='wilayah', y='produksi_pertahun', hue='wilayah', palette='viridis', legend=False, ax=ax)
        ax.set_title("Distribusi Produksi per Wilayah")
        ax.set_xlabel("Wilayah")
        ax.set_ylabel("Produksi (kg)")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(data['wilayah'].unique()))))  # Atur posisi tick
        ax.set_xticklabels(data['wilayah'].unique(), rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Produksi cengkeh bervariasi antar wilayah, dengan beberapa wilayah menunjukkan produksi yang lebih stabil.
        - Wilayah dengan produksi tinggi memiliki potensi untuk ditingkatkan lebih lanjut.
        """)

    # Tab 3: Analisis Risiko dan Rekomendasi Implementasi
    with tabs[2]:
        st.header("Analisis Risiko dan Rekomendasi Implementasi")
        
        # Contoh analisis risiko
        st.subheader("Risiko Produksi per Wilayah")
        risk_data = data.groupby('wilayah')['produksi_pertahun'].std().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=risk_data['wilayah'], y=risk_data['produksi_pertahun'], hue=risk_data['wilayah'], palette='coolwarm', legend=False, ax=ax)
        ax.set_title("Risiko Produksi per Wilayah")
        ax.set_xlabel("Wilayah")
        ax.set_ylabel("Standar Deviasi Produksi (kg)")
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(risk_data['wilayah']))))  # Atur posisi tick
        ax.set_xticklabels(risk_data['wilayah'], rotation=45)  # Atur label tick dengan rotasi
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Wilayah dengan risiko produksi tinggi memerlukan strategi mitigasi risiko yang lebih baik.
        - Rekomendasi implementasi termasuk diversifikasi produk dan peningkatan kualitas lahan.
        """)

    # Tab 4: Analisis Peluang Pasar Cengkeh di Pulau Morotai
    with tabs[3]:
        st.header("Analisis Peluang Pasar Cengkeh di Pulau Morotai")
        
        # Contoh analisis peluang pasar
        st.subheader("Peluang Pasar Berdasarkan Permintaan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=data, x='permintaan_pasar', y='produksi_pertahun', hue='permintaan_pasar', palette='cool', legend=False, ax=ax)
        ax.set_title("Peluang Pasar Berdasarkan Permintaan")
        ax.set_xlabel("Kategori Permintaan")
        ax.set_ylabel("Produksi (kg)")
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("""
        **Kesimpulan:**
        - Peluang pasar terbesar ada di wilayah dengan permintaan tinggi.
        - Wilayah dengan permintaan sedang memiliki potensi untuk ditingkatkan melalui strategi pemasaran.
        """)

    # Tab 5: Kesimpulan Utama
    with tabs[4]:
        st.header("Kesimpulan Utama")
        
        # Contoh kesimpulan utama
        st.markdown("""
        **Kesimpulan Utama:**
        - Produksi cengkeh di Pulau Morotai memiliki potensi besar untuk dikembangkan.
        - Peningkatan produksi dan pemasaran dapat meningkatkan profitabilitas.
        - Manajemen risiko dan diversifikasi produk diperlukan untuk mengurangi fluktuasi harga.
        """)

# Panggil fungsi main() untuk menjalankan dashboard
if __name__ == "__main__":
    main()
