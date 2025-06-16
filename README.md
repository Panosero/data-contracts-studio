# Data Contracts Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/github/v/release/Panosero/data-contracts-studio?sort=semver&display_name=tag&label=Version)](https://github.com/Panosero/data-contracts-studio/releases)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-007ACC.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Ready-green.svg)](#-production-deployment)

A modern, scalable data contract management platform built with React and FastAPI, following industry best practices and clean architecture principles.

## 📸 Screenshots

### Main Dashboard

*Contract management dashboard with search and filtering capabilities*
![main_dash](/docs/images/main_dash.png)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd data-contracts-studio

# Deploy with Docker (recommended)
make deploy

# Or start development environment
make dev
```

**🎯 That's it!** Your application will be running and ready to use.

## 🚀 Features

- **🎯 Modern Architecture**: Separate frontend (React + TypeScript) and backend (FastAPI + Python)
- **🤖 Auto-Generation**: Generate contracts from database schemas, API responses, and file uploads
- **📁 File Upload**: Drag & drop interface for CSV and JSON files with automatic parsing and type detection
- **🔍 Real-time Search**: Filter and search contracts with instant results
- **🛡️ Type Safety**: Full TypeScript support with comprehensive type definitions
- **📱 Responsive Design**: Mobile-first design with Tailwind CSS and dark mode
- **🐳 Production Ready**: Docker support, environment management, and deployment scripts
- **⚡ Performance**: Optimized builds, lazy loading, and efficient state management
- **🔒 Security**: Environment-based configuration with secure secret management

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **State Management**: React Query for server state
- **Forms**: React Hook Form with validation
- **Styling**: Tailwind CSS with custom design system
- **Routing**: React Router v6
- **Build Tool**: Create React App with optimizations

### Backend (FastAPI + Python)
- **Framework**: FastAPI with async support
- **Database**: SQLAlchemy with Alembic migrations
- **Validation**: Pydantic models with type validation
- **Architecture**: Clean architecture with services and repositories
- **API Documentation**: Auto-generated OpenAPI/Swagger docs


## Auto-Generation Features

The Data Contract Portal's auto-generation feature is designed to streamline the contract creation process by analyzing existing data sources and automatically inferring schema structures.

### Database Schema Import

**Purpose**: Convert SQL database schemas into standardized data contracts.

**How it works**:
1. **Schema Parsing**: The system parses SQL DDL statements to extract table structure
2. **Type Mapping**: SQL data types are automatically mapped to contract data types
3. **Constraint Detection**: NOT NULL constraints are converted to required field indicators
4. **Field Analysis**: Each column becomes a contract field with appropriate metadata

**Supported SQL Types**:
```sql
VARCHAR/TEXT     → string
INT/INTEGER      → integer
BOOLEAN          → boolean
TIMESTAMP        → timestamp
FLOAT/DECIMAL    → float
```

**Example Usage**:
```sql
-- Input Schema
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generated Contract
{
    "id": "integer",
    "name": "string",
    "email": "string",
    "created_at": "timestamp"
}
```

### API Response Import

**Purpose**: Generate contracts from existing API responses.

**How it works**:
1. **Sample Collection**: The system collects sample responses from API endpoints
2. **Schema Inference**: Analyzes JSON structure to infer field types and constraints
3. **Contract Generation**: Creates a contract schema based on inferred data

**Example Usage**:
```http
GET /api/v1/customers/1 HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>

-- Sample Response
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "created_at": "2023-01-01T12:00:00Z"
}

-- Generated Contract
{
    "id": "integer",
    "name": "string",
    "email": "string",
    "created_at": "timestamp"
}
```

### CSV/JSON File Import

**Purpose**: Allow contract generation from CSV or JSON files.

**How it works**:
1. **File Upload**: Users upload CSV or JSON files
2. **Format Detection**: The system detects file format and parses content
3. **Schema Creation**: Generates a contract schema based on file content

**Example Usage**:
```csv
id,name,email,created_at
1,John Doe,john.doe@example.com,2023-01-01 12:00:00
2,Jane Smith,jane.smith@example.com,2023-01-02 12:00:00

