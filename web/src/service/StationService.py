from ..repository import StationRepository

class StationService:

    @staticmethod
    def get_station(number):
        """
        Retrieve a station by its number.
        """
        return StationRepository.get_station_by_number(number)

    @staticmethod
    def get_all_stations():
        """
        Retrieve all stations.
        """
        return StationRepository.get_all_stations()
