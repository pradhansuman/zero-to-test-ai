# Environment Configuration Guide

This document explains how to configure the QA Automation Backend for different environments.

## Quick Start

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Update Configuration

Edit `.env` with your environment-specific values.

### 3. Verify Configuration

```bash
# Docker Compose
docker-compose config

# Direct Python
python -c "from app.config import settings; print(settings)"
```

---

## Environment Profiles

### Development

**Purpose:** Local development with hot reload

```bash
# .env
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql+asyncpg://qa_user:qa_password@localhost:5432/qa_automation
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Start:**
```bash
docker-compose up -d
cd backend
python init_db.py
python seed_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Staging

**Purpose:** Pre-production testing with production-like setup

```bash
# .env
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://qa_user:secure_password@postgres.staging.internal/qa_automation
REDIS_URL=redis://redis.staging.internal:6379
CORS_ORIGINS=["https://qa-staging.example.com"]
JWT_SECRET=<your-staging-secret>
```

**Start:**
```bash
docker-compose -f docker-compose.yml up -d
kubectl apply -f infrastructure/kubernetes/
```

### Production

**Purpose:** Production deployment with security hardening

```bash
# .env (Use secret management!)
DEBUG=false
LOG_LEVEL=WARN
DATABASE_URL=postgresql+asyncpg://qa_user:${PROD_DB_PASSWORD}@postgres.prod.internal/qa_automation
REDIS_URL=redis://redis.prod.internal:6379
CORS_ORIGINS=["https://qa-api.example.com"]
JWT_SECRET=${PROD_JWT_SECRET}
SENTRY_DSN=${SENTRY_DSN}
SENTRY_ENVIRONMENT=production
```

**Start:**
```bash
# Via Kubernetes
kubectl apply -f infrastructure/kubernetes/
kubectl set image deployment/qa-backend \
  backend=qa-backend:production \
  -n qa-automation
```

---

## Configuration Parameters

### Database

| Parameter | Description | Example |
|-----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://user:pass@host/db` |
| `TEST_DATABASE_URL` | SQLite for testing | `sqlite+aiosqlite:///:memory:` |

**Format:** `dialect+driver://user:password@host:port/database`

### Redis

| Parameter | Description | Example |
|-----------|-------------|---------|
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |

### JWT

| Parameter | Description | Default |
|-----------|-------------|---------|
| `JWT_SECRET` | Secret key for signing tokens | (required) |
| `JWT_ALGORITHM` | Algorithm for token signing | HS256 |
| `JWT_EXPIRATION_HOURS` | Token lifetime in hours | 24 |

⚠️ **Security:** JWT_SECRET must be at least 32 characters in production.

### CORS

| Parameter | Description | Example |
|-----------|-------------|---------|
| `CORS_ORIGINS` | Allowed frontend origins | `["http://localhost:3000"]` |

### Application

| Parameter | Description | Default |
|-----------|-------------|---------|
| `APP_NAME` | Application name | QA Automation Backend |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | false |

### Logging

| Parameter | Description | Default |
|-----------|-------------|---------|
| `LOG_LEVEL` | Log verbosity (DEBUG, INFO, WARN, ERROR) | INFO |
| `LOG_FORMAT` | Log format (json, text) | json |

### Email (Optional)

| Parameter | Description |
|-----------|-------------|
| `SMTP_HOST` | SMTP server hostname |
| `SMTP_PORT` | SMTP server port |
| `SMTP_USER` | SMTP authentication user |
| `SMTP_PASSWORD` | SMTP authentication password |
| `EMAIL_FROM` | Sender email address |

### AWS (Optional)

| Parameter | Description |
|-----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region |
| `S3_BUCKET` | S3 bucket for report storage |

### Celery

| Parameter | Description | Default |
|-----------|-------------|---------|
| `CELERY_BROKER_URL` | Message broker URL | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Result backend URL | `redis://localhost:6379/0` |
| `CELERY_TASK_TIMEOUT` | Task timeout in seconds | 3600 |
| `CELERY_TASK_MAX_RETRIES` | Max retries per task | 3 |