-- Generated Contract
{
    "id": "integer",
    "name": "string",
    "email": "string",
    "created_at": "timestamp"
}
```

## 📁 Project Structure

```
data-contracts-studio/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core functionality (config, database)
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── main.py                # Application entry point
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── types/             # TypeScript type definitions
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   └── package.json           # Node dependencies
├── docker-compose.yml         # Docker composition
├── docs/                      # Documentation
├── scripts/                   # Deployment and utility scripts
└── Makefile                   # Development commands
```

## 🛠️ Development Setup

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd data-contracts-studio
   ```

2. **Run the setup script**:
   ```bash
   chmod +x scripts/setup-dev.sh
   ./scripts/setup-dev.sh
   ```

3. **Start development environment**:
   ```bash
   make dev
   # or
   ./run-dev.sh
   ```

### Manual Setup

#### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+
- Git

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**:
   ```bash
   make db-init
   ```

6. **Start development server**:
   ```bash
   make backend-dev
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server**:
   ```bash
   make frontend-dev
   ```

### Available Commands

```bash
make help           # Show all available commands
make install        # Install all dependencies
make dev            # Start development environment
make test           # Run all tests
make lint           # Run code linting (flake8 + eslint)
make format         # Format code (Black + Prettier)
make build          # Build for production
make docker-up      # Start with Docker
make clean          # Clean build artifacts
```

### Code Style & Formatting

This project uses **Black** formatter with a **100-character line length**:

```bash
# Format all code (Python with Black, TypeScript with Prettier)
make format

# Check code style and linting
make lint

# Backend only formatting
cd backend && black app && isort app

# Frontend only formatting  
cd frontend && npm run format
```

**Configuration:**
- Python: Black formatter (100 chars), isort for imports, flake8 for linting
- TypeScript: Prettier formatter, ESLint for linting
- Line length: 100 characters for both Python and TypeScript

## ⚙️ Configuration (.env file)

### Simple Configuration with .env

All configuration is done through a single `.env` file:

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Edit with your settings
nano .env

# 3. Deploy
make deploy
```

### Key Configuration Options

```bash
# Server settings
SERVER_IP=192.168.1.100        # Your server IP (or auto-detect)
FRONTEND_PORT=80               # Web interface port
BACKEND_PORT=8888             # API port
DATABASE_PORT=5432            # Database port

# Secrets (keep secure!)
POSTGRES_PASSWORD=your-secure-db-password
SECRET_KEY=your-secure-secret-key

# API Keys for LLM features
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### Common Scenarios

**Standard server:**
```bash
SERVER_IP=192.168.1.100
FRONTEND_PORT=80
BACKEND_PORT=8888
```

**Shared server (avoid port conflicts):**
```bash
SERVER_IP=192.168.1.100
FRONTEND_PORT=8080
BACKEND_PORT=8001
DATABASE_PORT=5433
```

**Custom domain:**
```bash
SERVER_IP=data-contracts.company.com
FRONTEND_PORT=80
BACKEND_PORT=8888
```

## 🚀 Production Deployment

### Simple Deployment (Recommended)

1. **Quick deployment**:
   ```bash
   git clone <repo>
   cd data-contracts-studio
   make deploy
   ```
   
   The script will:
   - Create `.env` file if it doesn't exist
   - Auto-detect your server IP
   - Generate secure passwords and keys
   - Start Docker containers

2. **Custom configuration**:
   ```bash
   git clone <repo>
   cd data-contracts-studio
   cp .env.example .env
   # Edit .env with your settings
   nano .env
   make deploy
   ```
   
   # Deploy
   docker-compose up -d --build
   ```

## 🦭 Podman Deployment (Rootless Containers)

**Podman** is a secure, rootless alternative to Docker that's especially popular in enterprise environments and security-conscious deployments.

### Why Choose Podman?

