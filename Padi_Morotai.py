import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    csv_path = '/mount/src/project_mbkm/data_padi.csv'  # Sesuaikan path file CSV Anda
    data = pd.read_csv(csv_path)
    return data

# Fungsi untuk analisis strategi per wilayah
def analyze_regional_strategy(df):
    regional_metrics = df.groupby('wilayah').agg({
        'produksi_pertahun': ['mean', 'std'],
        'harga': ['mean', 'std'],
        'permintaan_pasar': lambda x: x.value_counts().index[0],
        'tingkat_konsumsi_perkapita_perkg': 'mean',
        'luas_lahan_hektar': 'mean',
        'tingkat_kesuburan_tanah': 'mean'
    })

    scaler = MinMaxScaler()
    metrics_for_scoring = ['produksi_pertahun', 'harga', 'tingkat_konsumsi_perkapita_perkg',
                           'luas_lahan_hektar', 'tingkat_kesuburan_tanah']

    regional_scores = pd.DataFrame()
    for metric in metrics_for_scoring:
        if metric in regional_metrics.columns.get_level_values(0):
            regional_scores[f'{metric}_score'] = scaler.fit_transform(
                regional_metrics[metric]['mean'].values.reshape(-1, 1)
            ).flatten()

    regional_scores['total_score'] = regional_scores.mean(axis=1)

    regional_scores['kategori'] = pd.qcut(regional_scores['total_score'],
                                           q=3,
                                           labels=['Berkembang', 'Potensial', 'Unggulan'])

    return regional_scores

# Fungsi untuk analisis risiko
def analyze_risks(df):
    risk_metrics = df.groupby('wilayah').agg({
        'produksi_pertahun': lambda x: x.std() / x.mean() * 100,
        'harga': lambda x: x.std() / x.mean() * 100,
        'tingkat_kesuburan_tanah': 'mean',
        'curah_hujan': lambda x: x.value_counts().index[0]
    })

    risk_metrics['risiko_produksi'] = pd.qcut(risk_metrics['produksi_pertahun'],
                                              q=3,
                                              labels=['Rendah', 'Sedang', 'Tinggi'])
    risk_metrics['risiko_harga'] = pd.qcut(risk_metrics['harga'],
                                           q=3,
                                           labels=['Rendah', 'Sedang', 'Tinggi'])

    weather_risk = df.pivot_table(
        values='produksi_pertahun',
        index='wilayah',
        columns='curah_hujan',
        aggfunc='mean'
    ).fillna(0)

    return {
        'risk_metrics': risk_metrics,
        'weather_risk': weather_risk
    }

