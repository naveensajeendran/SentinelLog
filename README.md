# SentinelLog

A production-ready, lightweight **log analysis and threat detection framework** designed for security engineers, DevOps teams, and security analysts. SentinelLog uses pattern-based rules to detect suspicious activities in logs with minimal overhead, and scales horizontally on AWS ECS Fargate.

---

##  Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/naveensajeendran/SentinelLog.git
cd SentinelLog
pip install -r requirements.txt

# Run tests
cd src
python -m pytest -v

# Start API
python -m uvicorn sentinellog.api.main:app --reload
# Visit http://localhost:8000/docs
```

### Docker
```bash
docker build -t sentinellog:latest .
docker run -p 8000:8000 sentinellog:latest
```

---

##  Key Features

-  **Pattern-Based Detection**  YAML-defined rules for flexible threat detection
-  **REST API**  FastAPI service with OpenAPI documentation
-  **Cloud-Native**  Containerized, stateless, horizontally scalable
-  **Hot-Reload Rules**  Update detection rules without restarting
-  **Multiple Alert Backends**  Email, Slack, webhooks (extensible)
-  **Comprehensive Tests**  16+ unit/integration tests
-  **Production-Ready**  CI/CD pipelines, Dockerfile, AWS deployment automation
-  **Security-Focused**  Input validation, error handling, audit-ready

---

##  Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**  Complete deployment guide (local, Docker, AWS ECS)
- **[SCALING_SUMMARY.md](SCALING_SUMMARY.md)**  Production readiness checklist and scaling strategy
- **API Docs**  Available at `/docs` (Swagger) and `/openapi.json` when running

---

##  Architecture

### Project Structure
```
SentinelLog/
 src/sentinellog/
    api/                          # FastAPI service
       main.py                   # App definition, health endpoints
       routes/scan_routes.py     # Threat scanning endpoints
       services/detection_service.py  # Business logic
    core/                         # Core detection engine
       detector.py               # ThreatDetector class
       rule_engine.py            # YAML rule parser & evaluator
       parser.py                 # Log file parser
       threats.py                # Threat dataclass
       utils.py                  # Helper functions
    alerts/                       # Alert integrations
       base.py                   # BaseAlert ABC
       email_alert.py            # Email alerts
       slack_alert.py            # Slack integration
       webhook_alert.py          # Generic webhooks
    realtime/                     # Realtime monitoring (optional)
       watcher.py                # File watcher
    tests/                        # Test suite
       test_api.py               # API integration tests (16 tests)
       test_detector.py
       test_rule_engine.py
       test_alerts.py
       ...
    rules/rules.yaml              # Detection rules (YAML)
 .github/workflows/
    ci-cd.yml                     # Test, lint, build, push
    deploy-aws.yml                # AWS ECS deployment
 Dockerfile                        # Multi-stage production build
 docker-compose.yml                # Local orchestration
 requirements.txt                  # Python dependencies
 DEPLOYMENT.md                     # Deployment guide
 SCALING_SUMMARY.md                # Scaling & cost info
 LICENSE                           # MIT License
 README.md                         # This file
```

---

##  API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
# {"status": "healthy", "service": "sentinellog", "version": "1.0.0"}
```

### Scan Logs
```bash
curl -X POST http://localhost:8000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d ''{"content": "Failed password for invalid user admin"}''
```

### List Rules
```bash
curl http://localhost:8000/api/v1/rules/list
```

### Hot-Reload Rules
```bash
curl -X POST http://localhost:8000/api/v1/rules/reload
```

---

##  Rule Definition (YAML)

Create rules in `rules/rules.yaml`:

```yaml
rules:
  - id: failed_login
    pattern: "Failed password|Invalid user"
    severity: high
    description: "Suspicious failed login attempt"
```

---

##  Testing

Run the test suite:
```bash
cd src
python -m pytest sentinellog/tests/ -v
# Expected: 16 passed
```

---

##  Deployment

### Local (Docker)
```bash
docker build -t sentinellog:latest .
docker run -p 8000:8000 sentinellog:latest
```

### AWS ECS Fargate (Automated)
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup.

---

##  Performance & Scaling

- **Image size**: ~400MB
- **Startup time**: 2-3 seconds
- **Memory**: 512MB (Fargate)
- **Throughput**: 100+ req/s per instance
- **Auto-scaling**: 1 to 10+ instances
- **Monthly cost**: ~$20-40 (MVP on AWS)

---

##  Security

-  Input Validation (Pydantic)
-  TLS Support (AWS ALB)
-  Secrets Management (AWS Secrets Manager)
-  IAM Role-Based Access
-  Image Scanning (ECR)
-  Security Checks in CI/CD (Bandit)

---

##  CI/CD Pipeline

Two GitHub Actions workflows:

1. **ci-cd.yml**  Test, lint, build, push on every push
2. **deploy-aws.yml**  Deploy to AWS ECS on main branch push

---

##  License

MIT License - See [LICENSE](LICENSE) file for details.

```
Copyright (c) 2025
SentinelLog Technologies Inc.
A Gemra Ventures–Associated Company
Authors and Co-Founders:
Naveen Sajeendran and Midunan Sivasaravanan

Permission is granted to licensed users to access and use this product under the terms set by SentinelLog Technologies Inc. No rights are granted to copy, modify, distribute, merge, publish, sublicense, sell, or otherwise transfer any portion of this product without explicit written authorization.

All copies or substantial portions of this product must retain this copyright notice.

This product is provided “AS IS,” without warranty of any kind, express or implied, including warranties of merchantability, fitness for a particular purpose, or non-infringement. In no event shall the authors, co-founders, or SentinelLog Technologies Inc. be liable for any damages arising from use of the product.

Use of this product constitutes acceptance of these terms.
All rights not expressly granted are reserved by SentinelLog Technologies Inc.
```

---

##  Contributing

Contributions are welcome! Fork, create a branch, commit, and open a PR.

---

##  Support

- **GitHub Issues**: [Report bugs](https://github.com/naveensajeendran/SentinelLog/issues)
- **API Docs**: http://localhost:8000/docs
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Made by Naveen Sajeendran**  
*Security threat detection, simplified.*
