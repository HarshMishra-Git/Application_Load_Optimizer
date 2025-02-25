import numpy as np

class MetricsCalculator:
    @staticmethod
    def calculate_utilization(server_loads, capacity=100):
        """Calculate server utilization percentage"""
        return np.mean(server_loads) / capacity * 100
    
    @staticmethod
    def calculate_load_distribution(server_metrics):
        """Calculate load distribution across servers"""
        loads = [metrics['avg_load'] for metrics in server_metrics.values()]
        return {
            'min_load': np.min(loads),
            'max_load': np.max(loads),
            'std_load': np.std(loads),
            'load_imbalance': np.max(loads) - np.min(loads)
        }
    
    @staticmethod
    def calculate_performance_metrics(response_times):
        """Calculate performance metrics"""
        return {
            'avg_response_time': np.mean(response_times),
            'p95_response_time': np.percentile(response_times, 95),
            'p99_response_time': np.percentile(response_times, 99)
        }
