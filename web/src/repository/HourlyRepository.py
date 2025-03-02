from ..model import Hourly
class HourlyRepository:

    @staticmethod
    def get_by_district(district):
        latest_dt = Hourly.query.filter_by(district=district).order_by(Hourly.dt.desc()).first().dt
        return Hourly.query.filter_by(district=district, dt=latest_dt)