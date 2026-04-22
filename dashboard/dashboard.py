import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    layout="wide"
)

# =========================
# STYLE CLEAN
# =========================
st.markdown("""
<style>
.main {
    background-color: #F9FAFB;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    font-weight: 600;
}
.stMetric {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("dashboard/data_day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter Data")

min_date = df["dteday"].min()
max_date = df["dteday"].max()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date]
)

season_list = sorted(df["season"].unique())
weather_list = sorted(df["weathersit"].unique())

season = st.sidebar.multiselect(
    "Musim",
    options=season_list,
    default=season_list
)

weather = st.sidebar.multiselect(
    "Cuaca",
    options=weather_list,
    default=weather_list
)

if st.sidebar.button("Reset Filter"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Gunakan filter untuk eksplorasi data")

# =========================
# APPLY FILTER
# =========================
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date)) &
    (df["season"].isin(season)) &
    (df["weathersit"].isin(weather))
]

# =========================
# HANDLE EMPTY
# =========================
if df.empty:
    st.warning("Data kosong. Ubah filter.")
    st.stop()

# =========================
# HEADER
# =========================
st.title("Dashboard Penyewaan Sepeda")
st.caption("Analisis penggunaan sepeda berdasarkan cuaca, musim, dan waktu")

# =========================
# KPI
# =========================
total = df["cnt"].sum()
avg = df["cnt"].mean()
peak_day = df.loc[df["cnt"].idxmax(), "dteday"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{int(total):,}")
col2.metric("Rata-rata Harian", f"{int(avg):,}")
col3.metric("Hari Tertinggi", peak_day.strftime("%d %b %Y"))

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["Overview", "Detail", "Insight"])

# =========================
# OVERVIEW
# =========================
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pengaruh Cuaca")
        weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()

        fig, ax = plt.subplots()
        sns.barplot(
            data=weather_avg,
            x="weathersit",
            y="cnt",
            hue="weathersit",
            palette="Blues",
            legend=False,
            ax=ax
        )
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Penggunaan Berdasarkan Musim")
        season_avg = df.groupby("season")["cnt"].mean().reset_index()

        fig, ax = plt.subplots()
        sns.barplot(
            data=season_avg,
            x="season",
            y="cnt",
            hue="season",
            palette="Greens",
            legend=False,
            ax=ax
        )
        plt.tight_layout()
        st.pyplot(fig)

# =========================
# DETAIL
# =========================
with tab2:

    st.subheader("Tren Penyewaan per Bulan")

    monthly = df.set_index("dteday").resample("ME")["cnt"].sum()

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(monthly.index, monthly.values, linewidth=2)
    plt.tight_layout()
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hari Kerja vs Libur")
        df["tipe_hari"] = df["workingday"].map({0:"Libur",1:"Kerja"})
        day_avg = df.groupby("tipe_hari")["cnt"].mean().reset_index()

        fig, ax = plt.subplots()
        sns.barplot(
            data=day_avg,
            x="tipe_hari",
            y="cnt",
            hue="tipe_hari",
            palette="coolwarm",
            legend=False,
            ax=ax
        )
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Distribusi Penyewaan")
        fig, ax = plt.subplots()
        sns.histplot(df["cnt"], bins=30, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)

# =========================
# INSIGHT
# =========================
with tab3:

    st.subheader("Ringkasan Eksekutif")

    st.markdown("""
**Temuan Utama**
- Penyewaan meningkat saat cuaca cerah  
- Musim Fall memiliki penyewaan tertinggi  
- Pola musiman konsisten sepanjang tahun  
- Aktivitas lebih tinggi pada hari kerja  

**Implikasi**
- Permintaan dapat diprediksi  
- Faktor eksternal berpengaruh signifikan  

**Rekomendasi**
- Optimalkan kapasitas saat peak  
- Tingkatkan promosi saat low demand  
- Gunakan data historis untuk strategi  
""")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    label="Download Data",
    data=df.to_csv(index=False),
    file_name="data_clean.csv"
)