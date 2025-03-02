from ..model import Daily
class DailyRepository:

    @staticmethod
    def get_by_district(district):
        latest_dt = Daily.query.filter_by(district=district).order_by(Daily.dt.desc()).first().dt
        return Daily.query.filter_by(district=district, dt=latest_dt)