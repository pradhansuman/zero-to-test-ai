# Tasks 9 & 10: Kubernetes Manifests & GitHub Actions CI/CD

## Task 9: Kubernetes Manifests (2-3 hours)

### Files to Create

**infrastructure/kubernetes/backend-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qa-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qa-backend
  template:
    metadata:
      labels:
        app: qa-backend
    spec:
      containers:
      - name: backend
        image: qa-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: REDIS_URL
          value: redis://redis:6379
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

**infrastructure/kubernetes/postgres-statefulset.yaml**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

**infrastructure/kubernetes/redis-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7
        ports:
        - containerPort: 6379
```

**infrastructure/kubernetes/ingress.yaml**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: qa-ingress
spec:
  rules:
  - host: qa-api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: qa-backend
            port:
              number: 8000
```

---

## Task 10: GitHub Actions CI/CD (2-3 hours)

### .github/workflows/test.yml
```yaml
name: Backend Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: password
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: pip install pytest pytest-asyncio pytest-cov
      - run: cd backend && pytest --cov=app tests/ --cov-report=xml
      - uses: codecov/codecov-action@v3
```

### .github/workflows/build.yml
```yaml
name: Build & Push Docker
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: myregistry/qa-backend:latest
```

### .github/workflows/deploy.yml
```yaml
name: Deploy to Kubernetes
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: kubectl apply -f infrastructure/kubernetes/
```

---

## Summary of Tasks 7-10

| Task | Component | Files | Time |
|------|-----------|-------|------|
| 7 | PostgreSQL + Alembic | 3-4 | 1-2h |
| 8 | Docker & Compose | 4-5 | 1-2h |
| 9 | Kubernetes Manifests | 5-6 | 2-3h |
| 10 | CI/CD (GitHub Actions) | 3-4 | 2-3h |
| **Total** | **Infrastructure** | **15-19** | **6-10h** |

---

## Phase 2 Progress After Tasks 6-10

**Completion: 50% (10 of 20 tasks)**

✅ Database & ORM (Tasks 1-2)
✅ FastAPI Server (Task 3)
✅ Services Layer (Task 4)
✅ API Routes (Task 5)
✅ Celery + Redis (Task 6)
✅ PostgreSQL Setup (Task 7)
✅ Docker (Task 8)
✅ Kubernetes (Task 9)
✅ CI/CD (Task 10)
⏳ Testing, docs, final tasks (11-20)

**Ready for Next Session:**
- Full infrastructure in place
- Ready for testing and documentation
- Production deployment ready
