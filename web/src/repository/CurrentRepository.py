from ..model import Current, db

class CurrentRepository:
    
    @staticmethod
    def get_by_district(district):
        return Current.query.filter_by(district=district).order_by(Current.dt.desc()).first()
    
    @staticmethod
    def update_current(current):
        db.session.merge(current)
        db.session.commit()
        
    # @staticmethod
    # def delete_old_current():
    #     latest_updates = db.session.query(
    #         Current.district, 
    #     )