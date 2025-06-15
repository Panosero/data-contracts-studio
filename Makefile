.PHONY: help install dev build test clean docker-build docker-up docker-down backend-dev frontend-dev

# Default target
help:
	@echo "Data Contracts Studio - Development Commands"
	@echo "============================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  install        - Install all dependencies (backend + frontend)"
	@echo "  clean          - Clean build artifacts and caches"
	@echo ""
	@echo "Development:"
	@echo "  dev            - Start both backend and frontend in development mode"
	@echo "  backend-dev    - Start only backend in development mode"
	@echo "  frontend-dev   - Start only frontend in development mode"
	@echo ""
	@echo "Testing:"
	@echo "  test           - Run all tests (backend + frontend)"
	@echo "  test-backend   - Run backend tests only"
	@echo "  test-frontend  - Run frontend tests only"
	@echo ""
	@echo "Building:"
	@echo "  build          - Build production versions of both apps"
	@echo "  build-backend  - Build backend only"
	@echo "  build-frontend - Build frontend only"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   - Build Docker images"
	@echo "  docker-up      - Start application with Docker Compose"
	@echo "  docker-down    - Stop Docker Compose services"
	@echo "  docker-dev     - Start development environment with Docker"
	@echo ""
	@echo "CI/CD & Deployment:"
	@echo "  ci-test        - Run CI tests (linting + unit tests)"
	@echo "  deploy-pages   - Deploy frontend to GitHub Pages"
	@echo "  deploy-server   - Deploy backend to server"
	@echo "  setup-ci       - Set up CI/CD configuration"

# Installation
install: install-backend install-frontend
	@echo "✅ All dependencies installed"

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Backend dependencies installed"

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

# Development
dev:
	@echo "🚀 Starting development environment..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@make -j2 backend-dev frontend-dev

backend-dev:
	@echo "🐍 Starting backend development server..."
	cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	@echo "⚛️  Starting frontend development server..."
	cd frontend && npm start

# Testing
test: test-backend test-frontend
	@echo "✅ All tests completed"

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && source venv/bin/activate && pytest

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false

# Building
build: build-backend build-frontend
	@echo "✅ Production build completed"

build-backend:
	@echo "🏗️ Building backend..."
	cd backend && source venv/bin/activate && python -m build

build-frontend:
	@echo "🏗️ Building frontend..."
	cd frontend && npm run build

# Docker
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting application with Docker Compose..."
	docker-compose up -d
	@echo "✅ Application started"
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost:8000"

docker-down:
	@echo "🐳 Stopping Docker Compose services..."
	docker-compose down

docker-dev:
	@echo "🐳 Starting development environment with Docker..."
	docker-compose -f docker-compose.dev.yml up --build

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	cd backend && rm -rf __pycache__ .pytest_cache build dist *.egg-info
	cd frontend && rm -rf node_modules build coverage
	docker system prune -f
	@echo "✅ Cleanup completed"

# Database
db-init:
	@echo "🗄️ Initializing database..."
	cd backend && source venv/bin/activate && python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
	@echo "✅ Database initialized"

db-migrate:
	@echo "🗄️ Running database migrations..."
	cd backend && source venv/bin/activate && alembic upgrade head
	@echo "✅ Database migrations completed"

# Linting and formatting
lint:
	@echo "🔍 Running linting..."
	cd backend && source venv/bin/activate && flake8 app
	cd frontend && npm run lint
	@echo "✅ Linting completed"

format:
	@echo "✨ Formatting code..."
	cd backend && source venv/bin/activate && black app && isort app
	cd frontend && npm run format
	@echo "✅ Code formatted"

# Health check
health:
	@echo "🏥 Checking application health..."
	@curl -f http://localhost:8000/health || echo "Backend not responding"
	@curl -f http://localhost:3000 || echo "Frontend not responding"

# CI/CD and Deployment
ci-test:
	@echo "🧪 Running CI tests..."
	make test
	make lint
	@echo "✅ All CI tests passed"

deploy-pages:
	@echo "📦 Deploying to GitHub Pages..."
	chmod +x scripts/deploy-github-pages.sh
	./scripts/deploy-github-pages.sh

deploy-server:
	@echo "🚀 Deploying to server..."
	chmod +x scripts/deploy-server.sh
	./scripts/deploy-server.sh

setup-ci:
	@echo "⚙️ Setting up CI/CD..."
	@echo "GitHub Actions workflow: .github/workflows/ci-cd.yml ✓"
	@echo "GitLab CI configuration: .gitlab-ci.yml ✓"
	@echo ""
	@echo "Next steps:"
	@echo "1. Set up repository secrets:"
	@echo "   - SERVER_HOST, SERVER_USER, SERVER_SSH_KEY"
	@echo "   - REACT_APP_API_URL"
	@echo "2. Enable GitHub Pages in repository settings"
	@echo "3. Configure deployment environments"
