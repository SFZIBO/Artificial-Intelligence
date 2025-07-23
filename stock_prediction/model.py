import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib
from data_preprocessing import preprocess_data

# Preprocess data
processed_data_path = preprocess_data('data/STOCK_ID_XIDX_TLKM.csv')
data = pd.read_csv(processed_data_path)

# Pilih fitur dan target
X = data[['Open', 'High', 'Low', 'Volume', '7D_Avg']].values
y = data['Close'].values.reshape(-1, 1)

# Normalisasi
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Bangun model
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mse')

# Callback early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Training
history = model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping]
)

# Simpan model dan scaler
model.save('saved_models/stock_model.h5')
# Simpan model dalam format .keras (direkomendasikan)
model.save('saved_models/stock_model.keras')  # Ganti .h5 dengan .keras
joblib.dump(scaler_X, 'saved_models/scaler_X.pkl')
joblib.dump(scaler_y, 'saved_models/scaler_y.pkl')

print("Model berhasil dilatih dan disimpan!")

# Di akhir model.py, tambahkan kode berikut:
import matplotlib.pyplot as plt

# Plot grafik loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.savefig('static/loss_plot.png')  # Simpan untuk ditampilkan di Flask
plt.show()