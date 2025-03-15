from ..model import Availability, db
from sqlalchemy import func, and_, exists, cast, Date

class AvailabilityRepository:

    @staticmethod
    def get_latest_availabilities():
        '''
        return latest data for each station in a list, ordered by last_update (newest first)
        '''
        latest_updates = Availability.query.with_entities(Availability.number, func.max(Availability.last_update).label('latest_update')).group_by(Availability.number).subquery()
        return Availability.query.join(latest_updates, and_(Availability.number == latest_updates.c.number, Availability.last_update == latest_updates.c.latest_update)).order_by(Availability.last_update.desc()).all()
        
    @staticmethod
    def update_availability(availability):
        db.session.merge(availability)
        db.session.commit()
        
    @staticmethod
    def delete_old_availabilities(keep_date):
        # Subquery to get the latest last_update for each station
        latest_updates = db.session.query(
            Availability.number,
            func.max(Availability.last_update).label('latest_last_update')
        ).group_by(Availability.number).subquery()

        # Delete rows that are not the latest or not on the specified keep_date
        db.session.query(Availability).filter(
            ~db.session.query(latest_updates).filter(
                and_(
                    Availability.number == latest_updates.c.number,
                    Availability.last_update == latest_updates.c.latest_last_update
                )
            ).exists() &
            (Availability.last_update.cast(Date) != keep_date)
        ).delete(synchronize_session=False)

        db.session.commit()
        
    @staticmethod
    def get_one_day_availability(keep_date):
        return Availability.query.filter(Availability.last_update.cast(Date) == keep_date).all()
    
    @staticmethod
    def get_one_day_availability_for_station(keep_date, station_number):
        return Availability.query.filter(and_(Availability.last_update.cast(Date) == keep_date, Availability.number == station_number)).all()