from db import db

class Circuit(db.Model):
    __tablename__ = 'circuits'

    circuitid = db.Column(db.Integer, primary_key=True)
    circuitref = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    country = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    alt = db.Column(db.Integer)
    url = db.Column(db.String(200))


class Piloto(db.Model):
    __tablename__ = 'qualifying'  # Cambia esto al nombre real de tu tabla
    
    raceid = db.Column(db.Integer, primary_key=True)
    driverid = db.Column(db.Integer, primary_key=True)
    constructorid = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=True)
    season = db.Column(db.Integer, nullable=False)
    circuitid = db.Column(db.Integer, nullable=False)
    q1 = db.Column(db.String(20),nullable=True)
    q2 = db.Column(db.String(20),nullable=True)
    q3 = db.Column(db.String(20),nullable=True)

class Driver(db.Model):
    __tablename__ = 'drivers'

    driverid = db.Column(db.Integer, primary_key=True)
    driverref = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer)
    code = db.Column(db.String(3))
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date)
class DriverSkill(db.Model):
    __tablename__ = 'driver_skill_per_season'  

    driverid = db.Column(db.Integer, primary_key=True)
    season_year = db.Column(db.Integer, primary_key=True)
    experience_scaled = db.Column(db.Float, nullable=False)
    habilidad = db.Column(db.Float, nullable=False)

class ConstructorDescribe(db.Model):
    __tablename__ = 'constructor_describe_per_season'

    constructorid = db.Column(db.Integer, primary_key=True)
    season_year = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Float, nullable=False)
    fiability = db.Column(db.Float, nullable=False)
    performance = db.Column(db.Float, nullable=False)