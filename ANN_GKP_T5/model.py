import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pickle

# Jika data sebenarnya dipisahkan oleh karakter lain (bukan koma)
df = pd.read_csv('dataset/cleaned_data.csv', sep=';')  # contoh untuk separator titik koma
# Rename kolom agar lebih rapi
df.columns = ['Komoditas', 'Tahun', 'Bulan', 'Harga']

# Buang baris yang tidak memiliki nilai valid
df.dropna(inplace=True)

# Ubah harga dari format 'Rp5.756' menjadi angka float
# Hapus baris dengan harga '-'
df = df[df['Harga'] != '-']
df['Harga'] = df['Harga'].str.replace('Rp', '').str.replace('.', '').astype(int)

# Tampilkan 5 data awal
print(df.head())

data_gkp_petani = df[df['Komoditas'] == 'GKP Tingkat Petani (Rp/Kg)']
data_gkp_petani = data_gkp_petani.reset_index(drop=True)

data = {
    "Tahun": data_gkp_petani['Tahun'].values,
    "Bulan": data_gkp_petani['Bulan'].values,
    "Harga": data_gkp_petani['Harga'].values
}

# Load data hasil pembersihan sebelumnya
df = pd.read_csv('dataset/cleaned_data.csv', skiprows=2)
df.columns = ['Komoditas', 'Tahun', 'Bulan', 'Harga']
df = df[df['Komoditas'] == 'GKP Tingkat Petani (Rp/Kg)'].dropna()

# Bersihkan harga dari format "Rp5.000"
df['Harga'] = df['Harga'].str.replace('Rp', '').str.replace('.', '').astype(int)

# Encode bulan ke angka
bulan_encoder = LabelEncoder()
df['Bulan_encoded'] = bulan_encoder.fit_transform(df['Bulan'])

# Siapkan data input dan output
X = df[['Tahun', 'Bulan_encoded']].values
y = df['Harga'].values.reshape(-1, 1)

# Normalisasi data
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Bagi data menjadi training dan validation set
x_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Buat model ANN
model = Sequential()
model.add(Dense(16, input_dim=2, activation='relu'))  # input: tahun dan bulan
model.add(Dense(8, activation='relu'))
model.add(Dense(1))  # output: harga pangan

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')
# Latih model
model.fit(x_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
#save model
model.save("model/model_pangan.h5")

# Simpan scaler
with open('scaler_x.pkl', 'wb') as f:
    pickle.dump(scaler_X, f)

with open('scaler_y.pkl', 'wb') as f:
    pickle.dump(scaler_y, f)





