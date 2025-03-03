import os

# Jcdecaux KEY
JCKEY = os.getenv('JCKEY')
# Google KEY
GOOGLE_MAP_KEY = os.getenv('GOOGLE_MAP_KEY')
GOOGLE_MAP_ID = os.getenv('GOOGLE_MAP_ID')
# Define OpenWeather URI
OPEN_WEATHER_KEY = os.getenv('OPEN_WEATHER_KEY')

# Define local database connection URL
LOCAL_DB_BIKES_URL = os.getenv('LOCAL_DB_BIKES_URL')

# Define remote database connection URL, use SSH tunnel through EC2 to connect to RDS, so this environment variable should be set on local computer
# make sure system variable EC2_PEM is added at first, and ssh-aws-database.sh is running.
REMOTE_DB_BIKES_URL = os.getenv("REMOTE_DB_BIKES_URL")

# Define remote database connection URL, this is for running on EC2 connected to RDS directly (no SSH tunnel), so this environment variable should be set on EC2
# make sure system variable EC2_PEM is added at first, and ssh-aws-ec2.sh is running.
EC2_DB_BIKES_URL = os.getenv('EC2_DB_BIKES_URL')

# Define jcdecaux URI
NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

# Define OpenWeather URI
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
OPEN_WEATHER_URI = f"https://api.openweathermap.org/data/3.0/onecall"

# BASED ON GOOGLE MAP
OPEN_WEATHER_DUBLIN_LOC = {
    "Dublin 1" : (53.3498006, -6.2602964),
    "Dublin 2" : (53.33989495293019, -6.254274088725324),
    "Dublin 3" : (53.363136602356775, -6.2214516594608895),
    "Dublin 4" : (53.32937028614333, -6.227505379264549),
    "Dublin 5" : (53.38405645086355, -6.192074738814579),
    "Dublin 6" : (53.308620496353655, -6.263115300940266),
    "Dublin 7" : (53.361373447484326, -6.291738981881436),
    "Dublin 6W" : (53.308452336281555, -6.3011585153597665),
    "Dublin 9" : (53.38160994528601, -6.246522438881569),
    "Dublin 8" : (53.34730496058491, -6.308295532263704),
    "Dublin 11" : (53.389730837478844, -6.292933667358706),
    "Dublin 10" : (53.34230308625651, -6.353184605237993),
    "Dublin 13" : (53.39444966991738, -6.149467127206714),
    "Dublin 12" : (53.321819029575884, -6.316445615576019),
    "Dublin 15" : (53.38301426214587, -6.416529267273791),
    "Dublin 14" : (53.295781834732075, -6.259299165607058),
    "Dublin 17" : (53.40045431947804, -6.205741738492062),
    "Dublin 16" : (53.27985993689113, -6.278983027670005),
    "Dublin 18" : (53.24670977941463, -6.177354976005729),
    "Dublin 20" : (53.35159704053917, -6.369375282829098),
    "Dublin 22" : (53.327317455022204, -6.400602324462271),
    "Dublin 24" : (53.28492603413517, -6.371306473267077),
}