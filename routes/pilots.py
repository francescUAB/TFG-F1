from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
from sqlalchemy.types import Float
from models import Piloto, Driver, DriverSkill, ConstructorDescribe
from datetime import date

pilots_bp = Blueprint('pilots_bp', __name__)

@pilots_bp.route('/pilots', methods=['GET'])
def obtener_pilotos():
    try:
        circuit = request.args.get('circuit')
        season = request.args.get('season')

        if not circuit or not season:
            return jsonify({"error": "Debes proporcionar un circuito y un año"}), 400

     
        pilotos = (
            Piloto.query
            .join(Driver, Piloto.driverid == Driver.driverid)
            .join(DriverSkill, (Piloto.driverid == DriverSkill.driverid) & (DriverSkill.season_year == season))
            .join(ConstructorDescribe, 
                  (Piloto.constructorid == ConstructorDescribe.constructorid) & 
                  (ConstructorDescribe.season_year == season))
            .filter(Piloto.circuitid == circuit, Piloto.season == season)
            .add_columns(
                Piloto.raceid,  # Agregado explícitamente
                Driver.surname,
                Driver.dob,  # Se agrega para calcular la edad
                Piloto.driverid,
                Piloto.constructorid,
                Piloto.position,
                Piloto.q1,
                Piloto.q2,
                Piloto.q3,
                func.least(
                    func.coalesce(func.cast(func.split_part(Piloto.q1, ":", 1), Float) * 60 +
                                  func.cast(func.split_part(Piloto.q1, ":", 2), Float), 9999),
                    func.coalesce(func.cast(func.split_part(Piloto.q2, ":", 1), Float) * 60 +
                                  func.cast(func.split_part(Piloto.q2, ":", 2), Float), 9999),
                    func.coalesce(func.cast(func.split_part(Piloto.q3, ":", 1), Float) * 60 +
                                  func.cast(func.split_part(Piloto.q3, ":", 2), Float), 9999)
                ).label('best_driver_time'),
                func.min(
                    func.least(
                        func.coalesce(func.cast(func.split_part(Piloto.q1, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q1, ":", 2), Float), 9999),
                        func.coalesce(func.cast(func.split_part(Piloto.q2, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q2, ":", 2), Float), 9999),
                        func.coalesce(func.cast(func.split_part(Piloto.q3, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q3, ":", 2), Float), 9999)
                    )
                ).over().label('session_best_time'),
                (
                    func.least(
                        func.coalesce(func.cast(func.split_part(Piloto.q1, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q1, ":", 2), Float), 9999),
                        func.coalesce(func.cast(func.split_part(Piloto.q2, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q2, ":", 2), Float), 9999),
                        func.coalesce(func.cast(func.split_part(Piloto.q3, ":", 1), Float) * 60 +
                                      func.cast(func.split_part(Piloto.q3, ":", 2), Float), 9999)
                    ) -
                    func.min(
                        func.least(
                            func.coalesce(func.cast(func.split_part(Piloto.q1, ":", 1), Float) * 60 +
                                          func.cast(func.split_part(Piloto.q1, ":", 2), Float), 9999),
                            func.coalesce(func.cast(func.split_part(Piloto.q2, ":", 1), Float) * 60 +
                                          func.cast(func.split_part(Piloto.q2, ":", 2), Float), 9999),
                            func.coalesce(func.cast(func.split_part(Piloto.q3, ":", 1), Float) * 60 +
                                          func.cast(func.split_part(Piloto.q3, ":", 2), Float), 9999)
                        )
                    ).over()
                ).label('time_difference'),
                DriverSkill.experience_scaled,
                DriverSkill.habilidad,
                ConstructorDescribe.experience.label('constructor_experience'),
                ConstructorDescribe.fiability.label('constructor_fiability'),
                ConstructorDescribe.performance.label('constructor_performance')
            )
            .all()
        )

        
        def calcular_edad(dob):
            if dob is None:
                return None
            today = date.today()
   
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

     
        resultado = []
        for piloto in pilotos:
            edad = calcular_edad(piloto.dob)
            resultado.append({
                "raceid": piloto.raceid,
                "driverid": piloto.driverid,
                "surname": piloto.surname,
                "age": edad,
                "constructorid": piloto.constructorid,
                "position": piloto.position,
                "q1": piloto.q1,
                "q2": piloto.q2,
                "q3": piloto.q3,
                "best_driver_time": piloto.best_driver_time,
                "session_best_time": piloto.session_best_time,
                "time_difference": piloto.time_difference,
                "experience_scaled": piloto.experience_scaled,
                "habilidad": piloto.habilidad,
                "constructor_experience": piloto.constructor_experience,
                "constructor_fiability": piloto.constructor_fiability,
                "constructor_performance": piloto.constructor_performance
            })

        return jsonify(resultado), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
