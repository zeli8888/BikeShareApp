import argparse
from flask import Flask
from src.controller import *
from src.config import *

def main(database='LOCAL'):
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        globals()[database+"_USER"], 
        globals()[database+"_PASSWORD"], 
        globals()[database+"_URI"], 
        globals()[database+"_PORT"], 
        globals()[database+"_DB"]
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(station_blueprint, url_prefix='/api')
    app.register_blueprint(availability_blueprint, url_prefix='/api')

    @app.route("/")
    def hello():
        return f"Hello World~~~"
    
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