import asyncio
import websockets
import json
import logging
import socket

class RealTimeMonitor:
    def __init__(self, load_balancer):
        self.load_balancer = load_balancer

    async def monitor_load(self, websocket, path):
        try:
            while True:
                server_metrics = self.load_balancer.get_server_metrics()
                await websocket.send(json.dumps(server_metrics))
                await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosedError as e:
            logging.error(f"WebSocket connection closed with exception: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in monitor_load: {e}")

async def start_real_time_monitor(load_balancer, port=6790):
    monitor = RealTimeMonitor(load_balancer)
    start_server = websockets.serve(monitor.monitor_load, "localhost", port)
    await start_server

def find_free_port():
    """Find a free port to use for the WebSocket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]