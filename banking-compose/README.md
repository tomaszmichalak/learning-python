# Banking Application - Docker Compose

This folder contains Docker Compose configurations for running the complete banking application stack, including the banking API (FastAPI) and banking web frontend (React + Vite + TypeScript).

## Architecture

The application consists of two main services:
- **banking-api**: FastAPI backend service with account and transaction management
- **banking-web**: React frontend with nginx proxy for API requests

### Service Communication

The local development setup uses nginx as a reverse proxy to handle API requests:
- Frontend requests to `/api/*` are proxied to the `banking-api` service
- This mimics the production ingress setup where `/api` requests are routed to the API service
- Eliminates CORS configuration needs and provides clean service-to-service communication
- Perfect preparation for Kubernetes deployment with ingress controllers

## Files Overview

- `docker-compose.yml` - Main configuration using nginx proxy approach (mimics production)
- `docker-compose.dev.yml` - Development override for direct API access (debugging only)

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Development Mode (Recommended)

```bash
# Start services with development configuration
docker compose up

# Or run in detached mode
docker compose up -d

# Build and start (if you made changes)
docker compose up --build
```

### Development with Direct API Access

For debugging purposes, you can bypass the proxy and use direct API access:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Web Application | http://localhost:3000 | React frontend |
| API (through proxy) | http://localhost:3000/api | API endpoints via nginx proxy (default) |
| API (direct) | http://localhost:8000 | Direct API access (debugging only) |
| API Documentation | http://localhost:8000/docs | FastAPI auto-generated docs |

## Configuration Options

### Environment Variables

The application supports several environment variables for configuration:

#### Banking API
- `HOST` - Host to bind to (default: 0.0.0.0)
- `PORT` - Port to run on (default: 8000)
- `PYTHONPATH` - Python module path (default: /app)

#### Banking Web
- `VITE_API_URL` - API endpoint URL for the frontend

### Development vs Production

| Mode | API Access | Use Case |
|------|------------|----------|
| Default (Proxy) | `/api` (proxied) | Standard development (mimics production) |
| Dev Override | `http://localhost:8000` | API debugging only |
| Production | `/api` (via ingress) | Production deployment with ingress controller |

## Service Health Checks

Both services include health checks:
- **banking-api**: Checks `http://localhost:8000/` endpoint
- **banking-web**: Checks nginx on port 80

## Networking

Services communicate through a custom bridge network `banking-network`, which:
- Provides service discovery via service names
- Isolates the application stack
- Enables secure inter-service communication

## Commands Reference

### Basic Operations

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs

# View logs for specific service
docker compose logs banking-api
docker compose logs banking-web
```

### Development Operations

```bash
# Rebuild and start (after code changes)
docker compose up --build

# Rebuild specific service
docker compose build banking-api

# Scale services (if needed)
docker compose up --scale banking-api=2
```

### Cleanup

```bash
# Stop and remove containers, networks
docker compose down

# Remove volumes as well
docker compose down -v

# Remove images
docker compose down --rmi all
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   lsof -i :8000
   
   # Stop conflicting processes or change ports in docker compose.yml
   ```

2. **Services not communicating**
   - Ensure both services are on the same network
   - Check service names in configuration
   - Verify health checks are passing

3. **API requests failing**
   ```bash
   # Check if API is accessible
   curl http://localhost:8000/
   curl http://localhost:3000/api/
   ```

4. **Frontend not loading**
   - Check nginx configuration
   - Verify build process completed successfully
   - Check browser developer tools for errors

### Debugging

```bash
# Execute commands inside containers
docker compose exec banking-api bash
docker compose exec banking-web sh

# Check container logs
docker compose logs -f banking-api

# Check service status
docker compose ps
```

## Kubernetes Migration

This Docker Compose setup is designed for easy migration to Kubernetes:

1. **Service names** (`banking-api`, `banking-web`) translate directly to Kubernetes services
2. **nginx proxy configuration** works with Kubernetes ingress
3. **Health checks** map to Kubernetes readiness/liveness probes
4. **Environment variables** can be managed via ConfigMaps/Secrets

## API Endpoints

The banking API provides the following endpoints:

- `GET /` - Welcome message
- `GET /accounts` - List all accounts
- `POST /accounts` - Create new account
- `GET /accounts/{account_id}` - Get specific account
- `GET /transactions` - List all transactions
- `POST /transactions` - Create new transaction
- `POST /transactions/transfer` - Transfer between accounts

For detailed API documentation, visit: http://localhost:8000/docs

## Development Workflow

1. Make changes to banking-api or banking-web code
2. Rebuild the affected service: `docker compose build <service-name>`
3. Restart services: `docker compose up -d`
4. Test changes at http://localhost:3000

For faster development cycles, consider using volume mounts for live code reloading.


## Testing

```bash
# Create an account and store the account ID in a variable
ACCOUNT_ID=$(curl -s -X POST "http://localhost:3000/api/accounts" -H "Content-Type: application/json" -d '{"account_holder": "Test User", "account_type": "savings", "balance": 1000.0}' | jq -r '.account_id')

# Verify the account was created and display the account ID
echo "Created account: $ACCOUNT_ID"

# Create a transaction using the stored account ID
curl -X POST "http://localhost:3000/api/transactions" -H "Content-Type: application/json" -d "{\"account_id\": \"$ACCOUNT_ID\", \"amount\": 150.0, \"transaction_type\": \"deposit\", \"description\": \"Test real-time update\"}"

# Alternative: Create account and transaction in one line
ACCOUNT_ID=$(curl -s -X POST "http://localhost:3000/api/accounts" -H "Content-Type: application/json" -d '{"account_holder": "Test User", "account_type": "savings", "balance": 1000.0}' | jq -r '.account_id') && curl -X POST "http://localhost:3000/api/transactions" -H "Content-Type: application/json" -d "{\"account_id\": \"$ACCOUNT_ID\", \"amount\": 250.0, \"transaction_type\": \"deposit\", \"description\": \"Automated test transaction\"}"
```