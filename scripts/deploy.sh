#!/bin/bash

# Data Contracts Studio - Production Deployment Script
# This script helps deploy the application to production

set -e

echo "🚀 Deploying Data Contracts Studio to production..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &>/dev/null; then
        print_error "Docker is required but not installed."
        exit 1
    fi

    if ! command -v docker-compose &>/dev/null; then
        print_error "Docker Compose is required but not installed."
        exit 1
    fi

    print_status "Docker and Docker Compose are available ✓"
}

# Build and deploy
deploy() {
    print_status "Building and deploying application..."

    # Build images
    print_status "Building Docker images..."
    docker-compose -f docker-compose.yml build

    # Start services
    print_status "Starting services..."
    docker-compose -f docker-compose.yml up -d

    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    sleep 30

    # Check health
    if docker-compose -f docker-compose.yml ps | grep -q "Up (healthy)"; then
        print_status "Application deployed successfully! 🎉"
        echo ""
        echo "Services are running:"
        echo "  Frontend: http://localhost"
        echo "  Backend:  http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "To stop the application:"
        echo "  docker-compose -f docker-compose.yml down"
    else
        print_error "Some services are not healthy. Check logs with:"
        echo "  docker-compose -f docker-compose.yml logs"
        exit 1
    fi
}

# Main deployment process
main() {
    print_status "Starting production deployment..."

    check_docker
    deploy

    print_status "Deployment complete! 🎉"
}

main "$@"
