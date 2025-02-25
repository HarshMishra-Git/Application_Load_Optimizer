![Application Load Optimizer](banner.png)

# Application Load Optimizer

The Application Load Optimizer is a comprehensive system designed to forecast application usage, balance server loads, and automate scaling based on real-time monitoring. The system leverages advanced machine learning models for forecasting, various load balancing algorithms, and automated scaling mechanisms to ensure optimal performance and resource utilization.

## Live Demo

Check out the live demo of the Application Load Optimizer: [Application Load Optimizer Live](https://app-load-optimizer.streamlit.app/)

## Features

- **Data Generation and Preprocessing**: Generate and preprocess synthetic application usage data.
- **Forecasting**: Use the Prophet model to forecast application usage based on historical data.
- **Load Balancing**: Implement various load balancing algorithms including Round Robin, Least Connections, IP Hash, and Weighted Round Robin.
- **Automated Scaling**: Automatically adjust the number of servers based on current load.
- **Real-Time Monitoring**: Monitor server loads in real-time.
- **Metrics Calculation**: Calculate utilization, load distribution, and performance metrics.

## Project Structure

- `app.py`: Main file containing the Streamlit and Flask applications.
- `app/`: Directory containing the application modules.
  - `__init__.py`: Initialization file for the app module.
  - `auto_scaler.py`: Contains the `AutoScaler` class for automated scaling.
  - `data_processor.py`: Contains the `DataProcessor` class for data generation and preprocessing.
  - `forecaster.py`: Contains the `Forecaster` class for application usage forecasting.
  - `load_balancer.py`: Contains the `LoadBalancer` class implementing various load balancing algorithms.
  - `metrics.py`: Contains the `MetricsCalculator` class for calculating utilization and performance metrics.
  - `real_time_monitor.py`: Contains the `RealTimeMonitor` class for real-time monitoring.
  - `utils.py`: Contains the `Visualizer` class for plotting data.
- `requirements.txt`: Specifies the required Python packages for the project.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HarshMishra-Git/Application_Load_Optimizer.git
   cd Application_Load_Optimizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   Set the necessary environment variables, such as `FLASK_SECRET_KEY`.

4. **Run Streamlit application**:
   ```bash
   streamlit run app.py
   ```

5. **Run Flask application**:
   ```bash
   flask run
   ```

## Usage

### Streamlit Interface

The Streamlit interface allows users to interact with the application, configure settings, generate forecasts, and simulate load balancing. 

### Flask API

The Flask API provides endpoints for forecasting and load balancing, as well as handling user authentication.

### Notifications

The application can send notifications via email. Users can configure the recipient email address and notification method in the Streamlit interface.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Developer Information

- **Name**: Harsh Mishra
- **Email**: harshmishra1132@gmail.com
