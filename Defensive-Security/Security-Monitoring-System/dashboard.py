from alerts.alert_manager import alerts


def display_dashboard():

    total_alerts = len(alerts)

    critical_count = 0
    high_count = 0
    medium_count = 0
    info_count = 0

    brute_force_count = 0
    file_integrity_count = 0
    network_count = 0

    for alert in alerts:

        severity = alert["severity"]

        if severity == "CRITICAL":
            critical_count += 1

        elif severity == "HIGH":
            high_count += 1

        elif severity == "MEDIUM":
            medium_count += 1

        elif severity == "INFO":
            info_count += 1

        detector = alert["detector"]

        if detector == "Brute Force Detector":
            brute_force_count += 1

        elif detector == "File Integrity Monitor":
            file_integrity_count += 1

        elif detector == "Network Detector":
            network_count += 1

    print("\n" + "=" * 50)
    print("              SECURITY DASHBOARD")
    print("=" * 50)

    print(f"Total Alerts: {total_alerts}")
    print()
    print(f"CRITICAL: {critical_count}")
    print(f"HIGH:     {high_count}")
    print(f"MEDIUM:   {medium_count}")
    print(f"INFO:     {info_count}")

    print()
    print("Alerts by Detector:")
    print(f"Brute Force Detector:    {brute_force_count}")
    print(f"File Integrity Monitor:  {file_integrity_count}")
    print(f"Network Detector:        {network_count}")

    print("=" * 50)