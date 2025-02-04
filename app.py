from flask import Flask
from db import db
from routes.circuits import circuits_bp
from routes.pilots import pilots_bp  
from routes.predict import predict_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:francesc1998@127.0.0.1:5432/f1_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(circuits_bp)
app.register_blueprint(pilots_bp) 
app.register_blueprint(predict_bp) 

@app.route('/')
def index():
    return {"mensaje": "Bienvenido a la API de Fórmula 1"}

if __name__ == '__main__':
    app.run(debug=True)
