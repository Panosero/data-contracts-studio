#!/bin/bash

# Data Contracts Studio - Docker Deployment Script with IP Detection
# This script helps deploy the application using Docker with IP-based configuration

set -e

echo "🚀 Deploying Data Contracts Studio with Docker..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}[CONFIG]${NC} $1"
}

# Get server IP address
get_server_ip() {
    print_status "Detecting server IP address..."
    
    # Try multiple methods to get the server's public IP
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || curl -s ipecho.net/plain 2>/dev/null || hostname -I | awk '{print $1}')
    
    if [ -z "$SERVER_IP" ]; then
        print_warning "Could not automatically detect server IP. Please enter it manually:"
        read -p "Enter your server IP address: " SERVER_IP
    fi
    
    print_info "Server IP detected/configured: $SERVER_IP"
    
    # Confirm with user
    read -p "Is this correct? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter the correct server IP address: " SERVER_IP
    fi
    
    export SERVER_IP
}

# Create .env file
create_env_file() {
    print_status "Creating environment configuration..."
    
    cat > .env <<EOF
# Server Configuration
SERVER_IP=$SERVER_IP

# Security
SECRET_KEY=$(openssl rand -hex 32)

# Database
POSTGRES_DB=datacontracts
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# API Configuration
DEBUG=False
ALLOWED_ORIGINS=["http://localhost", "http://127.0.0.1", "http://$SERVER_IP"]
EOF

    print_status "Environment file created ✓"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &>/dev/null; then
        print_error "Docker is required but not installed."
        print_info "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &>/dev/null; then
        print_error "Docker Compose is required but not installed."
        print_info "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi

    print_status "Docker and Docker Compose are available ✓"
}

# Build and deploy
deploy() {
    print_status "Building and deploying application..."

    # Stop existing containers
    docker-compose down 2>/dev/null || true

    # Build images with no cache for fresh build
    print_status "Building Docker images..."
    docker-compose build --no-cache

    # Start services
    print_status "Starting services..."
    docker-compose up -d

    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 15

    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_status "Services are running ✓"
    else
        print_error "Some services failed to start. Check logs:"
        docker-compose logs
        exit 1
    fi
}

# Show completion information
show_completion_info() {
    print_status "Deployment complete! 🎉"
    echo ""
    echo "Your application is now running:"
    echo "  📱 Website: http://$SERVER_IP"
    echo "  🔌 API: http://$SERVER_IP:8000/api/v1"
    echo "  📚 API Docs: http://$SERVER_IP:8000/docs"
    echo "  🗄️  Database: PostgreSQL on port 5432"
    echo ""
    echo "Useful commands:"
    echo "  📊 View logs: docker-compose logs -f"
    echo "  📈 Check status: docker-compose ps"
    echo "  🔄 Restart: docker-compose restart"
    echo "  🛑 Stop: docker-compose down"
    echo "  🔄 Update: git pull && docker-compose up -d --build"
    echo ""
    print_info "Access your application at: http://$SERVER_IP"
    print_warning "Make sure ports 80 and 8000 are open in your server's firewall"
    echo ""
    echo "🔐 Database credentials are stored in .env file"
    echo "🔑 API secret key has been generated automatically"
}

main() {
    check_docker
    get_server_ip
    create_env_file
    deploy
    show_completion_info
}

# Run deployment
main "$@"