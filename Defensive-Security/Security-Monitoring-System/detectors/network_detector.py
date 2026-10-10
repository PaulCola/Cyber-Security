
import time
import ipaddress
from datetime import datetime
from alerts.alert_manager import create_alert


connection_attempts = {}
last_alert_time = {}


def process_connection(ip_address, port, timestamp, port_threshold, time_window):

    if ip_address not in connection_attempts:
        connection_attempts[ip_address] = []

    connection_attempts[ip_address].append(
        (timestamp, port)
    )

    recent_connections = []

    for connection_time, connection_port in connection_attempts[ip_address]:

        time_difference = (
            timestamp - connection_time
        ).total_seconds()

        if 0 <= time_difference <= time_window:
            recent_connections.append(
                (connection_time, connection_port)
            )

    connection_attempts[ip_address] = recent_connections

    unique_ports = set()

    for connection_time, connection_port in recent_connections:
        unique_ports.add(connection_port)

    if len(unique_ports) >= port_threshold:

        should_alert = False

        if ip_address not in last_alert_time:
            should_alert = True

        else:
            seconds_since_alert = (
                timestamp - last_alert_time[ip_address]
            ).total_seconds()

            if seconds_since_alert >= time_window:
                should_alert = True

        if should_alert:
            create_alert(
                "HIGH",
                "Network Detector",
                f"Possible port scan from {ip_address}: "
                f"{len(unique_ports)} unique ports within {time_window} seconds"
            )

            last_alert_time[ip_address] = timestamp


def process_network_log_line(line, port_threshold, time_window):

    if not line.strip():
        return

    try:
        parts = line.split()

        if len(parts) != 3:
            raise ValueError("Invalid network log format")

        timestamp_string = parts[0]
        ip_address = parts[1]
        port = int(parts[2])

        # Validate the IP address
        ipaddress.ip_address(ip_address)

        # Validate the port number
        if not 1 <= port <= 65535:
            raise ValueError("Port must be between 1 and 65535")

        # Validate the timestamp
        timestamp = datetime.strptime(
            timestamp_string,
            "%H:%M:%S"
        )

        process_connection(
            ip_address,
            port,
            timestamp,
            port_threshold,
            time_window
        )

    except (ValueError, IndexError) as error:
        print(
            f"[WARNING] Network Detector skipped invalid log entry: "
            f"{line.strip()} ({error})"
        )


def monitor_network_log(file_path, port_threshold, time_window):

    with open(file_path, "r") as file:

        # Monitor new log entries only
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line:
                time.sleep(1)
                continue

            process_network_log_line(
                line,
                port_threshold,
                time_window
            )
