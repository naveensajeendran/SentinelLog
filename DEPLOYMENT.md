# SentinelLog Deployment Guide

## Overview

SentinelLog is now containerized and ready for production deployment. This guide covers local testing, Docker deployment, and AWS ECS Fargate scaling.

---

## Local Development & Testing

### 1. Run tests locally

```bash
cd src
python -m pytest sentinellog/tests/ -v
```

Expected: **16 tests passing**

### 2. Run API locally

```bash
# From project root
python -m uvicorn src.sentinellog.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit http://localhost:8000:
- `/health` — Health check (returns 200 with status)
- `/docs` — Interactive Swagger UI
- `/openapi.json` — OpenAPI schema
- `/api/v1/scan` — POST endpoint to scan logs

### 3. Build Docker image locally

```bash
docker build -t sentinellog:latest .
```

### 4. Run container locally

```bash
docker run -p 8000:8000 sentinellog:latest
```

Test endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Scan logs
curl -X POST http://localhost:8000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"content": "ERROR Failed login from 192.168.1.100"}'

# List rules
curl http://localhost:8000/api/v1/rules/list
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

Two workflows automatically trigger on push:

#### 1. **ci-cd.yml** (Main pipeline)
- Runs on every push to `main` or `develop`
- **Test job**: Python 3.11, 3.12, 3.13 with pytest
- **Lint job**: Flake8 and pylint checks
- **Build job**: Docker image build and push to GitHub Container Registry
- **Security job**: Bandit vulnerability scanning
- **Notify job**: Success notification

All jobs must pass before proceeding to deployment.

#### 2. **deploy-aws.yml** (AWS deployment)
- Runs **only** on `main` branch pushes and version tags
- Requires AWS credentials configured as GitHub Secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- Pushes image to ECR and updates ECS task definition
- Waits for service stability before returning

---

## AWS ECS Fargate Deployment

### Prerequisites

1. **AWS Account Setup**
   - ECS Cluster: `sentinellog-cluster`
   - Task Definition: `sentinellog-task`
   - Service: `sentinellog-service`
   - ECR Repository: `sentinellog`

2. **GitHub Secrets** (set in repo settings)
   ```
   AWS_ACCESS_KEY_ID = <your-access-key>
   AWS_SECRET_ACCESS_KEY = <your-secret-key>
   ```

3. **IAM Permissions** (minimum)
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "ecr:GetAuthorizationToken",
           "ecr:BatchGetImage",
           "ecr:GetDownloadUrlForLayer",
           "ecr:PutImage",
           "ecr:InitiateLayerUpload",
           "ecr:UploadLayerPart",
           "ecr:CompleteLayerUpload"
         ],
         "Resource": "arn:aws:ecr:*:*:repository/sentinellog"
       },
       {
         "Effect": "Allow",
         "Action": [
           "ecs:DescribeTaskDefinition",
           "ecs:DescribeServices",
           "ecs:DescribeTaskDefinition",
           "ecs:UpdateService"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

### Deployment Steps

1. **Create ECS Cluster** (one-time setup)
   ```bash
   aws ecs create-cluster --cluster-name sentinellog-cluster --region us-east-1
   ```

2. **Create ECR Repository** (one-time)
   ```bash
   aws ecr create-repository --repository-name sentinellog --region us-east-1
   ```

3. **Create Task Definition** (one-time)
   ```bash
   aws ecs register-task-definition \
     --family sentinellog-task \
     --network-mode awsvpc \
     --requires-compatibilities FARGATE \
     --cpu 256 \
     --memory 512 \
     --container-definitions '[
       {
         "name": "sentinellog",
         "image": "<ECR_REGISTRY>/sentinellog:latest",
         "portMappings": [{"containerPort": 8000, "hostPort": 8000, "protocol": "tcp"}],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/sentinellog",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         },
         "environment": [
           {"name": "SENTINEL_LOG_DIR", "value": "/app/logs"},
           {"name": "SENTINEL_RULES_FILE", "value": "/app/src/sentinellog/rules/rules.yaml"},
           {"name": "API_HOST", "value": "0.0.0.0"},
           {"name": "API_PORT", "value": "8000"}
         ]
       }
     ]'
   ```

4. **Create ECS Service** (one-time)
   ```bash
   aws ecs create-service \
     --cluster sentinellog-cluster \
     --service-name sentinellog-service \
     --task-definition sentinellog-task \
     --desired-count 1 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[<subnet-id>],securityGroups=[<sg-id>],assignPublicIp=ENABLED}"
   ```

5. **Push to GitHub**
   ```bash
   git push origin main
   ```
   This automatically triggers the CI/CD pipeline, builds the Docker image, and deploys to ECS.

### Monitoring Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster sentinellog-cluster \
  --services sentinellog-service

# View task logs
aws logs tail /ecs/sentinellog --follow
```

