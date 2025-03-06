from ..model import Station, db

class StationRepository:

    @staticmethod
    def get_all_stations():
        """
        Retrieve all stations from the database.
        """
        return Station.query.all()
    
    @staticmethod
    def update_station(station):
        """
        Update a station in the database.
        """
        db.session.merge(station)
        db.session.commit()
        