### Sentry (Optional)

| Parameter | Description |
|-----------|-------------|
| `SENTRY_DSN` | Sentry error tracking DSN |
| `SENTRY_ENVIRONMENT` | Environment name (development, staging, production) |

### Feature Flags

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ENABLE_ANALYTICS` | Enable analytics endpoints | true |
| `ENABLE_AI_FEATURES` | Enable AI-powered features | true |
| `ENABLE_WEBHOOKS` | Enable webhook integrations | true |

### Rate Limiting

| Parameter | Description | Default |
|-----------|-------------|---------|
| `RATE_LIMIT_ENABLED` | Enable rate limiting | true |
| `RATE_LIMIT_PER_HOUR` | Requests per hour | 1000 |
| `RATE_LIMIT_PER_SECOND` | Requests per second | 10 |

---

## Secret Management

### Local Development

Store secrets in `.env` file (never commit to git):

```bash
# .env
JWT_SECRET=my-super-secret-key-min-32-characters-long
```

### Docker Compose

Pass secrets via `.env`:

```bash
export JWT_SECRET=$(openssl rand -hex 32)
docker-compose up -d
```

### Kubernetes

Use Kubernetes Secrets:

```bash
# Create secret
kubectl create secret generic jwt-secret \
  --from-literal=JWT_SECRET="$(openssl rand -hex 32)" \
  -n qa-automation

# Reference in manifests
env:
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: jwt-secret
      key: JWT_SECRET
```

### AWS Secrets Manager

```python
# In app/config.py
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Usage
JWT_SECRET = get_secret('qa-backend/jwt-secret')
```

---

## Validation

Check configuration is correct:

```bash
# Docker Compose
docker-compose exec backend python -c "from app.config import settings; print(settings)"

# Kubernetes
kubectl exec -it deployment/qa-backend -n qa-automation -- python -c "from app.config import settings; print(settings)"
```

---

## Troubleshooting

### Database Connection Failed

```bash
# Check database URL
echo $DATABASE_URL

# Test connection (Docker Compose)
docker-compose exec postgres psql -U qa_user -d qa_automation -c "SELECT 1;"

# Kubernetes
kubectl exec postgres-0 -n qa-automation -- psql -U qa_user -d qa_automation -c "SELECT 1;"
```

### Redis Connection Failed

```bash
# Test Redis connection (Docker Compose)
docker-compose exec redis redis-cli ping

# Kubernetes
kubectl exec redis-<pod-hash> -n qa-automation -- redis-cli ping
```

### JWT Secret Errors

```bash
# Generate new secret
openssl rand -hex 32

# Update and restart
export JWT_SECRET="new-secret-value"
docker-compose restart backend
```

---

## Migration Between Environments

### Dev → Staging

1. Update `.env` with staging values
2. Update database URL
3. Verify CORS origins
4. Update JWT secret
5. Test health check: `curl https://qa-staging.example.com/health`

### Staging → Production

1. Rotate all secrets
2. Update database URL to production
3. Update CORS origins
4. Enable monitoring/Sentry
5. Set DEBUG=false
6. Run database migrations

```bash
kubectl set env deployment/qa-backend \
  DEBUG=false \
  LOG_LEVEL=WARN \
  -n qa-automation
```

---

## Environment Validation Checklist

- [ ] DATABASE_URL is set and correct
- [ ] REDIS_URL is set and correct
- [ ] JWT_SECRET is at least 32 characters
- [ ] CORS_ORIGINS includes frontend domain
- [ ] Email/SMTP configured (if email features enabled)
- [ ] AWS credentials set (if using S3)
- [ ] Sentry DSN configured (if using error tracking)
- [ ] LOG_LEVEL appropriate for environment
- [ ] DEBUG=false in production
- [ ] Health check passes: `curl /health`
