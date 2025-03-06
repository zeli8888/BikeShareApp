from sqlalchemy import func, and_, exists, cast, Date
from ..model import Hourly, db
class HourlyRepository:

    @staticmethod
    def get_by_district(district):
        latest_dt = Hourly.query.filter_by(district=district).order_by(Hourly.dt.desc()).first().dt
        return Hourly.query.filter_by(district=district, dt=latest_dt)
    
    @staticmethod
    def update_hourly(hourly):
        db.session.merge(hourly)
        db.session.commit()
        
    @staticmethod
    def delete_old_hourly():
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