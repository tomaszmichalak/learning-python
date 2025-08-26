"""WebSocket service for real-time banking data."""

import json
import asyncio
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException
from websocket_manager import manager
import logging

logger = logging.getLogger(__name__)


class WebSocketService:
    """WebSocket service for real-time transaction updates."""
    
    def __init__(self, account_service, transaction_service):
        self.account_service = account_service
        self.transaction_service = transaction_service
    
    async def handle_transaction_stream(
        self, 
        websocket: WebSocket, 
        account_id: Optional[str] = None
    ):
        """Handle real-time transaction streaming for a specific account or all accounts."""
        try:
            # Validate account if specified
            if account_id:
                try:
                    await self.account_service.get_account(account_id)
                except HTTPException:
                    await websocket.close(code=1008, reason="Account not found")
                    return
            
            # Connect to WebSocket manager
            await manager.connect(websocket, account_id)
            
            # Send initial transaction data
            if account_id:
                transactions = await self.transaction_service.get_account_transactions(account_id)
            else:
                transactions = await self.transaction_service.get_all_transactions()
            
            await manager.send_initial_data(websocket, transactions)
            
            # Send connection confirmation
            welcome_message = {
                "type": "connection_established",
                "data": {
                    "account_id": account_id,
                    "message": f"Connected to {'account-specific' if account_id else 'global'} transaction stream",
                    "initial_transactions_count": len(transactions)
                }
            }
            await manager.send_personal_message(json.dumps(welcome_message), websocket)
            
            # Keep the connection alive and handle incoming messages
            while True:
                try:
                    # Wait for client messages (like ping/pong or commands)
                    message = await websocket.receive_text()
                    await self._handle_client_message(websocket, message, account_id)
                except WebSocketDisconnect:
                    logger.debug("WebSocket disconnected normally")
                    break
                except RuntimeError as e:
                    if "WebSocket is not connected" in str(e):
                        logger.debug(f"WebSocket already closed: {e}")
                        break
                    else:
                        logger.error(f"Runtime error in WebSocket connection: {e}")
                        break
                except Exception as e:
                    logger.error(f"Unexpected error in WebSocket connection: {e}")
                    break
        
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            try:
                await websocket.close(code=1011, reason="Internal server error")
            except:
                pass  # Connection might already be closed
        finally:
            manager.disconnect(websocket)
    
    async def _handle_client_message(
        self, 
        websocket: WebSocket, 
        message: str, 
        account_id: Optional[str]
    ):
        """Handle messages from WebSocket clients."""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "ping":
                # Respond to ping with pong
                pong_response = {
                    "type": "pong",
                    "data": {
                        "timestamp": asyncio.get_event_loop().time()
                    }
                }
                await manager.send_personal_message(json.dumps(pong_response), websocket)
            
            elif message_type == "get_stats":
                # Send connection statistics
                stats = manager.get_connection_count()
                stats_response = {
                    "type": "stats",
                    "data": stats
                }
                await manager.send_personal_message(json.dumps(stats_response), websocket)
            
            elif message_type == "get_recent_transactions":
                # Send recent transactions
                limit = data.get("limit", 10)
                if account_id:
                    transactions = await self.transaction_service.get_account_transactions(account_id)
                else:
                    transactions = await self.transaction_service.get_all_transactions()
                
                recent_transactions = transactions[:limit]
                response = {
                    "type": "recent_transactions",
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
                        for t in recent_transactions
                    ]
                }
                await manager.send_personal_message(json.dumps(response), websocket)
            
            elif message_type == "get_account_balance":
                # Send current account balance
                if account_id:
                    account = await self.account_service.get_account(account_id)
                    balance_response = {
                        "type": "account_balance",
                        "data": {
                            "account_id": account_id,
                            "balance": float(account.balance),
                            "is_active": account.is_active
                        }
                    }
                    await manager.send_personal_message(json.dumps(balance_response), websocket)
                else:
                    error_response = {
                        "type": "error",
                        "data": {
                            "message": "Account balance can only be requested for account-specific connections"
                        }
                    }
                    await manager.send_personal_message(json.dumps(error_response), websocket)
            
            else:
                # Unknown message type
                error_response = {
                    "type": "error",
                    "data": {
                        "message": f"Unknown message type: {message_type}"
                    }
                }
                await manager.send_personal_message(json.dumps(error_response), websocket)
        
        except json.JSONDecodeError:
            error_response = {
                "type": "error",
                "data": {
                    "message": "Invalid JSON format"
                }
            }
            await manager.send_personal_message(json.dumps(error_response), websocket)
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
            error_response = {
                "type": "error",
                "data": {
                    "message": "Error processing message"
                }
            }
            await manager.send_personal_message(json.dumps(error_response), websocket)


def create_websocket_router(websocket_service: WebSocketService) -> APIRouter:
    """Create and configure the WebSocket router."""
    
    router = APIRouter()
    
    @router.websocket("/ws/transactions")
    async def websocket_all_transactions(websocket: WebSocket):
        """WebSocket endpoint for real-time updates of all transactions."""
        await websocket_service.handle_transaction_stream(websocket)
    
    @router.websocket("/ws/transactions/{account_id}")
    async def websocket_account_transactions(
        websocket: WebSocket, 
        account_id: str
    ):
        """WebSocket endpoint for real-time updates of account-specific transactions."""
        await websocket_service.handle_transaction_stream(websocket, account_id)
    
    @router.get("/ws/stats")
    async def get_websocket_stats():
        """Get WebSocket connection statistics."""
        return {
            "status": "ok",
            "connections": manager.get_connection_count()
        }
    
    return router
