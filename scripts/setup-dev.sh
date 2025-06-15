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

# Setup backend
setup_backend() {
    print_status "Setting up backend..."

    cd backend

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt

    # Copy environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cp .env.example .env 2>/dev/null || echo "DEBUG=True
DATABASE_URL=sqlite:///./data_contracts.db
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_ORIGINS=[\"http://localhost:3000\"]" >.env
    fi

    # Initialize database
    print_status "Initializing database..."
    python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

    cd ..
    print_status "Backend setup complete ✓"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."

    cd frontend

    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install

    # Copy environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cp .env.example .env 2>/dev/null || echo "REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
REACT_APP_VERSION=1.0.0" >.env
    fi

    cd ..
    print_status "Frontend setup complete ✓"
}

# Create run scripts
create_run_scripts() {
    print_status "Creating run scripts..."

    # Backend run script
    cat >run-backend.sh <<'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF
    chmod +x run-backend.sh

    # Frontend run script
    cat >run-frontend.sh <<'EOF'
#!/bin/bash
cd frontend
npm start
EOF
    chmod +x run-frontend.sh

    # Combined run script
    cat >run-dev.sh <<'EOF'
#!/bin/bash
echo "Starting Data Contracts Studio in development mode..."
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Start backend in background
./run-backend.sh &
BACKEND_PID=$!

# Start frontend in background
./run-frontend.sh &
FRONTEND_PID=$!

# Wait for user to press Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
    chmod +x run-dev.sh

    print_status "Run scripts created ✓"
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
    echo "To start the development environment:"
    echo "  ./run-dev.sh          # Start both frontend and backend"
    echo "  ./run-backend.sh      # Start only backend"
    echo "  ./run-frontend.sh     # Start only frontend"
    echo ""
    echo "URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
}

main "$@"
