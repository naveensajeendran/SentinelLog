# SentinelLog Architecture

## Overview

SentinelLog is a lightweight, cloud-native log analysis and threat detection platform designed to detect suspicious activity using rule-based pattern matching.

The system is designed around a stateless REST API architecture to support horizontal scaling, portability, and cloud deployment.

---

# High-Level Architecture

```text
Client / Log Source
        ↓
FastAPI REST API
        ↓
Input Validation (Pydantic)
        ↓
Detection Engine
        ↓
YAML Rule Processing
        ↓
Alert Backend
        ↓
Detection Response / Logs
```

---

# Core Components

## FastAPI Service

The FastAPI layer exposes REST endpoints for:

* log scanning
* rule management
* health monitoring
* rule hot-reloading

FastAPI was selected because of:

* asynchronous request handling
* automatic OpenAPI documentation
* lightweight performance
* strong Python ecosystem integration

---

## Detection Engine

The detection engine processes incoming log content and evaluates it against YAML-defined rules.

Responsibilities:

* parse log input
* load detection rules
* perform pattern matching
* generate structured detection responses

The engine is intentionally modular so additional detection strategies can be integrated later.

---

## Rule Management

Detection rules are stored in YAML format to separate detection logic from application code.

Benefits:

* easier rule updates
* non-code rule customization
* hot-reload support
* simplified maintenance

Example rule categories:

* failed SSH logins
* brute force attempts
* suspicious command execution
* unauthorized access attempts

---

## Alert System

The alert backend is designed to support multiple notification mechanisms.

Current and planned integrations:

* email alerts
* Slack webhooks
* custom HTTP webhooks
* SIEM forwarding

The alert layer is extensible and isolated from the detection engine.

---

## Containerization

SentinelLog uses Docker for portability and deployment consistency.

Benefits:

* reproducible environments
* simplified deployment
* isolated runtime dependencies
* compatibility with AWS ECS and Kubernetes

---

## Cloud Deployment

The application is designed for AWS ECS Fargate deployment.

Cloud-native design goals:

* stateless containers
* horizontal scaling
* automated deployments
* load-balanced traffic routing
* managed infrastructure

---

# Scalability Strategy

SentinelLog is designed to scale horizontally through:

* stateless service design
* container orchestration
* load balancing
* auto-scaling infrastructure

Future scaling improvements:

* Kafka-based ingestion
* distributed processing
* metrics aggregation
* asynchronous event pipelines

---

# Future Architecture Improvements

Planned enhancements:

* Kubernetes deployment support
* Prometheus monitoring
* Grafana dashboards
* RBAC authentication
* Terraform infrastructure provisioning
* distributed event streaming
* machine learning anomaly detection
