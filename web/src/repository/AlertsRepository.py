from ..model import Alerts, db
from datetime import datetime, timedelta
class AlertsRepository:
    
    @staticmethod
    def get_by_district(district):
        """Retrieves all active alerts for the given district.

        Args:
            district: The district for which to retrieve alerts

        Returns:
            A list of Alert objects representing the alerts that start within the next day and are still active for the given district.
        """
        current_time = datetime.now()
        one_day_later = current_time + timedelta(days=1)
        return Alerts.query.filter_by(district=district).filter(Alerts.start_time < one_day_later, Alerts.end_time > current_time).all()
    
    @staticmethod
    def update_alerts(alerts):
        db.session.merge(alerts)
        db.session.commit()
        
    @staticmethod
    def delete_old_alerts():
        db.session.query(Alerts).filter(Alerts.end_time < datetime.now()).delete(synchronize_session=False)
        db.session.commit()