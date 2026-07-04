# Pre-Flight Checklist - Infrastructure Setup

**Complete this checklist before deployment**

---

## 📋 Infrastructure Selection

Choose your deployment target:

- [ ] **Local Docker Compose** (development/testing)
- [ ] **Kubernetes (Self-managed)** (on-premises, multi-cloud)
- [ ] **AWS ECS** (Elastic Container Service)
- [ ] **AWS EKS** (Kubernetes on AWS)
- [ ] **Google Cloud GKE** (Kubernetes on GCP)
- [ ] **Azure AKS** (Kubernetes on Azure)
- [ ] **Heroku** (PaaS, simplest)
- [ ] **DigitalOcean App Platform**
- [ ] **Other:** _________________

---

## ✅ Required Credentials & Access

Depending on your infrastructure, you need:

### All Deployments
- [ ] PostgreSQL database (connection string)
- [ ] Redis cache (optional, connection string)
- [ ] SMTP credentials (for email notifications)
- [ ] Slack bot token (for Slack notifications)
- [ ] Teams webhook URL (for Teams notifications)

### Docker Registry
- [ ] Docker registry URL (Docker Hub, ECR, GCR, ACR)
- [ ] Registry username/password or API key
- [ ] `docker login` configured

### Kubernetes Deployments (EKS, GKE, AKS, Self-managed)
- [ ] `kubectl` installed and configured
- [ ] `kubectl` connected to correct cluster
- [ ] Namespace created (staging, production)
- [ ] Service account with deployment permissions

### AWS Deployments (ECS, EKS, EC2)
- [ ] AWS CLI installed and configured
- [ ] AWS credentials (Access Key & Secret)
- [ ] ECR repository created
- [ ] RDS database instance created

### Google Cloud Deployments (GKE)
- [ ] `gcloud` CLI installed and authenticated
- [ ] GKE cluster created
- [ ] Cloud SQL database instance
- [ ] Artifact Registry repository

### Azure Deployments (AKS)
- [ ] `az` CLI installed and authenticated
- [ ] AKS cluster created
- [ ] Azure Container Registry created
- [ ] Azure Database for PostgreSQL

### Heroku Deployments
- [ ] Heroku CLI installed
- [ ] `heroku login` authenticated
- [ ] Heroku app created
- [ ] Heroku PostgreSQL add-on provisioned

---

## 🔧 Pre-Deployment Setup

### Step 1: Create Environment File

Create `.env.production`:
```bash
# Database (REQUIRED)
DATABASE_URL=postgresql://user:pass@host:5432/qa_platform
DATABASE_POOL_SIZE=20

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Security
JWT_SECRET=<generate: openssl rand -hex 32>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Notifications
SMTP_HOST=<your-smtp-host>
SMTP_PORT=587
SMTP_USER=<your-smtp-user>
SMTP_PASSWORD=<your-smtp-password>

SLACK_BOT_TOKEN=xoxb-<your-slack-token>
TEAMS_WEBHOOK_URL=https://outlook.webhook.office.com/webhookb2/...

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=<optional-sentry-dsn>

# CORS
CORS_ORIGINS=["https://yourdomain.com","https://api.yourdomain.com"]
```

- [ ] `.env.production` created
- [ ] All required variables filled
- [ ] Secrets stored securely (not in git)

### Step 2: Verify Database Access

```bash
# Test database connection
psql $DATABASE_URL -c "SELECT 1"

# Expected: psql (PostgreSQL) x.x.x on ...
#           1
```

- [ ] Database accessible
- [ ] Correct schema/database name
- [ ] User has create table permissions

### Step 3: Verify Docker Setup

```bash
# Docker installed
docker --version

# Docker can build
docker build -t test:latest .

# Docker registry login
docker login

# Can push to registry
docker tag test:latest <registry>/test:latest
docker push <registry>/test:latest
```

- [ ] Docker CLI working
- [ ] Docker registry authenticated
- [ ] Can build and push images

### Step 4: Verify Kubernetes (if applicable)

```bash
# kubectl installed
kubectl version

# Connected to correct cluster
kubectl cluster-info

# Can access target namespace
kubectl get pods -n production

# Namespace exists
kubectl get ns | grep production
```

- [ ] kubectl configured
- [ ] Connected to correct cluster
- [ ] Production namespace exists
- [ ] Have deployment permissions

### Step 5: Verify Secrets

```bash
# All credentials present
echo "DATABASE_URL=$DATABASE_URL" | wc -c  # Should be >50
echo "JWT_SECRET=$JWT_SECRET" | wc -c      # Should be >50
echo "SMTP_PASSWORD=$SMTP_PASSWORD" | wc -c # Should be >20
```

- [ ] All secrets configured
- [ ] No placeholder values remaining
- [ ] Secrets stored securely

---

## 📊 Infrastructure Questionnaire

**Answer these to get deployment instructions:**

1. **Where are you deploying?**
   - Local/Development: ☐
   - Staging: ☐
   - Production: ☐

2. **Which platform?**
   - Docker Compose: ☐
   - Kubernetes (self-managed): ☐
   - AWS (ECS/EKS/EC2): ☐
   - Google Cloud (GKE/Cloud Run): ☐
   - Azure (AKS/App Service): ☐
   - Heroku: ☐
   - Other: ☐

3. **Database?**
   - Local PostgreSQL: ☐
   - RDS (AWS): ☐
   - Cloud SQL (GCP): ☐
   - Azure Database: ☐
   - Heroku PostgreSQL: ☐
   - Other: ☐

4. **Do you have?**
   - Docker registry access: ☐ YES ☐ NO
   - Kubernetes cluster: ☐ YES ☐ NO
   - Domain/SSL certificates: ☐ YES ☐ NO
   - DNS configured: ☐ YES ☐ NO

---

## 🚀 Next Steps

**After completing this checklist:**

1. Report your infrastructure choice
2. Report completed items above
3. Provide deployment platform details
4. I'll give you platform-specific deployment steps

---

## 📞 Quick Deployment Paths

**Fastest (5 min) - Local Docker:**
```bash
docker-compose up -d
./validate-deployment.sh
```

**Fast (10 min) - Heroku:**
```bash
heroku create qa-platform
heroku addons:create heroku-postgresql:standard-0
git push heroku main
```

**Standard (30 min) - Kubernetes:**
```bash
./deploy.sh production
./validate-deployment.sh
```

---

**Complete this checklist, then report your infrastructure type** ✅
