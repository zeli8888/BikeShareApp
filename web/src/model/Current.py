from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Current(db.Model):
    """
    Represents the current weather entity, storing information about the current weather.

    Attributes:
        district (str): The district associated with the current weather.
        dt (datetime): The date and time of the current weather.
        sunrise (datetime): The sunrise time of the current weather.
        sunset (datetime): The sunset time of the current weather.
        temp (float): The temperature of the current weather.
        feels_like (float): The feels-like temperature of the current weather.
        pressure (int): The pressure of the current weather.
        humidity (int): The humidity of the current weather.
        dew_point (float): The dew point of the current weather.
        clouds (int): The cloudiness of the current weather.
        uvi (float): The UV index of the current weather.
        visibility (int): The visibility of the current weather.
        wind_speed (float): The wind speed of the current weather.
        wind_gust (float): The wind gust of the current weather.
        wind_deg (int): The wind direction of the current weather.
        rain_1h (float): The amount of rain in the last hour.
        snow_1h (float): The amount of snow in the last hour.
        weather_id (int): The ID of the current weather.
        weather_main (str): The main description of the current weather.
        weather_description (str): The detailed description of the current weather.
        weather_icon (str): The icon representing the current weather.

    Methods:
        as_dict(): Returns a dictionary representation of the Current object.
        __repr__(): Returns a string representation of the Current object.
    """
    
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
        """
        Returns a dictionary representation of the Current object.

        The dictionary includes all columns of the Current object, with datetime
        values converted to the local timezone.

        Returns:
            dict: A dictionary representation of the Current object.
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
        Returns a string representation of the Current object.

        The string includes the district and date/time of the current weather.

        Returns:
            str: A string representation of the Current object.
        """
        return f"CurrentWeather('{self.district}', '{self.dt}')"