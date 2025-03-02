from ..repository import AvailabilityRepository
class AvailabilityService:

    @staticmethod
    def get_all_availabilities():
        return AvailabilityRepository.get_all_availabilities()
    
    @staticmethod
    def get_availability(number):
        return AvailabilityRepository.get_availability(number)
    
    @staticmethod
    def get_latest_availabilities():
        return AvailabilityRepository.get_latest_availabilities()
    
    @staticmethod
    def get_latest_availability(number):
        return AvailabilityRepository.get_latest_availability(number)