---

## Scaling & Auto-Scaling

### Manual Scaling

Update desired task count:
```bash
aws ecs update-service \
  --cluster sentinellog-cluster \
  --service sentinellog-service \
  --desired-count 3
```

### Auto-Scaling (ECS)

1. **Register Scalable Target**
   ```bash
   aws application-autoscaling register-scalable-target \
     --service-namespace ecs \
     --resource-id service/sentinellog-cluster/sentinellog-service \
     --scalable-dimension ecs:service:DesiredCount \
     --min-capacity 1 \
     --max-capacity 10
   ```

2. **Create Scaling Policy** (CPU-based)
   ```bash
   aws application-autoscaling put-scaling-policy \
     --policy-name sentinellog-cpu-scaling \
     --service-namespace ecs \
     --resource-id service/sentinellog-cluster/sentinellog-service \
     --scalable-dimension ecs:service:DesiredCount \
     --policy-type TargetTrackingScaling \
     --target-tracking-scaling-policy-configuration "TargetValue=70.0,PredefinedMetricSpecification={PredefinedMetricType=ECSServiceAverageCPUUtilization}"
   ```

---

## Environment Variables

Available configuration via env vars:

| Variable | Default | Purpose |
|----------|---------|---------|
| `SENTINEL_LOG_DIR` | `/app/logs` | Directory to read log files |
| `SENTINEL_RULES_FILE` | `/app/src/sentinellog/rules/rules.yaml` | YAML rules file path |
| `API_HOST` | `0.0.0.0` | API bind address |
| `API_PORT` | `8000` | API port |

---

## Security Best Practices

1. **Use AWS Secrets Manager** for credentials
   ```bash
   aws secretsmanager create-secret --name sentinellog/api-key --secret-string <key>
   ```

2. **Enable TLS** (AWS ELB or ALB)
3. **Implement API authentication** (JWT, OAuth)
4. **Rotate credentials** regularly
5. **Scan images** with ECR image scanning
6. **Use VPC** to isolate containers

---

## Next Steps

1. Set up **Prometheus metrics** endpoint for monitoring
2. Add **distributed tracing** with OpenTelemetry
3. Integrate **Grafana** for dashboards
4. Set up **alerting rules** in CloudWatch or Prometheus
5. Implement **database storage** (RDS PostgreSQL) for results
6. Add **message queue** (SQS/Kinesis) for async processing

---

## Support & Troubleshooting

**Issue: Docker build fails**
- Check `Dockerfile` syntax: `docker build --no-cache .`
- Verify `requirements.txt` dependencies: `pip install -r requirements.txt`

**Issue: API won't start**
- Check logs: `docker logs <container-id>`
- Verify port availability: `netstat -an | grep 8000`

**Issue: ECS deployment fails**
- Check IAM permissions and credentials
- Verify task definition syntax
- Review CloudWatch logs for task errors

---

## Quick Command Reference

```bash
# Local development
python -m uvicorn src.sentinellog.api.main:app --reload

# Docker
docker build -t sentinellog:latest .
docker run -p 8000:8000 sentinellog:latest

# ECS deployment (automated via GitHub Actions on push)
git push origin main

# View logs
docker logs <container-id>
aws logs tail /ecs/sentinellog --follow

# Scaling
aws ecs update-service --cluster sentinellog-cluster --service sentinellog-service --desired-count 3
```

---

**Repo**: https://github.com/naveensajeendran/SentinelLog  
**API Docs**: http://localhost:8000/docs  
**OpenAPI Schema**: http://localhost:8000/openapi.json
