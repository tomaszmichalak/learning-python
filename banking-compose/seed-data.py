#!/usr/bin/env python3
"""
Banking API Data Seeder
========================

This script creates example accounts and transactions for testing purposes.
It waits for the banking API to be ready, then seeds the database with sample data.
"""

import requests
import json
import time
import sys
from typing import Dict, List

# Configuration
API_BASE_URL = "http://banking-api:8000/api"
MAX_RETRIES = 30
RETRY_DELAY = 2

def wait_for_api():
    """Wait for the banking API to be ready"""
    print("🔄 Waiting for banking API to be ready...")
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_BASE_URL.replace('/api', '')}/", timeout=5)
            if response.status_code == 200:
                print("✅ Banking API is ready!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"⏳ Attempt {attempt + 1}/{MAX_RETRIES}: API not ready yet... {e}")
            time.sleep(RETRY_DELAY)
    
    print("❌ API failed to become ready within timeout period")
    return False

def create_account(account_data: Dict) -> Dict:
    """Create an account and return the response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/accounts",
            headers={"Content-Type": "application/json"},
            json=account_data,
            timeout=10
        )
        response.raise_for_status()
        account = response.json()
        print(f"✅ Created account: {account['account_holder']} (ID: {account['account_id'][:8]}...)")
        return account
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create account {account_data['account_holder']}: {e}")
        raise

def create_transaction(transaction_data: Dict) -> Dict:
    """Create a transaction and return the response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/transactions",
            headers={"Content-Type": "application/json"},
            json=transaction_data,
            timeout=10
        )
        response.raise_for_status()
        transaction = response.json()
        print(f"✅ Created {transaction['transaction_type']}: ${transaction['amount']:.2f} for account {transaction['account_id'][:8]}...")
        return transaction
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create transaction: {e}")
        raise

def seed_data():
    """Main function to seed the database with example data"""
    print("🌱 Starting data seeding process...")
    
    # Check if data already exists
    try:
        response = requests.get(f"{API_BASE_URL}/accounts", timeout=10)
        if response.status_code == 200:
            accounts = response.json()
            if len(accounts) > 0:
                print(f"📊 Found {len(accounts)} existing accounts. Skipping seed process.")
                return
    except requests.exceptions.RequestException:
        print("⚠️  Could not check existing accounts, proceeding with seeding...")

    # Create example accounts
    account_data = [
        {
            "account_holder": "Alice Johnson",
            "account_type": "checking",
            "initial_balance": 1500.0
        },
        {
            "account_holder": "Bob Smith", 
            "account_type": "savings",
            "initial_balance": 2000.0
        },
        {
            "account_holder": "Charlie Brown",
            "account_type": "checking", 
            "initial_balance": 750.0
        }
    ]
    
    created_accounts = []
    for account_info in account_data:
        account = create_account(account_info)
        created_accounts.append(account)
    
    print(f"✅ Created {len(created_accounts)} accounts")
    
    # Create initial deposits to fund the accounts
    for account in created_accounts:
        initial_balance = next(
            acc['initial_balance'] for acc in account_data 
            if acc['account_holder'] == account['account_holder']
        )
        
        if initial_balance > 0:
            deposit_transaction = {
                "account_id": account["account_id"],
                "amount": initial_balance,
                "transaction_type": "deposit",
                "description": f"Initial deposit for {account['account_holder']}"
            }
            create_transaction(deposit_transaction)
    
    # Create some example transactions
    time.sleep(1)  # Small delay to ensure deposits are processed
    
    alice_id = created_accounts[0]["account_id"]
    bob_id = created_accounts[1]["account_id"] 
    charlie_id = created_accounts[2]["account_id"]
    
    example_transactions = [
        {
            "account_id": alice_id,
            "amount": 200.0,
            "transaction_type": "withdrawal",
            "description": "ATM withdrawal - Coffee shop"
        },
        {
            "account_id": bob_id,
            "amount": 100.0,
            "transaction_type": "deposit", 
            "description": "Birthday gift deposit"
        },
        {
            "account_id": charlie_id,
            "amount": 50.0,
            "transaction_type": "withdrawal",
            "description": "Online purchase - Books"
        },
        {
            "account_id": alice_id,
            "amount": 300.0,
            "transaction_type": "deposit",
            "description": "Freelance payment"
        }
    ]
    
    for transaction in example_transactions:
        create_transaction(transaction)
        time.sleep(0.5)  # Small delay between transactions
    
    print("🎉 Data seeding completed successfully!")
    print(f"📊 Summary:")
    print(f"   - Created {len(created_accounts)} accounts")
    print(f"   - Created {len(created_accounts) + len(example_transactions)} transactions")
    print(f"   - Accounts: {', '.join([acc['account_holder'] for acc in created_accounts])}")

def main():
    """Main entry point"""
    print("🌱 Banking API Data Seeder Starting...")
    
    if not wait_for_api():
        print("❌ Exiting due to API unavailability")
        sys.exit(1)
    
    try:
        seed_data()
        print("✅ Data seeding process completed successfully!")
    except Exception as e:
        print(f"❌ Data seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
