#!/bin/bash
# Local Docker Deployment - QA Platform

set -e

echo "🚀 QA Platform - Local Docker Deployment"
echo "========================================"

# Stop any existing containers
docker-compose down -v 2>/dev/null || true

# Clean up
docker system prune -af --volumes 2>/dev/null || true

# Build fresh
echo "🔨 Building Docker image..."
docker-compose build --no-cache

# Start services
echo "📦 Starting services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start (90 seconds)..."
sleep 90

# Check status
echo "📊 Service Status:"
docker-compose ps

# Health check
echo "🔍 Health check..."
for i in {1..30}; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/api/health" || echo "000")
    if [ "$RESPONSE" = "200" ]; then
        echo "✅ API is healthy"
        break
    fi
    echo "⏳ Waiting... (attempt $i/30, HTTP $RESPONSE)"
    sleep 3
done

# Final health check
HEALTH=$(curl -s "http://localhost:8000/api/health")

echo ""
echo "✅ DEPLOYMENT COMPLETE"
echo ""
echo "🌐 Access Points:"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo "   Health: http://localhost:8000/api/health"
echo ""
echo "🗄️ Infrastructure:"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "📋 Commands:"
echo "   View logs: docker-compose logs -f api"
echo "   Stop: docker-compose down"
echo "   Restart: docker-compose restart"
echo ""
