# Windows IT Support Diagnostics Tool

A PowerShell-based diagnostic utility designed to automate common Windows troubleshooting tasks, identify potential system and network issues, and generate reports for IT Support investigations.

## Overview

This project demonstrates practical Windows administration, networking, system monitoring, and troubleshooting skills through an automated command-line application.

The tool collects diagnostic information, evaluates system health, and provides recommendations for issues requiring further investigation.

## Features

### System Information
- Retrieves the computer hostname and Windows operating system.
- Identifies the installed processor and total physical memory.
- Calculates system uptime.

### Network Diagnostics
- Identifies the active IPv4 address, default gateway, and configured DNS servers.
- Tests connectivity to the default gateway.
- Checks DNS resolution.
- Tests HTTPS connectivity using TCP port 443.

### System Health Monitoring
- Retrieves local disk capacity and available storage.
- Flags drives with less than 20% available space.
- Checks the status of selected Windows services.

### Automated Troubleshooting
- Identifies potential connectivity, DNS, storage, and service issues.
- Generates recommendations based on diagnostic results.
- Reports multiple issues independently.

### Diagnostic Report Generation
- Exports timestamped diagnostic reports in TXT format.
- Includes system information, network diagnostics, disk health, service status, and troubleshooting recommendations.
- Saves reports locally in a dedicated `reports` folder.

## Technologies Used

- PowerShell
- Windows Management Instrumentation through CIM
- Windows networking cmdlets
- Windows service management
- Git and GitHub

## Getting Started

### Requirements

- Windows 10 or Windows 11
- Windows PowerShell 5.1 or a compatible PowerShell environment
- Visual Studio Code or another text editor (optional)

### Running the Application

Clone the repository or download the project files.

Open PowerShell in the project directory and execute:

```powershell
.\diagnostics.ps1
```

The application runs diagnostic checks and displays the results in the terminal.

A timestamped report is automatically generated in the `reports` directory.

If script execution is restricted, review your organization's execution policy before running the application.

## Example Diagnostic Output

```text
==================================
       NETWORK DIAGNOSTICS
==================================
IPv4 Address: 192.168.2.188
Default Gateway: 192.168.2.1

[PASS] Default gateway is reachable
[PASS] DNS resolution successful
[PASS] HTTPS connectivity successful

==================================
       SYSTEM HEALTH
==================================

--- Disk Space ---
C: - 53 GB free (5.7%)
[WARNING] Low disk space on C:

--- Windows Services ---
[PASS] Winmgmt is running
[PASS] EventLog is running
[PASS] Dhcp is running

==================================
   TROUBLESHOOTING RECOMMENDATIONS
==================================

Issues requiring attention: 1

[RECOMMENDATION] LOW DISK SPACE on C: -
Review Storage settings, temporary files,
and unused applications.
```

*Example output is based on a local test and may differ depending on the computer.*

## Testing and Validation

The application was tested on Windows 11.

Testing included:

- Successful retrieval of system and network information.
- Verification of gateway, DNS, and HTTPS connectivity.
- Detection of low available disk space.
- Identification of a simulated DNS resolution failure.
- Generation of troubleshooting recommendations for multiple simultaneous warnings.
- Successful export of timestamped diagnostic reports.

## Project Structure

```text
IT-Support-Diagnostics/
├── diagnostics.ps1
├── README.md
├── .gitignore
└── reports/            # Generated locally; excluded from Git
```

## Skills Demonstrated

- Windows system administration
- PowerShell scripting and automation
- TCP/IP and DNS troubleshooting
- System health monitoring
- Windows service inspection
- Conditional logic and error handling
- Technical documentation and diagnostic reporting

## Limitations and Future Improvements

- Network checks currently use predefined destinations.
- A failed ping does not necessarily indicate that a device is offline.
- Service checks do not yet account for services configured to start only when needed.
- Future improvements may include configurable thresholds, multiple connectivity targets, structured JSON reports, and more detailed diagnostic summaries.

## Disclaimer

This tool is intended for educational purposes and authorized IT troubleshooting. It collects diagnostic information without automatically modifying system settings.

Generated reports may contain device and network information and are excluded from version control.