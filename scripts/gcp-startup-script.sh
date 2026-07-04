#!/bin/bash
# Google Cloud VM Startup Script
# Runs on first boot to configure and execute tests

set -euo pipefail

echo "🚀 Google Cloud VM Initialization Started"

# Update system
apt-get update
apt-get upgrade -y
apt-get install -y git curl wget build-essential

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt-get install -y nodejs

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
bash get-docker.sh
systemctl start docker
systemctl enable docker
usermod -aG docker $(whoami)

# Clone repository
cd /home/$(whoami)
git clone https://github.com/YOUR_ORG/qa-agents.git qa-tests
cd qa-tests

# Install dependencies
npm ci

# Install Playwright browsers
npx playwright install --with-deps chromium firefox

# Create directories for results
mkdir -p playwright-report test-results-store

# Upload results to Google Cloud Storage (optional)
# gsutil -m cp -r playwright-report gs://qa-results-bucket/

echo "✅ Google Cloud VM ready for testing"
