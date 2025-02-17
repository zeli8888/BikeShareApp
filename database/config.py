# Define remote database connection URL
REMOTE_USER = "admin"  # Your RDS username
REMOTE_PASSWORD = "as5071565"  # Your RDS password
REMOTE_URI = "127.0.0.1"  # Localhost because of SSH tunnel
REMOTE_PORT = "3333"  # Must match your tunnel port
REMOTE_DB = "dbbikes"  # Change to your database name

# Define local database connection URL
LOCAL_USER = "root"
LOCAL_PASSWORD = "as5071565"
LOCAL_URI = "127.0.0.1"
LOCAL_PORT = "3306"
LOCAL_DB = "local_dbbikes"

# Define jcdecaux URI
JCKEY = "a2e6d3120f108a84141fc12b5ea5beedba83906a"
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
# to check, just enter this in browser:
# https://api.jcdecaux.com/vls/v1/stations?JCKEY=a2e6d3120f108a84141fc12b5ea5beedba83906a?NAME=dublin

# Define OpenWeather URI
OPEN_WEATHER_KEY = "80f2c5a407c58ec93a6034f3d54aaef7"
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
OPEN_WEATHER_DUBLIN_LOC = ("53.3498006", "-6.2602964")
OPEN_WEATHER_URI = f"https://api.openweathermap.org/data/3.0/onecall"
# to check, just enter this in browser:
# https://api.openweathermap.org/data/3.0/onecall?lat=53.3498006&lon=-6.2602964&appid=80f2c5a407c58ec93a6034f3d54aaef7