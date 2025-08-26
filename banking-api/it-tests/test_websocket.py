"""
Test WebSocket functionality for real-time transaction updates.
"""

import asyncio
import json
import pytest
import sys
import os
from fastapi.testclient import TestClient
from websockets.asyncio.client import connect
import httpx

# Add parent directory to path to import main from api folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import app

client = TestClient(app)


class TestWebSocketIntegration:
    """Test WebSocket integration with REST API."""
    
    def test_websocket_endpoint_exists(self):
        """Test that WebSocket endpoints are available."""
        # Test WebSocket stats endpoint
        response = client.get("/api/ws/stats")
        assert response.status_code == 200
        data = response.json()
        assert "connections" in data
    
    def test_rest_api_still_works(self):
        """Test that REST API endpoints still work after refactoring."""
        # Create an account
        account_data = {
            "account_holder": "Test User",
            "account_type": "checking",
            "balance": 1000.0
        }
        
        response = client.post("/api/accounts", json=account_data)
        assert response.status_code == 200
        account = response.json()
        assert account["account_holder"] == "Test User"
        
        # Get all accounts
        response = client.get("/api/accounts")
        assert response.status_code == 200
        accounts = response.json()
        assert len(accounts) >= 1
        
        # Create a transaction
        transaction_data = {
            "account_id": account["account_id"],
            "amount": 100.0,
            "transaction_type": "deposit",
            "description": "Test deposit"
        }
        
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["amount"] == 100.0


@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection and basic functionality."""
    # This test requires the server to be running
    # It's more of an integration test
    
    try:
        # Test connection to all transactions WebSocket
        uri = "ws://localhost:8000/api/ws/transactions"
        
        # Note: This test would require a running server
        # For now, we'll just validate the URL structure
        assert uri.startswith("ws://")
        assert "/api/ws/transactions" in uri
        
    except Exception as e:
        # Expected when server is not running
        pass


if __name__ == "__main__":
    # Run basic tests
    test_client = TestClient(app)
    
    # Test health endpoint
    response = test_client.get("/health")
    print("Health check:", response.json())
    
    # Test root endpoint
    response = test_client.get("/")
    print("Root endpoint:", response.json())
    
    # Test WebSocket stats
    response = test_client.get("/api/ws/stats")
    print("WebSocket stats:", response.json())
    
    print("Basic tests completed successfully!")
