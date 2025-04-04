from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Daily(db.Model):

    district = db.Column(db.String(32), primary_key=True)
    dt = db.Column(db.DateTime, nullable=False, primary_key=True)
    future_dt = db.Column(db.DateTime, nullable=False, primary_key=True)
    sunrise = db.Column(db.DateTime)
    sunset = db.Column(db.DateTime)
    moonrise = db.Column(db.DateTime)
    moonset = db.Column(db.DateTime)
    moon_phase = db.Column(db.Float)
    summary = db.Column(db.String(256))
    temp_morn = db.Column(db.Float)
    temp_day = db.Column(db.Float)
    temp_eve = db.Column(db.Float)
    temp_night = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    feels_like_morn = db.Column(db.Float)
    feels_like_day = db.Column(db.Float)
    feels_like_eve = db.Column(db.Float)
    feels_like_night = db.Column(db.Float)
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    dew_point = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_gust = db.Column(db.Float)
    wind_deg = db.Column(db.Integer)
    clouds = db.Column(db.Integer)
    uvi = db.Column(db.Float)
    pop = db.Column(db.Float)
    rain = db.Column(db.Float)
    snow = db.Column(db.Float)
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
        return f"Daily(district='{self.district}', dt='{self.dt}', future_dt='{self.future_dt}')"