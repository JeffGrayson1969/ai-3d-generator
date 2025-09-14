import React, { useState, useEffect } from 'react'
import { Image, Download, Heart, Calendar } from 'lucide-react'
import ApiService from '../utils/ApiService'

const GalleryItem = ({ item }) => {
  const [liked, setLiked] = useState(false)

  const handleLike = () => {
    setLiked(!liked)
  }

  const handleDownload = async () => {
    try {
      // In a real implementation, this would download the model file
      window.open(item.model_url, '_blank')
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  return (
    <div className="glass p-4 rounded-lg hover:bg-white/10 transition-all duration-300">
      {/* Thumbnail */}
      <div className="aspect-square bg-gradient-to-br from-slate-700 to-slate-800 rounded-lg mb-3 relative overflow-hidden">
        {item.thumbnail_url ? (
          <img
            src={item.thumbnail_url}
            alt={item.prompt}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Image size={32} className="text-white/30" />
          </div>
        )}

        {/* Overlay Actions */}
        <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-2">
          <button
            onClick={handleLike}
            className={`p-2 rounded-full backdrop-blur-sm transition-colors ${
              liked ? 'bg-red-500/80 text-white' : 'bg-white/20 text-white/80 hover:bg-white/30'
            }`}
          >
            <Heart size={16} fill={liked ? 'currentColor' : 'none'} />
          </button>
          <button
            onClick={handleDownload}
            className="p-2 rounded-full bg-white/20 text-white/80 hover:bg-white/30 backdrop-blur-sm transition-colors"
          >
            <Download size={16} />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-2">
        <p className="text-white text-sm line-clamp-2 leading-relaxed">
          "{item.prompt}"
        </p>

        <div className="flex items-center justify-between text-xs text-white/50">
          <div className="flex items-center gap-1">
            <Calendar size={12} />
            <span>{new Date(item.created_at).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1">
              <Heart size={12} />
              {item.likes}
            </span>
            <span className="flex items-center gap-1">
              <Download size={12} />
              {item.downloads}
            </span>
          </div>
        </div>

        <div className="text-xs text-blue-300 bg-blue-400/10 px-2 py-1 rounded">
          {item.model_type}
        </div>
      </div>
    </div>
  )
}

const GallerySection = () => {
  const [galleryItems, setGalleryItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadGallery()
  }, [])

  const loadGallery = async () => {
    try {
      setLoading(true)
      const data = await ApiService.getGallery()

      // Create sample gallery items if none exist
      const sampleItems = data.examples || [
        {
          id: 'sample_1',
          prompt: 'A small red cube with smooth edges',
          thumbnail_url: null,
          model_url: '/api/static/models/cube.stl',
          model_type: 'demo',
          created_at: new Date().toISOString(),
          likes: 12,
          downloads: 34
        },
        {
          id: 'sample_2',
          prompt: 'A blue sphere with metallic surface',
          thumbnail_url: null,
          model_url: '/api/static/models/sphere.stl',
          model_type: 'demo',
          created_at: new Date(Date.now() - 86400000).toISOString(), // Yesterday
          likes: 8,
          downloads: 22
        },
        {
          id: 'sample_3',
          prompt: 'A green cylinder for mechanical parts',
          thumbnail_url: null,
          model_url: '/api/static/models/cylinder.stl',
          model_type: 'demo',
          created_at: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          likes: 15,
          downloads: 41
        },
        {
          id: 'sample_4',
          prompt: 'An orange pyramid with triangular base',
          thumbnail_url: null,
          model_url: '/api/static/models/pyramid.stl',
          model_type: 'demo',
          created_at: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
          likes: 6,
          downloads: 18
        }
      ]

      setGalleryItems(sampleItems)
      setError(null)
    } catch (err) {
      console.error('Failed to load gallery:', err)
      setError('Failed to load gallery')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="glass p-8 rounded-lg">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-white border-t-transparent"></div>
          <span className="ml-3 text-white">Loading gallery...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="glass p-8 rounded-lg">
        <div className="text-center text-red-400">
          <p>{error}</p>
          <button
            onClick={loadGallery}
            className="btn-primary mt-4"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="glass p-6 rounded-lg fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Image className="text-purple-400" size={24} />
        <h2 className="text-2xl font-bold text-white">Gallery</h2>
        <span className="text-white/50 text-sm">
          ({galleryItems.length} models)
        </span>
      </div>

      {galleryItems.length === 0 ? (
        <div className="text-center text-white/50 py-8">
          <Image size={48} className="mx-auto mb-4 text-white/30" />
          <p className="text-lg">No models in gallery yet</p>
          <p className="text-sm">Generated models will appear here</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {galleryItems.map((item) => (
            <GalleryItem key={item.id} item={item} />
          ))}
        </div>
      )}

      <div className="text-center mt-6">
        <button
          onClick={loadGallery}
          className="text-white/50 hover:text-white text-sm underline"
        >
          Refresh Gallery
        </button>
      </div>
    </div>
  )
}

export default GallerySection