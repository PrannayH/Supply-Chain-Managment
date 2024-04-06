from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error
import warnings

app = Flask(__name__)
CORS(app)

def get_top_demanded_products():
    warnings.filterwarnings("ignore")

    # Load the dataset
    data = pd.read_csv('hackathondataset.csv')

    # Preprocessing
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    time_series_data = data.groupby(['Order Date', 'Product ID'])['Unit quantity'].sum().reset_index()
    time_series_data = time_series_data.sort_values(by='Order Date')
    selected_product_id = time_series_data['Product ID'].value_counts().idxmax()
    selected_product_data = time_series_data[time_series_data['Product ID'] == selected_product_id]
    selected_product_series = selected_product_data.set_index('Order Date')['Unit quantity']

    # Split the data into train and test sets
    split_ratio = 0.8
    split_index = int(len(selected_product_series) * split_ratio)
    train_series = selected_product_series[:split_index]
    test_series = selected_product_series[split_index:]

    # ARIMA Model
    arima_order = (1, 1, 1)  # Example parameters
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        arima_model = ARIMA(train_series, order=arima_order)
        arima_model_fit = arima_model.fit()
        arima_forecast = arima_model_fit.forecast(steps=len(test_series))
    arima_rmse = np.sqrt(mean_squared_error(test_series, arima_forecast))

    # You can similarly define and fit SARIMA and LSTM models...
    # SARIMA Model
    sarima_order = (1, 1, 1, 12)  # Example parameters
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sarima_model = SARIMAX(train_series, order=(sarima_order[0:3]), seasonal_order=(1, 1, 1, sarima_order[3]))
        sarima_model_fit = sarima_model.fit()
        sarima_forecast = sarima_model_fit.forecast(steps=len(test_series))
    sarima_rmse = np.sqrt(mean_squared_error(test_series, sarima_forecast))

    # LSTM Model
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(np.array(train_series).reshape(-1, 1))
    scaled_test = scaler.transform(np.array(test_series).reshape(-1, 1))

    # Prepare data for LSTM
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    look_back = 1
    trainX, trainY = create_dataset(scaled_train, look_back)
    testX, testY = create_dataset(scaled_test, look_back)

    # Reshape input to be [samples, time steps, features] for LSTM
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(50, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

    # Make predictions
    lstm_predictions = model.predict(testX)
    lstm_predictions = scaler.inverse_transform(lstm_predictions)
    lstm_rmse = np.sqrt(mean_squared_error(test_series[1:len(lstm_predictions)+1], lstm_predictions))

    best_forecast = arima_forecast if arima_rmse < min(sarima_rmse, lstm_rmse) else (
    sarima_forecast if sarima_rmse < lstm_rmse else lstm_predictions)

    # Assume the best model is selected based on the lowest RMSE
    # For demonstration, let's select ARIMA as an example
    # You should include the logic to select the best model

    # Initialize a dictionary to store forecasted demand for each Product ID
    product_forecasts = {}

    # Iterate over each unique Product ID in the dataset
    for product_id in time_series_data['Product ID'].unique():
        product_data = time_series_data[time_series_data['Product ID'] == product_id]
        product_series = product_data.set_index('Order Date')['Unit quantity']
        
        if len(product_series) > 10:  # example threshold
            split_index = int(len(product_series) * split_ratio)
            train_series = product_series[:split_index]
            test_series = product_series[split_index:]
            
            model = ARIMA(train_series, order=arima_order)
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=len(test_series))
            
            total_forecasted_demand = forecast.sum()
            # Convert int64 to int
            product_forecasts[product_id] = int(total_forecasted_demand)

    # Sort products by their forecasted demand and select the top 3
    top_products = sorted(product_forecasts, key=product_forecasts.get, reverse=True)[:8]
    return [(product_id, product_forecasts[product_id]) for product_id in top_products]

@app.route('/predict', methods=['GET'])
def predict():
    top_products = get_top_demanded_products()
    response = {
        "demand": [
            {"Product ID": str(product_id), "Forecasted Demand": forecast}
            for product_id, forecast in top_products
        ]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
