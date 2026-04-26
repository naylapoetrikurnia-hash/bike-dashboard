import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bike Dashboard", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.insight {
    background: #eef2ff;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #4f46e5;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
df = pd.read_csv("dashboard/data_day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

season_map = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
weather_map = {1:"Clear",2:"Mist",3:"Light Rain/Snow",4:"Heavy Rain/Snow"}

df["season"] = df["season"].replace(season_map)
df["weathersit"] = df["weathersit"].replace(weather_map)

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Filter Dashboard")

# 🔥 FILTER TANGGAL (INI YANG KAMU MAU)
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [df["dteday"].min(), df["dteday"].max()]
)

season = st.sidebar.multiselect(
    "Musim",
    df["season"].unique(),
    default=df["season"].unique()
)

weather = st.sidebar.multiselect(
    "Cuaca",
    df["weathersit"].unique(),
    default=df["weathersit"].unique()
)

# FILTER
df = df[
    (df["dteday"] >= pd.to_datetime(date_range[0])) &
    (df["dteday"] <= pd.to_datetime(date_range[1])) &
    (df["season"].isin(season)) &
    (df["weathersit"].isin(weather))
]

# ================= HEADER =================
st.title("🚴 Analisis Penyewaan Sepeda (2011–2012)")

st.markdown("""
### 🎯 Pertanyaan Bisnis
1. Pengaruh cuaca terhadap penyewaan  
2. Musim dengan penyewaan tertinggi & terendah  
3. Tren penyewaan dari waktu ke waktu  
""")

# ================= KPI =================
c1,c2,c3 = st.columns(3)

c1.metric("Rata-rata", int(df["cnt"].mean()))
c2.metric("Maksimum", int(df["cnt"].max()))
c3.metric("Total Data", len(df))

st.markdown("---")

# ================= 1. CUACA =================
st.subheader("1️⃣ Pengaruh Cuaca")

col1,col2,col3 = st.columns(3)

col1.plotly_chart(px.scatter(df, x="temp", y="cnt", trendline="ols"), use_container_width=True)
col2.plotly_chart(px.scatter(df, x="hum", y="cnt", trendline="ols"), use_container_width=True)
col3.plotly_chart(px.scatter(df, x="windspeed", y="cnt", trendline="ols"), use_container_width=True)

st.markdown("""
<div class="insight">
✔ Temperatur memiliki pengaruh paling kuat terhadap penyewaan (positif).  
✔ Kelembapan dan angin berpengaruh negatif namun lemah.  
✔ Artinya: cuaca hangat = demand naik signifikan.
</div>
""", unsafe_allow_html=True)

# ================= 2. MUSIM =================
st.subheader("2️⃣ Pola Musim")

season_avg = df.groupby("season")["cnt"].mean().reset_index()

st.plotly_chart(px.bar(season_avg, x="season", y="cnt", color="season"),
                use_container_width=True)

st.markdown("""
<div class="insight">
✔ Fall = tertinggi  
✔ Spring = terendah  
✔ Summer juga tinggi (peak demand period)
</div>
""", unsafe_allow_html=True)

# ================= 3. TREND =================
st.subheader("3️⃣ Tren Waktu")

monthly = df.set_index("dteday").resample("M")["cnt"].sum().reset_index()

st.plotly_chart(px.line(monthly, x="dteday", y="cnt"),
                use_container_width=True)

st.markdown("""
<div class="insight">
✔ Terjadi tren peningkatan dari 2011 → 2012  
✔ Ada pola musiman (naik di pertengahan tahun)
</div>
""", unsafe_allow_html=True)

# ================= DISTRIBUSI =================
st.subheader("📊 Distribusi")

st.plotly_chart(px.histogram(df, x="cnt"), use_container_width=True)

# ================= KESIMPULAN =================
st.markdown("---")
st.subheader("📋 Kesimpulan")

st.success("""
Temperatur adalah faktor utama dalam meningkatkan penyewaan.  
Musim Fall dan Summer menjadi periode dengan permintaan tertinggi.  
Terdapat tren peningkatan dari waktu ke waktu.
""")

# ================= REKOMENDASI =================
st.subheader("🎯 Rekomendasi")

st.markdown("""
<div class="card">
✔ Fokuskan operasional pada musim Fall & Summer (peak demand).  
✔ Tambahkan armada saat cuaca cerah & temperatur tinggi.  
✔ Lakukan promosi di musim Spring (demand rendah).  
✔ Gunakan prediksi cuaca untuk optimasi supply.
</div>
""", unsafe_allow_html=True)