from sqlalchemy import func, and_, exists
from ..model import Daily, db
class DailyRepository:

    @staticmethod
    def get_by_district(district):
        latest_dt = Daily.query.filter_by(district=district).order_by(Daily.dt.desc()).first().dt
        return Daily.query.filter_by(district=district, dt=latest_dt)
    
    @staticmethod
    def update_daily(daily):
        db.session.merge(daily)
        db.session.commit()
        
    @staticmethod
    def delete_old_daily():
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