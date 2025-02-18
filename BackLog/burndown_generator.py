import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta
import seaborn as sns

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
def generate_burndown_chart(time_interval, subtasks, save_file):

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
    # plt.figure(figsize=(10, 5))
    # plt.plot(burndown_df['Date'], burndown_df['Remaining Points'], marker='o', linestyle='-')
    # plt.title('Sprint Burndown Chart')
    # plt.xlabel('Date')
    # plt.ylabel('Remaining Points')
    # plt.grid(True)
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.savefig(save_file)
    # Set the style and palette for Seaborn
    
    # Thank for the power of AI :)
    sns.set(style="whitegrid", palette="pastel")
    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot the actual burndown curve
    plt.plot(burndown_df['Date'], burndown_df['Remaining Points'], 
            marker='o', linestyle='-', color='#3498db', 
            markersize=5, linewidth=2, label='Remaining')

    # Calculate the ideal burndown curve
    start_points = burndown_df['Remaining Points'].iloc[0]
    end_points = 0
    total_days = len(burndown_df)-1
    ideal_burndown_df = burndown_df.copy().iloc[1:]
    ideal_burndown_df['Ideal Remaining Points'] = np.linspace(start_points, end_points, total_days)

    # Plot the ideal burndown curve with more fade
    plt.plot(ideal_burndown_df['Date'], ideal_burndown_df['Ideal Remaining Points'], 
            linestyle='--', color='#2ecc71', 
            linewidth=2, alpha=0.5, label='Ideal')  # Added alpha for fade effect

    plt.title('Group2 Sprint Burndown Chart', fontsize=18, fontweight='bold', color='#2c3e50')
    # plt.xlabel('Date', fontsize=14, color='#2c3e50')
    plt.ylabel('Story Points', fontsize=14, color='#2c3e50')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Customize tick parameters
    plt.xticks(rotation=45, fontsize=12, color='#34495e', fontweight='bold')
    plt.yticks(fontsize=12, color='#34495e', fontweight='bold')

    # Highlight the area under the actual curve to make it visually appealing
    plt.fill_between(burndown_df['Date'], burndown_df['Remaining Points'], 
                    color='#3498db', alpha=0.1)

    # Add a legend
    plt.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig(save_file, bbox_inches='tight', dpi=300)


# Main function to run the script
def main(file_path, save_file):
    time_interval, subtasks = parse_markdown(file_path)
    generate_burndown_chart(time_interval, subtasks, save_file)

if __name__ == "__main__":
    # to run:
    # python ./BackLog/burndown_generator.py --file_path ./BackLog/Group2SprintBacklogFeb4-Feb18.md --save_file ./BackLog/BurnDownFeb4-Feb18.png
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, action='store', default='./BackLog/Group2SprintBacklogFeb4-Feb18.md')
    parser.add_argument('--save_file', type=str, action='store', default='./BackLog/BurnDownFeb4-Feb18.png')
    args = parser.parse_args()
    main(args.file_path, args.save_file)