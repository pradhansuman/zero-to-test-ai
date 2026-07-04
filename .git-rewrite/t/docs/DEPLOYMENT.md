# Deployment Guide

Complete guide for deploying the QA Automation Backend to production.

---

## Pre-Deployment Checklist

- [ ] All tests passing (80%+ coverage)
- [ ] Security scan complete (OWASP)
- [ ] Database migrations tested
- [ ] Secrets rotated
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Runbooks documented
- [ ] Team trained

---

## Local Development Deployment

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 15
- Redis 7

### Setup

```bash
# 1. Clone repository
git clone https://github.com/yourorg/qa-automation.git
cd qa-automation

# 2. Copy environment template
cp .env.example .env

# 3. Update .env for development
# (Keep defaults for local development)

# 4. Start services
docker-compose up -d

# 5. Initialize database
docker-compose exec backend python init_db.py
docker-compose exec backend python seed_db.py

# 6. Verify health
curl http://localhost:8000/health

# 7. Access API
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs
# Redis: localhost:6379
# PostgreSQL: localhost:5432
```

---

## Kubernetes Deployment

### Prerequisites

- kubectl configured
- Kubernetes cluster (1.20+)
- Container registry access
- Persistent volume provider

### Step 1: Build & Push Docker Images

```bash
# Build images
docker build -t myregistry/qa-backend:v1.0.0 ./backend
docker build -t myregistry/qa-celery-worker:v1.0.0 -f backend/Dockerfile.worker ./backend

# Push to registry
docker push myregistry/qa-backend:v1.0.0
docker push myregistry/qa-celery-worker:v1.0.0
```

### Step 2: Create Namespace & Secrets

```bash
# Create namespace
kubectl create namespace qa-automation

# Create secrets
kubectl create secret generic db-credentials \
  --from-literal=url="postgresql+asyncpg://user:password@postgres:5432/qa_automation" \
  -n qa-automation

kubectl create secret generic jwt-secret \
  --from-literal=JWT_SECRET="$(openssl rand -hex 32)" \
  -n qa-automation
```

### Step 3: Deploy Services

```bash
# Apply manifests
kubectl apply -f infrastructure/kubernetes/postgres-statefulset.yaml
kubectl apply -f infrastructure/kubernetes/redis-deployment.yaml
kubectl apply -f infrastructure/kubernetes/backend-deployment.yaml
kubectl apply -f infrastructure/kubernetes/celery-deployment.yaml
kubectl apply -f infrastructure/kubernetes/ingress.yaml

# Wait for rollout
kubectl rollout status deployment/qa-backend -n qa-automation --timeout=5m
```

### Step 4: Verify Deployment

```bash
# Check pods
kubectl get pods -n qa-automation

# Check services
kubectl get svc -n qa-automation

# Check logs
kubectl logs -f deployment/qa-backend -n qa-automation

# Test health
kubectl exec -it deployment/qa-backend -n qa-automation -- \
  curl http://localhost:8000/health
```

### Step 5: Initialize Database

```bash
# Port forward to PostgreSQL
kubectl port-forward svc/postgres 5432:5432 -n qa-automation &

# Run migrations
DATABASE_URL=postgresql://user:pass@localhost/qa_automation \
  alembic upgrade head

# Seed data (optional)
kubectl exec -it deployment/qa-backend -n qa-automation -- \
  python seed_db.py
```

---

## Scaling

### Horizontal Scaling

```bash
# Scale backend replicas
kubectl scale deployment qa-backend --replicas=5 -n qa-automation

# Monitor scaling
kubectl get pods -n qa-automation -w

# Scale down
kubectl scale deployment qa-backend --replicas=3 -n qa-automation
```

### Resource Requests/Limits

Update in `backend-deployment.yaml`:

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi
```

---

## Rolling Updates

### Update Image

```bash
# Set new image
kubectl set image deployment/qa-backend \
  backend=myregistry/qa-backend:v1.1.0 \
  -n qa-automation

# Watch rollout
kubectl rollout status deployment/qa-backend -n qa-automation

# Rollback if needed
kubectl rollout undo deployment/qa-backend -n qa-automation
```

### Zero-Downtime Updates

```yaml
# In deployment spec
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

---

## Backup & Recovery

### Database Backup

