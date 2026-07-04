#!/bin/bash
# Production Deployment Script - Phases 1-5 QA Automation Platform
# Usage: ./deploy.sh [staging|production]

set -e  # Exit on error

ENVIRONMENT=${1:-staging}
REGISTRY=${DOCKER_REGISTRY:-docker.io}
IMAGE_NAME=${REGISTRY}/qa-platform
IMAGE_TAG=${VERSION:-v5.0.0}
NAMESPACE=${ENVIRONMENT}

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Validate environment
validate_environment() {
    log_info "Validating deployment environment..."

    if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
        log_error "Invalid environment. Use 'staging' or 'production'"
        exit 1
    fi

    # Check required tools
    for tool in docker kubectl git; do
        if ! command -v $tool &> /dev/null; then
            log_error "$tool is not installed"
            exit 1
        fi
    done

    # Check Kubernetes connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi

    log_success "Environment validation passed"
}

# Load environment variables
load_env_file() {
    log_info "Loading environment variables..."

    ENV_FILE=".env.${ENVIRONMENT}"
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        log_info "Create $ENV_FILE with required variables"
        exit 1
    fi

    set -a
    source "$ENV_FILE"
    set +a

    log_success "Environment variables loaded"
}

# Run tests
run_tests() {
    log_info "Running test suite..."

    if ! pytest tests/ -v --cov=app --cov-report=term-only; then
        log_error "Tests failed"
        exit 1
    fi

    log_success "All tests passed"
}

# Build Docker image
build_image() {
    log_info "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."

    if ! docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" \
        --build-arg ENVIRONMENT="${ENVIRONMENT}" \
        -f Dockerfile .; then
        log_error "Docker build failed"
        exit 1
    fi

    log_success "Docker image built successfully"
}

# Push to registry
push_image() {
    log_info "Pushing image to registry: ${REGISTRY}..."

    if ! docker push "${IMAGE_NAME}:${IMAGE_TAG}"; then
        log_error "Failed to push image to registry"
        exit 1
    fi

    log_success "Image pushed to registry"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."

    if [ -z "$DATABASE_URL" ]; then
        log_error "DATABASE_URL not set"
        exit 1
    fi

    # Create migration pod
    kubectl run db-migrate-${NAMESPACE}-$(date +%s) \
        --image="${IMAGE_NAME}:${IMAGE_TAG}" \
        --restart=Never \
        --namespace="${NAMESPACE}" \
        --env="DATABASE_URL=${DATABASE_URL}" \
        -- alembic upgrade head

    log_success "Database migrations completed"
}

# Deploy to Kubernetes
deploy_to_k8s() {
    log_info "Deploying to Kubernetes (${NAMESPACE})..."

    # Update image in deployment
    kubectl set image deployment/qa-platform \
        qa-platform="${IMAGE_NAME}:${IMAGE_TAG}" \
        -n "${NAMESPACE}" || {
        log_warning "Deployment not found, creating new deployment..."
        kubectl apply -f "k8s/${ENVIRONMENT}.yaml" -n "${NAMESPACE}"
    }

    # Wait for rollout
    if kubectl rollout status deployment/qa-platform -n "${NAMESPACE}" --timeout=5m; then
        log_success "Deployment successful"
    else
        log_error "Deployment failed or timed out"
        exit 1
    fi
}

# Health check
health_check() {
    log_info "Performing health checks..."

    # Get service endpoint
    SERVICE_IP=$(kubectl get svc qa-platform -n "${NAMESPACE}" -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "localhost")

    # Wait for service to be ready
    for i in {1..30}; do
        if curl -s "http://${SERVICE_IP}:8000/api/health" | grep -q '"status"'; then
            log_success "Health check passed"
            echo "Service URL: http://${SERVICE_IP}:8000"
            return 0
        fi
        log_info "Waiting for service to be ready... ($i/30)"
        sleep 2
    done

    log_error "Health check failed after 60 seconds"
    exit 1
}

# Validate deployment
validate_deployment() {
    log_info "Validating deployment..."

    # Check pod status
    POD_COUNT=$(kubectl get pods -n "${NAMESPACE}" -l app=qa-platform --field-selector=status.phase=Running -o json | jq '.items | length')

    if [ "$POD_COUNT" -gt 0 ]; then
        log_success "All pods running ($POD_COUNT pods)"
    else
        log_error "No running pods found"
        exit 1
    fi

    # Check for errors in logs
    if kubectl logs -n "${NAMESPACE}" -l app=qa-platform --tail=50 | grep -i "error\|critical"; then
        log_warning "Errors found in logs - review carefully"
    else
        log_success "No critical errors in logs"
    fi
}

# Rollback function
rollback() {
    log_warning "Rolling back deployment..."

    if kubectl rollout undo deployment/qa-platform -n "${NAMESPACE}"; then
        kubectl rollout status deployment/qa-platform -n "${NAMESPACE}"
        log_success "Rollback completed"
    else
        log_error "Rollback failed"
        exit 1
    fi
}

# Main deployment flow
main() {
    log_info "========================================="
    log_info "QA Platform Deployment - Phases 1-5"
    log_info "Environment: ${ENVIRONMENT}"
    log_info "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    log_info "========================================="

    validate_environment
    load_env_file
    run_tests
    build_image
    push_image

    # Ask for confirmation before database migration
    read -p "Run database migrations? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_migrations
    fi

    deploy_to_k8s
    health_check
    validate_deployment

    log_info "========================================="
    log_success "Deployment completed successfully!"
    log_info "Environment: ${ENVIRONMENT}"
    log_info "Image Tag: ${IMAGE_TAG}"
    log_info "========================================="
}

# Trap errors and rollback on failure
trap 'log_error "Deployment failed"; rollback' ERR

# Run main deployment
main "$@"
