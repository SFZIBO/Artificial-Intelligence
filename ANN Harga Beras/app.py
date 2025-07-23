# app.py  ── Flask backend prediksi harga GKP Petani
# ==================================================

from flask import Flask, render_template, request
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from pathlib import Path

# ────────── 1. Inisialisasi Flask ──────────
app = Flask(__name__)

# ────────── 2. Load model & scaler ─────────
MODEL_DIR = Path("model")
model     = load_model(MODEL_DIR / "model_pangan.h5")
scaler_x  = pickle.load(open(MODEL_DIR / "scaler_x.pkl", "rb"))
scaler_y  = pickle.load(open(MODEL_DIR / "scaler_y.pkl", "rb"))

# ────────── 3. Routing halaman utama ───────
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            tahun = int(request.form["tahun"])
            bulan = int(request.form["bulan"])   # 0‑11 sesuai LabelEncoder

            # Validasi sederhana
            if bulan < 0 or bulan > 11:
                raise ValueError("Bulan harus 0‑11")

            # Prediksi
            X_in          = np.array([[tahun, bulan]])
            X_scaled      = scaler_x.transform(X_in)
            y_scaled_pred = model.predict(X_scaled)
            harga_pred    = scaler_y.inverse_transform(y_scaled_pred)[0][0]

            prediction = f"{harga_pred:,.0f}"   # format ribuan
        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction)

# ────────── 4. Run app ─────────────────────
if __name__ == "__main__":
    app.run(debug=True)
