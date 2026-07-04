# Quick Start - Multi-Environment Test Execution

## 📋 One-Liner Commands

```bash
# LOCAL (fastest, no setup)
./scripts/test-runner.sh --env local

# DOCKER (consistent, no local deps)
./scripts/test-runner.sh --env docker

# AWS (scalable, pay-as-you-go)
./scripts/test-runner.sh --env aws --aws-region us-east-1

# GOOGLE CLOUD (enterprise scale)
./scripts/test-runner.sh --env gcp --gcp-zone us-central1-a

# AZURE (Microsoft ecosystem)
./scripts/test-runner.sh --env azure
```

---

## 🚀 Environment Selection Guide

### Choose **LOCAL** if:
- ✅ You're developing locally
- ✅ You want fastest execution
- ✅ You have Node.js 20+ installed
- ✅ You want zero cloud costs

### Choose **DOCKER** if:
- ✅ You want consistent environment
- ✅ You're in CI/CD pipeline
- ✅ You want to avoid setup
- ✅ You need cross-platform testing

### Choose **AWS** if:
- ✅ You need enterprise scale
- ✅ You have AWS credits
- ✅ You want auto-terminating instances
- ✅ You need regional testing

### Choose **GOOGLE CLOUD** if:
- ✅ You use Google Cloud ecosystem
- ✅ You need Kubernetes integration
- ✅ You want generous free tier
- ✅ You value Google infrastructure

### Choose **AZURE** if:
- ✅ You use Microsoft products
- ✅ You need Hybrid Cloud
- ✅ You have Azure subscriptions
- ✅ You test Windows applications

---

## 🎯 Common Tasks

### Run Smoke Tests Only
```bash
./scripts/test-runner.sh --env local --smoke
./scripts/test-runner.sh --env docker --smoke
./scripts/test-runner.sh --env aws --smoke
```

### Run with Specific Browser
```bash
./scripts/test-runner.sh --env local --browser firefox
./scripts/test-runner.sh --env docker --browser webkit
```

### Run with More Workers (Parallel Execution)
```bash
./scripts/test-runner.sh --env local --workers 8
./scripts/test-runner.sh --env docker --workers 16
```

### Run Specific Test Suite
```bash
npm test tests/e2e/shopnow.spec.ts
npm test tests/e2e/store-*.spec.ts
```

---

## 📊 Results & Reports

After tests complete, view results at:

```bash
# HTML Report (interactive)
open playwright-report/index.html

# JSON Results (structured data)
cat test-results-store/results.json

# Screenshots & Videos
ls -la test-results-store/*/
```

---

## ⚙️ Setup by Environment

### LOCAL Setup (5 minutes)
```bash
# 1. Install Node.js (if needed)
brew install node@20

# 2. Install dependencies
npm install

# 3. Install Playwright browsers
npx playwright install

# 4. Make script executable
chmod +x scripts/test-runner.sh

# 5. Run tests
./scripts/test-runner.sh --env local
```

### DOCKER Setup (2 minutes)
```bash
# 1. Make script executable
chmod +x scripts/test-runner.sh

# 2. Build image (automatic or manual)
docker build -f Dockerfile.test -t qa_agents-test:latest .

# 3. Run tests
./scripts/test-runner.sh --env docker
```

### AWS Setup (20 minutes)
```bash
# 1. Install AWS CLI
brew install awscli

# 2. Configure credentials
aws configure

# 3. Create key pair
aws ec2 create-key-pair --key-name qa-tests-key \
  --query 'KeyMaterial' --output text > ~/.ssh/qa-tests-key.pem
chmod 600 ~/.ssh/qa-tests-key.pem

# 4. Create security group
aws ec2 create-security-group --group-name qa-tests-sg \
  --description "QA Test Security Group"

# 5. Allow SSH
aws ec2 authorize-security-group-ingress --group-name qa-tests-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

# 6. Make script executable
chmod +x scripts/test-runner.sh scripts/aws-user-data.sh

# 7. Update AWS_REGION and security group ID in test-runner.sh

# 8. Run tests
./scripts/test-runner.sh --env aws
```

### GCP Setup (15 minutes)
```bash
# 1. Install gcloud CLI
brew install --cask google-cloud-sdk

# 2. Authenticate
gcloud init
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Make scripts executable
chmod +x scripts/test-runner.sh scripts/gcp-startup-script.sh

# 5. Run tests
./scripts/test-runner.sh --env gcp
```

### AZURE Setup (15 minutes)
```bash
# 1. Install Azure CLI
brew install azure-cli

# 2. Authenticate
az login

# 3. Set subscription
az account set --subscription YOUR_SUBSCRIPTION_ID

# 4. Create resource group
az group create --name qa-tests-rg --location eastus

# 5. Make scripts executable
chmod +x scripts/test-runner.sh scripts/azure-user-data.sh

# 6. Run tests
./scripts/test-runner.sh --env azure
```

---

## 💰 Cost Comparison (Per Test Run)

| Environment | Cost | Duration | Total Cost |
|-------------|------|----------|-----------|
| Local | $0 | 10 min | **$0** |
| Docker | $0 | 12 min | **$0** |
| AWS (t3.medium) | $0.0416/hr | 15 min | **$0.10** |
| GCP (e2-medium) | $0.033/hr | 15 min | **$0.08** |
| Azure (B2s) | $0.05/hr | 15 min | **$0.13** |

*Costs exclude data transfer and storage*

---

## 🐛 Troubleshooting

### "npm not found"
```bash
# Install Node.js
brew install node@20
node --version
```

### "Docker not found"
```bash
# Install Docker Desktop
brew install --cask docker
docker --version
```

### "AWS CLI not configured"
```bash
# Configure credentials
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region, Output format
```

### "Playwright browsers not installed"
```bash
# Install browsers
npx playwright install --with-deps
```

### Tests failing on CI/CD
```bash
# Use Docker environment (most consistent)
./scripts/test-runner.sh --env docker
```

---

## 📚 Full Documentation

For detailed setup and troubleshooting:
- See: `MULTI_ENV_DEPLOYMENT.md`
- See: `GUARDRAILS.md`
- See: `README.md`

---

## ✅ Verification

After setup, verify environment works:

```bash
# Local
node --version
npm --version
npx playwright --version

# Docker
docker --version
docker run hello-world

# AWS
aws sts get-caller-identity

# GCP
gcloud auth list
gcloud config list

# Azure
az account show
```

---

## 🎓 Next Steps

1. **Run locally first** - fastest feedback during development
2. **Use Docker for CI/CD** - consistent environments
3. **Use Cloud for load testing** - scale across regions
4. **Monitor costs** - set budget alerts
5. **Archive results** - track test history

**Happy Testing! 🚀**
