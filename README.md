# Dashboard Analisis Penyewaan Sepeda

Proyek ini merupakan analisis data Bike Sharing yang divisualisasikan dalam bentuk dashboard interaktif menggunakan Streamlit. Analisis difokuskan pada pengaruh faktor cuaca, musim, dan waktu terhadap jumlah penyewaan sepeda.

## Tujuan Analisis

* Mengidentifikasi pola penggunaan sepeda
* Menganalisis pengaruh cuaca dan musim terhadap jumlah penyewaan
* Menyajikan hasil analisis dalam bentuk dashboard interaktif

## Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── data_day.csv
├── notebook.ipynb
├── requirements.txt
└── README.md
```

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset yang berisi informasi terkait:

* Tanggal
* Kondisi cuaca
* Musim
* Jumlah penyewaan sepeda

Dataset utama yang digunakan pada dashboard:

* data_day.csv

## Proses Analisis

Analisis dilakukan pada file notebook.ipynb yang mencakup:

* Data cleaning dan preprocessing
* Exploratory Data Analysis (EDA)
* Visualisasi data
* Penarikan insight

## Insight Utama

* Penyewaan sepeda cenderung lebih tinggi pada kondisi cuaca cerah
* Musim Fall dan Summer memiliki jumlah penyewaan tertinggi
* Aktivitas penyewaan lebih tinggi pada hari kerja

## Rekomendasi

* Menyediakan lebih banyak unit sepeda pada musim dengan permintaan tinggi
* Meningkatkan strategi promosi pada periode dengan permintaan rendah
* Memanfaatkan data historis untuk perencanaan operasional

## Cara Menjalankan Dashboard

1. Install dependensi:

```
pip install -r requirements.txt
```

2. Jalankan aplikasi:

```
streamlit run dashboard/dashboard.py
```

## Author

Nayla Poetri Kurnia
