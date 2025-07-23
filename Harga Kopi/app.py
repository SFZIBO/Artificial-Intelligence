from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model regresi linear untuk harga kopi
model = joblib.load('model/regresi_linear_kopi.joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        kode_kabupaten_kota = int(request.form['kode_kabupaten_kota'])
        kode_bulan = int(request.form['kode_bulan'])
        
        # Format data input untuk prediksi
        input_data = np.array([[kode_kabupaten_kota, kode_bulan]])
        prediksi = model.predict(input_data)[0]  # Ambil nilai pertama dari array
        
        return render_template('result.html', 
                               kode_kabupaten_kota=kode_kabupaten_kota,
                               kode_bulan=kode_bulan,
                               prediksi=round(prediksi, 2))  # Format hasil prediksi
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)