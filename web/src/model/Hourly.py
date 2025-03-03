from .db import db

class Hourly(db.Model):

    district = db.Column(db.String(32), primary_key=True)
    dt = db.Column(db.DateTime, nullable=False, primary_key=True)
    future_dt = db.Column(db.DateTime, nullable=False, primary_key=True)
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
    pop = db.Column(db.Float)
    rain_1h = db.Column(db.Float)
    snow_1h = db.Column(db.Float)
    weather_id = db.Column(db.Integer)
    weather_main = db.Column(db.String(128))
    weather_description = db.Column(db.String(128))
    weather_icon = db.Column(db.String(32))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"Hourly(district='{self.district}', dt='{self.dt}', future_dt='{self.future_dt}')"