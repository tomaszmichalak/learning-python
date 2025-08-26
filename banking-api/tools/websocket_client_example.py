"""
Example WebSocket client for testing real-time transaction updates.

Usage:
    python websocket_client_example.py
    
    # In another terminal, create transactions via REST API:
    curl -X POST "http://localhost:8000/api/accounts" \
         -H "Content-Type: application/json" \
         -d '{"account_holder": "Test User", "account_type": "savings", "balance": 1000.0}'
    
    curl -X POST "http://localhost:8000/api/transactions" \
         -H "Content-Type: application/json" \
         -d '{"account_id": "ACCOUNT_ID", "amount": 100.0, "transaction_type": "deposit", "description": "Test deposit"}'
"""

import asyncio
import json
import websockets
import requests
from datetime import datetime


class BankingWebSocketClient:
    """Example WebSocket client for banking API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.ws_url = base_url.replace("http", "ws")
    
    async def connect_to_all_transactions(self):
        """Connect to WebSocket for all transaction updates."""
        uri = f"{self.ws_url}/api/ws/transactions"
        
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to {uri}")
                print("Listening for transaction updates...\n")
                
                # Send a ping to test two-way communication
                ping_message = {"type": "ping"}
                await websocket.send(json.dumps(ping_message))
                
                # Listen for messages
                async for message in websocket:
                    data = json.loads(message)
                    await self._handle_message(data)
        
        except Exception as e:
            print(f"Connection error: {e}")
    
    async def connect_to_account_transactions(self, account_id):
        """Connect to WebSocket for specific account transaction updates."""
        uri = f"{self.ws_url}/api/ws/transactions/{account_id}"
        
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to {uri}")
                print(f"Listening for account {account_id} transaction updates...\n")
                
                # Request account balance
                balance_request = {"type": "get_account_balance"}
                await websocket.send(json.dumps(balance_request))
                
                # Listen for messages
                async for message in websocket:
                    data = json.loads(message)
                    await self._handle_message(data)
        
        except Exception as e:
            print(f"Connection error: {e}")
    
    async def _handle_message(self, data):
        """Handle incoming WebSocket messages."""
        message_type = data.get("type")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if message_type == "connection_established":
            print(f"[{timestamp}] ✅ {data['data']['message']}")
            print(f"[{timestamp}] Initial transactions: {data['data']['initial_transactions_count']}")
        
        elif message_type == "transaction_update":
            transaction = data["data"]
            print(f"[{timestamp}] 💰 New Transaction!")
            print(f"   Account: {transaction['account_id']}")
            print(f"   Type: {transaction['transaction_type']}")
            print(f"   Amount: ${transaction['amount']:.2f}")
            print(f"   Balance After: ${transaction['balance_after']:.2f}")
            print(f"   Description: {transaction['description']}")
        
        elif message_type == "balance_update":
            balance_data = data["data"]
            print(f"[{timestamp}] 💳 Balance Update!")
            print(f"   Account: {balance_data['account_id']}")
            print(f"   New Balance: ${balance_data['new_balance']:.2f}")
        
        elif message_type == "initial_data":
            transactions = data["data"]
            print(f"[{timestamp}] 📊 Initial Data Received: {len(transactions)} transactions")
            for transaction in transactions[-3:]:  # Show last 3 transactions
                print(f"   - {transaction['transaction_type']}: ${transaction['amount']:.2f}")
        
        elif message_type == "pong":
            print(f"[{timestamp}] 🏓 Pong received")
        
        elif message_type == "account_balance":
            balance_data = data["data"]
            print(f"[{timestamp}] 💰 Current Balance: ${balance_data['balance']:.2f}")
            print(f"   Account Active: {balance_data['is_active']}")
        
        elif message_type == "stats":
            stats = data["data"]
            print(f"[{timestamp}] 📈 Connection Stats:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        
        elif message_type == "error":
            print(f"[{timestamp}] ❌ Error: {data['data']['message']}")
        
        else:
            print(f"[{timestamp}] 📨 Unknown message type: {message_type}")
        
        print()  # Empty line for readability
    
    def create_test_account(self):
        """Create a test account via REST API."""
        account_data = {
            "account_holder": "WebSocket Test User",
            "account_type": "checking",
            "balance": 1000.0
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/accounts", json=account_data)
            if response.status_code == 200:
                account = response.json()
                print(f"✅ Created test account: {account['account_id']}")
                return account["account_id"]
            else:
                print(f"❌ Failed to create account: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error creating account: {e}")
            return None
    
    def create_test_transaction(self, account_id, amount=100.0, transaction_type="deposit"):
        """Create a test transaction via REST API."""
        transaction_data = {
            "account_id": account_id,
            "amount": amount,
            "transaction_type": transaction_type,
            "description": f"WebSocket test {transaction_type}"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/transactions", json=transaction_data)
            if response.status_code == 200:
                transaction = response.json()
                print(f"✅ Created test transaction: ${amount} {transaction_type}")
                return transaction["transaction_id"]
            else:
                print(f"❌ Failed to create transaction: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error creating transaction: {e}")
            return None


async def main():
    """Main example function."""
    client = BankingWebSocketClient()
    
    print("Banking WebSocket Client Example")
    print("=" * 40)
    print("1. Connect to all transactions")
    print("2. Connect to specific account")
    print("3. Create test account and connect")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        await client.connect_to_all_transactions()
    
    elif choice == "2":
        account_id = input("Enter account ID: ").strip()
        if account_id:
            await client.connect_to_account_transactions(account_id)
        else:
            print("Invalid account ID")
    
    elif choice == "3":
        # Create test account
        account_id = client.create_test_account()
        if account_id:
            print(f"\nTest account created: {account_id}")
            print("You can now create transactions in another terminal:")
            print(f'curl -X POST "http://localhost:8000/api/transactions" \\')
            print(f'     -H "Content-Type: application/json" \\')
            print(f'     -d \'{{"account_id": "{account_id}", "amount": 100.0, "transaction_type": "deposit", "description": "Test"}}\'')
            print("\nConnecting to account-specific WebSocket...\n")
            
            await client.connect_to_account_transactions(account_id)
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    print("Make sure the banking API server is running on http://localhost:8000")
    print("Starting WebSocket client...\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 WebSocket client disconnected")
    except Exception as e:
        print(f"❌ Error: {e}")
