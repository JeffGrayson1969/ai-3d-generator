import React, { useState } from 'react'
import { Send, Settings } from 'lucide-react'

const GenerationForm = ({ onGenerate, isGenerating, models }) => {
  const [formData, setFormData] = useState({
    prompt: '',
    model_type: 'demo',
    quality: 'medium',
    format: 'stl'
  })
  const [showAdvanced, setShowAdvanced] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.prompt.trim()) return
    onGenerate(formData)
  }

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const availableModels = models.filter(model => model.available)

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Prompt Input */}
      <div>
        <label className="block text-white font-medium mb-2">
          Describe your 3D model
        </label>
        <textarea
          name="prompt"
          value={formData.prompt}
          onChange={handleChange}
          placeholder="A small red cube with rounded edges..."
          className="input-field resize-none h-24"
          disabled={isGenerating}
          required
        />
        <div className="text-xs text-white/50 mt-1">
          Be descriptive! Mention shapes, colors, sizes, and details.
        </div>
      </div>

      {/* Model Selection */}
      <div>
        <label className="block text-white font-medium mb-2">
          AI Model
        </label>
        <select
          name="model_type"
          value={formData.model_type}
          onChange={handleChange}
          className="input-field"
          disabled={isGenerating}
        >
          {availableModels.map(model => (
            <option key={model.name} value={model.name}>
              {model.name} - {model.description}
            </option>
          ))}
        </select>
      </div>

      {/* Advanced Settings Toggle */}
      <div className="flex items-center gap-2">
        <Settings size={16} className="text-white/60" />
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-white/60 hover:text-white text-sm underline"
        >
          {showAdvanced ? 'Hide' : 'Show'} Advanced Settings
        </button>
      </div>

      {/* Advanced Settings */}
      {showAdvanced && (
        <div className="space-y-4 p-4 rounded-lg bg-white/5">
          <div className="grid grid-cols-2 gap-4">
            {/* Quality Setting */}
            <div>
              <label className="block text-white font-medium mb-2 text-sm">
                Quality
              </label>
              <select
                name="quality"
                value={formData.quality}
                onChange={handleChange}
                className="input-field text-sm"
                disabled={isGenerating}
              >
                <option value="low">Low (Fast)</option>
                <option value="medium">Medium</option>
                <option value="high">High (Slow)</option>
                <option value="ultra">Ultra (Very Slow)</option>
              </select>
            </div>

            {/* Format Setting */}
            <div>
              <label className="block text-white font-medium mb-2 text-sm">
                Format
              </label>
              <select
                name="format"
                value={formData.format}
                onChange={handleChange}
                className="input-field text-sm"
                disabled={isGenerating}
              >
                <option value="stl">STL (3D Printing)</option>
                <option value="obj">OBJ (Blender)</option>
                <option value="ply">PLY (Research)</option>
                <option value="gltf">GLTF (Web)</option>
              </select>
            </div>
          </div>

          <div className="text-xs text-white/50">
            Higher quality settings take longer but produce better results.
          </div>
        </div>
      )}

      {/* Generate Button */}
      <button
        type="submit"
        disabled={isGenerating || !formData.prompt.trim()}
        className="btn-primary w-full flex items-center justify-center gap-3 text-lg py-4"
      >
        {isGenerating ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
            Generating...
          </>
        ) : (
          <>
            <Send size={20} />
            Generate 3D Model
          </>
        )}
      </button>

      {/* Model Info */}
      {availableModels.length === 0 && (
        <div className="text-center text-yellow-400 text-sm p-4 rounded-lg bg-yellow-400/10">
          No AI models are currently available. Please check back later.
        </div>
      )}

      {formData.model_type === 'demo' && (
        <div className="text-center text-blue-400 text-sm p-3 rounded-lg bg-blue-400/10">
          Demo mode creates simple geometric shapes based on your description.
        </div>
      )}
    </form>
  )
}

export default GenerationForm