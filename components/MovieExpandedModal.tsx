'use client'

import { useState, useEffect } from 'react'
import { X, Play, Info, Star, Calendar, Clock, Heart } from 'lucide-react'
import { Movie } from '@/lib/types'

interface MovieExpandedModalProps {
  movie: Movie | null
  onClose: () => void
  onPlay?: (movie: Movie) => void
  onDetails?: (movie: Movie) => void
}

export default function MovieExpandedModal({ movie, onClose, onPlay, onDetails }: MovieExpandedModalProps) {
  const [isFavorite, setIsFavorite] = useState(false)

  useEffect(() => {
    if (movie) {
      const favorites = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]')
      setIsFavorite(favorites.includes(movie.id))
    }
  }, [movie])

  const toggleFavorite = () => {
    if (!movie) return
    
    const favorites = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]')
    if (isFavorite) {
      const newFavorites = favorites.filter((id: string) => id !== movie.id)
      localStorage.setItem('fiapflix_favorites', JSON.stringify(newFavorites))
    } else {
      const newFavorites = [...favorites, movie.id]
      localStorage.setItem('fiapflix_favorites', JSON.stringify(newFavorites))
    }
    setIsFavorite(!isFavorite)
  }

  const handlePlay = () => {
    if (movie && onPlay) {
      onPlay(movie)
    }
  }

  const handleDetails = () => {
    if (movie && onDetails) {
      onDetails(movie)
    }
  }

  if (!movie) return null

  return (
    <div className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center" onClick={onClose}>
      <div 
        className="relative w-full h-full max-w-7xl max-h-[95vh] rounded-lg overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url(${movie.backdrop_url})`,
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-t from-black via-black/70 to-transparent" />
        </div>

        {/* Content */}
        <div className="relative z-10 h-full flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-6">
            <div className="flex items-center space-x-4">
              <h1 className="text-white text-2xl font-bold">FiapFlix</h1>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-300 transition-colors p-2 hover:bg-white/20 rounded"
            >
              <X size={24} />
            </button>
          </div>

          {/* Movie Info */}
          <div className="flex-1 flex items-center justify-center p-6">
            <div className="max-w-4xl w-full">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                {/* Movie Details */}
                <div className="space-y-6">
                  <div>
                    <h2 className="text-white text-4xl lg:text-6xl font-bold mb-4">
                      {movie.title_pt}
                    </h2>
                    <p className="text-gray-300 text-xl mb-6">{movie.title_en}</p>
                  </div>

                  <div className="flex items-center space-x-6 mb-6">
                    <div className="flex items-center space-x-2">
                      <Star className="text-yellow-400" size={24} />
                      <span className="text-white text-xl font-semibold">{movie.rating}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-gray-300">
                      <Calendar size={20} />
                      <span className="text-lg">{movie.year}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-gray-300">
                      <Clock size={20} />
                      <span className="text-lg">{movie.duration}</span>
                    </div>
                  </div>

                  <div className="mb-6">
                    <span className="bg-gray-800 text-white px-4 py-2 rounded-full text-lg">
                      {movie.genre}
                    </span>
                  </div>

                  <p className="text-gray-200 text-lg leading-relaxed mb-8">
                    {movie.sinopse}
                  </p>

                  <div className="flex space-x-4">
                    <button
                      onClick={handlePlay}
                      className="bg-netflix-red hover:bg-red-700 text-white px-8 py-4 rounded-lg flex items-center space-x-3 text-lg font-semibold transition-colors"
                    >
                      <Play size={24} />
                      <span>Assistir</span>
                    </button>
                    
                    <button
                      onClick={handleDetails}
                      className="bg-gray-600 hover:bg-gray-700 text-white px-8 py-4 rounded-lg flex items-center space-x-3 text-lg font-semibold transition-colors"
                    >
                      <Info size={24} />
                      <span>Mais Informações</span>
                    </button>
                    
                    <button
                      onClick={toggleFavorite}
                      className={`px-8 py-4 rounded-lg flex items-center space-x-3 text-lg font-semibold transition-colors ${
                        isFavorite 
                          ? 'bg-red-600 hover:bg-red-700 text-white' 
                          : 'bg-gray-600 hover:bg-gray-700 text-white'
                      }`}
                    >
                      <Heart size={24} className={isFavorite ? 'fill-current' : ''} />
                    </button>
                  </div>
                </div>

                {/* Movie Poster */}
                <div className="flex justify-center lg:justify-end">
                  <div className="relative group">
                    <img
                      src={movie.poster_url}
                      alt={movie.title_pt}
                      className="w-80 h-auto rounded-lg shadow-2xl"
                      onError={(e) => {
                        e.currentTarget.src = 'https://via.placeholder.com/320x480/1a1a1a/ffffff?text=Sem+Imagem'
                      }}
                    />
                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg flex items-center justify-center">
                      <button
                        onClick={handlePlay}
                        className="bg-netflix-red hover:bg-red-700 text-white px-6 py-3 rounded-full flex items-center space-x-2 transition-colors"
                      >
                        <Play size={20} />
                        <span>Assistir</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

