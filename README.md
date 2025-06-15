# Data Contracts Studio - Production Ready

A modern, scalable data contract management platform built with React and FastAPI, following industry best practices and clean architecture principles.

## 🚀 Features

- **Modern Architecture**: Separate frontend (React + TypeScript) and backend (FastAPI + Python)
- **Auto-Generation**: Generate contracts from database schemas, API responses, and CSV/JSON files
- **Real-time Search**: Filter and search contracts with real-time updates
- **Type Safety**: Full TypeScript support with proper type definitions
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Production Ready**: Docker support, environment management, and CI/CD ready

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

3. **Direct Usage**:
   - Download the `index.html` file
   - Open it directly in your web browser
   - No server setup required

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
make build          # Build for production
make docker-up      # Start with Docker
make clean          # Clean build artifacts
```

## 🚀 Production Deployment

### Using Docker (Recommended)

1. **Quick deployment**:
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

2. **Manual Docker deployment**:
   ```bash
   make docker-build
   make docker-up
   ```

### Manual Deployment

#### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
make db-migrate
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend Deployment
```bash
cd frontend
npm install
npm run build
# Serve the build folder with your preferred web server (nginx, apache, etc.)
```

## 🚀 Deployment Options

### Quick Deployment

| Platform           | Type          | Command              | Best For        |
| ------------------ | ------------- | -------------------- | --------------- |
| **GitHub Pages**   | Frontend Only | `make deploy-pages`  | Demo/Portfolio  |
| **Company Server** | Full Stack    | `make deploy-server` | Production      |
| **Docker**         | Full Stack    | `make docker-up`     | Any Environment |

### Detailed Deployment

See the [Deployment Guide](docs/deployment/README.md) for comprehensive instructions covering:

- 🌐 **GitHub Pages**: Free frontend hosting
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
REACT_APP_API_URL=http://localhost:8000/api/v1
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
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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
ALLOWED_ORIGINS=["http://localhost:3000"]
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
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
