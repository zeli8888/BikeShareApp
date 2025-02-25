# BikeShareApp
BikeShareApp from COMP30830 Software Engineering Module
# Installation
    python -m pip install -r requirements.txt
# Database
- ## Locally
    #### Need to set the database connection url system variable, check [config.py](web/src/config.py)
        export LOCAL_DB_BIKES_URL=your-local-database-url
- ## Remotely 
    #### Need EC2 pem file path as system variable: EC2_PEM
        export EC2_PEM=path/to/file/comp30830.pem
    #### The Public DNS of EC2 keeps changing, may need to modify in [ssh-aws-database.sh](database/ssh-aws-database.sh)
        ./database/ssh-aws-database.sh
    
# Scrape Data

#### Need to remember the process pid and use kill -9 pid to shut it down
#### Need to set key as your system variable: JCKEY, OPEN_WEATHER_KEY
    export JCKEY=your-jckey
    export OPEN_WEATHER_KEY=your-open-weather-key

- ## Locally
        nohup python -u database/weather_scraper.py --no_echo --loop > database/weather_scraper.log 2>&1 &
        nohup python -u database/bike_scraper.py --no_echo --loop > database/bike_scraper.log 2>&1 &
- ## Remotely 
        nohup python -u database/weather_scraper.py --database 'REMOTE' --no_echo --loop > database/weather_scraper.log 2>&1 &
        nohup python -u database/bike_scraper.py --database 'REMOTE' --no_echo --loop > database/bike_scraper.log 2>&1 &
# Save Database Data To CSV
- ## Locally
        python database/save_data.py
- ## Remotely
        python database/save_data.py --database 'REMOTE'
# Load CSV Data To Database
- ## Locally
        python database/load_data.py
- ## Remotely
        python database/load_data.py --database 'REMOTE'

# Web Application
#### Need to set Database first: [Database](#database)
#### Need to set Google Map key as your system variable: GOOGLE_MAP_KEY
    export GOOGLE_MAP_KEY=your-google-map-key
#### To Start On EC2
    python web/BikeShareApplication.py --database 'EC2' --no_debug
#### To Start Locally
    python web/BikeShareApplication.py

# Docs
- ## BackLog
    product backlog and sprint backlog are defined in 

        ./BackLog/Group2ProductBacklog.md 
    and

        ./BackLog/Group2SprintBacklog{date_range}.md

- ## Burn Down Chart
    Please make sure the Group2SprintBacklog{date_range}.md file is written in consistent format.
    Then run (replace date_range):

        python ./BackLog/burndown_generator.py --file_path ./BackLog/Group2SprintBacklog{date_range}.md --save_file ./BackLog/BurnDown{date_range}.png

    The burn down chart will be saved as

        ./BackLog/BurnDown{date_range}.png
# Description
- BackLog: files related to product backlog and sprint backlog including burn down chart
- labs: files from course example
- database: scraper files related to database
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
