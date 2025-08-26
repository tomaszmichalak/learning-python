import { useEffect, useState } from 'react'
import './App.css'
import { TransactionStream } from './components/TransactionStream'

interface Account {
  account_id: string
  account_holder: string
  account_type: string
  balance: number
  created_at: string
  is_active: boolean
}

function App() {
  const [accounts, setAccounts] = useState<Account[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null)
  const [showTransactionStream, setShowTransactionStream] = useState(false)

  useEffect(() => {
    fetchAccounts()
  }, [])

  const fetchAccounts = async () => {
    try {
      setLoading(true)
      // Use the proxy endpoint when in production, or environment variable for development
      const apiUrl = import.meta.env.VITE_API_URL || '/api'
      const response = await fetch(`${apiUrl}/accounts`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setAccounts(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch accounts')
    } finally {
      setLoading(false)
    }
  }

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
      day: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading accounts...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error loading accounts</h2>
          <p>{error}</p>
          <button onClick={fetchAccounts}>Retry</button>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Banking Dashboard</h1>
        <div className="header-actions">
          <button 
            onClick={() => setShowTransactionStream(!showTransactionStream)} 
            className="toggle-stream-btn"
          >
            {showTransactionStream ? 'Hide' : 'Show'} Live Transactions
          </button>
          <button onClick={fetchAccounts} className="refresh-btn">
            Refresh Accounts
          </button>
        </div>
      </header>

      <main className="main-content">
        {showTransactionStream && (
          <section className="transaction-stream-section">
            <TransactionStream 
              accountId={selectedAccountId || undefined}
              className="main-transaction-stream"
            />
          </section>
        )}

        <section className="accounts-section">
          <h2>Accounts</h2>
          {loading ? (
            <div className="loading">Loading accounts...</div>
          ) : error ? (
            <div className="error">
              <h3>Error loading accounts</h3>
              <p>{error}</p>
              <button onClick={fetchAccounts}>Retry</button>
            </div>
          ) : accounts.length === 0 ? (
            <div className="no-accounts">
              <p>No accounts found</p>
            </div>
          ) : (
            <div className="accounts-grid">
              {accounts.map((account) => (
                <div 
                  key={account.account_id} 
                  className={`account-card ${selectedAccountId === account.account_id ? 'selected' : ''}`}
                  onClick={() => {
                    setSelectedAccountId(selectedAccountId === account.account_id ? null : account.account_id)
                    if (!showTransactionStream) {
                      setShowTransactionStream(true)
                    }
                  }}
                >
                  <div className="account-header">
                    <h3>{account.account_holder}</h3>
                    <span className="account-type">{account.account_type}</span>
                  </div>
                  <div className="account-details">
                    <p className="account-id">
                      Account ID: {account.account_id}
                    </p>
                    <p className="balance">
                      Balance: {formatCurrency(account.balance)}
                    </p>
                    <p className="date">
                      Created: {formatDate(account.created_at)}
                    </p>
                    <p className="status">
                      Status: {account.is_active ? 'Active' : 'Inactive'}
                    </p>
                  </div>
                  {selectedAccountId === account.account_id && (
                    <div className="selected-indicator">
                      🔴 Viewing Live Transactions
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>


      </main>
    </div>
  )
}

export default App
