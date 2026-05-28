SentinelLog Testing Guide
Overview

SentinelLog uses automated testing to verify API behavior, rule processing, input validation, and detection logic.

The testing strategy focuses on:

validating core detection behavior
confirming API endpoints work correctly
catching malformed input
supporting CI/CD reliability
reducing deployment risk
Test Framework

SentinelLog uses pytest for unit and integration testing.

Run tests with:

cd src
python -m pytest sentinellog/tests/ -v

Expected result:

16 passed
Test Categories
Unit Tests

Unit tests validate individual components in isolation.

Examples:

rule loading
pattern matching
detection response formatting
input validation
alert formatting
Integration Tests

Integration tests validate how components work together.

Examples:

API request to detection engine
detection engine to YAML rules
rule reload endpoint behavior
health check endpoint response
API Testing

API tests confirm that the FastAPI endpoints return the expected responses.

Key endpoints tested:

GET /health
POST /api/v1/scan
GET /api/v1/rules/list
POST /api/v1/rules/reload

Example scan test:

def test_scan_detects_failed_login(client):
    response = client.post(
        "/api/v1/scan",
        json={"content": "Failed password for invalid user admin"}
    )

    assert response.status_code == 200
    assert response.json()["matched"] is True
Input Validation Testing

Input validation tests confirm that malformed or missing request data does not break the application.

Example cases:

empty log content
missing content field
invalid JSON payload
unsupported request structure

Expected behavior:

return clear error responses
avoid application crashes
preserve API stability
Rule Testing

Rule tests verify that YAML detection rules load correctly and trigger expected matches.

Test cases should confirm:

valid rules load successfully
invalid rules fail safely
rule IDs are returned in detection responses
severity levels are preserved
matching patterns trigger alerts
CI/CD Testing

GitHub Actions should run tests automatically on:

push to main
pull requests
deployment workflow triggers

Recommended CI checks:

pytest test suite
linting
Docker build validation
dependency checks
security scanning
Manual Testing

Manual API testing can be done through Swagger UI.

Start the app:

docker run -p 8000:8000 sentinellog:latest

Open:

http://localhost:8000/docs

Use the scan endpoint with:

{
  "content": "Failed password for invalid user admin"
}

Expected response:

{
  "matched": true,
  "rule_id": "ssh_failed_login",
  "severity": "medium",
  "message": "Failed SSH login pattern detected",
  "source": "auth.log"
}
Future Testing Improvements

Planned testing improvements:

add load testing with Locust or k6
add code coverage reporting
add mutation testing
add end-to-end deployment tests
add authentication and authorization tests
add container vulnerability scanning
add API contract testing
add performance benchmarks
Testing Goals

The goal of SentinelLog testing is to prove that the system can:

Detect suspicious log patterns
handle malformed input safely
expose stable API endpoints
support automated deployment workflows
remain reliable as new detection rules are added
