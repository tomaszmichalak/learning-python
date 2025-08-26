"""WebSocket connection manager for real-time transaction updates."""

import json
import asyncio
from typing import Dict, List, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from domains.transaction.models import Transaction
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time transaction updates."""
    
    def __init__(self):
        # Store active connections with optional account filtering
        self.active_connections: Dict[WebSocket, Optional[str]] = {}
        # Store connections by account_id for targeted updates
        self.account_connections: Dict[str, Set[WebSocket]] = {}
        # Store connections for all transactions (no filter)
        self.global_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket, account_id: Optional[str] = None):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[websocket] = account_id
        
        if account_id:
            if account_id not in self.account_connections:
                self.account_connections[account_id] = set()
            self.account_connections[account_id].add(websocket)
            logger.info(f"WebSocket connected for account: {account_id}")
        else:
            self.global_connections.add(websocket)
            logger.info("WebSocket connected for all transactions")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            account_id = self.active_connections[websocket]
            del self.active_connections[websocket]
            
            if account_id:
                if account_id in self.account_connections:
                    self.account_connections[account_id].discard(websocket)
                    if not self.account_connections[account_id]:
                        del self.account_connections[account_id]
                logger.info(f"WebSocket disconnected for account: {account_id}")
            else:
                self.global_connections.discard(websocket)
                logger.info("WebSocket disconnected from all transactions")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            self.disconnect(websocket)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")
            self.disconnect(websocket)
    
    async def broadcast_transaction(self, transaction: Transaction):
        """Broadcast a new transaction to relevant connections."""
        logger.info(f"🚀 Broadcasting transaction {transaction.transaction_id} to {len(self.global_connections)} global connections and {len(self.account_connections)} account-specific connections")
        
        transaction_data = {
            "type": "transaction_update",
            "data": {
                "transaction_id": transaction.transaction_id,
                "account_id": transaction.account_id,
                "amount": float(transaction.amount),
                "transaction_type": transaction.transaction_type.value,
                "description": transaction.description,
                "timestamp": transaction.timestamp.isoformat(),
                "balance_after": float(transaction.balance_after)
            }
        }
        
        message = json.dumps(transaction_data)
        logger.info(f"📨 Transaction message: {message}")
        
        # Send to global listeners (all transactions)
        await self._send_to_connections(self.global_connections, message)
        
        # Send to account-specific listeners
        if transaction.account_id in self.account_connections:
            await self._send_to_connections(
                self.account_connections[transaction.account_id], 
                message
            )
    
    async def broadcast_account_balance(self, account_id: str, new_balance: float):
        """Broadcast account balance update to relevant connections."""
        balance_data = {
            "type": "balance_update",
            "data": {
                "account_id": account_id,
                "new_balance": new_balance,
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        
        message = json.dumps(balance_data)
        
        # Send to global listeners
        await self._send_to_connections(self.global_connections, message)
        
        # Send to account-specific listeners
        if account_id in self.account_connections:
            await self._send_to_connections(
                self.account_connections[account_id], 
                message
            )
    
    async def send_initial_data(self, websocket: WebSocket, transactions: List[Transaction]):
        """Send initial transaction data when a client connects."""
        initial_data = {
            "type": "initial_data",
            "data": [
                {
                    "transaction_id": t.transaction_id,
                    "account_id": t.account_id,
                    "amount": float(t.amount),
                    "transaction_type": t.transaction_type.value,
                    "description": t.description,
                    "timestamp": t.timestamp.isoformat(),
                    "balance_after": float(t.balance_after)
                }
                for t in transactions
            ]
        }
        
        await self.send_personal_message(json.dumps(initial_data), websocket)
    
    async def _send_to_connections(self, connections: Set[WebSocket], message: str):
        """Send message to a set of connections, handling disconnections."""
        logger.info(f"📡 Sending message to {len(connections)} connections")
        if not connections:
            logger.warning("⚠️  No connections to send message to")
            return
            
        disconnected = set()
        
        for connection in connections.copy():
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error sending message to WebSocket: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    def get_connection_count(self) -> Dict[str, int]:
        """Get statistics about active connections."""
        return {
            "total_connections": len(self.active_connections),
            "global_connections": len(self.global_connections),
            "account_specific_connections": sum(len(conns) for conns in self.account_connections.values()),
            "accounts_with_connections": len(self.account_connections)
        }


# Global connection manager instance
manager = ConnectionManager()
