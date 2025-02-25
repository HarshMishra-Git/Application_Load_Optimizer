import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self):
        self.data = None

    def generate_sample_data(self, days=90):
        """Generate sample application usage data"""
        date_rng = pd.date_range(
            start=datetime.now() - timedelta(days=days),
            end=datetime.now(),
            freq='h'
        )

        # Generate synthetic data
        data = {
            'timestamp': date_rng,
            'active_users': np.random.normal(1000, 200, len(date_rng)),
            'server_load': np.random.normal(60, 15, len(date_rng)),
            'response_time': np.random.normal(200, 50, len(date_rng))
        }

        # Add seasonal patterns
        hours = date_rng.hour
        weekdays = date_rng.weekday

        # Daily pattern: peak during business hours
        daily_pattern = np.sin(np.pi * hours / 12) * 300
        # Weekly pattern: lower on weekends
        weekly_pattern = np.where(weekdays >= 5, -200, 0)

        data['active_users'] += daily_pattern + weekly_pattern
        data['active_users'] = np.maximum(data['active_users'], 0)

        self.data = pd.DataFrame(data)
        return self.data

    def preprocess_data(self, data=None):
        """Preprocess the data for modeling"""
        if data is not None:
            self.data = data

        if self.data is None:
            self.data = self.generate_sample_data()

        # Handle missing values using ffill instead of fillna(method='ffill')
        self.data = self.data.ffill()

        # Handle outliers using IQR method
        for column in ['active_users', 'server_load', 'response_time']:
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.data[column] = self.data[column].clip(lower_bound, upper_bound)

        # Feature engineering
        self.data['hour'] = self.data['timestamp'].dt.hour
        self.data['day_of_week'] = self.data['timestamp'].dt.dayofweek
        self.data['is_weekend'] = self.data['day_of_week'].isin([5, 6]).astype(int)

        return self.data

    def prepare_prophet_data(self, target_column='active_users'):
        """Prepare data for Prophet model"""
        if self.data is None:
            self.preprocess_data()
        prophet_data = self.data[['timestamp', target_column]].copy()
        prophet_data.columns = ['ds', 'y']
        return prophet_data