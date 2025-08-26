// Transaction types for TypeScript
export interface Transaction {
  transaction_id: string
  account_id: string
  amount: number
  transaction_type: 'deposit' | 'withdrawal' | 'transfer'
  description: string
  timestamp: string
  balance_after: number
}

export interface WebSocketMessage {
  type: 'transaction_update' | 'balance_update' | 'initial_data' | 'connection_established' | 'pong' | 'account_balance' | 'stats' | 'recent_transactions' | 'error'
  data: TransactionUpdate | BalanceUpdate | Transaction[] | ConnectionStats | { message: string } | { [key: string]: unknown }
}

export interface TransactionUpdate {
  transaction_id: string
  account_id: string
  amount: number
  transaction_type: string
  description: string
  timestamp: string
  balance_after: number
}

export interface BalanceUpdate {
  account_id: string
  new_balance: number
  timestamp: number
}

export interface ConnectionStats {
  total_connections: number
  global_connections: number
  account_specific_connections: number
  accounts_with_connections: number
}
