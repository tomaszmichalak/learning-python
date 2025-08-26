#!/usr/bin/env python3
"""
Direct debugging script for Banking API.
This script runs the FastAPI app directly without uvicorn for better debugging.
"""

import asyncio
import uvloop
from api.main import app
import uvicorn

def debug_main():
    """Run the Banking API in debug mode."""
    print("🐛 Starting Banking API in DEBUG mode...")
    print("🔍 Breakpoints in router methods should work now!")
    print("📍 Set breakpoints in:")
    print("   - api/services/debuggable_router.py methods")
    print("   - api/services/rest_service.py methods") 
    print("   - Domain service methods")
    print("")
    
    # Run with uvicorn but with better debugging options
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=False,  # Disable reload for debugging
        access_log=True,
        use_colors=True,
        loop="asyncio"  # Use asyncio loop for better debugging
    )

if __name__ == "__main__":
    debug_main()
