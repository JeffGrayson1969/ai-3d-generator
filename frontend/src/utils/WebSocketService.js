class WebSocketService {
  constructor() {
    this.ws = null
    this.listeners = {
      message: [],
      connect: [],
      disconnect: [],
      error: []
    }
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.isConnected = false
  }

  static getInstance() {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService()
    }
    return WebSocketService.instance
  }

  connect(url) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    try {
      this.ws = new WebSocket(url)

      this.ws.onopen = (event) => {
        console.log('WebSocket connected:', event)
        this.isConnected = true
        this.reconnectAttempts = 0
        this.emit('connect', event)
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('WebSocket message received:', data)
          this.emit('message', data)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
          this.emit('message', { raw: event.data })
        }
      }

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event)
        this.isConnected = false
        this.emit('disconnect', event)

        // Auto-reconnect logic
        if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
          console.log(`Attempting to reconnect... (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`)
          setTimeout(() => {
            this.reconnectAttempts++
            this.connect(url)
          }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts))
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.emit('error', error)
      }

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      this.emit('error', error)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnecting')
      this.ws = null
      this.isConnected = false
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        const message = typeof data === 'string' ? data : JSON.stringify(data)
        this.ws.send(message)
        console.log('WebSocket message sent:', data)
      } catch (error) {
        console.error('Failed to send WebSocket message:', error)
        this.emit('error', error)
      }
    } else {
      console.warn('WebSocket not connected, cannot send message:', data)
    }
  }

  // Event listener management
  on(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback)
    } else {
      console.warn(`Unknown event type: ${event}`)
    }
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback)
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error(`Error in WebSocket ${event} listener:`, error)
        }
      })
    }
  }

  // Convenience methods
  onMessage(callback) {
    this.on('message', callback)
  }

  onConnect(callback) {
    this.on('connect', callback)
  }

  onDisconnect(callback) {
    this.on('disconnect', callback)
  }

  onError(callback) {
    this.on('error', callback)
  }

  // Get connection status
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      readyState: this.ws ? this.ws.readyState : null,
      reconnectAttempts: this.reconnectAttempts
    }
  }
}

export default WebSocketService