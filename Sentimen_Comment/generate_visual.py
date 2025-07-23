# generate_visualisasi.py

import pandas as pd
import matplotlib.pyplot as plt
import os

# Buat folder output kalau belum ada
output_folder = 'static/images'
os.makedirs(output_folder, exist_ok=True)

# Baca dataset
df = pd.read_csv('data/dataset_komentar_labeled.csv')  # Pastikan ada kolom 'comment', 'sentiment', 'timestamp'

# -------- Distribusi Sentimen --------
def plot_distribusi_sentimen(df):
    platform_counts = df['platform'].value_counts()
    
    plt.figure(figsize=(6, 6))
    platform_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#2ecc71', '#e74c3c', '#f1c40f'])
    plt.title('Distribusi Sentimen')
    plt.ylabel('')  # Hapus label sumbu Y
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'distribusi_sentimen.png'))
    plt.close()
    
    print("[INFO] Grafik Distribusi Sentimen disimpan.")

# -------- Tren Komentar --------
def plot_tren_komentar(df):
    # Pastikan kolom timestamp dalam format datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Drop NaT (kalau ada timestamp error)
    df = df.dropna(subset=['timestamp'])
    
    # Hitung jumlah komentar per hari
    komentar_per_hari = df.groupby(df['timestamp'].dt.date).size()
    
    plt.figure(figsize=(10, 5))
    komentar_per_hari.plot(kind='line', marker='o', color='#3498db')
    plt.title('Tren Jumlah Komentar per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Komentar')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'tren_komentar.png'))
    plt.close()
    
    print("[INFO] Grafik Tren Komentar disimpan.")

# Jalankan semua
plot_distribusi_sentimen(df)
plot_tren_komentar(df)

print("[SUCCESS] Semua visualisasi selesai dibuat!")
