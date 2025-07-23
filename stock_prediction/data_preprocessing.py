import pandas as pd
import numpy as np

def preprocess_data(filepath):
    # Baca dataset dan konversi kolom angka (hilangkan koma)
    data = pd.read_csv(filepath)
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    for col in numeric_cols:
        data[col] = data[col].str.replace(',', '').astype(float)
    
    # Hitung 7D_Avg (rata-rata 7 hari sebelumnya)
    data['7D_Avg'] = data['Close'].rolling(window=7).mean().shift(1)
    data.dropna(inplace=True)  # Hapus baris dengan NaN
    
    # Simpan dataset yang sudah diproses
    processed_path = 'data/processed_tlkm_stock.csv'
    data.to_csv(processed_path, index=False)
    return processed_path