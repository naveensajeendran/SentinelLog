# Changelog

All notable changes to SentinelLog are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-27

### Added

#### Core Features
- ✅ FastAPI REST service with 6 endpoints (`/health`, `/scan`, `/rules/*`)
- ✅ YAML-based rule engine with pattern matching
- ✅ Log parser for structured entry generation
- ✅ Threat detector with rule evaluation
- ✅ Alert integrations (email, Slack, webhooks)

#### API & Service
- ✅ `/health` endpoint for load balancer health checks
- ✅ `/api/v1/scan` POST endpoint for threat scanning
- ✅ `/api/v1/rules/list` GET endpoint to list active rules
- ✅ `/api/v1/rules/reload` POST endpoint for hot-reload
- ✅ OpenAPI/Swagger documentation auto-generation (`/docs`)
- ✅ Input validation with Pydantic models
- ✅ Error handling with descriptive messages

#### Deployment & Infrastructure
- ✅ Production-grade Dockerfile (multi-stage, python:3.11-slim)
- ✅ `.dockerignore` for image optimization
- ✅ `docker-compose.yml` for local development
- ✅ GitHub Actions CI/CD pipeline (`ci-cd.yml`)
  - Tests on Python 3.11, 3.12, 3.13
  - Flake8 + pylint code quality checks
  - Docker build and push to GitHub Container Registry
  - Bandit security scanning
- ✅ AWS ECS Fargate deployment workflow (`deploy-aws.yml`)
  - Automated ECR push
  - ECS task definition updates
  - Service stability validation

#### Testing & Quality
- ✅ Comprehensive test suite (16 tests)
  - API endpoint integration tests (10 tests)
  - Detector and rule engine tests
  - Alert tests with mocking
  - Parser tests
- ✅ 100% test passing rate
- ✅ Code quality checks (flake8, pylint)
- ✅ Security scanning (Bandit)

#### Documentation
- ✅ [README.md](README.md) — Comprehensive project overview
- ✅ [DEPLOYMENT.md](DEPLOYMENT.md) — Detailed deployment guide (200+ lines)
- ✅ [SCALING_SUMMARY.md](SCALING_SUMMARY.md) — Production readiness summary
- ✅ [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution guidelines
- ✅ [LICENSE](LICENSE) — MIT License
- ✅ Inline code documentation with docstrings
- ✅ API documentation via Swagger UI

#### Architecture
- ✅ Modular core package (`sentinellog/core/`)
- ✅ Service layer pattern (`api/services/`)
- ✅ Separation of concerns (routes, services, core logic)
- ✅ Abstract base class for alerts (`alerts/base.py`)
- ✅ Lazy imports for optional dependencies

#### Configuration
- ✅ Environment variable support
  - `SENTINEL_LOG_DIR` — Log directory
  - `SENTINEL_RULES_FILE` — Rules file path
  - `API_HOST` — API bind address
  - `API_PORT` — API port
- ✅ Hot-reloadable rule configurations

### Security Features
- ✅ Input validation (Pydantic)
- ✅ Error handling (no internal details leaked)
- ✅ TLS-ready architecture
- ✅ AWS Secrets Manager integration path
- ✅ IAM role-based access for ECS
- ✅ ECR image scanning enabled
- ✅ Security checks in CI/CD

### Performance
- ✅ Containerized (~400MB image)
- ✅ Fast startup (2-3 seconds)
- ✅ Horizontal scalability
- ✅ ~100+ req/s throughput per instance
- ✅ Auto-scaling support (1-10+ instances)
- ✅ Low AWS costs (~$20-40/mo MVP)

### Developer Experience
- ✅ Easy local development setup
- ✅ Import validation tool (`tools/import_check.py`)
- ✅ Type hints throughout codebase
- ✅ Clear error messages
- ✅ OpenAPI schema auto-generation

---

## [0.1.0] - 2025-11-01

### Initial Release
- Basic log parsing functionality
- Rule-based threat detection
- Alert integrations
- Unit tests
- Project structure and setup

---

## Unreleased (Roadmap)

### Phase 2: Scale & Monitor
- [ ] Prometheus metrics endpoint
- [ ] CloudWatch alarms and Grafana dashboards
- [ ] OpenTelemetry distributed tracing
- [ ] Sentry error tracking integration

### Phase 3: Advanced Features
- [ ] Async job processing (SQS + Lambda)
- [ ] Database persistence (RDS PostgreSQL)
- [ ] Event streaming (Kinesis/Kafka)
- [ ] Admin UI for rule management
- [ ] Multi-tenant support

### Phase 4: Operations
- [ ] On-call rotation setup
- [ ] Incident playbooks and runbooks
- [ ] Blue-green deployments
- [ ] SLOs/SLIs tracking
- [ ] Advanced monitoring and alerting

### Future Enhancements
- [ ] Machine learning-based anomaly detection
- [ ] Custom rule templates
- [ ] Integration with SIEM platforms
- [ ] Kubernetes Helm charts
- [ ] Multi-cloud support (GCP, Azure)

---

## Versioning

SentinelLog follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (0.x to 1.x)
- **MINOR**: New features, backward compatible (1.0 to 1.1)
- **PATCH**: Bug fixes, backward compatible (1.0.0 to 1.0.1)

---

## How to Update

### Upgrade from 0.1.0 to 1.0.0

1. **Update dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Review changes**
   - New FastAPI service (optional for existing users)
   - Containerization support
   - Enhanced testing

3. **Update configuration** (if applicable)
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for environment variables

4. **Run tests**
   ```bash
   cd src
   python -m pytest sentinellog/tests/ -v
   ```

---

## Support & Links

- **Documentation**: [README.md](README.md), [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/naveensajeendran/SentinelLog/issues)
- **Discussions**: [GitHub Discussions](https://github.com/naveensajeendran/SentinelLog/discussions)
- **License**: [MIT License](LICENSE)

---

**Last Updated**: 2025-11-27  
**Maintainer**: Naveen Sajeendran [@naveensajeendran](https://github.com/naveensajeendran)
