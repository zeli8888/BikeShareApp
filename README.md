# BikeShareApp
BikeShareApp (Frontend) from COMP30830 Software Engineering moudle
# Installation
    python -m pip install -r requirements.txt
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
- labs: files from course
- data: example of fetched data for data format reference