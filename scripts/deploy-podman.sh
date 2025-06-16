#!/bin/bash

# Data Contracts Studio - Podman Deployment Script
# Optimized for rootless containers and enterprise security

set -e

echo "🚀 Data Contracts Studio - Podman Deployment"

# Colors for output
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

# Logging functions
print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_info() { echo -e "${BLUE}[CONFIG]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly COMPOSE_FILE="${PROJECT_ROOT}/podman-compose.yml"
readonly ENV_FILE="${PROJECT_ROOT}/.env"
readonly DATA_DIR="${PROJECT_ROOT}/data"

# Default configuration
DEFAULT_BACKEND_PORT=8888
DEFAULT_FRONTEND_PORT=80
DEFAULT_DATABASE_PORT=5432
DEFAULT_POSTGRES_DB=datacontracts
DEFAULT_POSTGRES_USER=postgres

# Function to check if podman is installed
check_podman() {
    print_status "Checking Podman installation..."
    
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed!"
        echo ""
        echo "Please install Podman:"
        echo "  - RHEL/CentOS/Fedora: sudo dnf install podman podman-compose"
        echo "  - Ubuntu/Debian: sudo apt install podman podman-compose"
        echo "  - macOS: brew install podman"
        exit 1
    fi
    
    if ! command -v podman-compose &> /dev/null && ! podman compose version &> /dev/null; then
        print_error "Podman Compose is not available!"
        echo ""
        echo "Please install podman-compose:"
        echo "  - pip install podman-compose"
        echo "  - Or use built-in: podman compose (Podman 4.0+)"
        exit 1
    fi
    
    print_status "✅ Podman $(podman --version | cut -d' ' -f3) is installed"
}

# Function to check if running rootless
check_rootless() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. For better security, consider running rootless."
        print_info "To set up rootless Podman:"
        echo "  1. podman system migrate"
        echo "  2. systemctl --user enable --now podman.socket"
        echo ""
        read -p "Continue as root? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_status "✅ Running rootless Podman (recommended)"
    fi
}

# Function to create environment file
create_env_file() {
    if [[ ! -f "$ENV_FILE" ]]; then
        print_warning ".env file not found. Creating from template..."
        
        cat > "$ENV_FILE" << EOF
# Data Contracts Studio - Podman Configuration
# Generated on $(date)

# Application Configuration
VERSION=1.0.0
APP_NAME=Data Contracts Studio
APP_VERSION=1.0.0

# Server Configuration
SERVER_IP=localhost
BACKEND_PORT=${DEFAULT_BACKEND_PORT}
FRONTEND_PORT=${DEFAULT_FRONTEND_PORT}
DATABASE_PORT=${DEFAULT_DATABASE_PORT}

# Database Configuration
POSTGRES_DB=${DEFAULT_POSTGRES_DB}
POSTGRES_USER=${DEFAULT_POSTGRES_USER}
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-16)

# Security Configuration
SECRET_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-32)
DEBUG=False

# Data Directory (for volume mounts)
DATA_DIR=${DATA_DIR}

# API Keys (set your actual keys)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
HUGGINGFACE_API_KEY=
AZURE_OPENAI_KEY=

# Podman-specific Configuration
UID=$(id -u)
GID=$(id -g)
EOF
        
        print_status "✅ Created .env file with secure defaults"
        print_warning "Please edit .env file and set your API keys!"
    else
        print_status "✅ Found existing .env file"
    fi
}

# Function to create data directories
create_directories() {
    print_status "Creating data directories..."
    
    mkdir -p "${DATA_DIR}/postgres_data"
    mkdir -p "${PROJECT_ROOT}/backend/data"
    
    # Set appropriate permissions for rootless
    if [[ $EUID -ne 0 ]]; then
        chmod 755 "${DATA_DIR}"
        chmod 750 "${DATA_DIR}/postgres_data"
    fi
    
    print_status "✅ Data directories created"
}

# Function to build images
build_images() {
    print_status "Building Podman images..."
    
    cd "$PROJECT_ROOT"
    
    # Build backend
    print_info "Building backend image..."
    podman build -f backend/Dockerfile.podman -t data-contracts-backend:latest backend/
    
    # Build frontend
    print_info "Building frontend image..."
    podman build -f frontend/Dockerfile.podman -t data-contracts-frontend:latest frontend/
    
    print_status "✅ Images built successfully"
}

