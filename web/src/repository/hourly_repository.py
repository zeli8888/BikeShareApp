from sqlalchemy import func, and_, exists, cast, Date
from ..model import Hourly, db
class HourlyRepository:
    """
    Represents a repository for managing hourly data.

    Methods:
        get_by_district(district): Returns the latest hourly data for the specified district.
        update_hourly(hourly): Updates the given hourly data in the database.
        delete_old_hourly(): Deletes old hourly data, keeping only the latest data for each district.
    """
    @staticmethod
    def get_by_district(district):
        """
        Returns the latest hourly data for the specified district.

        Args:
            district (str): The district for which to retrieve hourly data

        Returns:
            list[Hourly]: A list of Hourly objects representing the latest data for the specified district.
        """
        latest_dt = Hourly.query.filter_by(district=district).order_by(Hourly.dt.desc()).first().dt
        return Hourly.query.filter_by(district=district, dt=latest_dt)
    
    @staticmethod
    def update_hourly(hourly):
        """
        Updates the given hourly data in the database.

        Args:
            hourly (Hourly): The hourly data to update
        """
        db.session.merge(hourly)
        db.session.commit()
        
    @staticmethod
    def delete_old_hourly():
        """
        Deletes old hourly data, keeping only the latest data for each district.
        """
        latest_updates = db.session.query(
            Hourly.district,
            func.max(Hourly.dt).label('latest_dt')
        ).group_by(Hourly.district).subquery()

        db.session.query(Hourly).filter(
            ~db.session.query(latest_updates).filter(
                and_(
                    Hourly.district == latest_updates.c.district,
                    Hourly.dt == latest_updates.c.latest_dt
                )
            ).exists()
        ).delete(synchronize_session=False)

        db.session.commit()