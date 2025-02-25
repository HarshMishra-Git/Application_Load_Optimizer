import numpy as np
from collections import defaultdict

class LoadBalancer:
    def __init__(self, num_servers=3):
        self.num_servers = num_servers
        self.current_server = 0
        self.server_loads = defaultdict(list)
        self.server_response_times = defaultdict(list)
        self.connection_counts = defaultdict(int)  # For Least Connections
        self.weights = [1] * num_servers  # Default weights for Weighted Round Robin

        # Initialize server loads
        for server in range(num_servers):
            self.server_loads[server] = []
            self.server_response_times[server] = []
            self.connection_counts[server] = 0

    def round_robin(self, request_load):
        """Implement round-robin load balancing"""
        selected_server = self.current_server
        
        # Simulate server load
        load = np.random.normal(request_load, request_load * 0.1)
        response_time = load * np.random.uniform(0.8, 1.2)
        
        self.server_loads[selected_server].append(load)
        self.server_response_times[selected_server].append(response_time)
        
        # Update current server
        self.current_server = (self.current_server + 1) % self.num_servers
        
        return selected_server, load, response_time

    def least_connections(self, request_load):
        """Implement least connections load balancing"""
        selected_server = min(self.connection_counts, key=self.connection_counts.get)
        
        # Simulate server load
        load = np.random.normal(request_load, request_load * 0.1)
        response_time = load * np.random.uniform(0.8, 1.2)
        
        self.server_loads[selected_server].append(load)
        self.server_response_times[selected_server].append(response_time)
        self.connection_counts[selected_server] += 1
        
        return selected_server, load, response_time

    def ip_hash(self, request_ip, request_load):
        """Implement IP hash load balancing"""
        selected_server = hash(request_ip) % self.num_servers
        
        # Simulate server load
        load = np.random.normal(request_load, request_load * 0.1)
        response_time = load * np.random.uniform(0.8, 1.2)
        
        self.server_loads[selected_server].append(load)
        self.server_response_times[selected_server].append(response_time)
        
        return selected_server, load, response_time

    def weighted_round_robin(self, request_load):
        """Implement weighted round-robin load balancing"""
        server_weights = np.cumsum(self.weights)
        total_weight = server_weights[-1]
        random_weight = np.random.uniform(0, total_weight)
        selected_server = np.searchsorted(server_weights, random_weight)
        
        # Simulate server load
        load = np.random.normal(request_load, request_load * 0.1)
        response_time = load * np.random.uniform(0.8, 1.2)
        
        self.server_loads[selected_server].append(load)
        self.server_response_times[selected_server].append(response_time)
        
        return selected_server, load, response_time

    def get_server_metrics(self):
        """Calculate server performance metrics"""
        metrics = {}
        
        for server in range(self.num_servers):
            metrics[f'server_{server}'] = {
                'avg_load': np.mean(self.server_loads[server]) if self.server_loads[server] else 0,
                'max_load': np.max(self.server_loads[server]) if self.server_loads[server] else 0,
                'avg_response_time': np.mean(self.server_response_times[server]) if self.server_response_times[server] else 0
            }
            
        return metrics