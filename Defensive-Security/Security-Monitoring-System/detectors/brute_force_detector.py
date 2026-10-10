import time
import ipaddress
from datetime import datetime
from alerts.alert_manager import create_alert


failed_attempts = {}
last_alert_time = {}


def process_failed_login(ip_address, timestamp, threshold, time_window):

    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = []

    failed_attempts[ip_address].append(timestamp)

    recent_attempts = []

    for attempt_time in failed_attempts[ip_address]:

        time_difference = (
            timestamp - attempt_time
        ).total_seconds()

        if 0 <= time_difference <= time_window:
            recent_attempts.append(attempt_time)

    failed_attempts[ip_address] = recent_attempts

    if len(recent_attempts) >= threshold:

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
                "Brute Force Detector",
                f"Possible brute-force attack from {ip_address}: "
                f"{len(recent_attempts)} failed attempts within {time_window} seconds"
            )

            last_alert_time[ip_address] = timestamp


def process_log_line(line, threshold, time_window):

    # Ignore empty lines and unrelated log entries
    if not line.strip() or "Failed password" not in line:
        return

    try:
        parts = line.split()

        # Validate the basic log structure
        if len(parts) < 4:
            raise ValueError("Invalid authentication log format")

        time_string = parts[2]

        # Find the IP address after the word "from"
        if "from" not in parts:
            raise ValueError("Missing source IP address")

        from_index = parts.index("from")

        if from_index + 1 >= len(parts):
            raise ValueError("Missing IP address after 'from'")

        ip_address = parts[from_index + 1]

        # Validate the IP address
        ipaddress.ip_address(ip_address)

        # Convert the timestamp
        timestamp = datetime.strptime(
            time_string,
            "%H:%M:%S"
        )

        # Process the failed login attempt
        process_failed_login(
            ip_address,
            timestamp,
            threshold,
            time_window
        )

    except (ValueError, IndexError) as error:
        print(
            f"[WARNING] Brute Force Detector skipped invalid log entry: "
            f"{line.strip()} ({error})"
        )


def monitor_log(file_path, threshold, time_window):

    with open(file_path, "r") as file:

        # Start monitoring new entries only
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line:
                time.sleep(1)
                continue

            # Pass each entry to the processing function
            process_log_line(
                line,
                threshold,
                time_window
            )