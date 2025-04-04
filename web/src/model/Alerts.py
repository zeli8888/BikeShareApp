from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Alerts(db.Model):

    district = db.Column(db.String(32), primary_key=True)
    sender_name = db.Column(db.String(128), primary_key=True)
    event = db.Column(db.String(128), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    end_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    description = db.Column(db.Text)
    tags = db.Column(db.String(128))

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
        return f"Alert(district='{self.district}', sender_name='{self.sender_name}', event='{self.event}', start_time='{self.start_time}', end_time='{self.end_time}')"