```bash
# Manual backup
kubectl exec postgres-0 -n qa-automation -- \
  pg_dump -U qa_user qa_automation > backup.sql

# Automated backups (via CronJob)
kubectl apply -f infrastructure/kubernetes/backup-cronjob.yaml
```

### Restore Database

```bash
# Restore from backup
kubectl exec -i postgres-0 -n qa-automation -- \
  psql -U qa_user qa_automation < backup.sql
```

---

## Monitoring & Logging

### Port Forward Prometheus

```bash
kubectl port-forward svc/prometheus 9090:9090 -n qa-automation
```

### Port Forward Grafana

```bash
kubectl port-forward svc/grafana 3000:3000 -n qa-automation
# Access: http://localhost:3000
```

### View Logs

```bash
# Stream logs
kubectl logs -f deployment/qa-backend -n qa-automation

# Previous logs
kubectl logs deployment/qa-backend -n qa-automation --previous

# All container logs
kubectl logs deployment/qa-backend -n qa-automation --all-containers=true
```

---

## Troubleshooting

### Pod Won't Start

```bash
# Check events
kubectl describe pod <pod-name> -n qa-automation

# Check logs
kubectl logs <pod-name> -n qa-automation

# Check resource availability
kubectl top node
kubectl top pod -n qa-automation
```

### Service Not Reachable

```bash
# Check service endpoints
kubectl get endpoints -n qa-automation

# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -O- http://qa-backend:8000/health

# Check DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup qa-backend.qa-automation.svc.cluster.local
```

### Database Connection Issues

```bash
# Test database connection
kubectl exec -it deployment/qa-backend -n qa-automation -- \
  psql $DATABASE_URL -c "SELECT 1;"

# Check credentials
kubectl get secret db-credentials -n qa-automation -o yaml

# Verify environment variables
kubectl exec deployment/qa-backend -n qa-automation -- \
  env | grep DATABASE
```

---

## Post-Deployment Verification

1. **Health Checks**
   ```bash
   curl https://qa-api.example.com/health
   ```

2. **API Endpoints**
   ```bash
   # List projects
   curl -H "Authorization: Bearer $TOKEN" \
     https://qa-api.example.com/api/projects
   ```

3. **Database Connectivity**
   ```bash
   kubectl exec -it deployment/qa-backend -n qa-automation -- \
     python -c "from app.database.session import SessionLocal; print('DB OK')"
   ```

4. **Monitoring**
   - Check Prometheus scraping metrics
   - Verify Grafana dashboard
   - Review Sentry error tracking

5. **Logging**
   - View logs in ELK/CloudWatch
   - Check log volume and format
   - Verify error logging

---

## Rollback Procedure

If issues occur after deployment:

```bash
# Check rollout history
kubectl rollout history deployment/qa-backend -n qa-automation

# Rollback to previous version
kubectl rollout undo deployment/qa-backend -n qa-automation

# Rollback to specific revision
kubectl rollout undo deployment/qa-backend --to-revision=2 -n qa-automation

# Monitor rollback
kubectl rollout status deployment/qa-backend -n qa-automation -w
```

---

## Performance Tuning

### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_project_owner ON projects(owner_id);
CREATE INDEX idx_test_case_project ON test_cases(project_id);
CREATE INDEX idx_execution_status ON executions(status);

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM projects WHERE owner_id = 1;
```

### Connection Pooling

```python
# backend/app/database/session.py
engine = create_async_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
)
```

### Redis Caching

```python
# Cache project details
await redis.setex(f"project:{project_id}", 3600, project_json)
```

---

## Security Hardening

### TLS/SSL

Update Ingress for HTTPS:

```yaml
tls:
  - hosts:
    - qa-api.example.com
    secretName: tls-secret
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: qa-network-policy
spec:
  podSelector:
    matchLabels:
      app: qa-backend
  policyTypes:
    - Ingress
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            name: ingress-nginx
```

### RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: qa-backend
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list"]
```

---

## Maintenance

### Regular Tasks

- **Daily:** Check logs for errors, verify health checks
- **Weekly:** Review performance metrics, check disk space
- **Monthly:** Database maintenance, security updates, backups test
- **Quarterly:** Performance optimization, capacity planning

### Scheduled Maintenance Window

```bash
# Scale down during maintenance
kubectl scale deployment qa-backend --replicas=0 -n qa-automation

# Perform maintenance
# ...

# Scale back up
kubectl scale deployment qa-backend --replicas=3 -n qa-automation
```