- **🔒 Rootless**: Runs without root privileges for enhanced security
- **🏢 Enterprise-Ready**: Preferred by many organizations for production
- **⚡ Fast**: Lightweight container runtime without daemon
- **🔄 Compatible**: Drop-in replacement for most Docker commands
- **🛡️ Secure**: Better isolation and security by default

### Prerequisites

#### Install Podman

**macOS** (via Homebrew):
```bash
brew install podman
podman machine init
podman machine start
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install podman podman-compose
```

**CentOS/RHEL/Fedora**:
```bash
sudo dnf install podman podman-compose
```

**Verify Installation**:
```bash
podman --version
podman-compose --version
```

### Podman Deployment Options

#### 1. Development Environment
Perfect for local development with hot-reload and debugging:

```bash
# Start development environment
podman-compose -f podman-compose.dev.yml --env-file .env.dev up -d --build

# View logs
podman-compose -f podman-compose.dev.yml logs -f

# Stop environment
podman-compose -f podman-compose.dev.yml down
```

**Features:**
- ✅ React hot-reload on port 3333
- ✅ FastAPI auto-reload on port 8888
- ✅ SQLite database (no PostgreSQL needed)
- ✅ Volume mounts for live code editing
- ✅ Development debugging enabled

#### 2. Test Environment
Mimics production but with test data and configurations:

```bash
# Start test environment
podman-compose -f podman-compose.test.yml --env-file .env.test up -d --build

# Run tests
podman-compose -f podman-compose.test.yml exec backend pytest
podman-compose -f podman-compose.test.yml exec frontend npm test

# Stop environment
podman-compose -f podman-compose.test.yml down
```

**Features:**
- ✅ Production-like PostgreSQL database
- ✅ Optimized production builds
- ✅ Test data and configurations
- ✅ Health checks and monitoring

#### 3. Production Environment
Full production deployment with security and performance optimizations:

```bash
# Configure production environment
cp .env.podman.template .env.prod
nano .env.prod  # Edit with your production settings

# Deploy to production
podman-compose -f podman-compose.yml --env-file .env.prod up -d --build

# Monitor deployment
podman-compose -f podman-compose.yml ps
podman-compose -f podman-compose.yml logs
```

**Features:**
- ✅ PostgreSQL database with persistence
- ✅ Nginx reverse proxy
- ✅ Production optimizations
- ✅ Health checks and restart policies
- ✅ Secure networking and isolation

### Environment Configuration Files

The project includes pre-configured environment files for different deployment scenarios:

| File | Purpose | Database | Features |
|------|---------|----------|----------|
| `.env.dev` | Development | SQLite | Hot-reload, debugging |
| `.env.test` | Testing | PostgreSQL | Test data, CI/CD |
| `.env.prod` | Production | PostgreSQL | Security, performance |

### Podman Basic Commands

#### Container Management
```bash
# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# View container logs
podman logs <container-name>

# Execute command in container
podman exec -it <container-name> /bin/bash

# Stop container
podman stop <container-name>

# Remove container
podman rm <container-name>
```

#### Image Management
```bash
# List images
podman images

# Remove image
podman rmi <image-name>

# Build image
podman build -t my-app .

# Pull image from registry
podman pull registry.redhat.io/ubi8/ubi
```

#### Compose Operations
```bash
# Start services in background
podman-compose up -d

# Start services with build
podman-compose up -d --build

# View service status
podman-compose ps

# View logs for all services
podman-compose logs

# View logs for specific service
podman-compose logs frontend

# Stop all services
podman-compose down

# Stop and remove volumes
podman-compose down -v
```

### Debugging and Troubleshooting

#### Common Issues and Solutions

**1. Permission Denied Errors**
```bash
# Fix rootless permissions
podman unshare chown -R $(id -u):$(id -g) ./data
```

**2. Port Already in Use**
```bash
# Find process using port
lsof -i :8888
# Kill process or change port in compose file
```

**3. Container Won't Start**
```bash
# Check container logs
podman logs <container-name>

# Check system resources
podman system info

# Check for image issues
podman inspect <image-name>
```

