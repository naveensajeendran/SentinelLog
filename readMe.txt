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

Notes:
- `requirements.txt` includes runtime and test dependencies (e.g., `requests`, `pytest`, `rich`).

If you plan to run the API or install the package into a virtual environment, create and activate a virtualenv first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
python -m sentinellog.main
```

Ensure your log file (e.g., `logs/sample.log`) contains Linux authentication log entries.

Quick checks:
- To run a lightweight import sanity check (validates module imports):

```powershell
cd C:\Users\navee\Desktop\SentinelLog
python .\tools\import_check.py
```

---

## Developer Notes (Refactor & Key Concepts)

- **Core package**: The primary parsing, rule engine, detector, and threat representations now live under `src/sentinellog/core/`.
	- `core/parser.py` returns structured entries (dicts with a `raw` key and optional metadata).
	- `core/rule_engine.py` loads YAML rule definitions and evaluates log entries, returning `Threat` objects.
	- `core/detector.py` coordinates parsing and rule evaluation and accepts an optional `rules_path` (falls back to `rules/rules.yaml`). It provides a `run(entries)` helper for tests and programmatic use.

- **Rules**: Rules are stored as YAML files (example path: `rules/rules.yaml`). Each rule should include at least `id` and `pattern` fields.

- **Alerts**: Alert backends (email, Slack, webhook) live under `src/sentinellog/alerts/`. HTTP-based alerters use `requests` (lazy-imported) and will raise a clear error if `requests` is not installed.

- **Real-time watcher**: `src/sentinellog/realtime/watcher.py` provides a `FileWatcher` class (exported as `LogWatcher` for backward compatibility) that tails logs and invokes the detector.

---

## Example rules YAML

Create `rules/rules.yaml` with contents like:

```yaml
- id: FAILED_LOGIN
	pattern: "Failed password"
	level: HIGH
	metadata:
		source: auth_log

- id: SUSPICIOUS_IP
	pattern: "185."
	level: MEDIUM
```

---

## Tests

This repository includes unit tests under `src/sentinellog/tests/`. To run tests (after installing `pytest`):

```powershell
cd src
python -m pytest -q
```

If `pytest` is not installed, add it to your environment with `pip install -r requirements.txt`.

---

## Troubleshooting

- Import errors when running scripts: ensure you run modules from the `src` directory or have `src` on `PYTHONPATH`.
	- Example: `cd src` then `python -m sentinellog.main`.
- Missing `requests` errors for HTTP alerts: install `requests` (`pip install requests`) or ensure `requirements.txt` is installed.

---

## Contributing

Pull requests and issues are welcome! Please follow standard Python style, include unit tests for new features, and run `pytest` before submitting.

---

## License

MIT License

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