from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Memuat berkas biner pkl
model_lr = joblib.load('model_ipm_lr.pkl')
scaler_ipm = joblib.load('scaler_ipm.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediksi')
def prediksi_page():
    return render_template('prediksi.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features_raw = np.array([[data['ahh'], data['hls'], data['rls'], data['pengeluaran']]])
    features_scaled = scaler_ipm.transform(features_raw)
    predicted_cluster = model_lr.predict(features_scaled)[0]
    return jsonify({'cluster': int(predicted_cluster)})

if __name__ == '__main__':
    app.run(debug=True, port=8000)