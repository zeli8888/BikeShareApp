from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Availability(db.Model):
    number = db.Column(db.Integer, db.ForeignKey('station.number'), primary_key=True)
    last_update = db.Column(db.DateTime, primary_key=True)
    available_bikes = db.Column(db.Integer, nullable=False)
    available_bike_stands = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(128), nullable=False)

    def as_dict(self):
        local_tz = get_localzone()  # Automatically get the local timezone
        return {
            c.name: (
                getattr(self, c.name).astimezone(local_tz).isoformat() 
                if isinstance(getattr(self, c.name), datetime) 
                else getattr(self, c.name)
            ) 
            for c in self.__table__.columns
        }
    def __repr__(self):
        return f'<Availability {self.number}, {self.last_update}>'