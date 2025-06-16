# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2025-06-16

### Added
- Initial release of Data Contracts Studio
- React frontend with TypeScript support
- FastAPI backend with Python 3.9+
- SQLite database with Alembic migrations
- Docker containerization for both frontend and backend
- Contract management API endpoints
- Auto-generation service for contracts from:
  - Database schemas
  - API responses
  - File uploads (CSV/JSON)
- Modern UI with Tailwind CSS
- Comprehensive test suite
- Development and production deployment scripts
- CORS configuration for cross-origin requests
- Health check endpoints
- Linting and formatting tools
- Documentation and examples

### Technical Details
- **Frontend**: React 18.2+, TypeScript, Tailwind CSS, React Query, React Hook Form
- **Backend**: FastAPI 0.104+, SQLAlchemy 2.0+, Alembic, Pydantic
- **Database**: SQLite (development), PostgreSQL ready
- **Testing**: Jest (frontend), Pytest (backend)
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions ready
- **Deployment**: Production-ready with Nginx

### Security
- JWT authentication infrastructure
- CORS protection
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM

[Unreleased]: https://github.com/Panosero/data-contracts-studio/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/Panosero/data-contracts-studio/releases/tag/v0.0.1
