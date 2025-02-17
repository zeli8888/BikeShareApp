# BikeShareApp-API
BikeShareApp-API (Backend) from COMP30830 Software Engineering module
# Installation
    python -m pip install -r requirements.txt
# Fetch data
## Locally
    python database/weather_scraper.py
    python database/bike_scraper.py
## Remotely(the Public DNS of EC2 keeps changing, may need to modify in ssh-aws-database.sh)
## Need to remember the process pid and use kill -9 pid to shut it down
    ./database/ssh-aws-database.sh
    nohup python -u database/weather_scraper.py --database 'REMOTE' --no_echo --loop >> database/scraper.log 2>&1 &
    nohup python -u python database/bike_scraper.py --database 'REMOTE' --no_echo --loop >> database/scraper.log 2>&1 &
# Description
- database: config and scraper files related to database
- lab_example: example files from lab