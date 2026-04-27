# 🚲 Bike Sharing Data Analysis Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Data Analysis](https://img.shields.io/badge/Data%20Analysis-4CAF50?style=for-the-badge)

---

## 📌 Deskripsi Proyek

Proyek ini merupakan analisis data pada **Bike Sharing Dataset** untuk memahami faktor-faktor yang memengaruhi jumlah penyewaan sepeda pada periode **2011–2012**.

Analisis difokuskan pada:
- Pengaruh kondisi cuaca (temperatur, kelembapan, kecepatan angin)
- Pola musiman penyewaan sepeda
- Tren perubahan jumlah penyewaan dari waktu ke waktu

Hasil analisis divisualisasikan dalam bentuk **dashboard interaktif menggunakan Streamlit** untuk mendukung pengambilan keputusan berbasis data (*data-driven decision*).

---

## 🎯 Pertanyaan Bisnis

1. Bagaimana pengaruh kondisi cuaca (temperatur, kelembapan, dan kecepatan angin) terhadap jumlah penyewaan sepeda selama periode tahun 2011–2012?  
2. Pada musim apa jumlah penyewaan sepeda paling tinggi dan paling rendah selama periode tahun 2011–2012?  
3. Bagaimana tren perubahan jumlah penyewaan sepeda dari Januari 2011 hingga Desember 2012? 

---

## 🎯 Tujuan Analisis

- Mengidentifikasi pola penggunaan sepeda
- Menganalisis pengaruh cuaca terhadap jumlah penyewaan
- Mengetahui musim dengan permintaan tertinggi dan terendah
- Menganalisis tren penyewaan dari waktu ke waktu
- Menyajikan hasil analisis dalam bentuk dashboard interaktif

---

## 📁 Struktur Direktori

```bash
submission/
├── dashboard/
│   ├── dashboard.py
│   └── data_day.csv
├── notebook.ipynb
├── README.md
└── requirements.txt
```

## 🚀 Panduan Menjalankan Aplikasi
### 1. Clone Repository
```bash
git clone https://github.com/naylapoetrikurnia-hash/bike-dashboard.git
cd bike-dashboard
```

### 2. Instalasi Library
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard
```bash
streamlit run dashboard/dashboard.py
```

atau

```bash
python -m streamlit run dashboard/dashboard.py
```

Aplikasi akan otomatis terbuka di browser pada:
http://localhost:8501
