#!/usr/bin/env python3
"""
Start the Banking API server
"""

import uvicorn

if __name__ == "__main__":
    print("🏦 Starting Banking API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press CTRL+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
