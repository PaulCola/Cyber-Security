# Offensive Security Projects

### Network Diagnostics | Penetration Testing | Security Assessment

This section of my cybersecurity portfolio focuses on **offensive security, network reconnaissance, and vulnerability assessment fundamentals**.

Through hands-on development projects, I explore how networks and web services can be examined, how potential security weaknesses are identified, and how technical findings can be documented and analyzed.

My goal is to strengthen my understanding of networking, IT infrastructure, troubleshooting, and the methodologies used in penetration testing and security assessments.

## Featured Project

### PenTest Toolkit

**[View PenTest Toolkit](./PenTest-Toolkit/)**

A full-stack web application developed to integrate network reconnaissance and security testing tools into a centralized, user-friendly interface.

The application uses **React, TypeScript, Python, FastAPI, and SQLite** to manage scans, display results, and maintain scan history.

The toolkit currently includes two functional modules:

**1. Nmap — Network Discovery & Port Scanning**
- Executes Nmap scans through a web-based interface.
- Identifies open ports and available network services.
- Displays structured scan results for technical analysis.
- Supports scan cancellation and execution tracking.
- Maintains scan history for later review.
- Exports results in TXT and JSON formats.

**2. Gobuster — Web Directory Enumeration**
- Performs web directory enumeration against authorized test targets.
- Identifies accessible and potentially hidden web paths.
- Displays discovered paths and HTTP response information.
- Supports configurable scan options and custom wordlists.
- Provides scan cancellation and execution tracking.
- Stores previous scans for review and comparison.
- Exports results in TXT and JSON formats.

### Additional Functionality

- Centralized dashboard for accessing scanning modules.
- Workspace-based organization of scan activity.
- Persistent scan history using SQLite.
- Frontend-to-backend communication through REST APIs.
- Scan status monitoring and error handling.
- Structured results and downloadable reports.

## Technical Skills Demonstrated

| Skill Area | Practical Application |
|---|---|
| Networking Fundamentals | TCP/IP, ports, protocols, and service discovery |
| Network Troubleshooting | Investigating exposed services and network connectivity |
| Web Technologies | HTTP responses, URLs, and web server behaviour |
| Python Development | Backend services and command-line tool integration |
| API Development | Building REST endpoints using FastAPI |
| Frontend Development | React, TypeScript, and user interface design |
| Database Management | SQLite storage and retrieval of scan history |
| Technical Documentation | Organizing, reviewing, and exporting scan results |
| Security Fundamentals | Network reconnaissance and web enumeration |

## Relevance to IT Support

Although this project focuses on offensive security, many of the technical concepts are directly applicable to IT Support and infrastructure troubleshooting.

Through developing the toolkit, I have gained practical experience with:

- Understanding how devices communicate across networks.
- Identifying ports and services running on network hosts.
- Working with command-line networking utilities.
- Troubleshooting frontend, backend, and API connectivity.
- Investigating application errors and unexpected responses.
- Managing local development environments and dependencies.
- Organizing technical findings into readable reports.

These skills support my broader development in technical support, network administration, systems troubleshooting, and cybersecurity.

## Technologies Used

| Category | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | SQLite |
| Security Tools | Nmap, Gobuster |
| Development Environment | Windows, PowerShell, Git, GitHub |

## Future Development

I plan to expand the toolkit with additional security testing capabilities, including:

- WhatWeb for web technology identification.
- Nikto for web server security scanning.
- Additional scan configuration and reporting features.
- Improved result visualization and analysis.
- Expanded network diagnostic functionality.

These features are planned and are not part of the current implementation.

## Responsible Security Practices

All offensive security projects are developed for educational purposes and intended for testing within authorized environments.

Scanning and security assessment activities should only be performed against systems where explicit permission has been granted.

---

**[Back to Main Cybersecurity Portfolio](../README.md)**
