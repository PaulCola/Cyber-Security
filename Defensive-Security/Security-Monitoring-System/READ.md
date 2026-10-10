# Security Monitoring System

A Python-based security monitoring system designed to detect suspicious activity through log analysis, network connection monitoring, and file integrity checks.

This project demonstrates foundational **Blue Team cybersecurity concepts**, including threat detection, security event monitoring, alert generation, and incident visibility.

The system uses multithreading to run three independent security detectors simultaneously and provides a summary dashboard when monitoring stops.

## Features

### 1. Brute Force Detection
- Monitors simulated SSH authentication logs for failed login attempts.
- Tracks failed attempts by source IP address.
- Detects potential brute-force attacks based on configurable thresholds and time windows.
- Validates IP addresses and timestamps.
- Uses an alert cooldown to reduce duplicate alerts.

### 2. Network Port Scan Detection
- Monitors simulated network connection logs.
- Tracks unique destination ports accessed by individual source IP addresses.
- Identifies potential port-scanning activity.
- Validates IP addresses, port numbers, and timestamps.
- Uses configurable detection thresholds and alert cooldowns.

### 3. File Integrity Monitoring
- Uses SHA-256 hashing to monitor file integrity.
- Detects unauthorized or unexpected file modifications.
- Identifies file deletion and restoration.
- Establishes a new monitoring baseline when a deleted file is restored.
- Prevents repeated missing-file alerts during the same deletion incident.

### 4. Centralized Alert Management
- Generates alerts with timestamps, severity levels, detector names, and descriptions.
- Displays security alerts in the terminal.
- Stores generated alerts in `logs/security_alerts.log`.
- Tracks alerts generated during the current monitoring session.

### 5. Security Dashboard
- Displays the total number of alerts detected.
- Groups alerts by severity: CRITICAL, HIGH, MEDIUM, and INFO.
- Shows alert counts for each detector.
- Provides a summary when the application is stopped using `Ctrl+C`.

## Technologies Used

- **Python 3**
- Python standard library (`threading`, `datetime`, `hashlib`, `ipaddress`, `json`, `unittest`)
- SHA-256 hashing
- Log parsing and validation
- Multithreading
- Automated unit testing

## Project Structure

```text
Security-Monitoring-System/
├── alerts/
│   ├── __init__.py
│   └── alert_manager.py
├── config/
│   ├── config.json
│   └── config_loader.py
├── detectors/
│   ├── __init__.py
│   ├── brute_force_detector.py
│   ├── file_integrity_monitor.py
│   └── network_detector.py
├── logs/
│   ├── sample_auth.log
│   └── sample_network.log
├── monitored_files/
│   └── important.txt
├── tests/
│   ├── test_brute_force.py
│   ├── test_file_integrity.py
│   └── test_network.py
├── main.py
├── dashboard.py
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3 installed
- Git (optional, for cloning the repository)

The project uses Python's standard library and does not require additional third-party packages.

### Installation

Clone the repository:

```bash
git clone https://github.com/PaulCola/Security-Monitoring-System.git
```

Navigate to the project directory:

```bash
cd Security-Monitoring-System
```

Alternatively, download the repository as a ZIP file and extract it.

### Running the System

From the project root directory, run:

```bash
python main.py
```

The application starts all three detectors:

```text
==================================================
       SECURITY MONITORING SYSTEM
==================================================
[+] File Integrity Monitor: ONLINE
[+] Brute Force Detector: ONLINE
[+] Network Detector: ONLINE
[+] Security monitoring system running
[+] Press Ctrl+C to stop
```

The system monitors new entries appended to the sample log files and checks the configured monitored file for changes.

Press `Ctrl+C` to stop monitoring and display the security dashboard.

## Configuration

Detection settings are stored in `config/config.json`.

Example configuration:

```json
{
  "brute_force": {
    "threshold": 3,
    "time_window": 60
  },
  "file_integrity": {
    "check_interval": 2
  },
  "network": {
    "port_threshold": 3,
    "time_window": 60
  }
}
```

Settings can be adjusted to change detection sensitivity and monitoring intervals. Restart the application after modifying the configuration.

## Example Security Alerts

The following alerts were generated during a successful integration test:

```text
HIGH | Brute Force Detector | Possible brute-force attack from 192.168.1.25: 3 failed attempts within 60 seconds

HIGH | Network Detector | Possible port scan from 192.168.1.50: 3 unique ports within 60 seconds

CRITICAL | File Integrity Monitor | File modification detected: monitored_files/important.txt
```

### Example Dashboard Output

```text
==================================================
              SECURITY DASHBOARD
==================================================
Total Alerts: 3

CRITICAL: 1
HIGH:     2
MEDIUM:   0
INFO:     0

Alerts by Detector:
Brute Force Detector:    1
File Integrity Monitor:  1
Network Detector:        1
==================================================
```

This integration test confirmed that all three detectors could operate simultaneously and generate alerts that were correctly summarized by the dashboard.

## Automated Testing

The project includes automated tests using Python's built-in `unittest` framework.

Run all tests from the project root directory:

```bash
python -m unittest discover -s tests -v
```

### Test Coverage

| Component | Tests | Verified Behaviors |
|---|---:|---|
| Brute Force Detector | 7 | Detection, cooldown, thresholds, time windows, invalid IPs, invalid timestamps, missing IPs |
| Network Detector | 7 | Detection, cooldown, thresholds, time windows, invalid IPs, invalid ports, invalid timestamps |
| File Integrity Monitor | 4 | Modification, deletion, restoration, and monitoring after restoration |
| **Total** | **18** | **18 passing automated tests** |

The tests verify selected detection and error-handling behaviors. They do not represent exhaustive or 100% code coverage.

## Skills Demonstrated

Through this project, I gained practical experience with:

- Python programming and modular application design
- Blue Team security monitoring concepts
- Authentication log analysis
- Brute-force and port-scan detection logic
- File integrity verification using cryptographic hashing
- Multithreading and concurrent monitoring
- Input validation and error handling
- Configurable detection rules
- Alert management and reporting
- Automated testing and debugging

## Limitations

This is an educational cybersecurity project built to demonstrate security monitoring concepts.

- The authentication and network detectors operate on simulated log files rather than directly capturing live system or network events.
- Log timestamps use a time-only format, which limits handling of events spanning midnight.
- Monitoring is designed for a single local application instance.
- The dashboard summarizes alerts generated during the current session rather than providing historical analytics.
- The system is not intended to replace production SIEM, endpoint detection, or intrusion detection solutions.

## Future Improvements

Potential future enhancements include:

- Integration with real operating system authentication logs
- Live network traffic analysis
- Persistent alert storage and historical reporting
- Email or webhook notifications
- A graphical dashboard
- Improved timestamp handling and log rotation support

## Project Status

**Version 1.0 — Core implementation and testing complete**

- Three operational security detectors
- Configurable detection thresholds
- Centralized alert logging
- Terminal-based security dashboard
- 18 passing automated tests
- Successful end-to-end integration test

## Disclaimer

This project is intended for educational purposes and authorized security monitoring demonstrations only.