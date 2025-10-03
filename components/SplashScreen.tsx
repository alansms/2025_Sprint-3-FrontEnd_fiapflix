'use client'

import { useState, useEffect, useRef } from 'react'
import { Play, SkipForward } from 'lucide-react'

interface SplashScreenProps {
  onComplete: () => void
}

export default function SplashScreen({ onComplete }: SplashScreenProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [showSkip, setShowSkip] = useState(false)
  const [progress, setProgress] = useState(0)
  const videoRef = useRef<HTMLVideoElement>(null)
  const skipTimeoutRef = useRef<NodeJS.Timeout>()

  useEffect(() => {
    // Iniciar o vídeo automaticamente após 5 segundos
    const autoPlayTimeout = setTimeout(() => {
      handlePlay()
    }, 5000)

    // Mostrar botão de pular após 3 segundos
    skipTimeoutRef.current = setTimeout(() => {
      setShowSkip(true)
    }, 3000)

    return () => {
      clearTimeout(autoPlayTimeout)
      if (skipTimeoutRef.current) {
        clearTimeout(skipTimeoutRef.current)
      }
    }
  }, [])

  const handlePlay = () => {
    if (videoRef.current) {
      videoRef.current.play()
      setIsPlaying(true)
    }
  }

  const handleSkip = () => {
    if (videoRef.current) {
      videoRef.current.pause()
    }
    onComplete()
  }

  const handleVideoEnd = () => {
    onComplete()
  }

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      const progress = (videoRef.current.currentTime / videoRef.current.duration) * 100
      setProgress(progress)
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-black flex items-center justify-center">
      {/* Video Container */}
      <div className="relative w-full h-full">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          onEnded={handleVideoEnd}
          onTimeUpdate={handleTimeUpdate}
          preload="metadata"
        >
          <source src="/videos/abertura.mp4" type="video/mp4" />
          Seu navegador não suporta vídeos.
        </video>

        {/* Overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/20 via-transparent to-black/40" />

        {/* Logo FiapFlix */}
        <div className="absolute top-8 left-1/2 transform -translate-x-1/2 text-center">
          <p className="text-xl md:text-2xl text-gray-300 animate-fade-in-delay">
            Sistema de Recomendação de Filmes com IA
          </p>
        </div>

        {/* Play Button */}
        {!isPlaying && (
          <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
            <button
              onClick={handlePlay}
              className="bg-netflix-red hover:bg-red-700 text-white p-6 rounded-full transition-all duration-300 hover:scale-110 flex items-center space-x-3"
            >
              <Play size={32} fill="currentColor" />
              <span className="text-lg font-semibold">Assistir Abertura</span>
            </button>
          </div>
        )}

        {/* Skip Button */}
        {showSkip && (
          <div className="absolute top-8 right-8">
            <button
              onClick={handleSkip}
              className="bg-black/50 hover:bg-black/70 text-white px-6 py-3 rounded-full transition-all duration-300 flex items-center space-x-2"
            >
              <SkipForward size={20} />
              <span>Pular</span>
            </button>
          </div>
        )}

        {/* Progress Bar */}
        {isPlaying && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-800">
            <div 
              className="h-full bg-netflix-red transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}

        {/* Loading Text */}
        {isPlaying && (
          <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
            <p className="text-white text-lg animate-pulse">
              Carregando FiapFlix...
            </p>
          </div>
        )}
      </div>

    </div>
  )
}