# Function to start services
start_services() {
    print_status "Starting services with Podman Compose..."
    
    cd "$PROJECT_ROOT"
    
    # Use podman-compose or podman compose
    if command -v podman-compose &> /dev/null; then
        podman-compose -f "$COMPOSE_FILE" up -d
    else
        podman compose -f "$COMPOSE_FILE" up -d
    fi
    
    print_status "✅ Services started"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -sf "http://localhost:${BACKEND_PORT:-$DEFAULT_BACKEND_PORT}/health" > /dev/null 2>&1; then
            print_status "✅ Backend is healthy"
            break
        fi
        
        print_info "Waiting for backend... (attempt $attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        print_error "Backend health check failed"
        return 1
    fi
}

# Function to generate systemd service files
generate_systemd_services() {
    print_status "Generating systemd service files..."
    
    local service_dir="$HOME/.config/systemd/user"
    mkdir -p "$service_dir"
    
    # Generate pod service
    cat > "$service_dir/data-contracts-studio.service" << EOF
[Unit]
Description=Data Contracts Studio
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=on-failure
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run --name data-contracts-studio --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm --sdnotify=conmon --replace -d --pod-id-file %t/data-contracts-studio-pod.pod-id-file
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
EOF
    
    print_status "✅ Systemd service files generated"
    print_info "Enable auto-start with: systemctl --user enable data-contracts-studio.service"
}

# Function to show deployment info
show_deployment_info() {
    print_status "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Service Information:"
    echo "  Frontend: http://localhost:${FRONTEND_PORT:-$DEFAULT_FRONTEND_PORT}"
    echo "  Backend API: http://localhost:${BACKEND_PORT:-$DEFAULT_BACKEND_PORT}"
    echo "  Database: localhost:${DATABASE_PORT:-$DEFAULT_DATABASE_PORT}"
    echo ""
    echo "🔧 Useful Commands:"
    echo "  View logs: podman-compose -f $COMPOSE_FILE logs -f"
    echo "  Stop services: podman-compose -f $COMPOSE_FILE down"
    echo "  Restart services: podman-compose -f $COMPOSE_FILE restart"
    echo "  Update images: podman-compose -f $COMPOSE_FILE pull"
    echo ""
    echo "🔒 Security Notes:"
    echo "  - Services are running rootless"
    echo "  - Non-root users in containers"
    echo "  - Secure volume mounts"
    echo "  - Generated secure passwords"
    echo ""
}

# Function to show help
show_help() {
    echo "Data Contracts Studio - Podman Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  deploy     Full deployment (default)"
    echo "  build      Build images only"
    echo "  start      Start services only"
    echo "  stop       Stop services"
    echo "  restart    Restart services"
    echo "  logs       Show service logs"
    echo "  status     Show service status"
    echo "  systemd    Generate systemd service files"
    echo "  clean      Clean up containers and images"
    echo "  help       Show this help message"
    echo ""
}

# Main deployment function
main_deploy() {
    print_status "Starting Podman deployment process..."
    
    check_podman
    check_rootless
    create_env_file
    create_directories
    build_images
    start_services
    check_health
    generate_systemd_services
    show_deployment_info
}

# Command handling
case "${1:-deploy}" in
    deploy)
        main_deploy
        ;;
    build)
        check_podman
        build_images
        ;;
    start)
        check_podman
        start_services
        ;;
    stop)
        cd "$PROJECT_ROOT"
        if command -v podman-compose &> /dev/null; then
            podman-compose -f "$COMPOSE_FILE" down
        else
            podman compose -f "$COMPOSE_FILE" down
        fi
        print_status "✅ Services stopped"
        ;;
    restart)
        cd "$PROJECT_ROOT"
        if command -v podman-compose &> /dev/null; then
            podman-compose -f "$COMPOSE_FILE" restart
        else
            podman compose -f "$COMPOSE_FILE" restart
        fi
        print_status "✅ Services restarted"
        ;;
    logs)
        cd "$PROJECT_ROOT"
        if command -v podman-compose &> /dev/null; then
            podman-compose -f "$COMPOSE_FILE" logs -f
        else
            podman compose -f "$COMPOSE_FILE" logs -f
        fi
        ;;
    status)
        cd "$PROJECT_ROOT"
        if command -v podman-compose &> /dev/null; then
            podman-compose -f "$COMPOSE_FILE" ps
        else
            podman compose -f "$COMPOSE_FILE" ps
        fi
        ;;
    systemd)
        generate_systemd_services
        ;;
    clean)
        print_warning "This will remove all containers and images. Continue? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            cd "$PROJECT_ROOT"
            if command -v podman-compose &> /dev/null; then
                podman-compose -f "$COMPOSE_FILE" down --volumes
            else
                podman compose -f "$COMPOSE_FILE" down --volumes
            fi
            podman image prune -af
            print_status "✅ Cleanup completed"
        fi
        ;;
    help)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
