#!/bin/bash

# Data Contracts Studio - Simple Deployment
# Uses .env file for all configuration

set -e

echo "🚀 Data Contracts Studio - Simple Deployment"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_info() { echo -e "${BLUE}[CONFIG]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if .env exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found!"
        echo ""
        echo "Creating .env file from template..."

        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_status ".env file created from template"
        else
            print_error ".env.example not found!"
            exit 1
        fi

        echo ""
        print_warning "🔒 IMPORTANT: Edit .env file with your settings:"
        echo "  1. Set your SERVER_IP (or leave as auto-detect)"
        echo "  2. Change POSTGRES_PASSWORD to a secure password"
        echo "  3. Change SECRET_KEY to a secure random string"
        echo "  4. Add your API keys (OPENAI_API_KEY, etc.)"
        echo ""
        echo "Example:"
        echo "  nano .env"
        echo ""
        read -p "Press Enter after editing .env file..." -r
    fi
}

# Auto-detect server IP if needed
setup_server_ip() {
    # Load current .env
    if grep -q "SERVER_IP=auto-detect" .env; then
        print_status "Auto-detecting server IP..."

        SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || hostname -I | awk '{print $1}')

        if [ -z "$SERVER_IP" ]; then
            print_warning "Could not auto-detect IP. Please enter manually:"
            read -p "Server IP: " SERVER_IP
        fi

        print_info "Server IP: $SERVER_IP"

        # Update .env file
        sed -i.bak "s/SERVER_IP=auto-detect/SERVER_IP=$SERVER_IP/" .env
        rm -f .env.bak
    else
        SERVER_IP=$(grep "SERVER_IP=" .env | cut -d'=' -f2)
        print_info "Using configured IP: $SERVER_IP"
    fi
}

# Generate secure secrets if needed
setup_secrets() {
    print_status "Checking security configuration..."

    # Generate SECRET_KEY if needed
    if grep -q "SECRET_KEY=change-this" .env; then
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i.bak "s/SECRET_KEY=change-this.*/SECRET_KEY=$SECRET_KEY/" .env
        rm -f .env.bak
        print_status "Generated secure SECRET_KEY"
    fi

    # Generate DB password if needed
    if grep -q "POSTGRES_PASSWORD=change-this" .env; then
        DB_PASSWORD=$(openssl rand -base64 32)
        sed -i.bak "s/POSTGRES_PASSWORD=change-this.*/POSTGRES_PASSWORD=$DB_PASSWORD/" .env
        rm -f .env.bak
        print_status "Generated secure database password"
    fi
}

# Check Docker
check_docker() {
    if ! command -v docker &>/dev/null; then
        print_error "Docker is required. Install from: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &>/dev/null; then
        print_error "Docker Compose is required. Install from: https://docs.docker.com/compose/install/"
        exit 1
    fi

    print_status "Docker and Docker Compose available ✓"
}

# Deploy
deploy() {
    print_status "Starting deployment..."

    # Stop existing containers
    docker-compose down 2>/dev/null || true

    # Build and start
    print_status "Building and starting services..."
    docker-compose up -d --build

    # Wait for services
    print_status "Waiting for services to start..."
    sleep 15

    # Check status
    if docker-compose ps | grep -q "Up"; then
        print_status "Services are running ✓"
    else
        print_error "Some services failed to start!"
        echo ""
        echo "Check logs with: docker-compose logs"
        exit 1
    fi
}

# Show completion info
show_info() {
    # Get ports from .env
    FRONTEND_PORT=$(grep "FRONTEND_PORT=" .env | cut -d'=' -f2)
    BACKEND_PORT=$(grep "BACKEND_PORT=" .env | cut -d'=' -f2)

    echo ""
    print_status "🎉 Deployment Complete!"
    echo ""
    echo "Your application is running:"
    echo "  📱 Website:  http://$SERVER_IP:$FRONTEND_PORT"
    echo "  🔌 API:      http://$SERVER_IP:$BACKEND_PORT/api/v1"
    echo "  📚 Docs:     http://$SERVER_IP:$BACKEND_PORT/docs"
    echo ""
    echo "Useful commands:"
    echo "  📊 Logs:     docker-compose logs -f"
    echo "  📈 Status:   docker-compose ps"
    echo "  🔄 Restart:  docker-compose restart"
    echo "  🛑 Stop:     docker-compose down"
    echo ""

    if [ "$FRONTEND_PORT" != "80" ]; then
        print_warning "Make sure port $FRONTEND_PORT is open in your firewall"
    fi

    print_info "Configuration is stored in .env file"
}

# Main
main() {
    check_docker
    check_env_file
    setup_server_ip
    setup_secrets
    deploy
    show_info
}

main "$@"
