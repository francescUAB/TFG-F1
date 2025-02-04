from flask import request, jsonify, Blueprint
from joblib import load
import os
import pandas as pd

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Datos recibidos para predicción:", data)
        
        if 'model' not in data:
            return jsonify({"error": "Falta el campo requerido: model"}), 400

        model_type = data['model']
        
        if model_type == "Random Forest":
            ruta_modelo = os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\Random Forest models\random_forest_model_agrupacio_1.pkl')
            ruta_escalador = os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\Random Forest models\scaler_rf_agrupacio_1.pkl')
        elif model_type == "SVM":
            ruta_modelo = os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\SVM models\svm_model_agrupacio_1.pkl')
            ruta_escalador = os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\SVM models\scaler_agrupacio_1.pkl')
        else:
            return jsonify({"error": "Modelo no reconocido. Las opciones válidas son 'Random Forest' y 'SVM'."}), 400
        
        if not os.path.exists(ruta_modelo):
            return jsonify({"error": f"El archivo de modelo no existe: {ruta_modelo}"}), 500
        if not os.path.exists(ruta_escalador):
            return jsonify({"error": f"El archivo de escalador no existe: {ruta_escalador}"}), 500
        
        try:
            modelo = load(ruta_modelo)
            escalador = load(ruta_escalador)
            if escalador is None:
                return jsonify({"error": "El escalador cargado es None. Verifica el archivo."}), 500
        except Exception as e:
            return jsonify({"error": f"Error al cargar el modelo o escalador: {str(e)}"}), 500

        required_fields = [
            'constructorid', 
            'circuitid', 
            'grid', 
            'experience', 
            'hability',
            'constructor_experience', 
            'constructor_fiability', 
            'constructor_performance',
            'gap_to_best_time', 
            'age'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

        try:
            features = {
                'constructorid': int(data['constructorid']),
                'circuitid': int(data['circuitid']),
                'grid': int(data['grid']),
                'experience': float(data['experience']),
                'hability': float(data['hability']),
                'constructor_experience': float(data['constructor_experience']),
                'constructor_fiability': float(data['constructor_fiability']),
                'constructor_performance': float(data['constructor_performance']),
                'gap_to_best_time': float(data['gap_to_best_time']),
                'age': float(data['age'])
            }
        except Exception as e:
            return jsonify({"error": f"Error al convertir datos: {str(e)}"}), 400

        columns = [
            'constructorid', 
            'circuitid', 
            'grid', 
            'experience', 
            'hability',
            'constructor_experience', 
            'constructor_fiability', 
            'constructor_performance',
            'gap_to_best_time', 
            'age'
        ]
        df_features = pd.DataFrame([features], columns=columns)
        print("DataFrame de características para predicción:")
        print(df_features)
        
        features_scaled = escalador.transform(df_features)
        pred = modelo.predict(features_scaled)
        return jsonify({'predicted_position': int(pred[0])}), 200

    except Exception as e:
        print("Error en la predicción:", str(e))
        return jsonify({"error": str(e)}), 500
