#!/bin/bash
# AWS EC2 User Data Script
# Runs on instance startup to configure and execute tests

set -euo pipefail

echo "🚀 AWS EC2 Instance Initialization Started"

# Update system
yum update -y
yum install -y git curl wget

# Install Node.js 20.x
curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
yum install -y nodejs

# Install Docker
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# Clone repository
cd /home/ec2-user
git clone https://github.com/YOUR_ORG/qa-agents.git qa-tests
cd qa-tests

# Install dependencies
npm ci

# Install Playwright browsers
npx playwright install --with-deps chromium firefox

# Create directories for results
mkdir -p playwright-report test-results-store

echo "✅ Instance ready for testing"

# Log completion
echo "Instance initialization complete at $(date)" > /tmp/setup.log
