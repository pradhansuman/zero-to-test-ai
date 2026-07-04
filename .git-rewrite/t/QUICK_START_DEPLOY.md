# Quick Start Deployment - Phases 1-5

**5-Minute Setup for Development/Staging**

```bash
# 1. Prerequisites
# - Docker installed
# - Kubernetes access (kubectl configured)
# - PostgreSQL database available

# 2. Create environment file
cp .env.example .env.staging
# Edit .env.staging with your values:
# - DATABASE_URL=postgresql://user:pass@db:5432/qa_platform
# - JWT_SECRET=$(openssl rand -hex 32)
# - DOCKER_REGISTRY=your-registry.com

# 3. Run automated deployment
chmod +x deploy.sh
./deploy.sh staging

# 4. Validate deployment (in another terminal)
chmod +x validate-deployment.sh
./validate-deployment.sh

# 5. Access platform
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/api/health
```

---

## ✅ What Gets Deployed

✅ All 19 services  
✅ All 29 API endpoints  
✅ Database schemas (auto-migrated)  
✅ Health checks & monitoring  
✅ Authentication & authorization  
✅ Analytics & reporting  
✅ Notifications & webhooks  
✅ Phase 5 security & scale features  

---

## 🚨 Prerequisites

```bash
# Check Docker
docker --version

# Check Kubernetes
kubectl cluster-info

# Check database access
psql $DATABASE_URL -c "SELECT 1"

# Check required tools
which git curl jq
```

---

## 📊 Deployment Scripts

| Script | Purpose |
|--------|---------|
| `deploy.sh` | Automated deployment (test → build → push → deploy) |
| `validate-deployment.sh` | Post-deployment validation tests |

---

## 🔄 Production Deployment

For production, follow **DEPLOYMENT_GUIDE_PRODUCTION.md** (comprehensive 7-step guide)

---

**First Deploy:** `./deploy.sh staging`  
**Validate:** `./validate-deployment.sh`  
**Production:** Follow DEPLOYMENT_GUIDE_PRODUCTION.md
