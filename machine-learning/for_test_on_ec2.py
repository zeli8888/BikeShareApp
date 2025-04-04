import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
import warnings
# Ignore UserWarnings from Keras
warnings.filterwarnings("ignore", category=UserWarning, module="keras")


def visualize_prediction(y_test, y_pred, mae_bikes, r2_score_bikes, mae_docks, r2_score_docks, station_id):
    # Plot results for available_bikes
    plt.figure(figsize=(10, 6))
    plt.plot(y_test[:, 0], label='Actual Bikes', color='green')
    plt.plot(y_pred[:, 0], label='Predicted Bikes', color='red')
    plt.title(f'#{station_id} Station Available Bikes Forecast (MAE: {mae_bikes:.4f}, r2_score: {r2_score_bikes:.4f})')
    plt.xlabel('Hour Sequence')
    plt.ylabel('Available Bikes')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot results for available_docks
    plt.figure(figsize=(10, 6))
    plt.plot(y_test[:, 1], label='Actual Docks', color='green')
    plt.plot(y_pred[:, 1], label='Predicted Docks', color='red')
    plt.title(f'#{station_id} Station Available Docks Forecast (MAE: {mae_docks:.4f}, r2_score: {r2_score_docks:.4f})')
    plt.xlabel('Hour Sequence')
    plt.ylabel('Available Docks')
    plt.legend()
    plt.grid(True)
    plt.show()

def train_model(station_id, visualize=False):
    # Load the data
    data = pd.read_csv(f'training_data/station_{station_id}.csv')
    X = data.drop(['available_bikes', 'available_docks'], axis=1)
    y = data[['available_bikes', 'available_docks']]

    # Split the data into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X.values, y.values, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Standardize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    # Initialize the model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu', kernel_regularizer='l2'))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu', kernel_regularizer='l2'))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(16, activation='relu', kernel_regularizer='l2'))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='linear'))  # Output layer for two targets

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    # Early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=100, restore_best_weights=True)

    # Fit the model
    model.fit(X_train, y_train, epochs=800, batch_size=32, validation_data=(X_val, y_val), verbose=visualize, callbacks=[early_stopping])

    # Save the model
    model.save(f'trained_model/station_{station_id}_model.keras', include_optimizer=False)

    # Predict using the model
    model = load_model(f'trained_model/station_{station_id}_model.keras')
    y_pred = model.predict(X_test, verbose=visualize)

    # Evaluate each target separately
    mae_bikes = mean_absolute_error(y_test[:, 0], y_pred[:, 0])
    mae_docks = mean_absolute_error(y_test[:, 1], y_pred[:, 1])

    r2_score_bikes = r2_score(y_test[:, 0], y_pred[:, 0])
    r2_score_docks = r2_score(y_test[:, 1], y_pred[:, 1])
    
    if visualize:
        print(f"R2 Score for available_bikes: {r2_score_bikes}")
        print(f"R2 Score for available_docks: {r2_score_docks}")

        print(f"Mean Absolute Error for available_bikes: {mae_bikes}")
        print(f"Mean Absolute Error for available_docks: {mae_docks}")
        
        visualize_prediction(y_test, y_pred, mae_bikes, r2_score_bikes, mae_docks, r2_score_docks, station_id)
        
    return mae_bikes, r2_score_bikes, mae_docks, r2_score_docks

if __name__ == '__main__':
    mae_bikes, r2_score_bikes, mae_docks, r2_score_docks = train_model(1, True)