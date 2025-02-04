import pandas as pd
from joblib import load
import os


modelo = load(os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\SVM models\svm_model_agrupacio_1.pkl'))
escalador = load(os.path.abspath(r'C:\Users\Lenovo\Desktop\TFG\TFG GIT\TFG\F1_prediction_all_circuits\SVM models\scaler_agrupacio_1.pkl'))

datos_prueba = {
    'constructorid': 117,
    'circuitid': 4,
    'experience_scaled': 100.0,
    'habilidad': 84.0,
    'constructor_experience': 7.0,
    'constructor_fiability': 73.0,
    'constructor_performance': 78.0,
    'best_driver_time': 72.128,
    'time_difference': 0.745
}

df_prueba = pd.DataFrame([datos_prueba])
print("Datos de prueba:")
print(df_prueba)

df_prueba_scaled = escalador.transform(df_prueba)
pred = modelo.predict(df_prueba_scaled)
print("Predicción:")
print(pred)
