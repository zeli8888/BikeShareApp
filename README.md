# BikeShareApp
BikeShareApp (Frontend) from COMP30830 Software Engineering Module
# Installation
    python -m pip install -r requirements.txt
# Fetch data
## Locally
#### (need to change the database setting to yours)
    python database/weather_scraper.py
    python database/bike_scraper.py
## Remotely 
#### (the Public DNS of EC2 keeps changing, may need to modify in ssh-aws-database.sh)
#### Need to remember the process pid and use kill -9 pid to shut it down
    ./database/ssh-aws-database.sh
    nohup python -u database/weather_scraper.py --database 'REMOTE' --no_echo --loop >> database/scraper.log 2>&1 &
    nohup python -u python database/bike_scraper.py --database 'REMOTE' --no_echo --loop >> database/scraper.log 2>&1 &
# Docs
## BackLog
product backlog and sprint backlog are defined in 

    ./BackLog/Group2ProductBacklog.md 
and

    ./BackLog/Group2SprintBacklog{date_range}.md

## Burn Down Chart
Please make sure the Group2SprintBacklog{date_range}.md file is written in consistent format.
Then run (replace date_range):

    python ./BackLog/burndown_generator.py --file_path ./BackLog/Group2SprintBacklog{date_range}.md --save_file ./BackLog/BurnDown{date_range}.png

The burn down chart will be saved as

    ./BackLog/BurnDown{date_range}.png
# Description
- BackLog: files related to product backlog and sprint backlog including burn down chart
- labs: files from course example
- database: config and scraper files related to database
- web: files related to the web application
    - src: files relate to backend
        - controller: files handle requests from frontend
        - service: files handle business logic
        - repository: files interact with the database
    - templates: html files related to frontend
    - static: other files related to frontend
        - css: css files
        - js: javascript files
        - resources: images
