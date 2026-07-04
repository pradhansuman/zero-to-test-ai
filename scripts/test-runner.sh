#!/bin/bash
# Multi-Environment Test Runner
# Supports: Local, Docker, AWS, Google Cloud, Azure
# Usage: ./scripts/test-runner.sh --env [local|docker|aws|gcp|azure] [options]

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
ENV="local"
BROWSER="chromium"
WORKERS="4"
REPORTER="html"
STORE_RESULTS=true
DOCKER_IMAGE="qa_agents-test:latest"
AWS_REGION="us-east-1"
AWS_INSTANCE_TYPE="t3.medium"
GCP_ZONE="us-central1-a"
GCP_MACHINE_TYPE="e2-medium"

# Functions
show_help() {
  cat << 'EOF'
Usage: test-runner.sh [OPTIONS]

ENVIRONMENTS:
  --env local          Run tests on local machine (default)
  --env docker         Run tests in Docker container
  --env aws            Deploy to AWS EC2 and run tests
  --env gcp            Deploy to Google Cloud VM and run tests
  --env azure          Deploy to Azure VM and run tests

OPTIONS:
  --browser [chromium|firefox|webkit]  Browser to test (default: chromium)
  --workers [1-8]                      Number of parallel workers (default: 4)
  --reporter [html|json|junit]         Reporter format (default: html)
  --config [file]                      Playwright config file
  --spec [pattern]                     Test spec pattern (e.g., "store")
  --tag [tag]                          Run tests with specific tag
  --smoke                              Run smoke tests only (@smoke tag)
  --no-upload                          Don't upload results to S3/Cloud Storage
  --help                               Show this help message

EXAMPLES:
  # Run locally
  ./scripts/test-runner.sh --env local --browser chromium

  # Run in Docker
  ./scripts/test-runner.sh --env docker --workers 8

  # Run on AWS
  ./scripts/test-runner.sh --env aws --aws-region us-west-2

  # Run on Google Cloud
  ./scripts/test-runner.sh --env gcp --gcp-zone us-east1-b

  # Run smoke tests only
  ./scripts/test-runner.sh --env docker --smoke

EOF
}

# Parse arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --env)
        ENV="$2"
        shift 2
        ;;
      --browser)
        BROWSER="$2"
        shift 2
        ;;
      --workers)
        WORKERS="$2"
        shift 2
        ;;
      --reporter)
        REPORTER="$2"
        shift 2
        ;;
      --aws-region)
        AWS_REGION="$2"
        shift 2
        ;;
      --gcp-zone)
        GCP_ZONE="$2"
        shift 2
        ;;
      --smoke)
        SPEC="@smoke"
        shift
        ;;
      --no-upload)
        STORE_RESULTS=false
        shift
        ;;
      --help)
        show_help
        exit 0
        ;;
      *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
  done
}

# Local execution
run_local() {
  echo -e "${BLUE}🔄 Running tests LOCALLY${NC}"
  echo "Browser: $BROWSER | Workers: $WORKERS | Reporter: $REPORTER"

  npm test -- \
    --project="$BROWSER" \
    --workers="$WORKERS" \
    --reporter="$REPORTER"

  echo -e "${GREEN}✅ Tests completed locally${NC}"
}

# Docker execution
run_docker() {
  echo -e "${BLUE}🐳 Running tests in DOCKER${NC}"

  # Build Docker image if needed
  if ! docker image inspect "$DOCKER_IMAGE" >/dev/null 2>&1; then
    echo -e "${YELLOW}📦 Building Docker image: $DOCKER_IMAGE${NC}"
    docker build -f Dockerfile.test -t "$DOCKER_IMAGE" .
  fi

  echo "Running Docker container..."
  docker run --rm \
    --name qa-tests \
    -v "$(pwd)/playwright-report:/app/playwright-report" \
    -v "$(pwd)/test-results-store:/app/test-results-store" \
    -e BROWSER="$BROWSER" \
    -e WORKERS="$WORKERS" \
    "$DOCKER_IMAGE" \
    npm test -- --workers="$WORKERS" --reporter="$REPORTER"

  echo -e "${GREEN}✅ Tests completed in Docker${NC}"
}

