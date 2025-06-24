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
        # Obtener los datos del formulario
        engine_power = float(request.form['engine_power'])
        max_speed = float(request.form['max_speed'])
        cruise_speed = float(request.form['cruise_speed'])
        landing_distance = float(request.form['landing_distance'])
        empty_weight = float(request.form['empty_weight'])
        length = float(request.form['length'])
        
        data_df = pd.DataFrame(
            [[engine_power, max_speed, cruise_speed,landing_distance, empty_weight, length]],
            columns=['engine_power', 'max_speed', 'cruise_speed','landing_distance', 'empty_weight', 'length'])

        # Escalar los datos de entrada
        scaled_df = x_scaler.transform(data_df)
        app.logger.debug(f"DataFrame escalado: {scaled_df}")
        # # Realizar la predicción
        prediction = model.predict(scaled_df)
        app.logger.debug(f"Predicción (escalada): {prediction}")
        
        prediction_original = price_scaler.inverse_transform([[prediction[0]]])[0][0]
        app.logger.debug(f"Predicción: {prediction_original}")

        # Devolver el resultado como JSON
        return jsonify({'price': float(prediction_original)})

    except Exception as e:
        app.logger.error(f"Error en la predicción: {str(e)}")
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
