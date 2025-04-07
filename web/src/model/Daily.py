from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Daily(db.Model):
    """
    Represents the daily weather entity, storing information about the daily weather.

    Attributes:
        district (str): The district associated with the daily weather.
        dt (datetime): The date and time of the daily weather.
        future_dt (datetime): The future date and time of the daily weather.
        sunrise (datetime): The sunrise time of the daily weather.
        sunset (datetime): The sunset time of the daily weather.
        moonrise (datetime): The moonrise time of the daily weather.
        moonset (datetime): The moonset time of the daily weather.
        moon_phase (float): The moon phase of the daily weather.
        summary (str): A summary of the daily weather.
        temp_morn (float): The morning temperature of the daily weather.
        temp_day (float): The daytime temperature of the daily weather.
        temp_eve (float): The evening temperature of the daily weather.
        temp_night (float): The nighttime temperature of the daily weather.
        temp_min (float): The minimum temperature of the daily weather.
        temp_max (float): The maximum temperature of the daily weather.
        feels_like_morn (float): The feels-like morning temperature of the daily weather.
        feels_like_day (float): The feels-like daytime temperature of the daily weather.
        feels_like_eve (float): The feels-like evening temperature of the daily weather.
        feels_like_night (float): The feels-like nighttime temperature of the daily weather.
        pressure (int): The pressure of the daily weather.
        humidity (int): The humidity of the daily weather.
        dew_point (float): The dew point of the daily weather.
        wind_speed (float): The wind speed of the daily weather.
        wind_gust (float): The wind gust of the daily weather.
        wind_deg (int): The wind direction of the daily weather.
        clouds (int): The cloudiness of the daily weather.
        uvi (float): The UV index of the daily weather.
        pop (float): The precipitation probability of the daily weather.
        rain (float): The amount of rain of the daily weather.
        snow (float): The amount of snow of the daily weather.
        weather_id (int): The ID of the daily weather.
        weather_main (str): The main description of the daily weather.
        weather_description (str): The detailed description of the daily weather.
        weather_icon (str): The icon representing the daily weather.

    Methods:
        as_dict(): Returns a dictionary representation of the Daily object.
        __repr__(): Returns a string representation of the Daily object.
    """
    
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
        """
        Returns a dictionary representation of the Daily object.

        The dictionary includes all columns of the Daily object, with datetime
        values converted to the local timezone.

        Returns:
            dict: A dictionary representation of the Daily object.
        """
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
        """
        Returns a string representation of the Daily object.

        The string includes the district, date/time, and future date/time of the daily weather.

        Returns:
            str: A string representation of the Daily object.
        """

        return f"Daily(district='{self.district}', dt='{self.dt}', future_dt='{self.future_dt}')"