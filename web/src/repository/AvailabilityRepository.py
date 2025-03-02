from ..model import Availability
from sqlalchemy import func, and_

class AvailabilityRepository:

    @staticmethod
    def get_all_availabilities():
        return Availability.query.all()
    
    @staticmethod
    def get_availability(number):
        return Availability.query.filter_by(number=number)
    
    @staticmethod
    def get_latest_availabilities():
        latest_updates = Availability.query.with_entities(Availability.number, func.max(Availability.last_update).label('latest_update')).group_by(Availability.number).subquery()
        return Availability.query.join(latest_updates, and_(Availability.number == latest_updates.c.number, Availability.last_update == latest_updates.c.latest_update)).order_by(Availability.number).all()
    @staticmethod
    def get_latest_availability(number):
        return Availability.query.filter_by(number=number).order_by(Availability.last_update.desc()).first()