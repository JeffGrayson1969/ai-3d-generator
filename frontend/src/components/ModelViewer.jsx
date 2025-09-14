import React, { useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stage, Environment } from '@react-three/drei'
import * as THREE from 'three'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'
import { Loader } from 'lucide-react'

// 3D Model Component
const Model3D = ({ url, onLoad, onError }) => {
  const meshRef = useRef()
  const [geometry, setGeometry] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!url) {
      setGeometry(null)
      return
    }

    setLoading(true)
    const loader = new STLLoader()

    loader.load(
      url,
      (geometry) => {
        // Center the geometry
        geometry.computeBoundingBox()
        const center = new THREE.Vector3()
        geometry.boundingBox.getCenter(center)
        geometry.translate(-center.x, -center.y, -center.z)

        // Normalize size
        const size = new THREE.Vector3()
        geometry.boundingBox.getSize(size)
        const maxDim = Math.max(size.x, size.y, size.z)
        const scale = 2 / maxDim
        geometry.scale(scale, scale, scale)

        setGeometry(geometry)
        setLoading(false)
        onLoad?.()
      },
      (progress) => {
        // Loading progress
        console.log('Loading progress:', progress)
      },
      (error) => {
        console.error('Error loading model:', error)
        setLoading(false)
        onError?.(error)
      }
    )
  }, [url, onLoad, onError])

  // Rotate the model slowly
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.2
    }
  })

  if (!geometry) return null

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial
        color="#667eea"
        metalness={0.3}
        roughness={0.4}
      />
    </mesh>
  )
}

// Default Cube Component (shown when no model loaded)
const DefaultCube = () => {
  const meshRef = useRef()

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta * 0.3
    meshRef.current.rotation.y += delta * 0.2
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial
        color="#764ba2"
        metalness={0.2}
        roughness={0.5}
        transparent
        opacity={0.7}
      />
    </mesh>
  )
}

// Loading Spinner Component
const LoadingSpinner = () => {
  const meshRef = useRef()

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta * 2
    meshRef.current.rotation.y += delta * 3
  })

  return (
    <mesh ref={meshRef}>
      <octahedronGeometry args={[0.5]} />
      <meshStandardMaterial
        color="#ffffff"
        emissive="#667eea"
        emissiveIntensity={0.3}
        transparent
        opacity={0.8}
      />
    </mesh>
  )
}

// Main ModelViewer Component
const ModelViewer = ({ modelUrl, isLoading }) => {
  const [modelLoadError, setModelLoadError] = useState(false)
  const [modelLoaded, setModelLoaded] = useState(false)

  const handleModelLoad = () => {
    setModelLoaded(true)
    setModelLoadError(false)
  }

  const handleModelError = (error) => {
    setModelLoadError(true)
    setModelLoaded(false)
    console.error('Model loading error:', error)
  }

  // Reset states when modelUrl changes
  useEffect(() => {
    setModelLoaded(false)
    setModelLoadError(false)
  }, [modelUrl])

  return (
    <div className="w-full h-full relative bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg overflow-hidden">
      <Canvas
        camera={{ position: [3, 3, 3], fov: 50 }}
        gl={{ antialias: true, alpha: true }}
        shadows
      >
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />

        {/* Environment and Stage */}
        <Environment preset="studio" />

        <Stage
          contactShadow={{ opacity: 0.2, blur: 2 }}
          shadows={{ type: 'contact', opacity: 0.2, blur: 3 }}
          adjustCamera={false}
        >
          {/* Model Content */}
          {isLoading ? (
            <LoadingSpinner />
          ) : modelUrl && !modelLoadError ? (
            <Model3D
              url={modelUrl}
              onLoad={handleModelLoad}
              onError={handleModelError}
            />
          ) : (
            <DefaultCube />
          )}
        </Stage>

        {/* Camera Controls */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={!modelLoaded && !isLoading}
          autoRotateSpeed={2}
        />
      </Canvas>

      {/* Overlay Messages */}
      <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
        {isLoading && (
          <div className="bg-black/50 rounded-lg p-4 flex items-center gap-3 text-white backdrop-blur-sm">
            <Loader className="animate-spin" size={20} />
            <span>Generating 3D model...</span>
          </div>
        )}

        {modelLoadError && (
          <div className="bg-red-900/50 rounded-lg p-4 text-white backdrop-blur-sm">
            <span>Failed to load 3D model</span>
          </div>
        )}

        {!modelUrl && !isLoading && (
          <div className="text-white/50 text-center">
            <div className="text-6xl mb-4">🎨</div>
            <div className="text-lg font-medium">No model loaded</div>
            <div className="text-sm">Generate a 3D model to see it here</div>
          </div>
        )}
      </div>

      {/* Controls Info */}
      <div className="absolute bottom-4 left-4 text-xs text-white/50 pointer-events-none">
        <div>Left click + drag: Rotate</div>
        <div>Right click + drag: Pan</div>
        <div>Scroll: Zoom</div>
      </div>
    </div>
  )
}

export default ModelViewer