import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("data/data_pisang.csv")
    return df

# Fungsi utama untuk menjalankan dashboard
def main():
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: auto;
    }
    .stMarkdown {
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Memuat data
    data = load_data()

    # Judul dashboard
    st.title("Analisis Peluang Pasar Pisang di Pulau Morotai")

    # Membuat tab
    tab1, tab2, tab3, tab4 = st.tabs([
        "Tren Produksi", 
        "Analisis Pasar", 
        "Analisis Strategi", 
        "Rekomendasi"
    ])

    # Tab 1: Tren Produksi
    with tab1:
        st.header("Tren Produksi Pisang di Pulau Morotai")
        
        # Grafik tren produksi
        yearly_production = data.groupby('tahun')['produksi_pertahun'].sum()
        fig, ax = plt.subplots()
        yearly_production.plot(kind='line', ax=ax)
        ax.set_title('Tren Produksi Pisang per Tahun')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Total Produksi')
        st.pyplot(fig)
        plt.close(fig)
        st.write("**Kesimpulan:** Produksi pisang menunjukkan tren yang stabil dengan peningkatan signifikan pada tahun 2024.")

    # Tab 2: Analisis Pasar
    with tab2:
        st.header("Analisis Pasar Pisang di Pulau Morotai")
        
        # Grafik analisis pasar
        market_demand = data.groupby('permintaan_pasar')['produksi_pertahun'].mean()
        fig, ax = plt.subplots()
        market_demand.plot(kind='bar', ax=ax)
        ax.set_title('Rata-rata Produksi Berdasarkan Permintaan Pasar')
        ax.set_xlabel('Permintaan Pasar')
        ax.set_ylabel('Rata-rata Produksi')
        st.pyplot(fig)
        plt.close(fig)
        st.write("**Kesimpulan:** Wilayah dengan permintaan pasar tinggi memiliki rata-rata produksi 8.115 kg/tahun.")

    # Tab 3: Analisis Strategi
    with tab3:
        st.header("Analisis Strategi Pasar Pisang")
        
        # Grafik strategi pasar
        regional_scores = data.groupby('wilayah').agg({
            'produksi_pertahun': 'mean',
            'permintaan_pasar': lambda x: x.value_counts().index[0],
            'tingkat_konsumsi_perkapita_perkg': 'mean',
            'harga': 'mean'
        }).round(2)
        
        regional_scores['skor_potensi'] = (
            (regional_scores['produksi_pertahun'] / regional_scores['produksi_pertahun'].max()) * 0.3 +
            (regional_scores['tingkat_konsumsi_perkapita_perkg'] / regional_scores['tingkat_konsumsi_perkapita_perkg'].max()) * 0.3 +
            (regional_scores['harga'] / regional_scores['harga'].max()) * 0.4
        ).round(2)
        
        fig, ax = plt.subplots()
        regional_scores['skor_potensi'].sort_values(ascending=False).head().plot(kind='bar', ax=ax)
        ax.set_title('Top 5 Wilayah Paling Potensial')
        ax.set_xlabel('Wilayah')
        ax.set_ylabel('Skor Potensi')
        st.pyplot(fig)
        plt.close(fig)
        st.write("**Kesimpulan:** Pulau Morotai menempati peringkat kedua wilayah paling potensial dengan skor 0,91.")

    # Tab 4: Rekomendasi
    with tab4:
        st.header("Rekomendasi Strategis untuk Pisang di Pulau Morotai")
        st.write("""
        - Fokus pada peningkatan kualitas produksi pisang.
        - Ekspansi pasar ke luar daerah.
        - Manajemen risiko terkait fluktuasi harga.
        """)

# Panggil fungsi main() untuk menjalankan dashboard
if __name__ == "__main__":
    main()
