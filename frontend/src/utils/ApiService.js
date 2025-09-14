class ApiService {
  constructor() {
    this.baseURL = 'http://localhost:8000'
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(url, config)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      throw error
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health')
  }

  // Get available models
  async getModels() {
    return this.request('/models')
  }

  // Generate 3D model
  async generateModel(data) {
    return this.request('/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  // Get generation status
  async getGenerationStatus(jobId) {
    return this.request(`/generate/${jobId}`)
  }

  // Download generated model
  async downloadModel(jobId) {
    const url = `${this.baseURL}/download/${jobId}`

    try {
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Download failed: ${response.status}`)
      }

      // Create download link
      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = downloadUrl
      a.download = `model_${jobId}.stl`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(downloadUrl)

      return { success: true }
    } catch (error) {
      console.error('Download failed:', error)
      throw error
    }
  }

  // Get gallery
  async getGallery() {
    return this.request('/gallery')
  }

  // System status
  async getSystemStatus() {
    return this.request('/')
  }

  // Optimize model (if implemented)
  async optimizeModel(jobId, options = {}) {
    return this.request('/optimize', {
      method: 'POST',
      body: JSON.stringify({
        model_id: jobId,
        ...options
      })
    })
  }
}

// Export singleton instance
export default new ApiService()