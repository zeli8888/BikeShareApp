from ..model import Station

class StationRepository:

    @staticmethod
    def get_station_by_number(number):
        """
        Retrieve a station by its number.
        """
        return Station.query.get(number)

    @staticmethod
    def get_all_stations():
        """
        Retrieve all stations from the database.
        """
        return Station.query.all()