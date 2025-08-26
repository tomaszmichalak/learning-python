#!/usr/bin/env python3
"""
Start the Banking API server
"""

import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the parent directory to Python path so we can import api.main
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    print("🏦 Starting Banking API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press CTRL+C to stop the server")
    print("-" * 50)
    
    # Change working directory to parent so api module can be found
    os.chdir(parent_dir)
    
    # Use localhost for local development, 0.0.0.0 only when explicitly configured
    # This prevents the security scanner from flagging hardcoded bind-all-interfaces
    host = os.getenv("HOST", "127.0.0.1")  # Default to localhost for security
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "api.main:app", 
        host=host,  # Configurable via HOST environment variable
        port=port, 
        reload=True,
        log_level="info"
    )
