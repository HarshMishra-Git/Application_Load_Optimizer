import numpy as np
class AutoScaler:
    import numpy as np
    def __init__(self, load_balancer, scale_up_threshold, scale_down_threshold):
        self.load_balancer = load_balancer
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold

    def scale_up(self):
        """Add a new server to the load balancer"""
        self.load_balancer.num_servers += 1

    def scale_down(self):
        """Remove a server from the load balancer"""
        if self.load_balancer.num_servers > 1:
            self.load_balancer.num_servers -= 1

    def check_and_scale(self):
        """Check server loads and scale up/down as needed"""
        avg_loads = [np.mean(loads) for loads in self.load_balancer.server_loads.values() if loads]
        if not avg_loads:
            return

        max_load = max(avg_loads)

        if max_load > self.scale_up_threshold:
            self.scale_up()
        elif max_load < self.scale_down_threshold:
            self.scale_down()