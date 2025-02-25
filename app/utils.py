import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_forecast(forecast_df, actual_df, target_col='active_users'):
        """Create forecast vs actual plot"""
        fig = go.Figure()

        # Add actual values
        fig.add_trace(go.Scatter(
            x=actual_df['ds'],
            y=actual_df['y'],
            name='Actual',
            line=dict(color='blue')
        ))

        # Add forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            name='Forecast',
            line=dict(color='red')
        ))

        # Add confidence intervals
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'].tolist() + forecast_df['ds'].tolist()[::-1],
            y=forecast_df['yhat_upper'].tolist() + forecast_df['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval'
        ))

        fig.update_layout(
            title=f'{target_col} Forecast vs Actual',
            xaxis_title='Time',
            yaxis_title=target_col,
            hovermode='x unified'
        )

        return fig

    @staticmethod
    def plot_server_loads(server_metrics):
        """Create server load distribution plot"""
        servers = list(server_metrics.keys())
        loads = [metrics['avg_load'] for metrics in server_metrics.values()]

        fig = go.Figure(data=[
            go.Bar(
                x=servers,
                y=loads,
                marker_color='lightblue'
            )
        ])

        fig.update_layout(
            title='Server Load Distribution',
            xaxis_title='Server',
            yaxis_title='Average Load',
            hovermode='x'
        )

        return fig

    @staticmethod
    def plot_historical_data(data_df, target_col='load'):
        """Create historical data analysis plot"""
        fig = px.line(data_df, x='timestamp', y=target_col, title='Historical Load Data')
        return fig