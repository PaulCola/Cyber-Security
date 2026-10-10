from datetime import datetime


alerts = []


def create_alert(severity, detector, message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert = {
        "timestamp": timestamp,
        "severity": severity,
        "detector": detector,
        "message": message
    }

    alerts.append(alert)

    formatted_alert = (
        f"{alert['timestamp']} | "
        f"{alert['severity']} | "
        f"{alert['detector']} | "
        f"{alert['message']}"
    )

    print(formatted_alert)

    with open("logs/security_alerts.log", "a") as file:
        file.write(formatted_alert + "\n")