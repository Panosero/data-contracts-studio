# Data Contracts Studio - Backend

A modern, scalable data contract management platform backend built with FastAPI and Python.

## 🏗️ Architecture

```
backend/
├── app/                    # Main application code
│   ├── api/               # API routes and endpoints
│   ├── core/              # Core configuration and settings
│   ├── models/            # SQLAlchemy database models
│   ├── schemas/           # Pydantic schemas for validation
│   ├── services/          # Business logic layer
│   └── utils/             # Utility functions
├── alembic/               # Database migrations
├── data/                  # Database files (local development)
├── docs/                  # Backend-specific documentation
├── scripts/               # Utility scripts
│   └── migration/         # Migration scripts
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── utils/                 # Standalone utilities
├── main.py               # FastAPI application entry point
├── pyproject.toml        # Python project configuration
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip or poetry for package management

### Development Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or for development with all tools:
   pip install -e ".[dev]"
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start development server:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

## 🧪 Testing

### Run All Tests
```bash
# Using the test runner script
python scripts/run_tests.py

# Using pytest directly
python -m pytest tests/
```

### Test Categories
```bash
# Unit tests only
python scripts/run_tests.py --type unit

# Integration tests only  
python scripts/run_tests.py --type integration

# Code quality checks
python scripts/run_tests.py --type lint

# Type checking
python scripts/run_tests.py --type mypy
```

### Coverage Reports
```bash
# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 🔧 Code Quality

### Formatting and Linting
```bash
# Format code
python -m black app tests scripts
python -m isort app tests scripts

# Lint code
python -m flake8 app tests scripts

# Type checking
python -m mypy app
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 📊 Database

### Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Database Schema
The application uses SQLAlchemy ORM with the following main models:
- `DataContract`: Core data contract entity
- Additional models in `app/models/`

## 🔌 API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /version` - Version information
- `GET /api/v1/version` - API version information

### Data Contracts
- `GET /api/v1/contracts` - List all contracts
- `POST /api/v1/contracts` - Create new contract
- `GET /api/v1/contracts/{id}` - Get contract by ID
- `PUT /api/v1/contracts/{id}` - Update contract
- `DELETE /api/v1/contracts/{id}` - Delete contract

## 🛠️ Development Tools

### Scripts
- `scripts/run_tests.py` - Comprehensive test runner
- `scripts/migration/` - Database migration utilities
- `utils/debug_sanitize.py` - Debug utilities

### Configuration
- `pyproject.toml` - Python project configuration with tools setup
- `alembic.ini` - Database migration configuration
- `.flake8` - Flake8 linting configuration

## 📝 Best Practices

### Code Style
- **Line length**: 100 characters
- **Formatting**: Black with isort for imports
- **Type hints**: Required for all public functions
- **Docstrings**: Google-style docstrings for all modules, classes, and functions

### Testing Strategy
- **Unit tests**: Test individual functions and classes in isolation
- **Integration tests**: Test API endpoints and database interactions
- **Coverage target**: Minimum 80% code coverage
- **Test markers**: Use `@pytest.mark.unit` and `@pytest.mark.integration`

### Project Structure
- Follow **SOLID principles** for clean architecture
- Use **dependency injection** where appropriate
- Keep business logic in **service layer**
- Maintain **clear separation** between API, business logic, and data layers

## 🔄 Deployment

### Environment Variables
Key environment variables (see `.env.example`):
- `DATABASE_URL` - Database connection string
- `DEBUG` - Development mode flag
- `SECRET_KEY` - Application secret key

### Production Deployment
1. Build Docker image: `docker build -t data-contracts-backend .`
2. Set production environment variables
3. Run database migrations
4. Start application with production WSGI server

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

1. Follow the code style guidelines
2. Write tests for new functionality
3. Update documentation as needed
4. Run the full test suite before committing
5. Use meaningful commit messages

---

For more information, see the main project README in the repository root.
