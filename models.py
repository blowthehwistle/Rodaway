from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    english_name = db.Column(db.String(80))
    baptism_name = db.Column(db.String(80))
    grade = db.Column(db.String(10))
    phone_number = db.Column(db.String(15))
