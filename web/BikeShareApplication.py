import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Set to 3 to hide all logs, warnings, and errors
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import argparse
from flask import Flask, render_template, url_for
from src.controller import *
from src.config import *
import tensorflow as tf
tf.config.set_soft_device_placement(True)

def main(database='LOCAL'):
    
    app = Flask(__name__)
    if os.getenv(f'{database}_DB_BIKES_URL') is None:
        raise Exception(f"Invalid database choice, check your system variable for {database}_DB_BIKES_URL!")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(f'{database}_DB_BIKES_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(bikes_blueprint, url_prefix='/api')
    app.register_blueprint(weather_blueprint, url_prefix='/api')
    app.register_blueprint(prediction_blueprint, url_prefix='/api')
    
    @app.route("/")
    def index():
        return render_template("index.html",
                               GOOGLE_MAP_ID=GOOGLE_MAP_ID, 
                               GOOGLE_MAP_KEY=GOOGLE_MAP_KEY,
                               BIKES_URL=url_for('bikes.get_all_bikes', _external=True),
                               WEATHER_URL=url_for('weather.get_weather_by_district', _external=True),
                               CURRENT_BIKES_URL=url_for('bikes.get_all_current_bikes', _external=True),
                               CURRENT_WEATHER_URL=url_for('weather.get_current_weather_by_district', _external=True),
                               BIKES_ONE_DAY_URL=url_for('bikes.get_one_day_availability', _external=True),
                               BIKES_ONE_DAY_STATION_URL=url_for('bikes.get_one_day_availability', _external=True) + '/{}',
                               PREDICTION_URL=url_for('prediction.get_prediction_by_station', _external=True, station_id=1),
                               )
    
    return app

if __name__ == "__main__":
    # to run: 
    # python BikeShareApplication.py --database 'EC2' --no_debug
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--no_debug', action='store_true')
    args = parser.parse_args()
    app = main(args.database)
    if args.database == 'EC2':
        app.run(host='0.0.0.0', port=5000, debug=not args.no_debug)
    else:
        app.run(debug=not args.no_debug)