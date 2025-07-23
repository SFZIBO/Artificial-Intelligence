from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

# Load model dan scaler
try:
    model = load_model('saved_models/stock_model.keras')
    scaler_X = joblib.load('saved_models/scaler_X.pkl')
    scaler_y = joblib.load('saved_models/scaler_y.pkl')
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [
            float(request.form['open']),
            float(request.form['high']),
            float(request.form['low']),
            float(request.form['volume']),
            float(request.form['7d_avg'])
        ]
        
        input_scaled = scaler_X.transform(np.array(features).reshape(1, -1))
        pred_scaled = model.predict(input_scaled)
        pred_actual = scaler_y.inverse_transform(pred_scaled)
        
        return render_template(
            'index.html',
            prediction=f"Rp {pred_actual[0][0]:,.2f}",
            show_result=True
        )
    except Exception as e:
        return render_template(
            'index.html',
            error=f"Error: {str(e)}",
            show_result=False
        )

if __name__ == '__main__':
    app.run(debug=True)