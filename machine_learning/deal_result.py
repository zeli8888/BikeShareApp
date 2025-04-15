import re

def calculate_average_scores(file_path):
    """
    Calculate the average MAE and R2 scores for bikes and docks from a text file.

    Args:
        file_path (str): Path to the text file containing the model results.

    Returns:
        None
    """
    # Load the data from the text file
    with open(file_path, 'r') as f:
        data = f.read()

    # Extract the MAE and R2 scores for bikes and docks
    bike_mae_scores = []
    bike_r2_scores = []
    dock_mae_scores = []
    dock_r2_scores = []

    for line in data.split('\n'):
        match = re.search(r'Station \d+: MAE bikes: (\d+\.\d+), R2 score bikes: (\d+\.\d+), MAE docks: (\d+\.\d+), R2 score docks: (\d+\.\d+)', line)
        if match:
            bike_mae_scores.append(float(match.group(1)))
            bike_r2_scores.append(float(match.group(2)))
            dock_mae_scores.append(float(match.group(3)))
            dock_r2_scores.append(float(match.group(4)))

    # Calculate the average MAE and R2 scores for bikes and docks
    avg_bike_mae = sum(bike_mae_scores) / len(bike_mae_scores)
    avg_bike_r2 = sum(bike_r2_scores) / len(bike_r2_scores)
    avg_dock_mae = sum(dock_mae_scores) / len(dock_mae_scores)
    avg_dock_r2 = sum(dock_r2_scores) / len(dock_r2_scores)

    print(f'Average MAE for bikes: {avg_bike_mae:.4f}')
    print(f'Average R2 score for bikes: {avg_bike_r2:.4f}')
    print(f'Average MAE for docks: {avg_dock_mae:.4f}')
    print(f'Average R2 score for docks: {avg_dock_r2:.4f}')

if __name__ == "__main__":
    calculate_average_scores('machine_learning/model_results.txt')