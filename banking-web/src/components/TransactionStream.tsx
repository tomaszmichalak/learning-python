import React, { useEffect, useState } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import { Transaction } from '../types/transaction'
import './TransactionStream.css'

interface TransactionStreamProps {
  accountId?: string
  className?: string
}

export const TransactionStream: React.FC<TransactionStreamProps> = ({ 
  accountId, 
  className = '' 
}) => {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [connectionMessage, setConnectionMessage] = useState<string>('')

  // Create WebSocket URL
  const wsUrl = React.useMemo(() => {
    const baseUrl = 'ws://localhost:3000/api/ws/transactions'
    return accountId ? `${baseUrl}?account_id=${accountId}` : baseUrl
  }, [accountId])

  // Use the WebSocket hook
  const { isConnected, error, lastMessage } = useWebSocket(wsUrl)

  // Handle incoming messages
  useEffect(() => {
    if (!lastMessage) return

    interface WebSocketMessage {
      type: string
      data?: unknown
    }
    
    const message = lastMessage as WebSocketMessage
    console.log('Received message:', message)

    switch (message.type) {
      case 'connection_established': {
        const connectionData = message.data as { message?: string }
        setConnectionMessage(connectionData?.message || 'Connected')
        break
      }

      case 'initial_data': {
        if (Array.isArray(message.data)) {
          setTransactions(message.data)
        }
        break
      }

      case 'transaction_update': {
        if (message.data) {
          const transactionData = message.data as {
            transaction_id: string
            account_id: string
            amount: number
            transaction_type: 'deposit' | 'withdrawal' | 'transfer'
            description: string
            timestamp: string
            balance_after: number
          }
          const newTransaction: Transaction = {
            transaction_id: transactionData.transaction_id,
            account_id: transactionData.account_id,
            amount: transactionData.amount,
            transaction_type: transactionData.transaction_type,
            description: transactionData.description,
            timestamp: transactionData.timestamp,
            balance_after: transactionData.balance_after
          }
          setTransactions(prev => [newTransaction, ...prev].slice(0, 50))
        }
        break
      }

      default:
        console.log('Unknown message type:', message.type)
    }
  }, [lastMessage])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className={`transaction-stream ${className}`}>
      <div className="stream-header">
        <h3>🔄 Live Transaction Stream</h3>
        <div className="connection-info">
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
          </div>
          {connectionMessage && (
            <div className="connection-message">📡 {connectionMessage}</div>
          )}
        </div>

        {error && (
          <div className="error-message">⚠️ {error}</div>
        )}
      </div>

      <div className="stream-content">
        <div className="stream-stats">
          <div className="stat-item">
            <span className="stat-label">Total Transactions:</span>
            <span className="stat-value">{transactions.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Filter:</span>
            <span className="stat-value">{accountId ? `Account ${accountId.slice(0, 8)}...` : 'All Accounts'}</span>
          </div>
        </div>

        <div className="transactions-list">
          {transactions.length === 0 ? (
            <div className="no-transactions">
              {!isConnected && (
                <p>Waiting for connection...</p>
              )}
              {isConnected && (
                <p>No transactions yet. Try creating a transaction to see real-time updates!</p>
              )}
            </div>
          ) : (
            <div className="transaction-items">
              {transactions.map((transaction) => (
                <div 
                  key={transaction.transaction_id} 
                  className={`transaction-item ${transaction.transaction_type}`}
                >
                  <div className="transaction-header">
                    <span className={`transaction-type ${transaction.transaction_type}`}>
                      {transaction.transaction_type === 'deposit' ? '💰' : 
                       transaction.transaction_type === 'withdrawal' ? '💸' : '🔄'} 
                      {transaction.transaction_type.toUpperCase()}
                    </span>
                    <span className="transaction-amount">
                      {transaction.transaction_type === 'withdrawal' ? '-' : '+'}
                      {formatCurrency(transaction.amount)}
                    </span>
                  </div>
                  <div className="transaction-details">
                    <p className="transaction-description">{transaction.description}</p>
                    <div className="transaction-meta">
                      <span className="transaction-id">ID: {transaction.transaction_id.slice(0, 8)}...</span>
                      <span className="transaction-date">{formatDate(transaction.timestamp)}</span>
                    </div>
                    <div className="transaction-balance">
                      Balance after: {formatCurrency(transaction.balance_after)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
