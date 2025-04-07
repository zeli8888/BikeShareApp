from sqlalchemy import func, and_, exists
from ..model import Daily, db
class DailyRepository:
    """
    Represents a repository for managing daily data.

    Methods:
        get_by_district(district): Returns the latest daily data for the specified district.
        update_daily(daily): Updates the given daily data in the database.
        delete_old_daily(): Deletes old daily data, keeping only the latest data for each district.
    """

    @staticmethod
    def get_by_district(district):
        """
        Returns the latest daily data for the specified district.

        Args:
            district (str): The district for which to retrieve daily data

        Returns:
            list[Daily]: A list of Daily objects representing the latest data for the specified district.
        """
        latest_dt = Daily.query.filter_by(district=district).order_by(Daily.dt.desc()).first().dt
        return Daily.query.filter_by(district=district, dt=latest_dt)
    
    @staticmethod
    def update_daily(daily):
        """
        Updates the given daily data in the database.

        Args:
            daily (Daily): The daily data to update
        """
        db.session.merge(daily)
        db.session.commit()
        
    @staticmethod
    def delete_old_daily():
        """
        Deletes old daily data, keeping only the latest data for each district.
        """
        latest_updates = db.session.query(
            Daily.district,
            func.max(Daily.dt).label('latest_dt')
        ).group_by(Daily.district).subquery()

        db.session.query(Daily).filter(
            ~db.session.query(latest_updates).filter(
                and_(
                    Daily.district == latest_updates.c.district,
                    Daily.dt == latest_updates.c.latest_dt
                )
            ).exists()
        ).delete(synchronize_session=False)

        db.session.commit()