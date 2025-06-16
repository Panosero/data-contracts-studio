#!/bin/bash

# Data Contracts Studio - Development Setup Script
# This script sets up the development environment for both frontend and backend

set -e

echo "🚀 Setting up Data Contracts Studio development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."

    if ! command -v python3 &>/dev/null; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi

    if ! command -v node &>/dev/null; then
        print_error "Node.js is required but not installed."
        exit 1
    fi

    if ! command -v npm &>/dev/null; then
        print_error "npm is required but not installed."
        exit 1
    fi

    print_status "All requirements satisfied ✓"
}

# Setup backend using Makefile
setup_backend() {
    print_status "Setting up backend using Makefile..."

    # Use Makefile to install backend dependencies
    make install-backend

    # Copy environment file if it doesn't exist
    if [ ! -f "backend/.env" ]; then
        print_status "Creating backend .env file..."
        echo "DEBUG=True
DATABASE_URL=sqlite:///./data_contracts.db
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_ORIGINS=[\"http://localhost:3333\"]" >backend/.env
    fi

    # Initialize database using Makefile
    make db-init 2>/dev/null || {
        print_warning "Database initialization failed, trying manual setup..."
        cd backend
        source venv/bin/activate
        python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
        cd ..
    }

    print_status "Backend setup complete ✓"
}

# Setup frontend using Makefile
setup_frontend() {
    print_status "Setting up frontend using Makefile..."

    # Use Makefile to install frontend dependencies
    make install-frontend

    # Copy environment file if it doesn't exist
    if [ ! -f "frontend/.env" ]; then
        print_status "Creating frontend .env file..."
        echo "REACT_APP_API_URL=http://localhost:8888/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
REACT_APP_VERSION=1.0.0" >frontend/.env
    fi

    print_status "Frontend setup complete ✓"
}

# Create run scripts that use Makefile
create_run_scripts() {
    print_status "Creating run scripts that leverage Makefile..."

    # Backend run script - uses Makefile
    cat >run-backend.sh <<'EOF'
#!/bin/bash
echo "🐍 Starting backend using Makefile..."
make backend-dev
EOF
    chmod +x run-backend.sh

    # Frontend run script - uses Makefile
    cat >run-frontend.sh <<'EOF'
#!/bin/bash
echo "⚛️ Starting frontend using Makefile..."
make frontend-dev
EOF
    chmod +x run-frontend.sh

    # Combined run script - uses Makefile
    cat >run-dev.sh <<'EOF'
#!/bin/bash
echo "🚀 Starting Data Contracts Studio using Makefile..."
echo "Backend will be available at: http://localhost:8888"
echo "Frontend will be available at: http://localhost:3333"
echo "API Documentation: http://localhost:8888/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Use Makefile's dev command which runs both services
make dev
EOF
    chmod +x run-dev.sh

    print_status "Run scripts created (using Makefile) ✓"
}

# Main setup process
main() {
    print_status "Starting setup process..."

    check_requirements
    setup_backend
    setup_frontend
    create_run_scripts

    print_status "Setup complete! 🎉"
    echo ""
    echo "🚀 Super Quick Start:"
    echo "  make dev               # Install everything and start development"
    echo ""
    echo "🎯 Individual commands:"
    echo "  make backend-dev       # Start backend (auto-installs if needed)"
    echo "  make frontend-dev      # Start frontend (auto-installs if needed)"
    echo ""
    echo "📁 Alternative convenience scripts:"
    echo "  ./run-dev.sh          # Uses 'make dev'"
    echo "  ./run-backend.sh      # Uses 'make backend-dev'"
    echo "  ./run-frontend.sh     # Uses 'make frontend-dev'"
    echo ""
    echo "🔧 Other useful commands:"
    echo "  make test             # Run all tests"
    echo "  make lint             # Run linting"
    echo "  make clean            # Clean build artifacts"
    echo "  make help             # See all available commands"
    echo ""
    echo "🌍 URLs (when running):"
    echo "  Frontend: http://localhost:3333"
    echo "  Backend:  http://localhost:8888"
    echo "  API Docs: http://localhost:8888/docs"
}

main "$@"
