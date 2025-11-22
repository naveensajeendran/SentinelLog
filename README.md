# SentinelLog

SentinelLog is a lightweight, open-source log-analysis and threat-detection framework. It is designed for security engineers, developers, and analysts who want to quickly detect suspicious patterns in logs using rule-based scanning.

---

## Features

- 🔍 Pattern-based detection engine  
- 📜 Log parsing for Linux authentication logs  
- ⚠️ Alert generation with timestamps  
- 📦 Installable Python package  
- 🧪 Unit tests included  
- 🚀 Lightweight and beginner-friendly  

---

## Project Structure
```
SentinelLog/
├── logs/
│   └── sample.log
├── src/
│   └── sentinellog/
│       ├── __init__.py
│       ├── main.py
│       ├── detector.py
│       ├── parser.py
│       ├── rules.py
│       ├── alerts.py
│       ├── utils.py
│       └── tests/
│           ├── __init__.py
│           └── test_detector.py
├── requirements.txt
├── pyproject.toml
├── setup.cfg
└── readMe.txt
```

---

## Installation

Clone the repository:

```sh
git clone https://github.com/yourusername/SentinelLog.git
cd SentinelLog
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Run the main module to scan logs:

```sh
cd src
python -m sentinellog.main
```

Ensure your log file (e.g., `logs/sample.log`) contains Linux authentication log entries.

---

## Key Concepts

- **ThreatDetector**: Core class that scans log files and applies security rules.
- **SecurityRules**: Contains rule definitions for detecting suspicious patterns (e.g., failed logins, blacklisted IPs).
- **LogParser**: Parses log files into entries for analysis.
- **AlertManager**: Handles alert generation and output.
- **Rule-Based Scanning**: Easily extend detection by adding new rules in `rules.py`.
- **Unit Testing**: Tests in `tests/` ensure reliability and correctness.

---

## Example Log Entry

```
Nov 22 10:00:00 server sshd[12345]: Failed password for invalid user admin from 185.100.87.123 port 22 ssh2
```

---

## Extending SentinelLog

- Add new detection rules in `rules.py`.
- Implement custom log parsers in `parser.py` for different log formats.
- Enhance alerting in `alerts.py` (e.g., email, webhook).

---

## Contributing

Pull requests and issues are welcome! Please follow standard Python style and include unit tests for new features.

---

## License

MIT License
