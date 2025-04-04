from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Current(db.Model):

    district = db.Column(db.String(32), primary_key=True)
    dt = db.Column(db.DateTime, nullable=False, primary_key=True)
    sunrise = db.Column(db.DateTime)
    sunset = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    dew_point = db.Column(db.Float)
    clouds = db.Column(db.Integer)
    uvi = db.Column(db.Float)
    visibility = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    wind_gust = db.Column(db.Float)
    wind_deg = db.Column(db.Integer)
    rain_1h = db.Column(db.Float)
    snow_1h = db.Column(db.Float)
    weather_id = db.Column(db.Integer)
    weather_main = db.Column(db.String(128))
    weather_description = db.Column(db.String(128))
    weather_icon = db.Column(db.String(32))

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
        return f"CurrentWeather('{self.district}', '{self.dt}')"