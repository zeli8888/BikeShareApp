from ..model import Availability
class AvailabilityRepository:

    @staticmethod
    def get_all_availabilities():
        return Availability.query.all()
    
    @staticmethod
    def get_availability(number):
        return Availability.query.filter_by(number=number).order_by(Availability.last_update.desc()).first()
