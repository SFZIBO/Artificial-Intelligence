import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pickle

# ========================== 1. LOAD & CLEANING ===========================

# Load CSV dengan separator ';'
df = pd.read_csv('dataset/cleaned_data.csv', sep=';')

# Rename kolom (pastikan urutannya sesuai)
df.columns = ['Komoditas', 'Tahun', 'Bulan', 'Harga']

# Drop baris kosong dan baris dengan harga '-'
df.dropna(inplace=True)
df = df[df['Harga'] != '-']

# Bersihkan kolom Harga dari 'Rp' dan titik (.) → ubah ke int
df['Harga'] = df['Harga'].str.replace('Rp', '', regex=False).str.replace('.', '', regex=False).astype(int)

# ========================== 2. FILTER KOMODITAS =========================

# Ambil hanya komoditas "GKP Tingkat Petani (Rp/Kg)"
df = df[df['Komoditas'] == 'GKP Tingkat Petani (Rp/Kg)'].copy()

# Reset index
df.reset_index(drop=True, inplace=True)

# ========================== 3. ENCODE & NORMALIZE =======================

# Encode bulan menjadi angka (Januari → 0, Februari → 1, dst)
le_bulan = LabelEncoder()
df['Bulan_encoded'] = le_bulan.fit_transform(df['Bulan'])

# Input: Tahun dan Bulan_encoded
X = df[['Tahun', 'Bulan_encoded']].values
y = df[['Harga']].values  # jadi 2D

# Normalisasi fitur
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# ========================== 4. SPLIT & TRAIN MODEL ======================

x_train, x_valid, y_train, y_valid = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Bangun model ANN
model = Sequential()
model.add(Dense(16, activation='relu', input_dim=2))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))  # output layer

# Compile & train
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=100, validation_data=(x_valid, y_valid), verbose=1)

# ========================== 5. SAVE MODEL & SCALER =======================

# Simpan model
model.save("model/model_pangan.h5")

# Simpan scaler
with open('model/scaler_x.pkl', 'wb') as f:
    pickle.dump(scaler_X, f)

with open('model/scaler_y.pkl', 'wb') as f:
    pickle.dump(scaler_y, f)

print("✅ Model & scaler berhasil disimpan!")
