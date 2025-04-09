from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Hourly(db.Model):
    """
    Represents the hourly weather entity, storing information about the hourly weather.

    Attributes:
        district (str): The district associated with the hourly weather.
        dt (datetime): The date and time of the hourly weather.
        future_dt (datetime): The future date and time of the hourly weather.
        temp (float): The temperature of the hourly weather.
        feels_like (float): The feels-like temperature of the hourly weather.
        pressure (int): The pressure of the hourly weather.
        humidity (int): The humidity of the hourly weather.
        dew_point (float): The dew point of the hourly weather.
        clouds (int): The cloudiness of the hourly weather.
        uvi (float): The UV index of the hourly weather.
        visibility (int): The visibility of the hourly weather.
        wind_speed (float): The wind speed of the hourly weather.
        wind_gust (float): The wind gust of the hourly weather.
        wind_deg (int): The wind direction of the hourly weather.
        pop (float): The precipitation probability of the hourly weather.
        rain_1h (float): The amount of rain in the last hour of the hourly weather.
        snow_1h (float): The amount of snow in the last hour of the hourly weather.
        weather_id (int): The ID of the hourly weather.
        weather_main (str): The main description of the hourly weather.
        weather_description (str): The detailed description of the hourly weather.
        weather_icon (str): The icon representing the hourly weather.

    Methods:
        as_dict(): Returns a dictionary representation of the Hourly object.
        __repr__(): Returns a string representation of the Hourly object.
    """
    
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
        """
        Returns a dictionary representation of the Hourly object.

        The dictionary includes all columns of the Hourly object, with datetime
        values converted to the local timezone.

        Returns:
            dict: A dictionary representation of the Hourly object.
        """
        local_tz = get_localzone()  # Automatically get the local timezone
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime):
                try:
                    result[c.name] = value.astimezone(local_tz).isoformat()
                except Exception: # avoid 1970-01-01 timestamp causing errors
                    result[c.name] = value
            else:
                result[c.name] = value
        return result
    def __repr__(self):
        """
        Returns a string representation of the Hourly object.

        The string includes the district, date/time, and future date/time of the hourly weather.

        Returns:
            str: A string representation of the Hourly object.
        """

        return f"Hourly(district='{self.district}', dt='{self.dt}', future_dt='{self.future_dt}')"
