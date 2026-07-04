# Multi-Environment Test Execution Guide

Production users can run the QA test suite across 5 different environments:
1. **Local** - Host machine (macOS, Linux, Windows)
2. **Docker** - Containerized execution
3. **AWS** - Amazon EC2 instances
4. **Google Cloud** - Google Cloud VMs
5. **Azure** - Microsoft Azure VMs

---

## Quick Start

```bash
# Run locally (default)
./scripts/test-runner.sh --env local

# Run in Docker
./scripts/test-runner.sh --env docker

# Run on AWS
./scripts/test-runner.sh --env aws --aws-region us-west-2

# Run on Google Cloud
./scripts/test-runner.sh --env gcp --gcp-zone us-east1-b

# Run on Azure
./scripts/test-runner.sh --env azure
```

---

## 1. LOCAL EXECUTION

### Requirements
- Node.js 20+
- npm 10+
- Chromium/Firefox/WebKit browsers (installed via Playwright)
- 4GB RAM minimum, 8GB recommended
- macOS, Linux, or Windows

### Installation

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install

# Make test runner executable
chmod +x scripts/test-runner.sh
```

### Running Tests

```bash
# Default (all tests, chromium)
./scripts/test-runner.sh --env local

# Specific browser
./scripts/test-runner.sh --env local --browser firefox

# Parallel workers
./scripts/test-runner.sh --env local --workers 8

# Smoke tests only
./scripts/test-runner.sh --env local --smoke

# Specific test file
npm test tests/e2e/shopnow.spec.ts
```

### Results Location
- HTML Report: `./playwright-report/index.html`
- JSON Results: `./test-results-store/`
- Test Videos: `./test-results-store/**/video.webm`

### Pros ✅
- Fastest execution
- No infrastructure overhead
- Easy debugging
- Local file access

### Cons ❌
- Requires local setup
- Resource intensive
- OS-specific issues

---

## 2. DOCKER EXECUTION

### Requirements
- Docker Desktop 20.10+
- 8GB RAM
- 10GB disk space

### Setup

```bash
# Build test Docker image
docker build -f Dockerfile.test -t qa_agents-test:latest .

# Or use pre-built image
docker pull qa-agents/test:latest
```

### Running Tests

```bash
# Basic execution
./scripts/test-runner.sh --env docker

# With specific workers
./scripts/test-runner.sh --env docker --workers 8

# Smoke tests
./scripts/test-runner.sh --env docker --smoke

# Manual Docker command
docker run --rm \
  -v $(pwd)/playwright-report:/app/playwright-report \
  qa_agents-test:latest \
  npm test -- --workers=4
```

### Volume Mounts

The Docker container mounts:
- `playwright-report/` - HTML test report
- `test-results-store/` - Raw test results
- `screenshots/` - Test screenshots
- `videos/` - Test videos

### Results Location
- Inside container: `/app/playwright-report/`
- On host: `./playwright-report/`

### Environment Variables

```bash
docker run -e WORKERS=8 -e BROWSER=chromium qa_agents-test:latest
```

### Pros ✅
- Consistent environment
- Cross-platform
- Isolated from host
- Easy scaling
- CI/CD ready

### Cons ❌
- Additional setup
- Slower than local
- Larger disk footprint

---

## 3. AWS EXECUTION

### Prerequisites

```bash
# Install AWS CLI
brew install awscli

# Configure AWS credentials
aws configure

# Create EC2 key pair
aws ec2 create-key-pair --key-name qa-tests-key --query 'KeyMaterial' --output text > ~/.ssh/qa-tests-key.pem
chmod 600 ~/.ssh/qa-tests-key.pem

# Create security group
aws ec2 create-security-group \
  --group-name qa-tests-sg \
  --description "Security group for QA tests"

# Add SSH inbound rule
aws ec2 authorize-security-group-ingress \
  --group-name qa-tests-sg \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

### Update Configuration

Edit `scripts/test-runner.sh` with your AWS details:
```bash
AMI_ID="ami-0c55b159cbfafe1f0"  # Ubuntu 22.04 for your region
AWS_REGION="us-east-1"
AWS_INSTANCE_TYPE="t3.medium"
```

### Running Tests

```bash
# Standard (default region)
./scripts/test-runner.sh --env aws

# Specific region
./scripts/test-runner.sh --env aws --aws-region us-west-2

# Larger instance for parallel execution
AWS_INSTANCE_TYPE=t3.large ./scripts/test-runner.sh --env aws
```

### Instance Lifecycle

1. ✅ Launch EC2 instance
2. ✅ Wait for initialization
3. ✅ SSH and run tests
4. ✅ Download results
5. ✅ Terminate instance

### Cost Estimation

- t3.medium: ~$0.0416/hour (~$1/day)
- t3.large: ~$0.0832/hour (~$2/day)
- Data transfer: ~$0.01/GB

### Pros ✅
- Scalable
- Auto-terminating
- No local resources used
- Enterprise-grade infrastructure
- Cross-region support

### Cons ❌
- AWS account required
- Cost per run (~$0.50-$2)
- Setup complexity
- Network latency

---

## 4. GOOGLE CLOUD EXECUTION

### Prerequisites

