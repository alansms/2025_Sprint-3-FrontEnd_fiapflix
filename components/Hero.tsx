'use client'

import { useState, useEffect } from 'react'
import { Play, Info, Star } from 'lucide-react'
import { Movie } from '@/lib/types'

interface HeroProps {
  movies: Movie[]
}

export default function Hero({ movies }: HeroProps) {
  const [currentMovie, setCurrentMovie] = useState<Movie | null>(null)
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    if (movies.length > 0) {
      setCurrentMovie(movies[0])
    }
  }, [movies])

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % movies.length)
      setCurrentMovie(movies[currentIndex])
    }, 5000)

    return () => clearInterval(interval)
  }, [movies, currentIndex])

  if (!currentMovie) {
    return (
      <div className="relative h-screen bg-netflix-black flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white text-lg">Carregando filme em destaque...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative h-screen overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url(${currentMovie.backdrop_url || '/api/placeholder/1920/1080'})`
        }}
      />

      {/* Content */}
      <div className="relative z-10 h-full flex items-center">
        <div className="px-4 md:px-8 lg:px-16 max-w-4xl">
          <div className="fade-in">
            {/* Movie Title */}
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-4 leading-tight">
              {currentMovie.title_en}
            </h1>

            {/* Movie Info */}
            <div className="flex items-center space-x-4 mb-6">
              <div className="flex items-center space-x-2">
                <Star className="text-yellow-400" size={20} fill="currentColor" />
                <span className="text-white text-lg font-semibold">
                  {currentMovie.rating}
                </span>
              </div>
              <span className="text-white text-lg">•</span>
              <span className="text-white text-lg">{currentMovie.year}</span>
              <span className="text-white text-lg">•</span>
              <span className="text-white text-lg">{currentMovie.genre}</span>
            </div>

            {/* Synopsis */}
            <p className="text-white text-lg md:text-xl mb-8 max-w-2xl leading-relaxed">
              {currentMovie.sinopse?.length > 200 
                ? `${currentMovie.sinopse.substring(0, 200)}...` 
                : currentMovie.sinopse
              }
            </p>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <button className="netflix-button flex items-center justify-center space-x-2 py-3 px-8 text-lg">
                <Play size={24} fill="currentColor" />
                <span>Assistir</span>
              </button>
              
              <button className="netflix-button-secondary flex items-center justify-center space-x-2 py-3 px-8 text-lg">
                <Info size={24} />
                <span>Mais Informações</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Movie Indicators */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {movies.slice(0, 5).map((_, index) => (
          <button
            key={index}
            onClick={() => {
              setCurrentIndex(index)
              setCurrentMovie(movies[index])
            }}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentIndex 
                ? 'bg-white scale-125' 
                : 'bg-white/50 hover:bg-white/75'
            }`}
          />
        ))}
      </div>
    </div>
  )
}
