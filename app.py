import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from app.data_processor import DataProcessor
from app.forecaster import Forecaster
from app.load_balancer import LoadBalancer
from app.utils import Visualizer
from app.auto_scaler import AutoScaler
from app.notifications import send_notification  # Import the notification function
from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Flask app for API and authentication
app_flask = Flask(__name__)
app_flask.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use environment variable

login_manager = LoginManager()
login_manager.init_app(app_flask)

class User(UserMixin):
    # User model definition...
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app_flask.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic...
    pass

@app_flask.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@app_flask.route('/api/forecast', methods=['POST'])
def api_forecast():
    data = request.json
    # Forecasting logic...
    response = {
        "forecast": "example_forecast_data"
    }
    return jsonify(response)

@app_flask.route('/api/load_balance', methods=['POST'])
def api_load_balance():
    data = request.json
    # Load balancing logic...
    response = {
        "load_balance": "example_load_balance_data"
    }
    return jsonify(response)

# Streamlit app
st.set_page_config(
    page_title="Application Load Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'forecaster' not in st.session_state:
    st.session_state.forecaster = Forecaster()
if 'load_balancer' not in st.session_state:
    st.session_state.load_balancer = LoadBalancer()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = Visualizer()
if 'auto_scaler' not in st.session_state:
    st.session_state.auto_scaler = AutoScaler(st.session_state.load_balancer, scale_up_threshold=80, scale_down_threshold=20)
if 'notification_method' not in st.session_state:
    st.session_state.notification_method = "Email"  # Default notification method
if 'recipient_email' not in st.session_state:
    st.session_state.recipient_email = ""

# Sidebar
st.sidebar.title("Configuration")
page = st.sidebar.selectbox("Select Page", ["Forecasting", "Load Balancing", "Settings"])

# Data generation parameters
with st.sidebar.expander("Data Configuration"):
    days = st.number_input("Number of days", min_value=30, max_value=365, value=90)
    if st.button("Generate New Data"):
        st.session_state.data = st.session_state.data_processor.generate_sample_data(days=days)
        st.session_state.prophet_data = st.session_state.data_processor.prepare_prophet_data()

# Initialize data if not exists
if 'data' not in st.session_state:
    st.session_state.data = st.session_state.data_processor.generate_sample_data()
    st.session_state.prophet_data = st.session_state.data_processor.prepare_prophet_data()

# Input field for recipient email
st.sidebar.text_input("Recipient Email", key='recipient_email', help="Enter the recipient email address for notifications.")

if page == "Forecasting":
    st.title("📈 Application Usage Forecasting")

    # Display raw data
    with st.expander("View Raw Data"):
        st.dataframe(st.session_state.data)

    # Forecasting parameters
    col1, col2 = st.columns(2)
    with col1:
        forecast_periods = st.slider("Forecast Periods (hours)", 24, 168, 24)
    with col2:
        target_col = st.selectbox("Target Variable", ["active_users", "server_load", "response_time"])

    # Train and forecast
    if st.button("Generate Forecast"):
        with st.spinner("Training model and generating forecast..."):
            prophet_data = st.session_state.data_processor.prepare_prophet_data(target_col)
            st.session_state.forecaster.train(prophet_data)
            forecast = st.session_state.forecaster.predict(periods=forecast_periods)
            
            # Plot forecast
            fig = st.session_state.visualizer.plot_forecast(forecast, prophet_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show metrics
            metrics = st.session_state.forecaster.get_metrics(
                prophet_data['y'][-forecast_periods:],
                forecast['yhat'][-forecast_periods:]
            )
            st.subheader("Forecast Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("MAE", f"{metrics['MAE']:.2f}")
            col2.metric("MSE", f"{metrics['MSE']:.2f}")
            col3.metric("RMSE", f"{metrics['RMSE']:.2f}")

            # Send notification
            recipient_email = st.session_state.recipient_email  # Get the recipient email from session state
            details = f"Forecast Periods: {forecast_periods}\nTarget Column: {target_col}\nMetrics:\nMAE: {metrics['MAE']:.2f}\nMSE: {metrics['MSE']:.2f}\nRMSE: {metrics['RMSE']:.2f}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            send_notification(st.session_state.notification_method, "Forecast generated successfully.", recipient_email, details)

elif page == "Load Balancing":
    st.title("⚖️ Load Balancing Simulation")

    # Load balancing parameters
    col1, col2 = st.columns(2)
    with col1:
        num_servers = st.slider("Number of Servers", 2, 10, 3)
        st.session_state.load_balancer = LoadBalancer(num_servers=num_servers)
    with col2:
        request_load = st.slider("Average Request Load", 10, 100, 50)

    # Load balancing algorithm selection
    algorithm = st.selectbox("Select Load Balancing Algorithm", ["Round Robin", "Least Connections", "IP Hash", "Weighted Round Robin"])

    # Simulate load balancing
    if st.button("Simulate Load Balancing"):
        with st.spinner("Simulating load balancing..."):
            # Simulate requests
            if algorithm == "Round Robin":
                for _ in range(100):
                    st.session_state.load_balancer.round_robin(request_load)
            elif algorithm == "Least Connections":
                for _ in range(100):
                    st.session_state.load_balancer.least_connections(request_load)
            elif algorithm == "IP Hash":
                for _ in range(100):
                    st.session_state.load_balancer.ip_hash(f"192.168.0.{_}", request_load)
            elif algorithm == "Weighted Round Robin":
                for _ in range(100):
                    st.session_state.load_balancer.weighted_round_robin(request_load)

            # Get and display metrics
            server_metrics = st.session_state.load_balancer.get_server_metrics()

            # Plot server loads
            fig = st.session_state.visualizer.plot_server_loads(server_metrics)
            st.plotly_chart(fig, use_container_width=True)

            # Display detailed metrics
            st.subheader("Server Metrics")
            cols = st.columns(len(server_metrics))
            for i, (server, metrics) in enumerate(server_metrics.items()):
                cols[i].metric(
                    f"Server {i}",
                    f"Load: {metrics['avg_load']:.1f}",
                    f"Response: {metrics['avg_response_time']:.1f}ms"
                )

            # Send notification
            recipient_email = st.session_state.recipient_email  # Get the recipient email from session state
            details = f"Algorithm: {algorithm}\nNumber of Servers: {num_servers}\nRequest Load: {request_load}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            send_notification(st.session_state.notification_method, "Load balancing simulation completed.", recipient_email, details)

    # Auto-scaling check
    if st.button("Check Auto-scaling"):
        st.session_state.auto_scaler.check_and_scale()
        st.write(f"Number of Servers: {st.session_state.load_balancer.num_servers}")
        # Send notification
        recipient_email = st.session_state.recipient_email  # Get the recipient email from session state
        details = f"Auto-scaling check completed.\nNumber of Servers: {st.session_state.load_balancer.num_servers}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_notification(st.session_state.notification_method, "Auto-scaling check completed.", recipient_email, details)

elif page == "Settings":
    st.title("⚙️ Settings")

    # Customizable settings
    st.subheader("Forecasting Model Settings")
    forecasting_model = st.selectbox("Select Forecasting Model", ["Prophet", "ARIMA", "XGBoost"])
    st.write(f"Current model: {forecasting_model}")

    st.subheader("Load Balancing Algorithm Settings")
    load_balancing_algorithm = st.selectbox("Select Load Balancing Algorithm", ["Round Robin", "Least Connections", "IP Hash", "Weighted Round Robin"])
    st.write(f"Current algorithm: {load_balancing_algorithm}")

    st.subheader("Notification Preferences")
    notification_method = st.selectbox("Notification Method", ["Email"])
    st.session_state.notification_method = notification_method  # Save the selected notification method
    st.write(f"Current notification method: {notification_method}")

    st.subheader("Appearance")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    st.write(f"Current theme: {theme}")