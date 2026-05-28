# SentinelLog Deployment Guide

# Local Development Setup

## Prerequisites

Required tools:

* Python 3.11+
* Docker
* Git

---

# Clone Repository

```bash
git clone https://github.com/naveensajeendran/SentinelLog.git
cd SentinelLog
```

---

# Run Locally

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Application

```bash
uvicorn sentinellog.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Docker Deployment

## Build Docker Image

```bash
docker build -t sentinellog:latest .
```

## Run Container

```bash
docker run -p 8000:8000 sentinellog:latest
```

---

# AWS ECS Fargate Deployment

## Deployment Overview

SentinelLog is designed for containerized deployment on AWS ECS Fargate.

Infrastructure components:

* ECS Cluster
* ECS Service
* Application Load Balancer
* ECR Repository
* IAM Roles
* CloudWatch Logs

---

# Deployment Workflow

## Step 1: Build Docker Image

```bash
docker build -t sentinellog .
```

## Step 2: Push to AWS ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ecr-url>
docker tag sentinellog:latest <ecr-url>/sentinellog:latest
docker push <ecr-url>/sentinellog:latest
```

## Step 3: Deploy ECS Service

Deployment is automated using GitHub Actions workflows.

---

# CI/CD Pipeline

GitHub Actions pipelines handle:

* automated testing
* linting
* Docker image builds
* ECR publishing
* ECS deployment

Deployment triggers:

* push to main branch
* pull request validation

---

# Environment Variables

Example configuration:

```env
APP_ENV=production
LOG_LEVEL=INFO
AWS_REGION=us-east-1
```

---

# Monitoring

Recommended monitoring tools:

* AWS CloudWatch
* ECS Service Metrics
* Container Logs
* API Health Checks

---

# Future Deployment Improvements

Planned enhancements:

* Kubernetes deployment manifests
* Terraform infrastructure provisioning
* Prometheus metrics integration
* Grafana dashboards
* blue-green deployments
* automated rollback support
