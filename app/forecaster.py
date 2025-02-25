from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import IsolationForest

class Forecaster:
    def __init__(self):
        self._initialize_model()
        self.forecast = None

    def _initialize_model(self):
        """Initialize a new Prophet model"""
        try:
            self.model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True,
                seasonality_mode='multiplicative'
            )
        except Exception as e:
            print(f"Error initializing Prophet model: {e}")
            raise

    def train(self, data):
        """Train the Prophet model"""
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")
            if not all(col in data.columns for col in ['ds', 'y']):
                raise ValueError("Data must contain 'ds' and 'y' columns")

            # Initialize new model before training
            self._initialize_model()
            self.model.fit(data)
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            raise

    def predict(self, periods=24):
        """Generate forecasts"""
        try:
            future = self.model.make_future_dataframe(periods=periods, freq='h')
            self.forecast = self.model.predict(future)
            return self.forecast
        except Exception as e:
            print(f"Error generating forecast: {e}")
            raise

    def get_metrics(self, actual, predicted):
        """Calculate forecast accuracy metrics"""
        try:
            mae = mean_absolute_error(actual, predicted)
            mse = mean_squared_error(actual, predicted)
            rmse = np.sqrt(mse)

            return {
                'MAE': mae,
                'MSE': mse,
                'RMSE': rmse
            }
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            raise

    def get_components(self):
        """Get trend and seasonality components"""
        try:
            if self.forecast is None:
                raise ValueError("Must run predict() before getting components")
            return self.model.plot_components(self.forecast)
        except Exception as e:
            print(f"Error getting components: {e}")
            raise

    def detect_anomalies(self, forecast_df):
        """Detect anomalies in the forecasted load"""
        try:
            model = IsolationForest(contamination=0.1)
            forecast_df['anomaly'] = model.fit_predict(forecast_df[['yhat']])
            return forecast_df
        except Exception as e:
            print(f"Error detecting anomalies: {e}")
            raise