import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ======================
# STYLE
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
# MAPPING
# ======================

weather_map = {
    1: 'Clear',
    2: 'Mist',
    3: 'Light Rain/Snow'
}

day_map = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}

day_df['Kondisi Cuaca'] = day_df['weathersit'].map(weather_map)
hour_df['Hari'] = hour_df['weekday'].map(day_map)

# ======================
# SIDEBAR
# ======================

st.sidebar.header("Filter Data")

year_option = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua", "2011", "2012"]
)

weather_option = st.sidebar.multiselect(
    "Pilih Cuaca",
    day_df['Kondisi Cuaca'].dropna().unique(),
    default=day_df['Kondisi Cuaca'].dropna().unique()
)

day_option = st.sidebar.multiselect(
    "Pilih Hari",
    list(day_map.values()),
    default=list(day_map.values())
)

# ✅ VALIDASI FILTER (ANTI ERROR)
if len(weather_option) == 0:
    st.warning("⚠️ Pilih minimal satu kondisi cuaca.")
    st.stop()

if len(day_option) == 0:
    st.warning("⚠️ Pilih minimal satu hari.")
    st.stop()

# ======================
# FILTER DATA
# ======================

filtered_day = day_df.copy()
filtered_hour = hour_df.copy()

if year_option != "Semua":
    yr_val = 0 if year_option == "2011" else 1
    filtered_day = filtered_day[filtered_day['yr'] == yr_val]
    filtered_hour = filtered_hour[filtered_hour['yr'] == yr_val]

filtered_day = filtered_day[
    filtered_day['Kondisi Cuaca'].isin(weather_option)
]

filtered_hour = filtered_hour[
    filtered_hour['Hari'].isin(day_option)
]

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
    st.metric("Total Penyewaan", int(filtered_day['cnt'].sum()))

with col2:
    st.metric("Rata-rata Harian", int(filtered_day['cnt'].mean()))

with col3:
    st.metric("Hari Terbanyak", int(filtered_day['cnt'].max()))

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
# TAB 1
# ======================

with tab1:

    st.subheader("🌦️ Pengaruh Cuaca")

    weather_avg = filtered_day.groupby('Kondisi Cuaca')['cnt'].mean().reset_index()

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
            ax.annotate(f'{p.get_height():.0f}',
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='bottom')

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Penyewaan tertinggi terjadi saat kondisi Clear dan menurun pada Mist hingga Light Rain/Snow.
        <br><br>
        Cuaca menjadi faktor penting dalam menentukan aktivitas penggunaan sepeda.
        </div>
        """, unsafe_allow_html=True)

# ======================
# TAB 2
# ======================

with tab2:

    st.subheader("⏰ Pola Penyewaan per Jam")

    hourly_avg = filtered_hour.groupby('hr')['cnt'].mean().reset_index()
    hourly_avg['Jam'] = hourly_avg['hr'].apply(lambda x: f"{x:02d}:00")

    col1, col2 = st.columns([3,2])

    with col1:
        fig, ax = plt.subplots(figsize=(10,4))

        sns.lineplot(
            data=hourly_avg,
            x='Jam',
            y='cnt',
            marker='o',
            color="#dc2626",
            linewidth=2.5,
            ax=ax
        )

        ax.axvspan(7, 9, color='gray', alpha=0.1)
        ax.axvspan(16, 18, color='gray', alpha=0.1)

        plt.xticks(rotation=45)

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        ax.grid(True, linestyle="--", alpha=0.4)

        st.pyplot(fig)

    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Terdapat dua puncak utama pada pagi dan sore hari yang menunjukkan pola commuting.
        <br><br>
        Aktivitas terendah terjadi pada dini hari.
        </div>
        """, unsafe_allow_html=True)

# ======================
# TAB 3
# ======================

with tab3:

    st.subheader("📅 Rata-rata Penyewaan Sepeda per Hari")

    daily_avg = (
        filtered_hour.groupby('Hari')['cnt']
        .mean()
        .reindex(list(day_map.values()))
    )

    col1, col2 = st.columns([3,2])

    with col1:
        fig, ax = plt.subplots(figsize=(8,5))

        sns.barplot(
            x=daily_avg.index,
            y=daily_avg.values,
            color="#dc2626",
            ax=ax
        )

        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}',
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='bottom')

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Penyewaan lebih tinggi pada hari kerja dibandingkan akhir pekan.
        <br><br>
        Hal ini menunjukkan penggunaan sepeda sebagai transportasi rutin.
        </div>
        """, unsafe_allow_html=True)

# ======================
# TAB 4
# ======================

with tab4:

    st.subheader("📊 Clustering Penyewaan Sepeda per Jam")

    hourly_avg = filtered_hour.groupby('hr')['cnt'].mean().reset_index()
    hourly_avg['Jam'] = hourly_avg['hr'].apply(lambda x: f"{x:02d}:00")

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
            x='Jam',
            y='cnt',
            hue='Kategori',
            dodge=False,
            palette="Reds",
            ax=ax
        )

        plt.xticks(rotation=45)

        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}',
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='bottom', fontsize=8)

        ax.set_facecolor("#fff5f5")
        fig.patch.set_facecolor("#fff5f5")

        st.pyplot(fig)

    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>Insight</b><br><br>
        Jam sibuk terjadi pada pagi dan sore hari.
        <br><br>
        Aktivitas rendah terjadi pada malam hingga dini hari.
        </div>
        """, unsafe_allow_html=True)
