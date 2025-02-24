from .db import db

class Station(db.Model):
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(128))
    banking = db.Column(db.Integer)
    bike_stands = db.Column(db.Integer)
    name = db.Column(db.String(128))
    position_lat = db.Column(db.Float)
    position_lng = db.Column(db.Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f'<Station {self.name}>'