# Fungsi untuk rekomendasi implementasi
def generate_recommendations(df):
    regional_scores = analyze_regional_strategy(df)
    risk_analysis = analyze_risks(df)

    recommendations = pd.DataFrame(index=df['wilayah'].unique())

    recommendations['kategori'] = regional_scores['kategori']
    recommendations['risiko_produksi'] = risk_analysis['risk_metrics']['risiko_produksi']
    recommendations['risiko_harga'] = risk_analysis['risk_metrics']['risiko_harga']

    def get_recommendation(row):
        if row['kategori'] == 'Unggulan':
            if row['risiko_produksi'] == 'Rendah':
                return 'Ekspansi agresif, fokus peningkatan kapasitas'
            else:
                return 'Ekspansi terkendali, fokus manajemen risiko'
        elif row['kategori'] == 'Potensial':
            if row['risiko_harga'] == 'Rendah':
                return 'Pengembangan bertahap, fokus efisiensi'
            else:
                return 'Pengembangan selektif, diversifikasi pasar'
        else:
            return 'Evaluasi ulang strategi, fokus perbaikan fundamental'

    recommendations['rekomendasi'] = recommendations.apply(get_recommendation, axis=1)

    return recommendations

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

    # Sidebar untuk navigasi
    st.sidebar.title("Menu")
    menu_options = [
        "Analisis Data Produksi dan Permintaan", 
        "Analisis Data Produksi, Permintaan, dan Kompetisi", 
        "Analisis Strategi Per Wilayah dan Analisis Risiko", 
        "Analisis Peluang Pasar Padi di Pulau Morotai"
    ]
    choice = st.sidebar.selectbox("Pilih Menu", menu_options)

    if choice == "Analisis Data Produksi dan Permintaan":
        st.header("📊 Analisis Data Produksi dan Permintaan")
        submenu = st.radio("Pilih Submenu:", 
                           ["Tren Produksi per Tahun", 
                            "Wilayah dengan Produksi Tertinggi", 
                            "Pengaruh Curah Hujan terhadap Produksi", 
                            "Analisis Permintaan Pasar", 
                            "Analisis Harga per Wilayah", 
                            "Analisis Korelasi", 
                            "Wilayah Paling Potensial"])

        if submenu == "Tren Produksi per Tahun":
            st.subheader("📈 Tren Produksi per Tahun")
            yearly_production = data.groupby('tahun')['produksi_pertahun'].agg(['mean', 'sum']).round(2)
            st.write(yearly_production)
            
            fig = px.line(yearly_production, x=yearly_production.index, y='mean', title='Rata-rata Produksi per Tahun')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Produksi padi mengalami fluktuasi dari tahun ke tahun.
                - Produksi tertinggi terjadi pada tahun 2023 dengan rata-rata 2.137 ton dan total produksi 161.868 ton.
                - Penurunan produksi terlihat pada tahun 2020 dan 2022.
                """)

        elif submenu == "Wilayah dengan Produksi Tertinggi":
            st.subheader("🏆 Wilayah dengan Produksi Tertinggi")
            top_regions = data.groupby('wilayah')['produksi_pertahun'].agg(['mean', 'sum']).round(2).sort_values('sum', ascending=False)
            st.write(top_regions.head())
            
            fig = px.bar(top_regions.head(), x='sum', y=top_regions.head().index, title='Top 5 Wilayah Berdasarkan Total Produksi')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Kabupaten Halmahera Tengah memimpin dengan rata-rata produksi tertinggi sebesar 3.071,09 ton dan total produksi 107.488 ton.
                - Kabupaten Pulau Taliabu dan Kota Ternate juga menunjukkan performa produksi yang baik.
                """)

        elif submenu == "Pengaruh Curah Hujan terhadap Produksi":
            st.subheader("🌧️ Pengaruh Curah Hujan terhadap Produksi")
            rain_production = data.groupby('curah_hujan')['produksi_pertahun'].agg(['mean', 'count']).round(2)
            st.write(rain_production)
            
            fig = px.bar(rain_production.reset_index(), x='curah_hujan', y='mean', title='Rata-rata Produksi Berdasarkan Curah Hujan')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Produksi tertinggi terjadi pada wilayah dengan curah hujan tinggi (rata-rata produksi 2.749,75 ton).
                - Curah hujan sedang dan rendah menghasilkan rata-rata produksi lebih rendah.
                """)

        elif submenu == "Analisis Permintaan Pasar":
            st.subheader("📊 Analisis Permintaan Pasar")
            market_demand = data.groupby('permintaan_pasar').agg({
                'produksi_pertahun': 'mean',
                'harga': 'mean',
                'wilayah': 'count'
            }).round(2)
            st.write(market_demand)
            
            fig = px.bar(market_demand.reset_index(), x='permintaan_pasar', y='produksi_pertahun', title='Rata-rata Produksi Berdasarkan Permintaan Pasar')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Wilayah dengan permintaan pasar tinggi memiliki rata-rata produksi yang lebih tinggi.
                - Harga cenderung lebih stabil di wilayah dengan permintaan pasar tinggi.
                """)

        elif submenu == "Analisis Harga per Wilayah":
            st.subheader("💰 Analisis Harga per Wilayah")
            price_analysis = data.groupby('wilayah').agg({
                'harga': ['mean', 'min', 'max'],
                'permintaan_pasar': lambda x: x.value_counts().index[0]
            }).round(2)
            st.write(price_analysis.head())
            
            price_analysis_mean = price_analysis['harga']['mean'].reset_index()
            fig = px.bar(price_analysis_mean, x='wilayah', y='mean', title='Rata-rata Harga Berdasarkan Wilayah')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Harga rata-rata tertinggi ditemukan di Kabupaten Halmahera Tengah (Rp 9.550,09), diikuti oleh Kabupaten Halmahera Selatan (Rp 9.486,80).
                - Wilayah dengan harga lebih rendah seperti Kabupaten Halmahera Timur (Rp 8.799,42) memiliki permintaan pasar rendah.
                """)

        elif submenu == "Analisis Korelasi":
            st.subheader("🔗 Analisis Korelasi")
            correlation = data[['produksi_pertahun', 'harga', 'luas_lahan_hektar', 'tingkat_konsumsi_perkapita_perkg']].corr()
            st.write(correlation)
            
            fig = px.imshow(correlation, text_auto=True, title='Heatmap Korelasi')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Produksi tahunan memiliki korelasi yang lemah terhadap harga (0,020), luas lahan (-0,079), dan tingkat konsumsi per kapita (-0,021).
                - Faktor eksternal seperti curah hujan mungkin memiliki pengaruh yang lebih signifikan terhadap produksi dibandingkan faktor internal seperti luas lahan.
                """)

        elif submenu == "Wilayah Paling Potensial":
            st.subheader("🌟 Wilayah Paling Potensial")
            potential_regions = data.groupby('wilayah').agg({
                'produksi_pertahun': 'mean',
                'permintaan_pasar': lambda x: x.value_counts().index[0],
                'tingkat_konsumsi_perkapita_perkg': 'mean',
                'harga': 'mean'
            }).round(2)

            potential_regions['skor_potensi'] = (
                (potential_regions['produksi_pertahun'] / potential_regions['produksi_pertahun'].max()) * 0.3 +
                (potential_regions['tingkat_konsumsi_perkapita_perkg'] / potential_regions['tingkat_konsumsi_perkapita_perkg'].max()) * 0.3 +
                (potential_regions['harga'] / potential_regions['harga'].max()) * 0.4
            ).round(2)

            st.write(potential_regions.sort_values('skor_potensi', ascending=False).head())
            
            fig = px.bar(potential_regions.sort_values('skor_potensi', ascending=False).head(), 
                         x='skor_potensi', y=potential_regions.sort_values('skor_potensi', ascending=False).head().index, 
                         title='Top 5 Wilayah Paling Potensial')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Kabupaten Halmahera Tengah adalah wilayah paling potensial dengan skor potensi 0,96, didukung oleh produksi tinggi (3.071,09 ton), harga terbaik (Rp 9.550,09), dan permintaan pasar tinggi.
                - Kabupaten Halmahera Barat (skor potensi 0,95) dan Halmahera Selatan (skor potensi 0,91) juga memiliki potensi besar.
                """)

    elif choice == "Analisis Data Produksi, Permintaan, dan Kompetisi":
        st.header("📈 Analisis Data Produksi, Permintaan, dan Kompetisi")
        submenu = st.radio("Pilih Submenu:", 
                           ["Analisis Seasonality (Pola Produksi Berdasarkan Curah Hujan)", 
                            "Proyeksi Permintaan Produksi (2025-2026)", 
                            "Analisis Kompetisi (Market Share Wilayah)", 
                            "Analisis Faktor Harga"])

        if submenu == "Analisis Seasonality (Pola Produksi Berdasarkan Curah Hujan)":
            st.subheader("🌧️ Analisis Seasonality (Pola Produksi Berdasarkan Curah Hujan)")
            seasonal_patterns = data.groupby('curah_hujan')['produksi_pertahun'].mean().reset_index()
            seasonal_patterns.rename(columns={'produksi_pertahun': 'rata_produksi'}, inplace=True)
            st.write(seasonal_patterns)
            
            fig = px.bar(seasonal_patterns, x='curah_hujan', y='rata_produksi', title='Rata-rata Produksi Berdasarkan Curah Hujan')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Produksi meningkat seiring dengan curah hujan, dengan rata-rata produksi tertinggi pada curah hujan tinggi.
                - Harga cenderung lebih rendah pada wilayah dengan curah hujan tinggi, sementara curah hujan rendah memiliki harga tertinggi.
                """)

        elif submenu == "Proyeksi Permintaan Produksi (2025-2026)":
            st.subheader("📅 Proyeksi Permintaan Produksi (2025-2026)")
            yearly_trend = data.groupby('tahun').agg({
                'produksi_pertahun': 'mean',
                'permintaan_pasar': lambda x: x.value_counts().index[0],
                'harga': 'mean'
            }).reset_index()

            X = yearly_trend[['tahun']]
            y = yearly_trend['produksi_pertahun']
            model = LinearRegression()
            model.fit(X, y)

            future_years = pd.DataFrame({'tahun': [2025, 2026]})
            projections = model.predict(future_years)

            projections_df = pd.DataFrame({
                'tahun': future_years['tahun'],
                'proyeksi_produksi': projections.round(2)
            })
            st.write(projections_df)
            
            fig = px.line(yearly_trend, x='tahun', y='produksi_pertahun', title='Proyeksi Produksi (2025-2026)')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Proyeksi produksi stabil pada kisaran 2.662 ton per tahun.
                - Tren ini menunjukkan pertumbuhan produksi yang stagnan, sehingga diperlukan inovasi atau optimalisasi untuk mendorong peningkatan produksi.
                """)

        elif submenu == "Analisis Kompetisi (Market Share Wilayah)":
            st.subheader("🏆 Analisis Kompetisi (Market Share Wilayah)")
            market_share = data.groupby('wilayah').agg({
                'produksi_pertahun': 'sum',
                'luas_lahan_hektar': 'mean',
                'harga': 'mean'
            })
            market_share['market_share'] = (market_share['produksi_pertahun'] / market_share['produksi_pertahun'].sum() * 100).round(2)
            st.write(market_share.sort_values('market_share', ascending=False).head())
            
            fig = px.bar(market_share.sort_values('market_share', ascending=False).head(), 
                         x='market_share', y=market_share.sort_values('market_share', ascending=False).head().index, 
                         title='Market Share Top 5 Wilayah')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Kabupaten Halmahera Tengah memiliki market share tertinggi (13,45%), diikuti oleh Pulau Taliabu (13,19%) dan Kota Ternate (11,28%).
                - Wilayah dengan market share tinggi juga memiliki rata-rata produksi tinggi, menunjukkan dominasi produksi sebagai faktor kunci persaingan.
                """)

        elif submenu == "Analisis Faktor Harga":
            st.subheader("💰 Analisis Faktor Harga")
            price_correlation = data[['harga', 'produksi_pertahun', 'tingkat_konsumsi_perkapita_perkg',
                                    'luas_lahan_hektar', 'tingkat_kesuburan_tanah']].corr()['harga']
            st.write(price_correlation)
            
            fig = px.bar(price_correlation, x=price_correlation.index, y=price_correlation.values, title='Korelasi Faktor dengan Harga')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Harga memiliki korelasi lemah dengan produksi tahunan (0,02) dan tingkat konsumsi per kapita (0,016), menunjukkan bahwa faktor-faktor ini bukan pendorong utama harga.
                - Korelasi negatif antara harga dan tingkat kesuburan tanah (-0,067) menunjukkan wilayah dengan tanah lebih subur cenderung memiliki harga lebih rendah, mungkin karena efisiensi produksi.
                """)

    elif choice == "Analisis Strategi Per Wilayah dan Analisis Risiko":
        st.header("📊 Analisis Strategi Per Wilayah dan Analisis Risiko")
        submenu = st.radio("Pilih Submenu:", 
                           ["Top 5 Wilayah Unggulan (Wilayah Unggulan & Wilayah Potensial)", 
                            "Analisis Risiko", 
                            "Rekomendasi Implementasi", 
                            "Strategi Umum"])

        if submenu == "Top 5 Wilayah Unggulan (Wilayah Unggulan & Wilayah Potensial)":
            st.subheader("🌟 Top 5 Wilayah Unggulan (Wilayah Unggulan & Wilayah Potensial)")
            regional_metrics = data.groupby('wilayah').agg({
                'produksi_pertahun': ['mean', 'std'],
                'harga': ['mean', 'std'],
                'permintaan_pasar': lambda x: x.value_counts().index[0],
                'tingkat_konsumsi_perkapita_perkg': 'mean',
                'luas_lahan_hektar': 'mean',
                'tingkat_kesuburan_tanah': 'mean'
            })

            scaler = MinMaxScaler()
            metrics_for_scoring = ['produksi_pertahun', 'harga', 'tingkat_konsumsi_perkapita_perkg',
                                   'luas_lahan_hektar', 'tingkat_kesuburan_tanah']

            regional_scores = pd.DataFrame()
            for metric in metrics_for_scoring:
                if metric in regional_metrics.columns.get_level_values(0):
                    regional_scores[f'{metric}_score'] = scaler.fit_transform(
                        regional_metrics[metric]['mean'].values.reshape(-1, 1)
                    ).flatten()

            regional_scores['total_score'] = regional_scores.mean(axis=1)

            regional_scores['kategori'] = pd.qcut(regional_scores['total_score'],
                                                   q=3,
                                                   labels=['Berkembang', 'Potensial', 'Unggulan'])

            st.write(regional_scores.sort_values('total_score', ascending=False).head())
            
            fig = px.bar(regional_scores.sort_values('total_score', ascending=False).head(), 
                         x='total_score', y=regional_scores.sort_values('total_score', ascending=False).head().index, 
                         title='Top 5 Wilayah Unggulan')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Wilayah dengan kategori unggulan memiliki skor total di atas 0.55, seperti wilayah **2, 5, 8, dan 9**, yang menunjukkan potensi besar untuk peningkatan produksi dan efisiensi.
                - Wilayah dengan skor total mendekati 0.50 seperti wilayah **0**, menunjukkan adanya potensi yang dapat dioptimalkan lebih lanjut melalui investasi dan pengembangan.
                """)

        elif submenu == "Analisis Risiko":
            st.subheader("⚠️ Analisis Risiko")
            risk_metrics = data.groupby('wilayah').agg({
                'produksi_pertahun': lambda x: x.std() / x.mean() * 100,
                'harga': lambda x: x.std() / x.mean() * 100,
                'tingkat_kesuburan_tanah': 'mean',
                'curah_hujan': lambda x: x.value_counts().index[0]
            })

            risk_metrics['risiko_produksi'] = pd.qcut(risk_metrics['produksi_pertahun'],
                                                      q=3,
                                                      labels=['Rendah', 'Sedang', 'Tinggi'])
            risk_metrics['risiko_harga'] = pd.qcut(risk_metrics['harga'],
                                                   q=3,
                                                   labels=['Rendah', 'Sedang', 'Tinggi'])

            weather_risk = data.pivot_table(
                values='produksi_pertahun',
                index='wilayah',
                columns='curah_hujan',
                aggfunc='mean'
            ).fillna(0)

            st.write(risk_metrics.sort_values('produksi_pertahun', ascending=False).head())
            
            fig = px.bar(risk_metrics.sort_values('produksi_pertahun', ascending=False).head(), 
                         x='produksi_pertahun', y=risk_metrics.sort_values('produksi_pertahun', ascending=False).head().index, 
                         title='Risiko Produksi per Wilayah')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - **Kota Ternate** dan **Kabupaten Halmahera Utara** memiliki risiko produksi dan harga yang tinggi.
                - Faktor utama risiko termasuk fluktuasi harga tinggi dan curah hujan rendah, yang dapat menghambat stabilitas produksi.
                """)

        elif submenu == "Rekomendasi Implementasi":
            st.subheader("📝 Rekomendasi Implementasi")
            regional_scores = analyze_regional_strategy(data)
            risk_analysis = analyze_risks(data)

            recommendations = pd.DataFrame(index=data['wilayah'].unique())

            recommendations['kategori'] = regional_scores['kategori']
            recommendations['risiko_produksi'] = risk_analysis['risk_metrics']['risiko_produksi']
            recommendations['risiko_harga'] = risk_analysis['risk_metrics']['risiko_harga']

            def get_recommendation(row):
                if row['kategori'] == 'Unggulan':
                    if row['risiko_produksi'] == 'Rendah':
                        return 'Ekspansi agresif, fokus peningkatan kapasitas'
                    else:
                        return 'Ekspansi terkendali, fokus manajemen risiko'
                elif row['kategori'] == 'Potensial':
                    if row['risiko_harga'] == 'Rendah':
                        return 'Pengembangan bertahap, fokus efisiensi'
                    else:
                        return 'Pengembangan selektif, diversifikasi pasar'
                else:
                    return 'Evaluasi ulang strategi, fokus perbaikan fundamental'

            recommendations['rekomendasi'] = recommendations.apply(get_recommendation, axis=1)
            st.write(recommendations.head())
            
            fig = px.bar(recommendations.head(), x='rekomendasi', y=recommendations.head().index, title='Rekomendasi Implementasi per Wilayah')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - **Kabupaten Halmahera Tengah:** Risiko moderat dengan stabilitas harga yang baik. Fokus pada evaluasi strategi untuk meningkatkan efisiensi produksi.
                - **Kabupaten Pulau Morotai dan Halmahera Barat:** Risiko rendah pada produksi dan harga. Strategi perbaikan fundamental di wilayah ini dapat meningkatkan output dan daya saing.
                """)

        elif submenu == "Strategi Umum":
            st.subheader("📋 Strategi Umum")
            with st.expander("Lihat Strategi Umum"):
                st.write("""
                **Strategi Umum:**
                - **Penguatan Infrastruktur Produksi:** Investasi dalam teknologi pertanian dan manajemen air di wilayah dengan curah hujan rendah.
                - **Diversifikasi Produk dan Pemasaran:** Mengembangkan produk bernilai tambah untuk wilayah dengan risiko harga tinggi guna menstabilkan pendapatan.
                - **Pengelolaan Risiko:** Wilayah dengan risiko tinggi memerlukan pendekatan mitigasi risiko yang komprehensif, termasuk kontrak harga tetap dan pengelolaan stok.
                """)

    elif choice == "Analisis Peluang Pasar Padi di Pulau Morotai":
        st.header("🌾 Analisis Peluang Pasar Padi di Pulau Morotai")
        submenu = st.radio("Pilih Submenu:", 
                           ["Produksi Padi di Pulau Morotai", 
                            "Permintaan Lokal dan Konsumsi Beras", 
                            "Potensi Ekonomi dan Harga Pasar", 
                            "Faktor Pendukung (Pemerintah dan Infrastruktur, Keanekaragaman Hayati)", 
                            "Tantangan (Keterbatasan Lahan, Kendala Teknologi dan Modal)", 
                            "Peluang Strategis (Pengembangan Varietas Unggul, Diversifikasi Pasar, Kerjasama dengan Petani Lokal)", 
                            "Rekomendasi (Peningkatan Kapasitas Produksi, Penguatan Rantai Pasok, Pembangunan Kemitraan)"])

        if submenu == "Produksi Padi di Pulau Morotai":
            st.subheader("🌾 Produksi Padi di Pulau Morotai")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.line(morotai_data, x='tahun', y='produksi_pertahun', title='Produksi Padi di Pulau Morotai per Tahun')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Produksi padi di Pulau Morotai menunjukkan tren yang fluktuatif dari tahun ke tahun.
                - Pada tahun 2023, produksi mencapai puncaknya dengan 2.137 ton, tetapi pada tahun 2019 produksi hanya 1.232 ton.
                - Curah hujan yang tinggi di wilayah ini menjadi salah satu faktor pendukung produksi padi.
                """)

        elif submenu == "Permintaan Lokal dan Konsumsi Beras":
            st.subheader("🍚 Permintaan Lokal dan Konsumsi Beras")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.bar(morotai_data, x='tahun', y='tingkat_konsumsi_perkapita_perkg', title='Tingkat Konsumsi Beras per Kapita di Pulau Morotai')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Tingkat konsumsi beras per kapita di Pulau Morotai cenderung stabil, dengan rata-rata sekitar 200 kg per tahun.
                - Kebutuhan beras tahunan di Pulau Morotai diperkirakan mencapai 5.820 ton, yang menunjukkan potensi pasar yang besar.
                """)

        elif submenu == "Potensi Ekonomi dan Harga Pasar":
            st.subheader("💰 Potensi Ekonomi dan Harga Pasar")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.line(morotai_data, x='tahun', y='harga', title='Harga Beras di Pulau Morotai per Tahun')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Harga beras di Pulau Morotai cenderung fluktuatif, dengan puncak harga tertinggi pada tahun 2019 sebesar Rp 13.876.
                - Harga yang tinggi ini disebabkan oleh biaya distribusi yang mahal dari wilayah produsen utama.
                - Dengan meningkatkan produksi lokal, harga beras dapat ditekan dan daya saing pasar lokal dapat ditingkatkan.
                """)

        elif submenu == "Faktor Pendukung (Pemerintah dan Infrastruktur, Keanekaragaman Hayati)":
            st.subheader("🏛️ Faktor Pendukung (Pemerintah dan Infrastruktur, Keanekaragaman Hayati)")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.bar(morotai_data, x='curah_hujan', title='Distribusi Curah Hujan di Pulau Morotai')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Curah hujan di Pulau Morotai didominasi oleh kategori **tinggi**, yang sangat mendukung pertanian padi.
                - Dukungan pemerintah dalam pembangunan infrastruktur seperti irigasi dan jalan juga menjadi faktor pendukung utama.
                - Keanekaragaman hayati di Pulau Morotai memungkinkan pengembangan varietas padi lokal yang adaptif.
                """)

        elif submenu == "Tantangan (Keterbatasan Lahan, Kendala Teknologi dan Modal)":
            st.subheader("🚧 Tantangan (Keterbatasan Lahan, Kendala Teknologi dan Modal)")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.line(morotai_data, x='tahun', y='luas_lahan_hektar', title='Luas Lahan Pertanian di Pulau Morotai per Tahun')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Luas lahan pertanian di Pulau Morotai cenderung stabil, dengan rata-rata sekitar 60 hektar per tahun.
                - Keterbatasan lahan menjadi tantangan utama, karena sebagian besar lahan digunakan untuk kegiatan lain seperti pariwisata dan perikanan.
                - Kendala teknologi dan modal juga menghambat peningkatan produksi padi.
                """)

        elif submenu == "Peluang Strategis (Pengembangan Varietas Unggul, Diversifikasi Pasar, Kerjasama dengan Petani Lokal)":
            st.subheader("🚀 Peluang Strategis (Pengembangan Varietas Unggul, Diversifikasi Pasar, Kerjasama dengan Petani Lokal)")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.bar(morotai_data, x='tahun', y='tingkat_kesuburan_tanah', title='Tingkat Kesuburan Tanah di Pulau Morotai per Tahun')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Tingkat kesuburan tanah di Pulau Morotai cukup tinggi, dengan rata-rata skor 7 dari 10.
                - Peluang strategis meliputi pengembangan varietas padi unggul yang tahan terhadap kondisi tanah berpasir dan liat.
                - Diversifikasi pasar dan kerjasama dengan petani lokal dapat meningkatkan produktivitas dan kualitas hasil panen.
                """)

        elif submenu == "Rekomendasi (Peningkatan Kapasitas Produksi, Penguatan Rantai Pasok, Pembangunan Kemitraan)":
            st.subheader("📝 Rekomendasi (Peningkatan Kapasitas Produksi, Penguatan Rantai Pasok, Pembangunan Kemitraan)")
            morotai_data = data[data['wilayah'] == 'Kabupaten Pulau Morotai']
            fig = px.scatter(morotai_data, x='luas_lahan_hektar', y='produksi_pertahun', title='Hubungan Luas Lahan dan Produksi di Pulau Morotai')
            st.plotly_chart(fig)
            
            with st.expander("Kesimpulan"):
                st.write("""
                - Terdapat korelasi positif antara luas lahan dan produksi padi di Pulau Morotai.
                - Rekomendasi utama meliputi peningkatan kapasitas produksi melalui teknologi pertanian modern, penguatan rantai pasok untuk mengurangi biaya distribusi, dan pembangunan kemitraan dengan pemerintah dan investor.
                """)

# Panggil fungsi main() untuk menjalankan dashboard
if __name__ == "__main__":
    main()
