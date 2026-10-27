PenTest Toolkit
Network Diagnostics & Security Testing Application
PenTest Toolkit is a full-stack desktop-oriented web application that brings network reconnaissance and web enumeration tools into one interface. I developed it to strengthen my understanding of networking, command-line utilities, application troubleshooting, and full-stack development while practicing security testing in authorized lab environments.

The application currently integrates Nmap and Gobuster, allowing users to configure scans, monitor execution, review structured results, save workspace-specific scan history, and export reports.
Project status: Functional portfolio project; additional modules and improvements are planned.

Why I Built It
My goal was to go beyond running commands individually and build an application that connects the user interface, backend services, operating-system processes, and persistent data storage.

The project gave me practical experience with skills relevant to IT Support and junior technical roles, including:
- Understanding TCP/IP networking, ports, and network services.
- Interpreting HTTP responses and troubleshooting web service accessibility.
- Using Windows PowerShell and command-line tools to configure and test software.
- Diagnosing issues across a React frontend, Python API, and external utilities.
- Managing application processes, errors, and scan cancellation.
- Organizing technical results into repeatable reports and historical records.
Features
Nmap — Network and Service Discovery
The Nmap module provides a graphical interface for running supported network scans against permitted lab targets.
- Six available scan configurations.
- Scan execution with progress timing and cancellation.
- Structured parsing of Nmap XML output.
- Results organized for easier review of discovered hosts, ports, and services.
- Workspace-specific scan history stored in SQLite.
- Saved scan retrieval and deletion.
- TXT and JSON report exports.
IT Support relevance: Reinforces networking fundamentals, port and service identification, and the interpretation of diagnostic information used when investigating connectivity or service availability issues.
Gobuster — Web Directory Enumeration
The Gobuster module provides an interface for testing web paths on authorized local or private lab targets.
- URL-based scan configuration with an included starter wordlist.
- Live elapsed-time display and scan cancellation.
- Structured results showing discovered paths, HTTP status codes, and response sizes.
- Counts of successful responses and redirects.
- Workspace-specific scan history, with View, Refresh, and Delete actions.
- TXT and JSON report exports.
- Access to raw terminal output for troubleshooting.
IT Support relevance: Builds familiarity with HTTP status codes, web application behavior, command-line diagnostics, and interpreting service responses.
Workspaces and Scan History
- Organize testing activity by workspace and target.
- Keep Nmap and Gobuster scan records associated with the selected workspace.
- Reopen previous results without rerunning scans.
- Delete outdated scan records.
- Store history locally using SQLite.
Technical Stack
Layer	Technology	Purpose
Frontend	React, TypeScript, Vite	Interactive application interface
Styling	Tailwind CSS	Responsive layout and component styling
Backend	Python, FastAPI	API endpoints, validation, and scan orchestration
Database	SQLite	Persistent scan history
Network diagnostics	Nmap	Host, port, and service discovery
Web enumeration	Gobuster	Directory and file path discovery
Development environment	Windows, PowerShell	Local setup, execution, and troubleshooting


Application Architecture
React / TypeScript Frontend
            |
            | HTTP requests
            v
      FastAPI Backend
         /       \
        v         v
  Nmap / Gobuster  SQLite
  command-line     scan history
      tools
The frontend sends scan requests to FastAPI. The backend validates the request, invokes the appropriate installed tool, collects and parses its output, and returns structured results. Completed scans are saved to SQLite for later retrieval.

This architecture helped me practice tracing problems between application layers, rather than treating the user interface, API, and operating-system tools as separate systems.
Screenshots
Add screenshots from the running application to an images/ folder and update the paths below.

Dashboard / Workspace Management
<!-- ![Dashboard](images/dashboard.png) -->


Nmap Scan Results
<!-- ![Nmap Results](images/nmap-results.png) -->


Gobuster Scan Results and History
<!-- ![Gobuster Results](images/gobuster-results.png) -->

Running the Project Locally
Prerequisites
- Windows with PowerShell
- Node.js and npm
- Python 3 and pip
- Nmap installed and accessible to the backend
- Gobuster installed locally
Note: The current backend uses a local Gobuster executable configuration. Update its executable path for your own installation before running scans. The included backend/wordlists/common.txt is a small starter wordlist for demonstrations.

1. Clone the Repository
git clone https://github.com/PaulCola/Cyber-Security.git
cd Cyber-Security/Offensive-Security/PenTest-Toolkit
If you are using a different repository layout, adjust the folder path accordingly.
2. Install Frontend Dependencies
npm install
3. Set Up the Python Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn
Install any other Python dependencies required by the backend source. If a requirements.txt is included, prefer:
pip install -r requirements.txt
4. Start the Backend
From the backend directory with the virtual environment activated:
python -m uvicorn main:app --reload
Backend API documentation: http://127.0.0.1:8000/docs
5. Start the Frontend
In a second terminal, from the project root:
npm run dev
Frontend: http://localhost:5173
6. Try a Lab Scan
1. Create or select a workspace with a local or private lab target.
2. Open Reconnaissance → Nmap or Reconnaissance → Gobuster.
3. Choose the supported scan settings and run the scan.
4. Review the results, open saved history, or export a report.
For a simple Gobuster demonstration, the locally running FastAPI documentation page at http://127.0.0.1:8000/docs can serve as an authorized test endpoint.
Skills Demonstrated
Networking and troubleshooting: TCP/IP concepts, ports and services, HTTP responses, interpreting diagnostic output, and investigating issues across application layers.

Technical support workflows: Windows PowerShell, installation and configuration of tools, environment setup, process management, error investigation, and technical documentation.

Software and systems: React, TypeScript, Python, FastAPI, REST APIs, SQLite, asynchronous frontend requests, and command-line tool integration.

Security fundamentals: Reconnaissance, service discovery, web enumeration, and scope-limited testing in authorized environments.
Current Limitations and Future Improvements
This is an evolving portfolio project, not a replacement for enterprise network monitoring or professional penetration-testing platforms.

Potential future enhancements include:
- Additional reconnaissance tools such as WhatWeb and Nikto.
- More scan configuration and wordlist options.
- Improved input validation and error handling.
- Expanded reporting and result comparison.
- Additional testing, documentation, and deployment improvements.
Responsible Use
Only scan systems you own or have explicit permission to test. The current project is intended for localhost and private lab environments. Do not use it to scan third-party systems without authorization.
Project Focus
This project reflects my interest in both IT infrastructure/support and cybersecurity. It demonstrates my ability to learn technical tools, connect different software components, troubleshoot issues, and present diagnostic information in a practical, usable interface.
