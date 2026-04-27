import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bike Dashboard", layout="wide")

# ================= CLEAN PREMIUM CSS =================
st.markdown("""
<style>
:root {
    --primary: #1e40af;
    --gray-50: #f8fafc;
    --gray-100: #f1f5f9;
    --gray-200: #e5e7eb;
    --gray-500: #64748b;
    --dark: #1e293b;
}

/* GLOBAL */
.main {
    background: var(--gray-50);
}
.block-container {
    max-width: 1200px;
}

/* HERO */
.hero-header {
    background: var(--gray-100);
    padding: 26px 30px;
    border-radius: 16px;
    border: 1px solid var(--gray-200);
    margin-bottom: 24px;
}
.hero-title {
    font-size: 40px;     
    font-weight: 800;     
    color: #0f172a;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 16px;     
    color: #64748b;
    margin-top: 6px;
}

/* SECTION TITLE */
.section-title {
    margin-top: 40px;
    margin-bottom: 10px;
}

.section-title h2 {
    font-size: 28px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 4px;
}

.section-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 20px;
}

.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 30px 0;
}

.insight-box {
    background: #f1f5f9;
    border-left: 4px solid #3b82f6;
    padding: 18px;
    border-radius: 10px;
    margin-top: 16px;
    font-size: 15px;
    line-height: 1.6;
}
            
/* KPI UPGRADE */
[data-testid="stMetric"] {
    background: white;
    border-radius: 14px;
    padding: 1.6rem;
    border: 1px solid #e5e7eb;
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    font-size: 36px !important;   /* INI YANG GEDE */
    font-weight: 700 !important;  /* INI YANG TEBEL */
    color: #111827 !important;
}

/* KPI CAPTION */
.kpi-caption {
    margin-top: 14px;
    font-size: 14px;
    color: #6b7280;
}

/* RECOMMEND */
.recommend-box {
    background: #ecfdf5;
    border-left: 4px solid #22c55e;
    padding: 16px;
    border-radius: 10px;
    margin-top: 18px;
    font-size: 16px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
df = pd.read_csv("dashboard/data_day.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

season_map = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
weather_map = {1:"Clear",2:"Mist",3:"Light Rain/Snow",4:"Heavy Rain/Snow"}

df["season"] = df["season"].replace(season_map)
df["weathersit"] = df["weathersit"].replace(weather_map)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🎛️ Filter Dashboard")
    st.caption("Atur tampilan data sesuai kebutuhan.")

    date_range = st.date_input(
        "📅 Rentang Tanggal",
        [df["dteday"].min().date(), df["dteday"].max().date()]
    )

    season = st.multiselect(
        "🌤️ Pilih Musim",
        options=sorted(df["season"].unique()),
        default=sorted(df["season"].unique())
    )

    weather = st.multiselect(
        "☁️ Pilih Cuaca",
        options=sorted(df["weathersit"].unique()),
        default=sorted(df["weathersit"].unique())
    )

    st.markdown("---")
    st.markdown("### ℹ️ Keterangan")

    st.markdown("""
    Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan:

    - Tren waktu  
    - Faktor cuaca  
    - Pola musiman  
    - Performa penyewaan  
    """)

# ================= FILTER =================
df_filtered = df.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered["dteday"] >= pd.to_datetime(date_range[0])) &
        (df_filtered["dteday"] <= pd.to_datetime(date_range[1]))
    ]

if season:
    df_filtered = df_filtered[df_filtered["season"].isin(season)]

if weather:
    df_filtered = df_filtered[df_filtered["weathersit"].isin(weather)]

# ================= HEADER =================


st.markdown("""
<div class="hero-header">
    <div class="hero-title">🚴 Dashboard Analisis Penyewaan Sepeda</div>
    <div class="hero-subtitle">
        Dashboard ini dirancang untuk menjawab bagaimana <b>faktor cuaca</b>, <b>musim</b>, 
dan <b>tren waktu</b> memengaruhi jumlah penyewaan sepeda pada periode <b>2011–2012</b>.
    </div>
</div>
""", unsafe_allow_html=True)

# ================= KPI =================
st.markdown("""
<div class="section-title">
<h2>📊 Ringkasan Utama</h2>
</div>
<div class="section-subtitle">
Gambaran umum performa penyewaan sepeda selama periode pengamatan
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Rata-rata Penyewaan", int(df_filtered["cnt"].mean()))
c2.metric("Median Penyewaan", int(df_filtered["cnt"].median()))
c3.metric("Penyewaan Maksimum", int(df_filtered["cnt"].max()))
c4.metric("Jumlah Data", len(df_filtered))

st.markdown("""
<div class="kpi-caption">
Secara umum, penyewaan sepeda berada pada level stabil dengan rata-rata sekitar <b>4.504 unit/hari</b>. 
Namun, terdapat lonjakan signifikan pada kondisi tertentu yang mengindikasikan bahwa permintaan sangat dipengaruhi oleh faktor eksternal seperti <b>cuaca dan musim</b>.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= SCATTER =================
st.markdown("""
<div class="section-title">
<h2>🌤️ 1. Faktor Cuaca terhadap Penyewaan</h2>
</div>
<div class="section-subtitle">
Untuk memahami faktor utama yang memengaruhi permintaan, analisis difokuskan pada variabel cuaca seperti temperatur, kelembapan, dan kecepatan angin
</div>
""", unsafe_allow_html=True)

col1,col2,col3 = st.columns(3)

for col, var in zip([col1, col2, col3], ["temp","hum","windspeed"]):
    fig = px.scatter(df_filtered, x=var, y="cnt", trendline="ols")
    fig.update_traces(marker=dict(color="#3b82f6", size=6, opacity=0.6))
    fig.update_layout(plot_bgcolor="white")
    col.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-box">
<b>🔍 Insight:</b><br><br>

Analisis menunjukkan bahwa <b>temperatur memiliki pengaruh paling dominan</b> terhadap jumlah penyewaan sepeda. 
Semakin tinggi temperatur, jumlah penyewaan cenderung meningkat secara signifikan, terlihat dari pola hubungan positif yang cukup kuat.

Sebaliknya, <b>kelembapan (humidity) dan kecepatan angin (windspeed)</b> menunjukkan hubungan negatif, 
namun dengan kekuatan yang relatif lemah. Hal ini mengindikasikan bahwa kedua faktor tersebut 
hanya berperan sebagai faktor pendukung, bukan penentu utama.

Hal ini menunjukkan bahwa <b>temperatur dapat digunakan sebagai indikator utama dalam memprediksi permintaan</b>, 
sehingga perencanaan operasional sebaiknya menyesuaikan dengan kondisi suhu untuk mengoptimalkan ketersediaan sepeda.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= SEASON =================
st.markdown("""
<div class="section-title">
<h2>🍂 2. Pola Musiman Penyewaan</h2>
</div>
<div class="section-subtitle">
Setelah memahami pengaruh cuaca, analisis dilanjutkan untuk melihat pola permintaan berdasarkan musim
</div>
""", unsafe_allow_html=True)

season_avg = df_filtered.groupby("season")["cnt"].mean().reset_index()

fig = px.bar(
    season_avg,
    x="season",
    y="cnt",
    color="season",
    color_discrete_sequence=["#bfdbfe","#93c5fd","#60a5fa","#2563eb"]
)
fig.update_layout(plot_bgcolor="white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-box">
<b>🔍 Insight:</b><br><br>

Terdapat pola musiman yang cukup jelas dalam penyewaan sepeda. 
<b>Musim Fall dan Summer menunjukkan tingkat penyewaan tertinggi</b>, 
yang mengindikasikan bahwa kondisi cuaca yang lebih hangat dan nyaman 
mendorong peningkatan aktivitas pengguna.

Sebaliknya, <b>musim Spring memiliki tingkat penyewaan terendah</b>, 
menunjukkan bahwa transisi musim belum cukup mendukung aktivitas luar ruangan.

Selain itu, variasi penyewaan pada musim dengan demand tinggi juga lebih besar, 
yang menandakan adanya fluktuasi aktivitas pengguna yang lebih dinamis.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= TREND =================
st.markdown("""
<div class="section-title">
<h2>📈 3. Tren Penyewaan Sepeda</h2>
</div>
<div class="section-subtitle">
Untuk melengkapi analisis, tren waktu digunakan untuk melihat bagaimana permintaan berkembang dari waktu ke waktu
</div>
""", unsafe_allow_html=True)

df_filtered["dteday"] = pd.to_datetime(df_filtered["dteday"])

monthly = (
    df_filtered
    .set_index("dteday")
    .resample("MS")   # ⬅️ GANTI "M" → "MS"
    ["cnt"]
    .sum()
    .reset_index()
)

fig = px.line(monthly, x="dteday", y="cnt", markers=True)
fig.update_traces(line=dict(color="#1e40af", width=3))
fig.update_layout(plot_bgcolor="white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-box">
<b>🔍 Insight:</b><br><br>

Tren penyewaan sepeda menunjukkan pola <b>fluktuatif namun cenderung meningkat</b> 
dari tahun 2011 ke 2012.

Pada setiap tahun, penyewaan cenderung:
<ul>
<li>Meningkat dari awal hingga pertengahan tahun</li>
<li>Mencapai puncak pada pertengahan–akhir tahun</li>
<li>Kemudian menurun kembali menjelang akhir periode</li>
</ul>

Selain itu, tingkat penyewaan pada <b>tahun 2012 secara konsisten lebih tinggi</b> dibandingkan 2011, 
yang mengindikasikan adanya peningkatan permintaan secara keseluruhan.

Pola ini memperkuat adanya <b>pengaruh musiman sekaligus tren pertumbuhan</b>.
<br><br>
Peningkatan ini mengindikasikan adanya <b>pertumbuhan adopsi layanan</b> serta meningkatnya minat masyarakat terhadap penggunaan sepeda sebagai transportasi.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= FINAL =================
st.markdown("""
<div class="section-title">
<h2>📋 Kesimpulan & Rekomendasi</h2>
</div>
<div class="section-subtitle">
Ringkasan akhir dari seluruh analisis untuk mendukung pengambilan keputusan berbasis data
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="insight-box">
    <b>📋 Kesimpulan:</b><br><br>
    <b>Temperatur</b> memiliki pengaruh paling kuat terhadap peningkatan penyewaan (hubungan positif), 
    sedangkan <b>kelembapan</b> dan <b>kecepatan angin</b> berdampak negatif namun relatif lemah. 
    Pola <b>musiman</b> terlihat jelas, dengan puncak permintaan pada <b>Fall & Summer</b> dan terendah di <b>Spring</b>. 
    Selain itu, terdapat <b>tren peningkatan</b> jumlah penyewaan dari <b>2011 ke 2012</b>.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="recommend-box">
    <b>🎯 Rekomendasi:</b><br><br>
    • Optimalkan ketersediaan sepeda pada periode <b>high demand</b> (Fall & Summer)<br>
    • Gunakan <b>temperatur</b> sebagai indikator utama dalam prediksi permintaan<br>
    • Terapkan <b>strategi promosi</b> pada periode demand rendah (Spring)<br>
    • Sesuaikan operasional berdasarkan <b>pola musiman dan tren waktu</b>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; color:#64748b; font-size:13px; margin-top:30px;'>
Dashboard Analisis Penyewaan Sepeda • Nayla Poetri Kurnia
</div>
""", unsafe_allow_html=True)