"""
REST API integration tests for the Banking API
Run this after starting the FastAPI server to test the REST endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 10  # seconds - timeout for all HTTP requests


def test_banking_api():
    print("🏦 Testing Banking API")
    print("=" * 50)
    
    # 1. Create two accounts
    print("\n1. Creating accounts...")
    
    account1_data = {
        "account_holder": "Alice Smith",
        "account_type": "checking",
        "balance": 1000.0
    }
    
    account2_data = {
        "account_holder": "Bob Johnson",
        "account_type": "savings",
        "balance": 500.0
    }
    
    # Create account 1
    response1 = requests.post(f"{BASE_URL}/accounts", json=account1_data, timeout=REQUEST_TIMEOUT)
    if response1.status_code == 200:
        account1 = response1.json()
        print(f"✅ Created account for {account1['account_holder']}")
        print(f"   Account ID: {account1['account_id']}")
        print(f"   Balance: ${account1['balance']}")
    else:
        print(f"❌ Failed to create account 1: {response1.text}")
        return
    
    # Create account 2
    response2 = requests.post(f"{BASE_URL}/accounts", json=account2_data, timeout=REQUEST_TIMEOUT)
    if response2.status_code == 200:
        account2 = response2.json()
        print(f"✅ Created account for {account2['account_holder']}")
        print(f"   Account ID: {account2['account_id']}")
        print(f"   Balance: ${account2['balance']}")
    else:
        print(f"❌ Failed to create account 2: {response2.text}")
        return
    
    # 2. Make a deposit
    print("\n2. Making a deposit...")
    
    deposit_data = {
        "account_id": account1['account_id'],
        "amount": 250.0,
        "transaction_type": "deposit",
        "description": "Paycheck deposit"
    }
    
    response = requests.post(f"{BASE_URL}/transactions", json=deposit_data, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        transaction = response.json()
        print(f"✅ Deposit successful!")
        print(f"   Amount: ${transaction['amount']}")
        print(f"   New balance: ${transaction['balance_after']}")
    else:
        print(f"❌ Deposit failed: {response.text}")
    
    # 3. Make a withdrawal
    print("\n3. Making a withdrawal...")
    
    withdrawal_data = {
        "account_id": account2['account_id'],
        "amount": 100.0,
        "transaction_type": "withdrawal",
        "description": "ATM withdrawal"
    }
    
    response = requests.post(f"{BASE_URL}/transactions", json=withdrawal_data, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        transaction = response.json()
        print(f"✅ Withdrawal successful!")
        print(f"   Amount: ${transaction['amount']}")
        print(f"   New balance: ${transaction['balance_after']}")
    else:
        print(f"❌ Withdrawal failed: {response.text}")
    
    # 4. Transfer funds
    print("\n4. Transferring funds...")
    
    transfer_data = {
        "from_account_id": account1['account_id'],
        "to_account_id": account2['account_id'],
        "amount": 200.0,
        "description": "Money transfer to Bob"
    }
    
    response = requests.post(f"{BASE_URL}/transfers", json=transfer_data, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        transactions = response.json()
        print(f"✅ Transfer successful!")
        print(f"   Amount transferred: ${transfer_data['amount']}")
        print(f"   From {account1['account_holder']}: New balance ${transactions[0]['balance_after']}")
        print(f"   To {account2['account_holder']}: New balance ${transactions[1]['balance_after']}")
    else:
        print(f"❌ Transfer failed: {response.text}")
    
    # 5. Get account details
    print("\n5. Checking final account balances...")
    
    response1 = requests.get(f"{BASE_URL}/accounts/{account1['account_id']}", timeout=REQUEST_TIMEOUT)
    response2 = requests.get(f"{BASE_URL}/accounts/{account2['account_id']}", timeout=REQUEST_TIMEOUT)
    
    if response1.status_code == 200 and response2.status_code == 200:
        acc1 = response1.json()
        acc2 = response2.json()
        print(f"✅ {acc1['account_holder']}: ${acc1['balance']}")
        print(f"✅ {acc2['account_holder']}: ${acc2['balance']}")
    
    # 6. Get transaction history for account 1
    print(f"\n6. Transaction history for {account1['account_holder']}...")
    
    response = requests.get(f"{BASE_URL}/accounts/{account1['account_id']}/transactions", timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        transactions = response.json()
        print(f"✅ Found {len(transactions)} transactions:")
        for tx in transactions:
            print(f"   {tx['transaction_type'].title()}: ${tx['amount']} - {tx['description']}")
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    try:
        test_banking_api()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server.")
        print("Please make sure the FastAPI server is running on http://localhost:8000")
        print("Start it with: python main.py")
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after {REQUEST_TIMEOUT} seconds.")
        print("The server might be overloaded or unresponsive.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
