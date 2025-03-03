import argparse
from flask import Flask, render_template, jsonify
from src.controller import *
from src.config import *

def main(database='LOCAL'):
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = globals()[database+"_DB_BIKES_URL"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(station_blueprint, url_prefix='/api')
    app.register_blueprint(availability_blueprint, url_prefix='/api')
    app.register_blueprint(weather_blueprint, url_prefix='/api')

    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/map")
    def map():
        return render_template("map.html", GOOGLE_MAP_ID=GOOGLE_MAP_ID, GOOGLE_MAP_KEY=GOOGLE_MAP_KEY)
    
    return app

if __name__ == "__main__":
    # to run: 
    # python BikeShareApplication.py --database 'EC2' --no_debug
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--no_debug', action='store_true')
    args = parser.parse_args()
    app = main(args.database)
    app.run(debug=not args.no_debug)