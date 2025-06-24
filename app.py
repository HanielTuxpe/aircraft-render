from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import numpy as np
from flask_cors import CORS
import logging
import pickle

app = Flask(__name__)
CORS(app)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)
    
# Cargar el modelo entrenado
# model = joblib.load("air_model.pkl")
model = joblib.load("modelo_precio.pkl")
price_scaler = joblib.load('price_scaler.pkl')
x_scaler = joblib.load('x_scaler.pkl')
app.logger.debug("Modelo cargado correctamente.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos del JSON
        data = request.get_json()
        engine_power = float(data['engine_power'])
        max_speed = float(data['max_speed'])
        cruise_speed = float(data['cruise_speed'])
        landing_distance = float(data['landing_distance'])
        empty_weight = float(data['empty_weight'])
        length = float(data['length'])

        # Crear DataFrame
        data_df = pd.DataFrame(
            [[engine_power, max_speed, cruise_speed, landing_distance, empty_weight, length]],
            columns=['engine_power', 'max_speed', 'cruise_speed', 'landing_distance', 'empty_weight', 'length']
        )

        # Escalar y predecir
        scaled_df = x_scaler.transform(data_df)
        app.logger.debug(f"Datos escalados: {scaled_df}")
        
        prediction = model.predict(scaled_df)
        app.logger.debug(f"Predicción cruda: {prediction}")
        prediction_original = price_scaler.inverse_transform([[prediction[0]]])[0][0]
        app.logger.debug(f"Predicción original: {prediction_original}")

        return jsonify({'price': float(prediction_original)})

    except Exception as e:
        app.logger.error(f"Error en la predicción: {str(e)}")
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
