import dbinfo
import requests
import json
import time
import traceback

NAME="Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
APIKEY="a2e6d3120f108a84141fc12b5ea5beedba83906a"
def write_to_db(text):
    pass
def main():
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"apikey":APIKEY, "contract":NAME})
            write_to_db(json.loads(r.text))
            print("writting!")
            time.sleep(5*60)
        except:
            print(traceback.format_exc())
    return
main()
# nohup python -u scraper.py >> scraper.log 2>&1 &