from .db import db
from tzlocal import get_localzone
from datetime import datetime
class Alerts(db.Model):
    """
    Represents an Alert entity, storing information about alerts in the database.

    Attributes:
        district (str): The district associated with the alert.
        sender_name (str): The name of the sender who triggered the alert.
        event (str): The event that triggered the alert.
        start_time (datetime): The start time of the alert.
        end_time (datetime): The end time of the alert.
        description (str): A description of the alert.
        tags (str): Tags associated with the alert.

    Methods:
        as_dict(): Returns a dictionary representation of the Alert object.
        __repr__(): Returns a string representation of the Alert object.
    """
    
    district = db.Column(db.String(32), primary_key=True)
    sender_name = db.Column(db.String(128), primary_key=True)
    event = db.Column(db.String(128), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    end_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    description = db.Column(db.Text)
    tags = db.Column(db.String(128))

    def as_dict(self):
        """
        Returns a dictionary representation of the Alert object.

        The dictionary includes all columns of the Alert object, with datetime
        values converted to the local timezone.

        Returns:
            dict: A dictionary representation of the Alert object.
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
        Returns a string representation of the Alert object.

        The string includes the district, sender_name, event, start_time, and
        end_time of the alert.

        Returns:
            str: A string representation of the Alert object.
        """
        return f"Alert(district='{self.district}', sender_name='{self.sender_name}', event='{self.event}', start_time='{self.start_time}', end_time='{self.end_time}')"