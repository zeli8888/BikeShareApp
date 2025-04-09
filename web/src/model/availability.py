from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Availability(db.Model):
    """
    Represents an Availability entity, storing information about bike availability.

    Attributes:
        number (int): The number of the station.
        last_update (datetime): The last update time of the availability.
        available_bikes (int): The number of available bikes.
        available_bike_stands (int): The number of available bike stands.
        status (str): The status of the availability.

    Methods:
        as_dict(): Returns a dictionary representation of the Availability object.
        __repr__(): Returns a string representation of the Availability object.
    """
    
    number = db.Column(db.Integer, db.ForeignKey('station.number'), primary_key=True)
    last_update = db.Column(db.DateTime, primary_key=True)
    available_bikes = db.Column(db.Integer, nullable=False)
    available_bike_stands = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(128), nullable=False)

    def as_dict(self):
        """
        Returns a dictionary representation of the Availability object.

        The dictionary includes all columns of the Availability object, with datetime
        values converted to the local timezone.

        Returns:
            dict: A dictionary representation of the Availability object.
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
        Returns a string representation of the Availability object.

        The string includes the number and last update time of the availability.

        Returns:
            str: A string representation of the Availability object.
        """
        return f'<Availability {self.number}, {self.last_update}>'
