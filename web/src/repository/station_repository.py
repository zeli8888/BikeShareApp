from ..model import Station, db

class StationRepository:
    """
    Represents a repository for managing station data.

    Methods:
        get_all_stations(): Retrieves all stations from the database.
        update_station(station): Updates a station in the database.
    """
    
    @staticmethod
    def get_all_stations():
        """
        Retrieves all stations from the database.

        Returns:
            list[Station]: A list of Station objects representing all stations in the database.
        """
        return Station.query.all()
    
    @staticmethod
    def update_station(station):
        """
        Updates a station in the database.

        Args:
            station (Station): The station to update
        """
        db.session.merge(station)
        db.session.commit()
        