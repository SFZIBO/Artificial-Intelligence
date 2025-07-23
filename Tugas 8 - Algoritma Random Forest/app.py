from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import joblib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model
model = joblib.load('model/garbage_classifier.pkl')
classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Ekstrak fitur dan prediksi
    features = extract_features(filepath).reshape(1, -1)
    prediction = model.predict(features)[0]
    result = classes[prediction]
    
    return render_template('result.html', 
                           image_path=filepath, 
                           prediction=result)