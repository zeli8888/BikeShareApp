from ..model import Alerts, db
from datetime import datetime, timedelta
class AlertsRepository:
    """
    Represents a repository for managing alerts.

    Methods:
        get_by_district(district): Retrieves all active alerts for the given district.
        update_alerts(alerts): Updates the given alerts in the database.
        delete_old_alerts(): Deletes all alerts that have ended.
    """
    
    @staticmethod
    def get_by_district(district):
        """
        Retrieves all active alerts for the given district.

        Args:
            district (str): The district for which to retrieve alerts

        Returns:
            list[Alert]: A list of Alert objects representing the alerts that start within the next day and are still active for the given district.
        """
        current_time = datetime.now()
        one_day_later = current_time + timedelta(days=1)
        return Alerts.query.filter_by(district=district).filter(Alerts.start_time < one_day_later, Alerts.end_time > current_time).all()
    
    @staticmethod
    def update_alerts(alerts):
        """
        Updates the given alerts in the database.

        Args:
            alerts (list[Alert]): The alerts to update
        """
        db.session.merge(alerts)
        db.session.commit()
        
    @staticmethod
    def delete_old_alerts():
        """
        Deletes all alerts that have ended.
        """
        db.session.query(Alerts).filter(Alerts.end_time < datetime.now()).delete(synchronize_session=False)
        db.session.commit()