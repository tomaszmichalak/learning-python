import { useCallback, useEffect, useRef, useState } from 'react'

interface UseWebSocketReturn {
  isConnected: boolean
  error: string | null
  lastMessage: unknown
}

export const useWebSocket = (url: string): UseWebSocketReturn => {
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastMessage, setLastMessage] = useState<unknown>(null)
  
  const ws = useRef<WebSocket | null>(null)
  const reconnectAttempts = useRef(0)
  const maxReconnectAttempts = 3
  const reconnectTimeoutRef = useRef<number | null>(null)
  const currentUrl = useRef<string | null>(null)
  const isInitialized = useRef(false)

  console.log(`[SimpleWebSocket] Hook called with URL: ${url}`)

  const cleanup = useCallback(() => {
    console.log('[SimpleWebSocket] Cleaning up connection')
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
    if (ws.current) {
      // Set cleanup handlers to prevent reconnection during cleanup
      ws.current.onopen = null
      ws.current.onmessage = null
      ws.current.onerror = null
      ws.current.onclose = null
      
      // Close with normal closure code
      if (ws.current.readyState === WebSocket.OPEN || ws.current.readyState === WebSocket.CONNECTING) {
        console.log('[SimpleWebSocket] Closing WebSocket with code 1000')
        ws.current.close(1000, 'Component unmounting')
      }
      ws.current = null
    }
    setIsConnected(false)
    setError(null) // Clear any existing errors
    currentUrl.current = null
    isInitialized.current = false
    reconnectAttempts.current = 0 // Reset reconnection attempts
  }, [])

  const connect = useCallback(() => {
    // Prevent connection if already connecting or if URL hasn't changed
    if (!url || ws.current || currentUrl.current === url) {
      return
    }
    
    currentUrl.current = url
    
    try {
      console.log(`[SimpleWebSocket] Connecting to: ${url} (attempt ${reconnectAttempts.current + 1})`)
      
      ws.current = new WebSocket(url)

      ws.current.onopen = () => {
        console.log('[SimpleWebSocket] Connected successfully')
        setIsConnected(true)
        setError(null)
        reconnectAttempts.current = 0
      }

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('[SimpleWebSocket] Message received:', data)
          setLastMessage(data)
        } catch (e) {
          console.error('[SimpleWebSocket] Failed to parse message:', e)
        }
      }

      ws.current.onerror = (event) => {
        console.error('[SimpleWebSocket] Connection error:', event)
        setError('WebSocket connection error')
      }

      ws.current.onclose = (event) => {
        console.log(`[SimpleWebSocket] Connection closed: code=${event.code}, reason="${event.reason}", wasClean=${event.wasClean}`)
        setIsConnected(false)
        ws.current = null
        
        // Only attempt to reconnect on unexpected closures and under max attempts
        if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts && currentUrl.current === url) {
          const delay = Math.min(2000 * Math.pow(2, reconnectAttempts.current), 10000)
          console.log(`[SimpleWebSocket] Scheduling reconnection in ${delay}ms (attempt ${reconnectAttempts.current + 1}/${maxReconnectAttempts})`)
          
          reconnectTimeoutRef.current = window.setTimeout(() => {
            reconnectAttempts.current += 1
            connect()
          }, delay)
        } else if (reconnectAttempts.current >= maxReconnectAttempts) {
          setError('Failed to reconnect after multiple attempts')
          console.log('[SimpleWebSocket] Max reconnection attempts reached')
        } else {
          console.log('[SimpleWebSocket] Not reconnecting: code=1000 (normal closure) or different URL')
        }
      }
    } catch (error) {
      console.error('[SimpleWebSocket] Failed to create WebSocket:', error)
      setError('Failed to create WebSocket connection')
      ws.current = null
    }
  }, [url])

  useEffect(() => {
    // Only initialize once or when URL changes
    if (!isInitialized.current || currentUrl.current !== url) {
      isInitialized.current = true
      
      if (!url) {
        cleanup()
        return
      }

      // If URL changed, cleanup first
      if (currentUrl.current !== url) {
        cleanup()
      }

      connect()
    }

    return cleanup
  }, [url, connect, cleanup])

  return { isConnected, error, lastMessage }
}
