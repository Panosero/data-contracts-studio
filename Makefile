.PHONY: help install dev build test clean docker-build docker-up docker-down backend-dev frontend-dev deploy deploy-pages deploy-server version release

# Default target
help:
	@echo "Data Contracts Studio - Development Commands"
	@echo "============================================="
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make dev       - Install dependencies and start development servers"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  install        - Install all dependencies (backend + frontend)"
	@echo "  install-backend - Install only backend dependencies"
	@echo "  install-frontend - Install only frontend dependencies"
	@echo "  check-deps     - Check if dependencies are installed"
	@echo "  clean          - Clean build artifacts and caches"
	@echo ""
	@echo "🔧 Development:"
	@echo "  dev            - Install dependencies and start both servers"
	@echo "  backend-dev    - Start backend server (auto-installs if needed)"
	@echo "  frontend-dev   - Start frontend server (auto-installs if needed)"
	@echo ""
	@echo "🧪 Testing:"
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
	@echo "📋 Versioning & Release:"
	@echo "  version        - Show current version"
	@echo "  release        - Create a new release (usage: make release VERSION=0.0.2)"
	@echo ""
	@echo "CI/CD & Deployment:"
	@echo "  deploy         - Simple deployment using .env file"
	@echo "  deploy-pages   - Deploy frontend to GitHub Pages"
	@echo "  deploy-server  - Deploy to server without Docker"
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
dev: install
	@echo "🚀 Starting development environment..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@make -j2 backend-dev frontend-dev

backend-dev:
	@echo "🐍 Starting backend development server..."
	@if [ ! -d "backend/venv" ]; then \
		echo "🔧 Backend virtual environment not found. Installing..."; \
		make install-backend; \
	fi
	cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	@echo "⚛️  Starting frontend development server..."
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "🔧 Frontend dependencies not found. Installing..."; \
		make install-frontend; \
	fi
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

deploy:
	@echo "🚀 Deploying Data Contracts Studio..."
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh

deploy-pages:
	@echo "📦 Deploying to GitHub Pages..."
	chmod +x scripts/deploy-github-pages.sh
	./scripts/deploy-github-pages.sh

deploy-server:
	@echo "🚀 Deploying to server without Docker..."
	chmod +x scripts/deploy-server.sh
	sudo ./scripts/deploy-server.sh

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

# Check status of dependencies
check-deps:
	@echo "🔍 Checking dependencies status..."
	@if [ -d "backend/venv" ]; then \
		echo "✅ Backend virtual environment: Found"; \
	else \
		echo "❌ Backend virtual environment: Missing (run 'make install-backend')"; \
	fi
	@if [ -d "frontend/node_modules" ]; then \
		echo "✅ Frontend dependencies: Found"; \
	else \
		echo "❌ Frontend dependencies: Missing (run 'make install-frontend')"; \
	fi
	@if [ -f "backend/data_contracts.db" ]; then \
		echo "✅ Database: Found"; \
	else \
		echo "⚠️  Database: Not initialized (will be created automatically)"; \
	fi

# Version and Release Management
version:
	@echo "📋 Data Contracts Studio Version Information"
	@echo "============================================="
	@echo "Current Version: $(shell cat VERSION)"
	@echo ""
	@echo "Component Versions:"
	@echo "- Root Package:     $(shell grep '"version"' package.json | head -1 | cut -d'"' -f4)"
	@echo "- Frontend:         $(shell grep '"version"' frontend/package.json | head -1 | cut -d'"' -f4)"
	@echo "- Backend API:      $(shell grep 'app_version:' backend/app/core/config.py | cut -d'"' -f2)"
	@echo ""
	@echo "Git Information:"
	@echo "- Branch:           $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "- Last Commit:      $(shell git log -1 --pretty=format:'%h - %s (%cr)' 2>/dev/null || echo 'No git history')"
	@echo "- Tags:             $(shell git tag --sort=-version:refname | head -3 | tr '\n' ' ' 2>/dev/null || echo 'No tags')"

release:
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ VERSION is required. Usage: make release VERSION=0.0.2"; \
		exit 1; \
	fi
	@echo "🚀 Creating release $(VERSION)..."
	chmod +x scripts/release.sh
	./scripts/release.sh $(VERSION)