# AWS execution
run_aws() {
  echo -e "${BLUE}☁️  Running tests on AWS EC2${NC}"
  echo "Region: $AWS_REGION | Instance Type: $AWS_INSTANCE_TYPE"

  if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not installed${NC}"
    echo "Install with: brew install awscli"
    exit 1
  fi

  INSTANCE_NAME="qa-tests-$(date +%s)"
  AMI_ID="ami-0c55b159cbfafe1f0"  # Ubuntu 22.04 LTS (update for your region)

  echo -e "${YELLOW}🚀 Launching EC2 instance: $INSTANCE_NAME${NC}"

  INSTANCE_ID=$(aws ec2 run-instances \
    --region "$AWS_REGION" \
    --image-id "$AMI_ID" \
    --instance-type "$AWS_INSTANCE_TYPE" \
    --key-name qa-tests-key \
    --security-group-ids sg-xxxxxxxx \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --user-data file://scripts/aws-user-data.sh \
    --query 'Instances[0].InstanceId' \
    --output text)

  echo "Instance ID: $INSTANCE_ID"
  echo -e "${YELLOW}⏳ Waiting for instance to be ready...${NC}"

  aws ec2 wait instance-running --region "$AWS_REGION" --instance-ids "$INSTANCE_ID"

  INSTANCE_IP=$(aws ec2 describe-instances \
    --region "$AWS_REGION" \
    --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

  echo "Instance IP: $INSTANCE_IP"

  # Wait for SSH to be ready
  sleep 30

  echo -e "${YELLOW}📡 Running tests on instance...${NC}"

  ssh -i ~/.ssh/qa-tests-key.pem "ec2-user@$INSTANCE_IP" << 'SSHEOF'
    cd /home/ec2-user/qa-tests
    npm test -- --workers=8 --reporter=html
  SSHEOF

  echo -e "${YELLOW}📥 Downloading results...${NC}"

  scp -i ~/.ssh/qa-tests-key.pem \
    "ec2-user@$INSTANCE_IP:/home/ec2-user/qa-tests/playwright-report/*" \
    ./playwright-report/

  echo -e "${YELLOW}🧹 Terminating instance...${NC}"
  aws ec2 terminate-instances \
    --region "$AWS_REGION" \
    --instance-ids "$INSTANCE_ID"

  echo -e "${GREEN}✅ Tests completed on AWS${NC}"
}

# Google Cloud execution
run_gcp() {
  echo -e "${BLUE}☁️  Running tests on Google Cloud${NC}"
  echo "Zone: $GCP_ZONE | Machine Type: $GCP_MACHINE_TYPE"

  if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
  fi

  INSTANCE_NAME="qa-tests-$(date +%s)"

  echo -e "${YELLOW}🚀 Creating GCP VM: $INSTANCE_NAME${NC}"

  gcloud compute instances create "$INSTANCE_NAME" \
    --zone="$GCP_ZONE" \
    --machine-type="$GCP_MACHINE_TYPE" \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --metadata-from-file startup-script=scripts/gcp-startup-script.sh \
    --scopes=https://www.googleapis.com/auth/cloud-platform

  echo -e "${YELLOW}⏳ Waiting for VM to be ready...${NC}"
  sleep 45

  echo -e "${YELLOW}📡 Running tests on VM...${NC}"

  gcloud compute ssh "$INSTANCE_NAME" \
    --zone="$GCP_ZONE" \
    --command="cd /home/$(whoami)/qa-tests && npm test -- --workers=8 --reporter=html"

  echo -e "${YELLOW}📥 Downloading results...${NC}"

  gcloud compute scp \
    "$INSTANCE_NAME:/home/$(whoami)/qa-tests/playwright-report/*" \
    ./playwright-report/ \
    --zone="$GCP_ZONE" \
    --recurse

  echo -e "${YELLOW}🧹 Deleting VM...${NC}"
  gcloud compute instances delete "$INSTANCE_NAME" \
    --zone="$GCP_ZONE" \
    --quiet

  echo -e "${GREEN}✅ Tests completed on Google Cloud${NC}"
}

# Azure execution
run_azure() {
  echo -e "${BLUE}☁️  Running tests on Azure${NC}"

  if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI not installed${NC}"
    echo "Install with: brew install azure-cli"
    exit 1
  fi

  INSTANCE_NAME="qa-tests-$(date +%s)"
  RESOURCE_GROUP="qa-tests-rg"

  echo -e "${YELLOW}🚀 Creating Azure VM: $INSTANCE_NAME${NC}"

  az vm create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$INSTANCE_NAME" \
    --image UbuntuLTS \
    --size Standard_B2s \
    --admin-username azureuser \
    --custom-data scripts/azure-user-data.sh

  echo -e "${YELLOW}⏳ Waiting for VM to be ready...${NC}"
  sleep 45

  VM_IP=$(az vm show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$INSTANCE_NAME" \
    --show-details \
    --query publicIps \
    --output tsv)

  echo "VM IP: $VM_IP"

  echo -e "${YELLOW}📡 Running tests on VM...${NC}"

  ssh "azureuser@$VM_IP" << 'SSHEOF'
    cd /home/azureuser/qa-tests
    npm test -- --workers=8 --reporter=html
  SSHEOF

  echo -e "${YELLOW}📥 Downloading results...${NC}"

  scp -r "azureuser@$VM_IP:/home/azureuser/qa-tests/playwright-report/*" \
    ./playwright-report/

  echo -e "${YELLOW}🧹 Deleting VM...${NC}"
  az vm delete \
    --resource-group "$RESOURCE_GROUP" \
    --name "$INSTANCE_NAME" \
    --yes

  echo -e "${GREEN}✅ Tests completed on Azure${NC}"
}

# Main execution
main() {
  parse_args "$@"

  echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
  echo -e "${BLUE}🧪 QA Test Runner - Multi-Environment Execution${NC}"
  echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
  echo "Environment: $ENV"
  echo "Browser: $BROWSER"
  echo "Workers: $WORKERS"
  echo "Reporter: $REPORTER"
  echo ""

  case "$ENV" in
    local)
      run_local
      ;;
    docker)
      run_docker
      ;;
    aws)
      run_aws
      ;;
    gcp)
      run_gcp
      ;;
    azure)
      run_azure
      ;;
    *)
      echo -e "${RED}❌ Unknown environment: $ENV${NC}"
      show_help
      exit 1
      ;;
  esac

  echo ""
  echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
  echo -e "${GREEN}✅ Test execution completed!${NC}"
  echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
  echo ""
  echo "📊 Results available at:"
  echo "   HTML Report: ./playwright-report/index.html"
  echo "   JSON Results: ./test-results-store/"
}

# Run
main "$@"
