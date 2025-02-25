# Application Load Optimizer Final Report

## About the Project

The Application Load Optimizer is a comprehensive system designed to forecast application usage, balance server loads, and automate scaling based on real-time monitoring. The system leverages advanced machine learning models for forecasting, various load balancing algorithms, and automated scaling mechanisms to ensure optimal performance and resource utilization.

### Developer Information

- **Name**: Harsh Mishra
- **Email**: harshmishra1132@gmail.com

## Project Structure

The project is organized into the following files and directories:

- `app.py`: Main file containing the Streamlit and Flask applications.
- `app/__init__.py`: Initialization file for the app module, importing main classes and functions.
- `app/auto_scaler.py`: Contains the `AutoScaler` class for automated scaling.
- `app/data_processor.py`: Contains the `DataProcessor` class for data generation and preprocessing.
- `app/forecaster.py`: Contains the `Forecaster` class for application usage forecasting.
- `app/load_balancer.py`: Contains the `LoadBalancer` class implementing various load balancing algorithms.
- `app/metrics.py`: Contains the `MetricsCalculator` class for calculating utilization and performance metrics.
- `requirements.txt`: Specifies the required Python packages for the project.

## Project Pipeline

### 1. Data Generation and Preprocessing

The `DataProcessor` class in `app/data_processor.py` is responsible for generating and preprocessing synthetic application usage data. The data includes timestamps, active users, server load, and response time, with daily and weekly seasonal patterns.

#### Key Methods:

- `generate_sample_data(days=90)`: Generates synthetic data for a specified number of days.
- `preprocess_data(data=None)`: Preprocesses the data by handling missing values, outliers, and feature engineering.
- `prepare_prophet_data(target_column='active_users')`: Prepares data for the Prophet model used in forecasting.

### 2. Forecasting Application Usage

The `Forecaster` class in `app/forecaster.py` uses the Prophet model to forecast application usage based on historical data. It also calculates forecast accuracy metrics and detects anomalies.

#### Key Methods:

- `train(data)`: Trains the Prophet model on the provided data.
- `predict(periods=24)`: Generates forecasts for a specified number of periods (hours).
- `get_metrics(actual, predicted)`: Calculates Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE).
- `detect_anomalies(forecast_df)`: Detects anomalies in the forecasted data using Isolation Forest.

### 3. Load Balancing

The `LoadBalancer` class in `app/load_balancer.py` implements various load balancing algorithms, including Round Robin, Least Connections, IP Hash, and Weighted Round Robin. It also calculates server performance metrics.

#### Key Methods:

- `round_robin(request_load)`: Implements Round Robin load balancing.
- `least_connections(request_load)`: Implements Least Connections load balancing.
- `ip_hash(request_ip, request_load)`: Implements IP Hash load balancing.
- `weighted_round_robin(request_load)`: Implements Weighted Round Robin load balancing.
- `get_server_metrics()`: Calculates average and maximum load, and average response time for each server.

### 4. Automated Scaling

The `AutoScaler` class in `app/auto_scaler.py` automatically scales the number of servers based on the current load. It checks the average server load and scales up or down as needed.

#### Key Methods:

- `scale_up()`: Adds a new server to the load balancer.
- `scale_down()`: Removes a server from the load balancer.
- `check_and_scale()`: Checks server loads and decides whether to scale up or down.

### 5. Metrics Calculation

The `MetricsCalculator` class in `app/metrics.py` calculates utilization, load distribution, and performance metrics for the servers.

#### Key Methods:

- `calculate_utilization(server_loads, capacity=100)`: Calculates server utilization percentage.
- `calculate_load_distribution(server_metrics)`: Calculates load distribution across servers.
- `calculate_performance_metrics(response_times)`: Calculates average, 95th percentile, and 99th percentile response times.

## Deployment

The project uses both Streamlit and Flask for deployment:

### Streamlit

Streamlit is used for the web interface, allowing users to interact with the application, configure settings, generate forecasts, and simulate load balancing. The main Streamlit application is defined in `app.py`.

### Flask

Flask is used to provide API endpoints for forecasting and load balancing, as well as handling user authentication. The Flask application is also defined in `app.py`.

### Running the Application

To run the application, follow these steps:

1. **Install Dependencies**: Ensure all required packages are installed by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**: Set the necessary environment variables, such as `FLASK_SECRET_KEY`.

3. **Run Streamlit Application**: Start the Streamlit application by running:
   ```bash
   streamlit run app.py
   ```

4. **Run Flask Application**: Start the Flask application by running:
   ```bash
   flask run
   ```

### Notifications

The application can send notifications via email. Users can configure the recipient email address and notification method in the Streamlit interface.

## Models and Algorithms

### Forecasting Model: Prophet

The `Forecaster` class uses the Prophet model to forecast application usage. Prophet is a robust time series forecasting model developed by Facebook, designed to handle daily, weekly, and yearly seasonality with ease. It can also incorporate holiday effects and missing data.

#### Key Features of Prophet:

- **Seasonality**: Automatically detects daily, weekly, and yearly seasonal patterns.
- **Trend**: Handles different types of trend changes.
- **Holidays**: Allows incorporating holiday effects.
- **Outliers**: Robust to missing data and outliers.

### Load Balancing Algorithms

The `LoadBalancer` class implements the following load balancing algorithms:

1. **Round Robin**: Distributes requests evenly across all servers. It cycles through the list of servers and assigns each request to the next server in line.

2. **Least Connections**: Assigns requests to the server with the fewest active connections. This helps in balancing the load more evenly when servers have different capacities.

3. **IP Hash**: Uses the client's IP address to determine which server should handle the request. This ensures that the same client is always directed to the same server, useful for session persistence.

4. **Weighted Round Robin**: Similar to Round Robin, but allows assigning weights to servers. Servers with higher weights receive more requests.

### Automated Scaling

The `AutoScaler` class automatically adjusts the number of servers based on current load. It uses predefined thresholds to decide when to scale up or down.

#### Scaling Logic:

- **Scale Up**: Adds a new server if the maximum load exceeds the scale-up threshold.
- **Scale Down**: Removes a server if the maximum load is below the scale-down threshold and there is more than one server.

### Metrics Calculation

The `MetricsCalculator` class provides methods to calculate various metrics to evaluate server performance and load distribution.

#### Key Metrics:

- **Utilization**: Percentage of server capacity used.
- **Load Distribution**: Measures the distribution of load across servers, including minimum, maximum, standard deviation, and load imbalance.
- **Performance**: Includes average response time, 95th percentile, and 99th percentile response times.

## Conclusion

The Application Load Optimizer is a robust system designed to ensure optimal application performance through advanced forecasting, load balancing, and automated scaling. It provides a user-friendly interface for configuration and monitoring, making it a valuable tool for managing application loads efficiently.

For any further questions or contributions, please contact the developer:

- **Name**: Harsh Mishra
- **Email**: harshmishra1132@gmail.com
