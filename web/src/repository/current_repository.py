from ..model import Current, db
from sqlalchemy import func, and_, exists

class CurrentRepository:
    
    @staticmethod
    def get_by_district(district):
        return Current.query.filter_by(district=district).order_by(Current.dt.desc()).first()
    
    @staticmethod
    def update_current(current):
        db.session.merge(current)
        db.session.commit()
        
    @staticmethod
    def delete_old_current():
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