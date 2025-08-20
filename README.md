# Learning Python - Monorepo

This repository contains multiple Python learning projects organized as a monorepo with intelligent CI/CD pipelines.

## Repository Structure

```
learning-python/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── ci.yml         # Main CI/CD pipeline
│       ├── docker.yml     # Docker build and test
│       └── test-python-module.yml  # Reusable testing workflow
├── banking-api/           # Banking REST API with package-by-feature architecture
├── basics/                # Basic Python learning scripts
└── README.md             # This file
```

## Projects

### 🏦 Banking API
A comprehensive REST API demonstrating clean architecture and package-by-feature organization.
- **Tech Stack**: FastAPI, Pydantic, Docker
- **Architecture**: Package-by-Feature, Repository Pattern, Domain-Driven Design
- **Features**: Account management, transactions, transfers
- **Location**: [`banking-api/`](./banking-api/)

### 📚 Basics
Simple Python scripts for learning basic concepts.
- **Location**: [`basics/`](./basics/)

## CI/CD Strategy

This monorepo uses **intelligent path-based triggers** to optimize CI/CD performance:

### 🎯 Smart Change Detection
- Only runs tests for modules that have changed
- Uses `dorny/paths-filter` action for precise path detection
- Supports both individual module changes and global changes

### 🔄 Workflows Overview

#### 1. **Main CI Pipeline** (`.github/workflows/ci.yml`)
Triggered on: Push to `main`, Pull Requests

**Features:**
- **Change Detection**: Only test modules with changes
- **Python Testing**: Runs on Python 3.13
- **Reusable Workflows**: Uses `test-python-module.yml` for consistency
- **Security Scanning**: Bandit and Safety checks
- **Integration Tests**: API endpoint testing

#### 2. **Docker Pipeline** (`.github/workflows/docker.yml`)
Triggered on: Changes to modules with Docker support

**Features:**
- **Docker builds**: For modules with Docker support
- **Container Testing**: Health checks and API validation
- **Docker Compose Testing**: Full stack validation

#### 3. **Reusable Testing** (`.github/workflows/test-python-module.yml`)
Called by other workflows for consistent testing

**Features:**
- **Parameterized Testing**: Configurable Python versions and test commands
- **Comprehensive Checks**: Linting, formatting, type checking, testing
- **Caching**: Intelligent pip dependency caching
- **Flexible**: Adapts to different module structures

### 🏷️ Release Strategy

#### Module-Specific Releases
```bash
# Release banking-api version 1.2.0
git tag banking-api-v1.2.0
git push origin banking-api-v1.2.0
```

#### Global Releases
```bash
# Release all modules as version 1.0.0
git tag v1.0.0
git push origin v1.0.0
```

### 🔧 Module Requirements

For a module to be fully supported by the CI/CD pipeline:

#### ✅ **Minimum Requirements**
- Python files (`.py`)
- At least one of: `requirements.txt`, test files, or `Dockerfile`

#### 🚀 **Full CI/CD Support**
- `requirements.txt` - Python dependencies
- `requirements-dev.txt` - Development dependencies (optional)
- Test files (`test_*.py` or `tests/` directory)
- `Dockerfile` - For Docker pipeline support
- `docker-compose.yml` - For full stack testing (optional)

#### 📋 **Best Practices**
- Use `requirements.in` files for `pip-tools` compatibility
- Include health check endpoints in Docker containers
- Follow semantic versioning for releases
- Add module-specific documentation

### 🎯 Benefits of This Approach

1. **⚡ Performance**: Only builds/tests what changed
2. **🔄 Consistency**: Reusable workflows ensure uniform testing
3. **🛡️ Security**: Automated vulnerability scanning
4. **📦 Modularity**: Each module can be developed and released independently
5. **🤖 Automation**: Minimal manual intervention required
6. **📊 Visibility**: Clear status badges and reporting
7. **🔧 Maintainability**: Easy to add new modules or modify existing ones

### 🚀 Adding a New Module

1. Create your module directory with Python files
2. Add `requirements.txt` if you have dependencies
3. Add tests (`test_*.py` or `tests/` directory)
4. Add `Dockerfile` if you want Docker support
5. Update the path filters in `.github/workflows/ci.yml`
6. The CI/CD pipeline will automatically detect and test your module!

### 📊 Status Badges

Add these badges to your module READMEs:

```markdown
![CI](https://github.com/tomaszmichalak/learning-python/workflows/CI%2FCD%20Pipeline/badge.svg)
![Docker](https://github.com/tomaszmichalak/learning-python/workflows/Docker%20Build%20%26%20Test/badge.svg)
```

## Development Workflow

### Local Development
```bash
# Clone the repository
git clone https://github.com/tomaszmichalak/learning-python.git
cd learning-python

# Work on a specific module
cd banking-api
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if available

# Run tests
python run_domain_tests.py  # banking-api specific
pytest -v                   # general testing
```

### Creating a Pull Request
1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes in the relevant module(s)
3. Commit your changes: `git commit -m "feat(banking-api): add new feature"`
4. Push to GitHub: `git push origin feature/my-feature`
5. Create a Pull Request
6. The CI pipeline will automatically run tests for changed modules

### Releasing a Module
1. Update version numbers and documentation
2. Commit changes: `git commit -m "chore(banking-api): prepare v1.2.0 release"`
3. Tag the release: `git tag banking-api-v1.2.0`
4. Push tag: `git push origin banking-api-v1.2.0`
5. Create a GitHub release manually if desired

---

This monorepo setup provides a scalable foundation for learning and experimenting with Python while maintaining professional CI/CD practices. Each module can grow independently while benefiting from shared infrastructure and best practices.
