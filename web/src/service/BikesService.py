from ..repository import StationRepository, AvailabilityRepository

class BikesService:
    @staticmethod
    def get_all_bikes():
        """
        Retrieve all stations' bikes.
        """
        bikes = {}
        bikes['stations'] = [station.as_dict() for station in StationRepository.get_all_stations()]
        bikes['availabilities'] = [availability.as_dict() for availability in AvailabilityRepository.get_latest_availabilities()]
        return bikes

    @staticmethod
    def get_bikes(number):
        """
        Retrieve one station's bikes condition.
        """
        bikes = {}
        bikes['station'] = StationRepository.get_station_by_number(number).as_dict()
        bikes['availability'] = AvailabilityRepository.get_latest_availabilities().as_dict()
        return bikes