import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to parse the markdown file and extract user story points
def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract user stories and their points
    subtasks = re.findall(
        r'- \*\*Task \d+\:\*\*.*\n.*- Estimated Points: \[(\d+)\].*\n.*- Assigned To\: \[(.*)\].*\n.*- Description\: \[(.*)\]\n.*- Finish Time\: \[(.*)\]', 
                          content)

    time_interval_match = re.match(r'\# Group2 Sprint Backlog.*\n.*# \[(.*) - (.*)\]', content)
    time_interval = [time_interval_match.group(1), time_interval_match.group(2)]
    for i in range(2):
        time_interval[i] = datetime.strptime(f"{time_interval[i]} {datetime.now().year}", "%b %d %Y")

    subtasks = pd.DataFrame(subtasks, columns=['Points', 'Assigned To', 'Description', "Finish Time"])
    subtasks["Finish Time"] = pd.to_datetime(subtasks['Finish Time']+" "+str(datetime.now().year), format='%dth %b %Y').dt.date
    subtasks['Points'] = subtasks['Points'].astype(int)
    time_interval = pd.date_range(start=time_interval[0], end=time_interval[1])[:-1].to_pydatetime()
    return time_interval, subtasks

# Function to generate burndown chart
def generate_burndown_chart(time_interval, subtasks, savefile):

    start_date = time_interval[0]
    total_points = subtasks["Points"].sum()
    remaining_points = np.array([total_points for i in range(len(time_interval)+1)])
    for task in range(len(subtasks)):
        index = (subtasks.iloc[task]["Finish Time"]-start_date.date()).days+1
        remaining_points[index:] -= subtasks.iloc[task]["Points"]
        
    day_interval = [time_interval[0]] + list(time_interval)
    
    # Create a DataFrame for the burndown chart
    burndown_df = pd.DataFrame({'Date': day_interval, 'Remaining Points': remaining_points})

    # Plot the burndown chart
    plt.figure(figsize=(10, 5))
    plt.plot(burndown_df['Date'], burndown_df['Remaining Points'], marker='o', linestyle='-')
    plt.title('Sprint Burndown Chart')
    plt.xlabel('Date')
    plt.ylabel('Remaining Points')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(savefile)

# Main function to run the script
def main():
    file_path = 'd:\\study_software\\GitHub\\BikeShareApp\\BackLog\\Group2SprintBacklogFeb4-Feb18.md'

    time_interval, subtasks = parse_markdown(file_path)
    generate_burndown_chart(time_interval, subtasks, ".\BackLog\BurnDownFeb4-Feb18.png")

if __name__ == "__main__":
    main()
