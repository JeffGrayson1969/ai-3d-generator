import React, { useState, useEffect } from 'react'
import { Loader, Download, Eye, Zap } from 'lucide-react'
import ModelViewer from './components/ModelViewer'
import GenerationForm from './components/GenerationForm'
import StatusIndicator from './components/StatusIndicator'
import GallerySection from './components/GallerySection'
import ApiService from './utils/ApiService'
import WebSocketService from './utils/WebSocketService'

function App() {
  const [currentGeneration, setCurrentGeneration] = useState(null)
  const [models, setModels] = useState([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)

  useEffect(() => {
    // Load available models on startup
    loadModels()

    // Initialize WebSocket connection
    const wsService = WebSocketService.getInstance()
    wsService.connect('ws://localhost:8000/ws')

    wsService.onMessage((data) => {
      if (data.job_id && currentGeneration?.id === data.job_id) {
        setCurrentGeneration(prev => ({
          ...prev,
          status: data.status,
          progress: data.progress,
          message: data.message
        }))

        if (data.status === 'completed' || data.status === 'failed') {
          setIsGenerating(false)
        }
      }
    })

    wsService.onConnect(() => setWsConnected(true))
    wsService.onDisconnect(() => setWsConnected(false))

    return () => {
      wsService.disconnect()
    }
  }, [currentGeneration?.id])

  const loadModels = async () => {
    try {
      const modelsData = await ApiService.getModels()
      setModels(modelsData)
    } catch (error) {
      console.error('Failed to load models:', error)
    }
  }

  const handleGenerate = async (formData) => {
    try {
      setIsGenerating(true)
      const response = await ApiService.generateModel(formData)
      setCurrentGeneration(response)
    } catch (error) {
      console.error('Generation failed:', error)
      setIsGenerating(false)
    }
  }

  const handleDownload = async () => {
    if (currentGeneration?.id && currentGeneration.status === 'completed') {
      try {
        await ApiService.downloadModel(currentGeneration.id)
      } catch (error) {
        console.error('Download failed:', error)
      }
    }
  }

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8 fade-in">
          <h1 className="text-5xl font-bold gradient-text mb-4">
            AI 3D Generator
          </h1>
          <p className="text-xl text-white/80 mb-2">
            Transform your ideas into 3D models with the power of AI
          </p>
          <div className="flex items-center justify-center gap-4 text-sm text-white/60">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              <span>{wsConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <span>•</span>
            <span>{models.filter(m => m.available).length} models available</span>
          </div>
        </header>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Generation Panel */}
          <div className="glass p-6 fade-in">
            <div className="flex items-center gap-3 mb-6">
              <Zap className="text-yellow-400" size={24} />
              <h2 className="text-2xl font-bold text-white">Generate</h2>
            </div>

            <GenerationForm
              onGenerate={handleGenerate}
              isGenerating={isGenerating}
              models={models}
            />

            {/* Status Section */}
            {currentGeneration && (
              <div className="mt-6 space-y-4">
                <StatusIndicator
                  status={currentGeneration.status}
                  progress={currentGeneration.progress}
                  message={currentGeneration.message}
                />

                {/* Action Buttons */}
                <div className="flex gap-3">
                  {currentGeneration.status === 'completed' && (
                    <button
                      onClick={handleDownload}
                      className="btn-primary flex items-center gap-2"
                    >
                      <Download size={18} />
                      Download STL
                    </button>
                  )}
                  {currentGeneration.file_url && (
                    <button className="btn-primary flex items-center gap-2 bg-green-600">
                      <Eye size={18} />
                      View Model
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* 3D Viewer Panel */}
          <div className="glass p-6 fade-in">
            <div className="flex items-center gap-3 mb-6">
              <Eye className="text-blue-400" size={24} />
              <h2 className="text-2xl font-bold text-white">Preview</h2>
            </div>

            <div className="model-viewer">
              <ModelViewer
                modelUrl={currentGeneration?.file_url}
                isLoading={isGenerating}
              />
            </div>

            <div className="mt-4 text-center text-white/60 text-sm">
              {currentGeneration?.status === 'completed'
                ? 'Use mouse to rotate • Scroll to zoom'
                : 'Generate a 3D model to see the preview'
              }
            </div>
          </div>
        </div>

        {/* Gallery Section */}
        <GallerySection />

        {/* Footer */}
        <footer className="text-center text-white/40 text-sm mt-8">
          <p>
            Built with React, Three.js, and FastAPI •
            <span className="ml-2">Open Source AI 3D Generation</span>
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App