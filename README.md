# Bike Sharing Data Analysis Dashboard 

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis dataset Bike Sharing guna memahami pola penggunaan sepeda berdasarkan waktu, hari, dan kondisi cuaca. Hasil analisis divisualisasikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Struktur Direktori
submission
├── dashboard
│ ├── dashboard.py
│ └── main_data.csv
├── data
│ ├── day.csv
│ └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Setup Environment - Anaconda
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pip install -r requirements.txt

## Run Streamlit App
streamlit run dashboard/dashboard.py