**4. Database Connection Issues**
```bash
# Check database container status
podman-compose ps db

# Connect to database directly
podman-compose exec db psql -U postgres -d datacontracts

# Check database logs
podman-compose logs db
```

#### Debugging Commands

**Container Inspection:**
```bash
# Inspect running container
podman inspect <container-name>

# Check container processes
podman top <container-name>

# Monitor container stats
podman stats <container-name>
```

**Network Debugging:**
```bash
# List networks
podman network ls

# Inspect network
podman network inspect <network-name>

# Test connectivity between containers
podman exec frontend ping backend
```

**Volume Management:**
```bash
# List volumes
podman volume ls

# Inspect volume
podman volume inspect <volume-name>

# Backup volume data
podman run --rm -v <volume-name>:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .
```

#### Performance Monitoring

```bash
# System-wide stats
podman system info

# Container resource usage
podman stats

# Check image sizes
podman images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Clean up unused resources
podman system prune -a
```

#### Development Workflow

**Hot Development Cycle:**
```bash
# 1. Start development environment
podman-compose -f podman-compose.dev.yml --env-file .env.dev up -d

# 2. Make code changes (auto-reloads)
# Edit files in ./frontend/src or ./backend/app

# 3. View logs for debugging
podman-compose -f podman-compose.dev.yml logs -f frontend
podman-compose -f podman-compose.dev.yml logs -f backend

# 4. Run tests
podman-compose -f podman-compose.dev.yml exec backend pytest
podman-compose -f podman-compose.dev.yml exec frontend npm test

# 5. Clean shutdown
podman-compose -f podman-compose.dev.yml down
```

**Production Deployment Cycle:**
```bash
# 1. Test locally first
podman-compose -f podman-compose.test.yml --env-file .env.test up -d --build

# 2. Deploy to production
podman-compose -f podman-compose.yml --env-file .env.prod up -d --build

# 3. Monitor deployment
watch "podman-compose -f podman-compose.yml ps"

# 4. Check health
curl http://localhost:8888/health
curl http://localhost:3333

# 5. View production logs
podman-compose -f podman-compose.yml logs -f
```

### Security Best Practices

#### Rootless Security
```bash
# Always run rootless (automatically enabled)
podman info | grep -i rootless

# Check user namespaces
podman unshare cat /proc/self/uid_map
```

#### Network Security
```bash
# Use custom networks
podman network create app-network

# Limit container communication
# Edit compose files to use specific networks
```

#### Secret Management
```bash
# Never commit secrets to version control
echo "*.env" >> .gitignore
echo ".env.*" >> .gitignore

# Use environment files
cp .env.podman.template .env.prod
chmod 600 .env.prod  # Restrict permissions
```

### Migration from Docker

**For Docker users, Podman is nearly identical:**

```bash
# Replace docker commands with podman
alias docker='podman'
alias docker-compose='podman-compose'

# Most Docker commands work unchanged:
podman run hello-world
podman build -t myapp .
podman-compose up -d
```

**Key Differences:**
- No daemon required (faster startup)
- Rootless by default (more secure)
- Pod support (Kubernetes-like grouping)
- Better integration with systemd

### Server Deployment without Containers

For direct server deployment:

```bash
sudo ./scripts/deploy-server.sh
```

### Manual Deployment

#### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
export ALLOWED_ORIGINS='["http://YOUR_SERVER_IP"]'
make db-migrate
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8888
```

#### Frontend Deployment
```bash
cd frontend
npm install
REACT_APP_API_URL=http://YOUR_SERVER_IP:8888/api/v1 npm run build
# Serve the build folder with your preferred web server (nginx, apache, etc.)
```

## 🚀 Deployment Options

### Quick Deployment

| Platform               | Type          | Command                           | Best For       | Access Method              |
| ---------------------- | ------------- | --------------------------------- | -------------- | -------------------------- |
| **Docker**             | Full Stack    | `./scripts/deploy.sh`             | Production     | http://SERVER_IP           |
| **Server (No Docker)** | Full Stack    | `sudo ./scripts/deploy-server.sh` | Production     | http://SERVER_IP           |
| **GitHub Pages**       | Frontend Only | `make deploy-pages`               | Demo/Portfolio | https://username.github.io |

### IP-Based Deployment Features

✅ **Automatic IP Detection**: Scripts automatically detect your server's public IP  
✅ **No Domain Required**: Access via `http://YOUR_SERVER_IP`  
✅ **CORS Configuration**: Properly configured for cross-origin requests  
✅ **Firewall Instructions**: Clear guidance on required ports  
✅ **SSL Optional**: Can be added later if you get a domain  

