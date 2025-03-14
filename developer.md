# BikeShareApp
BikeShareApp from COMP30830 Software Engineering Module
This file is for the usage of developers, it records some useful commands for reuse.
    
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

# GitHub
    git checkout -b feature_name
    git add .
    git commit -m "feat(feature_name): description"
    git push -u origin feature_name
    
    git checkout main
    git merge feature_name --no-commit
    git push
    git branch -d feature_name
    git push origin --delete feature_name

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
