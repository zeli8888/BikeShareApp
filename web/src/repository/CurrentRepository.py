from ..model import Current

class CurrentRepository:
    
    @staticmethod
    def get_by_district(district):
        return Current.query.filter_by(district=district).order_by(Current.dt.desc()).first()