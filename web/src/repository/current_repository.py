from ..model import Current, db
from sqlalchemy import func, and_, exists

class CurrentRepository:
    """
    Represents a repository for managing current data.

    Methods:
        get_by_district(district): Returns the latest current data for the specified district.
        update_current(current): Updates the given current data in the database.
        delete_old_current(): Deletes old current data, keeping only the latest data for each district.
    """
    
    @staticmethod
    def get_by_district(district):
        """
        Returns the latest current data for the specified district.

        Args:
            district (str): The district for which to retrieve current data

        Returns:
            Current: The latest Current object for the specified district, or None if no data is found.
        """
        return Current.query.filter_by(district=district).order_by(Current.dt.desc()).first()
    
    @staticmethod
    def update_current(current):
        """
        Updates the given current data in the database.

        Args:
            current (Current): The current data to update
        """
        db.session.merge(current)
        db.session.commit()
        
    @staticmethod
    def delete_old_current():
        """
        Deletes old current data, keeping only the latest data for each district.
        """
        latest_updates = db.session.query(
            Current.district,
            func.max(Current.dt).label('latest_dt')
        ).group_by(Current.district).subquery()

        db.session.query(Current).filter(
            ~db.session.query(latest_updates).filter(
                and_(
                    Current.district == latest_updates.c.district,
                    Current.dt == latest_updates.c.latest_dt
                )
            ).exists()
        ).delete(synchronize_session=False)

        db.session.commit()