### Detailed Deployment

See the [Deployment Guide](docs/deployment/README.md) for comprehensive instructions covering:

- 🌐 **IP-Based Access**: No domain configuration needed
- 🏢 **Company Servers**: Full production deployment  
- ☁️ **Cloud Platforms**: Heroku, Vercel, Railway
- 🐳 **Docker**: Containerized deployment
- 🔄 **CI/CD**: Automated deployments

### GitHub Pages Setup (Frontend Demo)

```bash
# Deploy frontend to GitHub Pages
make deploy-pages

# Your site will be available at:
# https://username.github.io/data-contracts-studio
```

### Company Server Setup (Full Production)

```bash
# Deploy to your company server (requires sudo access)
make deploy-server

# Sets up:
# - Python backend with Gunicorn + Supervisor
# - React frontend with Nginx
# - SSL certificates (optional)
# - Monitoring and log rotation
```

### Docker Deployment (Any Environment)

```bash
# Development
docker-compose -f docker-compose.dev.yml up --build

# Production
make docker-up
```

## 🔄 CI/CD Integration

The project includes pre-configured CI/CD pipelines:

- **GitHub Actions**: `.github/workflows/ci-cd.yml`
- **GitLab CI**: `.gitlab-ci.yml`

**Features:**
- ✅ Automated testing (backend + frontend)
- ✅ Security scanning
- ✅ Docker image building
- ✅ Deployment to GitHub Pages
- ✅ Server deployment via SSH

**Setup:**
```bash
make setup-ci  # Shows required secrets/variables
```

## 🌐 Environment Configuration

### Development
```bash
# Backend
DATABASE_URL=sqlite:///./data_contracts.db
DEBUG=True
SECRET_KEY=dev-secret-key

# Frontend  
REACT_APP_API_URL=http://localhost:8888/api/v1
```

### Production
```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/db
DEBUG=False
SECRET_KEY=your-secure-secret-key

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com/api/v1
```

## 📚 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8888/docs
- **ReDoc**: http://localhost:8888/redoc

### Key Endpoints

- `GET /api/v1/contracts` - List all contracts
- `POST /api/v1/contracts` - Create a new contract
- `GET /api/v1/contracts/{id}` - Get contract by ID
- `PUT /api/v1/contracts/{id}` - Update contract
- `DELETE /api/v1/contracts/{id}` - Delete contract
- `POST /api/v1/contracts/auto-generate` - Auto-generate from source

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DEBUG=False
DATABASE_URL=sqlite:///./data_contracts.db
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:3333"]
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8888/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
```

## 🎨 Design System

The application uses a consistent design system built with Tailwind CSS:

- **Colors**: Green-based palette for primary actions
- **Typography**: Clean, readable font hierarchy
- **Components**: Reusable UI components with consistent styling
- **Animations**: Subtle animations for better UX

## 🔒 Security Features

- **Input Validation**: Pydantic models with strict validation
- **CORS Protection**: Configurable CORS settings
- **SQL Injection Prevention**: SQLAlchemy ORM usage
- **XSS Protection**: React's built-in XSS prevention
- **Environment Security**: Sensitive data in environment variables

## 📈 Performance Optimizations

- **Frontend**: React Query for caching, code splitting, lazy loading
- **Backend**: Async FastAPI, database connection pooling
- **Database**: Proper indexing, optimized queries
- **Build**: Production optimizations, minification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

---

Built with ❤️ using modern web technologies and best practices.
