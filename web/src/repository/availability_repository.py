from ..model import Availability, db
from sqlalchemy import func, and_, exists, cast, Date

class AvailabilityRepository:
    """
    Represents a repository for managing availability data.

    Methods:
        get_latest_availabilities(): Returns the latest availability data for each station.
        update_availability(availability): Updates the given availability data in the database.
        delete_old_availabilities(keep_date): Deletes old availability data, keeping only the latest data for each station and data for the specified keep_date.
        get_one_day_availability(keep_date): Returns all availability data for the specified keep_date.
        get_one_day_availability_for_station(keep_date, station_number): Returns all availability data for the specified keep_date and station number.
    """
    
    @staticmethod
    def get_latest_availabilities():
        """
        Returns the latest availability data for each station, ordered by last_update (newest first).

        Returns:
            list[Availability]: A list of Availability objects representing the latest data for each station.
        """
        latest_updates = Availability.query.with_entities(Availability.number, func.max(Availability.last_update).label('latest_update')).group_by(Availability.number).subquery()
        return Availability.query.join(latest_updates, and_(Availability.number == latest_updates.c.number, Availability.last_update == latest_updates.c.latest_update)).order_by(Availability.last_update.desc()).all()
        
    @staticmethod
    def update_availability(availability):
        """
        Updates the given availability data in the database.

        Args:
            availability (Availability): The availability data to update
        """
        db.session.merge(availability)
        db.session.commit()
        
    @staticmethod
    def delete_old_availabilities(keep_date):
        """
        Deletes old availability data, keeping only the latest data for each station and data for the specified keep_date.

        Args:
            keep_date (Date): The date for which to keep availability data
        """
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
        """
        Returns all availability data for the specified keep_date.

        Args:
            keep_date (Date): The date for which to retrieve availability data

        Returns:
            list[Availability]: A list of Availability objects representing the data for the specified keep_date.
        """
        return Availability.query.filter(Availability.last_update.cast(Date) == keep_date).all()
    
    @staticmethod
    def get_one_day_availability_for_station(keep_date, station_number):
        """
        Returns all availability data for the specified keep_date and station number.

        Args:
            keep_date (Date): The date for which to retrieve availability data
            station_number (int): The station number for which to retrieve availability data

        Returns:
            list[Availability]: A list of Availability objects representing the data for the specified keep_date and station number.
        """
        return Availability.query.filter(and_(Availability.last_update.cast(Date) == keep_date, Availability.number == station_number)).all()