# Contributing to SentinelLog

First off, thank you for considering contributing to SentinelLog! It's people like you that make SentinelLog such a great tool.

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem** in as much detail as possible
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps** and point out what the problem is
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details**: OS, Python version, dependencies

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Follow the [Python Style Guide](#python-style-guide)
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline
* Avoid platform-dependent code

---

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/SentinelLog.git
cd SentinelLog
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

---

## Python Style Guide

### General

* Use [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style
* Use 4 spaces for indentation (not tabs)
* Keep lines under 120 characters
* Use type hints for function arguments and return values

### Naming

* Classes: `PascalCase`
* Functions and variables: `snake_case`
* Constants: `UPPER_SNAKE_CASE`
* Private methods/attributes: prefix with `_`

### Docstrings

Use docstrings for all public modules, functions, classes, and methods:

```python
def scan_log_file(filepath: str) -> list[Threat]:
    """Scan a log file for threats.
    
    Args:
        filepath: Path to the log file to scan.
        
    Returns:
        List of detected threats ordered by severity.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not readable.
    """
```

### Type Hints

```python
from typing import Optional, List

def process_entries(entries: List[dict]) -> Optional[dict]:
    """Process log entries."""
    pass
```

---

## Testing

### Running Tests

```bash
cd src
python -m pytest sentinellog/tests/ -v
```

### Writing Tests

* Test files should be named `test_*.py` or `*_test.py`
* Use descriptive test names
* Aim for high coverage (currently 95%+)
* Use fixtures for common setup

Example:
```python
def test_detector_identifies_failed_login():
    """Test that detector identifies failed login attempts."""
    detector = ThreatDetector("rules/rules.yaml")
    entry = {"raw": "Failed password for user admin", "fields": [...]}
    
    threats = detector.engine.evaluate(entry)
    
    assert len(threats) > 0
    assert threats[0].level == "high"
```

---

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add threat severity filtering to API

- Adds severity query parameter to /api/v1/scan endpoint
- Implements severity level validation
- Updates tests and documentation
- Fixes #123
```

---

## Pull Request Process

1. **Update documentation** — Keep README.md and docs up-to-date
2. **Add tests** — Include tests for new functionality
3. **Run linting** — Ensure code passes flake8 and pylint
4. **Run tests** — All tests must pass (16/16)
5. **Update CHANGELOG** — Document your changes
6. **Create PR** — Reference related issues with `#issue-number`

The repository maintainers will review your PR as soon as possible.

---

## Linting

Before committing, run linting tools:

```bash
# Flake8
flake8 src/sentinellog --max-line-length=120

# Pylint
pylint src/sentinellog --exit-zero
```

To auto-format code:
```bash
black src/sentinellog
```

---

## Documentation

* Update [README.md](README.md) for user-facing changes
* Update [DEPLOYMENT.md](DEPLOYMENT.md) for deployment changes
* Add docstrings to all public functions and classes
* Include examples in docstrings where helpful

---

## Issues and Discussions

* Use [GitHub Issues](https://github.com/naveensajeendran/SentinelLog/issues) for bug reports and feature requests
* Use [GitHub Discussions](https://github.com/naveensajeendran/SentinelLog/discussions) for questions and general discussion

---

## License

By contributing to SentinelLog, you agree that your contributions will be licensed under the MIT License.

---

## Additional Notes

### Issue and Pull Request Labels

* `bug` — Something isn't working
* `enhancement` — New feature or request
* `documentation` — Improvements or additions to documentation
* `good first issue` — Good for newcomers
* `help wanted` — Extra attention is needed
* `question` — Further information is requested
* `security` — Security-related issue

---

## Recognition

Contributors will be recognized in:
* [README.md](README.md) acknowledgments section
* Release notes for significant contributions

---

Thank you for contributing! 🎉
