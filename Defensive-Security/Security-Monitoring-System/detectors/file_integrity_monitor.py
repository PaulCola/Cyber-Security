import hashlib
from alerts.alert_manager import create_alert
import time

file_hashes = {}
missing_files = set()

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def register_file(file_path):
    file_hashes[file_path] = calculate_hash(file_path)

    print(f"[+] Monitoring file: {file_path}")



def check_file(file_path):

    try:
        current_hash = calculate_hash(file_path)

        # If the file was previously missing but now exists again
        if file_path in missing_files:
            create_alert(
                "INFO",
                "File Integrity Monitor",
                f"Monitored file restored: {file_path}"
            )

            missing_files.remove(file_path)

            # Establish a new baseline for the restored file
            file_hashes[file_path] = current_hash
            return

        if current_hash != file_hashes[file_path]:
            create_alert(
                "CRITICAL",
                "File Integrity Monitor",
                f"File modification detected: {file_path}"
            )

            file_hashes[file_path] = current_hash

    except FileNotFoundError:

        # Only alert if we haven't already reported this file missing
        if file_path not in missing_files:
            create_alert(
                "CRITICAL",
                "File Integrity Monitor",
                f"Monitored file missing: {file_path}"
            )

            missing_files.add(file_path)

    except PermissionError:
        create_alert(
            "HIGH",
            "File Integrity Monitor",
            f"Permission denied while accessing: {file_path}"
        )

def monitor_file(file_path, check_interval):
    register_file(file_path)

    while True:
        check_file(file_path)
        time.sleep(check_interval)
