'''
***WARNING:*** if it stops working:
- delete browsing data OR
- go in incognito mode OR
- open new window OR
- sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
'''
from flask import Flask, g, render_template, jsonify
import json
from sqlalchemy import create_engine

USER = "root"
PASSWORD = ""
PORT = "3306"
DB = ""
URI = "127.0.0.1"

# Connect to the database and create the engine variable
def connect_to_db():
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)
    engine = create_engine(connection_string, echo = True)
    
    return engine

# Create the engine variable and store it in the global Flask variable 'g'
def get_db():
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine

app = Flask(__name__, static_url_path='')

@app.route("/")
def main():
    return render_template("index.html")

# Show all stations in json
@app.route('/stations')
def get_stations():
    engine = get_db()
    
    stations = []
    rows = engine.execute("SELECT * from station;")
    
    for row in rows:
        stations.append(dict(row))
    
    return jsonify(stations)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)