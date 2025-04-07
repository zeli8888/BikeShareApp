from .db import db

class Station(db.Model):
    """
    Represents a Station entity, storing information about bike stations.

    Attributes:
        number (int): The unique number of the station.
        address (str): The address of the station.
        banking (int): The banking status of the station.
        bike_stands (int): The number of bike stands at the station.
        name (str): The name of the station.
        position_lat (float): The latitude of the station's position.
        position_lng (float): The longitude of the station's position.

    Methods:
        as_dict(): Returns a dictionary representation of the Station object.
        __repr__(): Returns a string representation of the Station object.
    """
    
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(128))
    banking = db.Column(db.Integer)
    bike_stands = db.Column(db.Integer)
    name = db.Column(db.String(128))
    position_lat = db.Column(db.Float)
    position_lng = db.Column(db.Float)

    def as_dict(self):
        """
        Returns a dictionary representation of the Station object.

        The dictionary includes all columns of the Station object.

        Returns:
            dict: A dictionary representation of the Station object.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        """
        Returns a string representation of the Station object.

        The string includes the name of the station.

        Returns:
            str: A string representation of the Station object.
        """
        return f'<Station {self.name}>'