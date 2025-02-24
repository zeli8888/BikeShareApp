from ..repository import AvailabilityRepository
class AvailabilityService:

    @staticmethod
    def get_all_availabilities():
        return AvailabilityRepository.get_all_availabilities()
    
    @staticmethod
    def get_availability(number):
        return AvailabilityRepository.get_availability(number)