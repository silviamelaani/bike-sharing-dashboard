import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

absolute_path = os.path.dirname(__file__)

day_df = pd.read_csv(os.path.join(absolute_path, "day.csv"))
hour_df = pd.read_csv(os.path.join(absolute_path, "hour.csv"))

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ======================
# BACKGROUND STYLE
# ======================

st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#7f1d1d,#dc2626,#ef4444);
background-attachment: fixed;
}

.block-container {
background: rgba(255,255,255,0.96);
padding: 2rem;
border-radius: 15px;
}

.insight-box {
background: #fff5f5;
padding: 18px;
border-radius: 12px;
border-left: 6px solid #ef4444;
box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# ======================
# LOAD DATA
# ======================

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")


# ======================
# HEADER
# ======================

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis Pola Penyewaan Sepeda berdasarkan berbagai faktor")


# ======================
# KPI
# ======================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", int(day_df['cnt'].sum()))

with col2:
    st.metric("Rata-rata Harian", int(day_df['cnt'].mean()))

with col3:
    st.metric("Hari Terbanyak", int(day_df['cnt'].max()))


# ======================
# TABS
# ======================

tab1, tab2, tab3, tab4 = st.tabs([
    "Pengaruh Cuaca",
    "Pola Jam",
    "Rata-rata Harian",
    "Clustering Jam"
])


# ======================
# TAB 1 - PENGARUH CUACA
# ======================

with tab1:

    st.subheader("🌦️ Pengaruh Cuaca")

    weather_map = {
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    }

    day_df['Kondisi Cuaca'] = day_df['weathersit'].map(weather_map)
    weather_avg = day_df.groupby('Kondisi Cuaca')['cnt'].mean().reset_index()

    col1, col2 = st.columns([3,2])

    with col1:

        fig, ax = plt.subplots(figsize=(8,4))

        sns.barplot(
            data=weather_avg,
            x='Kondisi Cuaca',
            y='cnt',
            hue='Kondisi Cuaca',
            palette="Reds",
            legend=False,
            ax=ax
        )

        for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.0f}',
                (p.get_x()+p.get_width()/2, p.get_height()),
                ha='center',
                va='bottom'
            )

        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan")

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:

        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Penyewaan sepeda paling tinggi terjadi saat cuaca cerah. 
        Hal ini menunjukkan bahwa pengguna lebih nyaman menggunakan 
        sepeda ketika kondisi lingkungan mendukung aktivitas luar ruangan.
        <br><br>
        Ketika cuaca mulai berkabut atau hujan, jumlah penyewaan 
        mengalami penurunan karena faktor kenyamanan dan keamanan.
        <br><br>
        Kondisi cuaca menjadi faktor penting dalam penggunaan bike sharing.
        </div>
        """, unsafe_allow_html=True)


# ======================
# TAB 2 - POLA JAM
# ======================

with tab2:

    st.subheader("⏰ Pola Penyewaan per Jam")

    hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()

    col1, col2 = st.columns([3,2])

    with col1:

        fig, ax = plt.subplots(figsize=(10,4))

        sns.lineplot(
            data=hourly_avg,
            x='hr',
            y='cnt',
            marker='o',
            color="#dc2626",
            linewidth=2.5,
            ax=ax
        )

        ax.set_xticks(range(24))

        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Penyewaan")

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        ax.grid(True, linestyle="--", alpha=0.4)

        st.pyplot(fig)

    with col2:

        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Terlihat dua puncak penyewaan utama yaitu pagi sekitar 
        jam 08.00 dan sore sekitar jam 17.00–18.00. 
        Hal ini menunjukkan sepeda digunakan untuk aktivitas 
        commuting seperti berangkat dan pulang kerja.
        <br><br>
        Penyewaan terendah terjadi pada dini hari sekitar 
        jam 00.00–05.00 karena aktivitas masyarakat masih rendah.
        <br><br>
        Pola ini menunjukkan sepeda lebih banyak digunakan 
        sebagai transportasi harian dibandingkan rekreasi malam hari.
        </div>
        """, unsafe_allow_html=True)


# ======================
# TAB 3 - RATA RATA HARIAN
# ======================

with tab3:

    st.subheader("📅 Rata-rata Penyewaan Sepeda per Hari")

    day_map = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }

    hour_df['weekday_label'] = hour_df['weekday'].map(day_map)

    daily_avg = hour_df.groupby('weekday_label')['cnt'].mean().reset_index()

    order = [
        'Sunday','Monday','Tuesday',
        'Wednesday','Thursday','Friday','Saturday'
    ]

    col1, col2 = st.columns([3,2])

    with col1:

        fig, ax = plt.subplots(figsize=(8,5))

        sns.barplot(
            data=daily_avg,
            x='weekday_label',
            y='cnt',
            order=order,
            hue='weekday_label',
            palette="Reds",
            legend=False,
            ax=ax
        )

        for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.0f}',
                (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center',
                va='bottom'
            )

        ax.set_title('Rata-rata Penyewaan Sepeda per Hari')
        ax.set_xlabel('Hari')
        ax.set_ylabel('Rata-rata Penyewaan')

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:

        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Rata-rata penyewaan sepeda menunjukkan pola penggunaan 
        lebih tinggi pada hari kerja dibandingkan akhir pekan. 
        Hal ini menunjukkan sepeda digunakan sebagai transportasi 
        harian seperti pergi bekerja atau sekolah.
        <br><br>
        Pada akhir pekan, jumlah penyewaan cenderung lebih rendah 
        karena aktivitas commuting berkurang dan penggunaan lebih 
        bersifat rekreasi.
        </div>
        """, unsafe_allow_html=True)


# ======================
# TAB 4 - CLUSTERING
# ======================

with tab4:

    st.subheader("📊 Clustering Penyewaan Sepeda per Jam")

    hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()

    def categorize(cnt):
        if cnt < 100:
            return "Low"
        elif cnt < 300:
            return "Medium"
        else:
            return "High"

    hourly_avg['Kategori'] = hourly_avg['cnt'].apply(categorize)

    col1, col2 = st.columns([3,2])

    with col1:

        fig, ax = plt.subplots(figsize=(10,5))

        sns.barplot(
            data=hourly_avg,
            x='hr',
            y='cnt',
            hue='Kategori',
            dodge=False,
            palette="Reds",
            ax=ax
        )

        for p in ax.patches:
            ax.annotate(
                f'{p.get_height():.0f}',
                (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center',
                va='bottom',
                fontsize=8
            )

        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Penyewaan")

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:

        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Jam sibuk terjadi pada pagi dan sore hari dengan kategori tinggi.
        Hal ini menunjukkan sepeda digunakan untuk aktivitas commuting.
        <br><br>
        Pada malam hari termasuk kategori rendah karena aktivitas menurun.
        </div>
        """, unsafe_allow_html=True)
