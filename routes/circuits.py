from flask import Blueprint, jsonify
from models import Circuit


circuits_bp = Blueprint('circuits_bp', __name__)

@circuits_bp.route('/circuits', methods=['GET'])
def obtener_circuitos():
    try:
    
        circuitos = Circuit.query.all()
        resultado = [
            {
                "circuitid": c.circuitid,
                "circuitref": c.circuitref,
                "name": c.name,
                "location": c.location,
                "country": c.country,
                "lat": c.lat,
                "lng": c.lng,
                "alt": c.alt,
                "url": c.url
            }
            for c in circuitos
        ]

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
