import psutil
import time
import json

def collect_metrics():
    metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "network_usage": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    }
    return metrics

if __name__ == "__main__":
    while True:
        metrics = collect_metrics()
        print(json.dumps(metrics, indent=4))
        time.sleep(5)  # Collect data every 5 seconds
