from app import db
from datetime import datetime

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    transmission = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)
    rent = db.Column(db.Boolean, default=False)

