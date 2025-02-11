import dbinfo
import requests
import json

STATIONS_URI = 'https://api.jcdecaux.com/vls/v1/stations/42'
# r = requests.get(dbinfo.STATIONS_URI, params={"apiKey":dbinfo.JCKEY, "contract":dbinfo.NAME})
r = requests.get(STATIONS_URI, params={"apiKey":dbinfo.JCKEY, "contract":dbinfo.NAME})
data = json.loads(r.text)
print(json.dumps(data, indent = 4))