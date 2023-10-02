import psutil
import json

# Function to collect CPU metrics
def collect_cpu_metrics():
    cpu_metrics = {
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_percent": psutil.cpu_percent(interval=1, percpu=True),
        "cpu_times_percent": [entry._asdict() for entry in psutil.cpu_times_percent(interval=1, percpu=True)],
        "cpu_count": psutil.cpu_count(logical=False),  # Physical CPU count
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "cpu_freq": psutil.cpu_freq(percpu=True),
        "load_avg": psutil.getloadavg(),
    }
    return cpu_metrics

# Function to collect memory metrics
def collect_memory_metrics():
    memory_metrics = {
        "virtual_memory": psutil.virtual_memory()._asdict(),
        "swap_memory": psutil.swap_memory()._asdict(),
    }
    return memory_metrics

# Function to collect disk metrics
def collect_disk_metrics():
    partitions = psutil.disk_partitions()
    disk_metrics = {}
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)._asdict()
            io_counters = psutil.disk_io_counters(perdisk=True).get(partition.device, {})
            disk_metrics[partition.device] = {
                "usage": usage,
                "io_counters": io_counters,
            }
        except (PermissionError, FileNotFoundError) as e:
            # Handle the exception, e.g., print a message or log it
            print(f"Error accessing {partition.device}: {e}")
    return disk_metrics

# Function to collect network metrics
def collect_network_metrics():
    network_metrics = {
        "net_io_counters": psutil.net_io_counters()._asdict(),
        "net_connections": [conn._asdict() for conn in psutil.net_connections(kind="inet")],
        "net_if_addrs": {iface: [addr._asdict() for addr in addrs] for iface, addrs in psutil.net_if_addrs().items()},
    }
    return network_metrics

# Function to collect sensor metrics (if available)
def collect_sensor_metrics():
    try:
        sensor_metrics = {
            "sensors_temperatures": psutil.sensors_temperatures(fahrenheit=False),
            "sensors_fans": psutil.sensors_fans(),
        }
        return sensor_metrics
    except AttributeError:
        return {}  # Some systems may not support sensors

# Function to collect other system metrics
def collect_other_metrics():
    other_metrics = {
        "boot_time": psutil.boot_time(),
        "users": [user._asdict() for user in psutil.users()],
    }
    return other_metrics

# Main function to collect all metrics
def collect_all_metrics():
    all_metrics = {
        "cpu_metrics": collect_cpu_metrics(),
        "memory_metrics": collect_memory_metrics(),
        "disk_metrics": collect_disk_metrics(),
        "network_metrics": collect_network_metrics(),
        "sensor_metrics": collect_sensor_metrics(),
        "other_metrics": collect_other_metrics(),
    }
    return all_metrics

if __name__ == "__main__":
    metrics_data = collect_all_metrics()

    # You can now use metrics_data in your main Python script.
    # For example, you can convert it to JSON and save it to a file.
    with open("metrics.json", "w") as f:
        json.dump(metrics_data, f, indent=4)

    print("Metrics data collected and saved to 'metrics.json'")
