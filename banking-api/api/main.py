"""
Banking API with separated REST and WebSocket services.

This application provides:
- REST API for banking operations (accounts, transactions, transfers)
- WebSocket API for real-time transaction updates
- Clear separation between synchronous REST operations and asynchronous real-time data
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import domain services
from domains.account.memory_repository import InMemoryAccountRepository
from domains.account.service import AccountService
from domains.transaction.memory_repository import InMemoryTransactionRepository
from domains.transaction.service import TransactionService

# Import separated services (from services directory)
from services.rest_service import RESTService, create_rest_router
from services.websocket_service import WebSocketService, create_websocket_router
from services.websocket_manager import manager
from services.debuggable_router import create_debuggable_router

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for better debugging
logger = logging.getLogger(__name__)

# Debug flag - set to True for easier debugging
USE_DEBUGGABLE_ROUTER = True

# Create FastAPI application
app = FastAPI(
    title="Banking API with WebSocket",
    description="A banking API with REST endpoints and WebSocket for real-time transaction updates",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize repositories
account_repository = InMemoryAccountRepository()
transaction_repository = InMemoryTransactionRepository()

# Initialize domain services
account_service = AccountService(account_repository)
transaction_service = TransactionService(transaction_repository, account_service)

# Initialize application services
rest_service = RESTService(account_service, transaction_service, manager)
websocket_service = WebSocketService(account_service, transaction_service)

# Create routers
if USE_DEBUGGABLE_ROUTER:
    logger.info("🐛 Using debuggable router for better debugging experience")
    rest_router = create_debuggable_router(rest_service)
else:
    logger.info("Using standard router")
    rest_router = create_rest_router(rest_service)

websocket_router = create_websocket_router(websocket_service)

# Include routers
app.include_router(rest_router, prefix="/api", tags=["REST API"])
app.include_router(websocket_router, prefix="/api", tags=["WebSocket"])


@app.get("/")
async def root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to Banking API with WebSocket support",
        "version": "3.0.0",
        "endpoints": {
            "rest_api": "/api/accounts, /api/transactions, /api/transfers",
            "websocket": "/api/ws/transactions, /api/ws/transactions/{account_id}",
            "documentation": "/docs",
            "websocket_stats": "/api/ws/stats"
        },
        "websocket_info": {
            "all_transactions": "ws://localhost:8000/api/ws/transactions",
            "account_specific": "ws://localhost:8000/api/ws/transactions/{account_id}",
            "supported_messages": ["ping", "get_stats", "get_recent_transactions", "get_account_balance"]
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    connection_stats = manager.get_connection_count()
    return {
        "status": "healthy",
        "services": {
            "rest_api": "operational",
            "websocket": "operational"
        },
        "websocket_connections": connection_stats
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info("Banking API with WebSocket starting up...")
    logger.info("REST API available at: /api/")
    logger.info("WebSocket API available at: /api/ws/")
    logger.info("Documentation available at: /docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info("Banking API shutting down...")
    # Note: WebSocket connections will be automatically closed by FastAPI


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use localhost for local development, 0.0.0.0 only when explicitly configured
    # This prevents the security scanner from flagging hardcoded bind-all-interfaces
    host = os.getenv("HOST", "127.0.0.1")  # Default to localhost for security
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
