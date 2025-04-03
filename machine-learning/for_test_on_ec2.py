from datetime import datetime
import os
import pandas as pd
import numpy as np
import holidays
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
data = pd.read_csv(f'training_data/station_1.csv', parse_dates=['time'], index_col='time')

# Features and target variables
features = ['hour_sin', 'hour_cos','temperature_celsius', 'relative_humidity_percent', 'barometric_pressure_hpa', 'is_holiday', 'is_weekend']
targets = ['available_bikes', 'available_docks']

# Move target columns to the last
data = data[[col for col in data.columns if col not in targets] + targets]

# Create sequences of data for LSTM
def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length), 0:-2]  # features
        y = data[i:(i + seq_length), -2:]   # targets
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# Sequence length, 24 hours, from 0:00 to 23:00
seq_length = 24

# Create sequences
x, y = create_sequences(data.values, seq_length)

# Split the data, 80% for training and 20% for testing
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True)
# Split training data into training and validation sets (80% for training and 20% for validation)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, shuffle=True)

# Predict using the model
model = load_model(f'station_1_model.h5')
predictions = model.predict(x_test)

# Inverse transform the predictions and actual values
inverse_predictions = []
for prediction in predictions:
    inverse_predictions.append(target_scaler.inverse_transform(prediction))
predictions = np.array(inverse_predictions).reshape(-1,2)
inverse_y_test = []
for y in y_test:
    inverse_y_test.append(target_scaler.inverse_transform(y))
y_test = np.array(inverse_y_test).reshape(-1,2)

# Calculate MAE and R2 score for both bikes and docks
mae_bikes = mean_absolute_error(y_test[:, 0], predictions[:, 0])
r2_score_bikes = r2_score(y_test[:, 0], predictions[:, 0])
mae_docks = mean_absolute_error(y_test[:, 1], predictions[:, 1])
r2_score_docks = r2_score(y_test[:, 1], predictions[:, 1])

# UML Modelling, Use Case Diagram, and Class Diagram
# SmartDraw (instead of Store the image, do the screen shot to avoid paying)
# StarUML
# DrawIO
# PlantUML AND PlantText