```bash
# Install Google Cloud SDK
# macOS:
brew install --cask google-cloud-sdk

# Linux:
curl https://sdk.cloud.google.com | bash

# Initialize and authenticate
gcloud init
gcloud auth login

# Set default project
gcloud config set project YOUR_PROJECT_ID

# Create VM image (custom or use Ubuntu)
# Already configured for Ubuntu 22.04 LTS
```

### Running Tests

```bash
# Standard (default zone)
./scripts/test-runner.sh --env gcp

# Specific zone
./scripts/test-runner.sh --env gcp --gcp-zone us-west1-b

# Larger machine type for parallel execution
GCP_MACHINE_TYPE=e2-standard-2 ./scripts/test-runner.sh --env gcp
```

### Instance Lifecycle

1. ✅ Create Compute Engine VM
2. ✅ Run startup script
3. ✅ SSH and execute tests
4. ✅ Download results to Cloud Storage
5. ✅ Delete VM

### Cost Estimation

- e2-medium: ~$0.033/hour (~$0.80/day)
- e2-standard-2: ~$0.084/hour (~$2/day)
- Persistent disk: ~$0.04/month per GB

### Pros ✅
- Google Cloud Scale
- Easy scalability
- Integrated monitoring
- Cloud Storage integration
- Generous free tier

### Cons ❌
- Google Cloud account required
- Cost per run (~$0.20-$0.50)
- Learning curve
- Zone availability varies

---

## 5. AZURE EXECUTION

### Prerequisites

```bash
# Install Azure CLI
brew install azure-cli

# Login to Azure
az login

# Set subscription
az account set --subscription YOUR_SUBSCRIPTION_ID

# Create resource group
az group create --name qa-tests-rg --location eastus
```

### Running Tests

```bash
# Standard execution
./scripts/test-runner.sh --env azure

# Larger VM for more workers
AZURE_VM_SIZE=Standard_B4ms ./scripts/test-runner.sh --env azure
```

### Instance Lifecycle

1. ✅ Create Azure VM
2. ✅ Run custom script extension
3. ✅ SSH and execute tests
4. ✅ Download results
5. ✅ Delete VM and resources

### Cost Estimation

- Standard_B2s: ~$0.05/hour (~$1.20/day)
- Standard_B4ms: ~$0.166/hour (~$4/day)

### Pros ✅
- Microsoft ecosystem integration
- Enterprise support
- Hybrid cloud options
- Good for Windows testing
- Competitive pricing

### Cons ❌
- Azure account required
- Setup complexity
- Cost per run (~$0.25-$0.50)
- Slower startup than AWS/GCP

---

## Comparison Matrix

| Aspect | Local | Docker | AWS | GCP | Azure |
|--------|-------|--------|-----|-----|-------|
| **Setup Time** | 5 min | 2 min | 20 min | 15 min | 15 min |
| **Execution Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Cost** | $0 | $0 | $0.50 | $0.20 | $0.25 |
| **Scalability** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Maintenance** | High | Medium | Low | Low | Medium |
| **Setup Complexity** | Low | Low | High | High | High |
| **Cross-Platform** | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: QA Tests

on: [push, pull_request]

jobs:
  test-local:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm test

  test-docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -f Dockerfile.test -t qa-test .
      - run: |
          docker run --rm \
            -v $(pwd)/playwright-report:/app/playwright-report \
            qa-test npm test
```

### Upload Results

```bash
# AWS S3
aws s3 sync ./playwright-report s3://qa-results-bucket/$(date +%Y-%m-%d-%H-%M-%S)/

# Google Cloud Storage
gsutil -m cp -r ./playwright-report gs://qa-results-bucket/

# Azure Blob Storage
az storage blob upload-batch -d results -s playwright-report
```

---

## Troubleshooting

### Local Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm ci

# Reinstall browsers
npx playwright install --with-deps
```

### Docker Issues

```bash
# Rebuild image without cache
docker build --no-cache -f Dockerfile.test -t qa_agents-test:latest .

# Run with verbose output
docker run --rm -it qa_agents-test:latest npm test -- --reporter=verbose
```

### Cloud Issues

```bash
# AWS: Check instance logs
aws ec2 get-console-output --instance-id i-xxxxxxxx

# GCP: Check serial port output
gcloud compute instances get-serial-port-output INSTANCE_NAME

# Azure: Check boot diagnostics
az vm boot-diagnostics get-boot-log --name VM_NAME --resource-group RG_NAME
```

---

## Best Practices

1. **Use Docker for CI/CD** - Consistent, reproducible environments
2. **Use Local for Development** - Fastest iteration
3. **Use Cloud for Load Testing** - Scale testing across regions
4. **Monitor Costs** - Set up billing alerts
5. **Clean Up Resources** - Terminate unused instances
6. **Version Control** - Keep scripts in git
7. **Log Results** - Archive test reports for audit trails

---

## Support & Resources

- Playwright Docs: https://playwright.dev
- AWS EC2 Guide: https://docs.aws.amazon.com/ec2/
- Google Cloud VMs: https://cloud.google.com/compute/docs
- Azure VMs: https://docs.microsoft.com/en-us/azure/virtual-machines/
