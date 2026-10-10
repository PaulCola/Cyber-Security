import threading
import time

from dashboard import display_dashboard
from detectors.brute_force_detector import monitor_log
from detectors.file_integrity_monitor import monitor_file
from detectors.network_detector import monitor_network_log
from config.config_loader import load_config

config = load_config()


AUTH_LOG = "logs/sample_auth.log"
NETWORK_LOG = "logs/sample_network.log"
FILE_TO_MONITOR = "monitored_files/important.txt"


def main():

    print("=" * 50)
    print("       SECURITY MONITORING SYSTEM")
    print("=" * 50)

    file_monitor_thread = threading.Thread(
    target=monitor_file,
    args=(
        FILE_TO_MONITOR,
        config["file_integrity"]["check_interval"]
        ),
        daemon=True
    )
    brute_force_thread = threading.Thread(
    target=monitor_log,
    args=(
        AUTH_LOG,
        config["brute_force"]["threshold"],
        config["brute_force"]["time_window"]
        ),
        daemon=True
    )

    network_thread = threading.Thread(
    target=monitor_network_log,
    args=(
        NETWORK_LOG,
        config["network"]["port_threshold"],
        config["network"]["time_window"]
        ),
        daemon=True
    )

    file_monitor_thread.start()
    brute_force_thread.start()
    network_thread.start()

    print("[+] File Integrity Monitor: ONLINE")
    print("[+] Brute Force Detector: ONLINE")
    print("[+] Network Detector: ONLINE")
    print("[+] Security monitoring system running")
    print("[+] Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[+] Security monitoring system stopped")
        display_dashboard()


if __name__ == "__main__":
    main()