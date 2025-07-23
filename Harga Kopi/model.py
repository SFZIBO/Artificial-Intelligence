import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# pip install numpy pandas matplotlib seaborn scikit-learn flask

def train_model():
    # Load dataset
    df = pd.read_csv('data/data_harga_kopi.csv',header=1,delimiter=';',names=[
        'id', 
        'kode_provinsi', 
        'nama_provinsi', 
        'kode_kabupaten_kota', 
        'nama_kabupaten_kota', 
        'kode_bulan', 
        'nama_bulan', 
        'rata_rata_harga_produsen', 
        'satuan', 
        'tahun'
    ])
    print(df.head())
    print(df.columns)

    df = df.dropna(subset=['kode_kabupaten_kota', 'kode_bulan', 'rata_rata_harga_produsen'])

    # Pastikan semua kolom numerik
    df['kode_kabupaten_kota'] = pd.to_numeric(df['kode_kabupaten_kota'], errors='coerce')
    df['kode_bulan'] = pd.to_numeric(df['kode_bulan'], errors='coerce')
    df['rata_rata_harga_produsen'] = pd.to_numeric(df['rata_rata_harga_produsen'], errors='coerce')

    # Drop NaN setelah konversi
    df = df.dropna()


    # Pilih fitur dan target
    X = df[['kode_kabupaten_kota', 'kode_bulan']]
    y = df['rata_rata_harga_produsen']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    
    print("✅ Model berhasil dilatih dan disimpan!")

    # Pastikan folder 'model/' ada
    os.makedirs('model', exist_ok=True)
    # Simpan model
    joblib.dump(model, 'model/regresi_linear_kopi.joblib')
    
    # Plot hasil prediksi (hanya menggunakan kode_bulan untuk visualisasi)
    plt.scatter(X_test['kode_bulan'], y_test, color='blue', label='Actual')
    plt.scatter(X_test['kode_bulan'], model.predict(X_test), color='red', label='Predicted')
    plt.title('Regresi Linear - Prediksi Harga Kopi')
    plt.xlabel('Bulan')
    plt.ylabel('Harga Rata-rata Produsen (Rp)')
    plt.legend()
    plt.savefig('static/plot_kopi.png')

    return model.score(X_test, y_test)

# Panggil fungsi untuk melatih model
train_model()
