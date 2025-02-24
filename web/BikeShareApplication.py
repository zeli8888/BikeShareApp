import sys, os
# Append the project directory to the system path
sys.path.append(os.path.abspath(''))
from flask import Flask, Blueprint, jsonify
from src.controller.StationController import station_blueprint
from src.repository.usage import *

app = Flask(__name__)
app.register_blueprint(station_blueprint, url_prefix='/api')

@app.route("/")
def hello():
    return f"{LOCAL_DB}"

if __name__ == "__main__":
    app.run(debug=True)