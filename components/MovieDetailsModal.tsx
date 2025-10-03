'use client'

import { useState, useEffect } from 'react'
import { X, Star, Calendar, Clock, Users, Award, Play, Heart } from 'lucide-react'
import { Movie } from '@/lib/types'

interface MovieDetailsModalProps {
  movie: Movie | null
  onClose: () => void
  onPlay?: (movie: Movie) => void
}

export default function MovieDetailsModal({ movie, onClose, onPlay }: MovieDetailsModalProps) {
  const [isFavorite, setIsFavorite] = useState(false)

  useEffect(() => {
    if (movie) {
      // Verificar se o filme está nos favoritos
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

  if (!movie) return null

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div 
        className="bg-gray-900 w-full max-w-4xl max-h-[90vh] rounded-lg overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <h2 className="text-white font-bold text-xl">Detalhes do Filme</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-700 rounded"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="flex flex-col lg:flex-row">
            {/* Poster */}
            <div className="lg:w-1/3 p-6">
              <div className="relative group">
                <img
                  src={movie.poster_url}
                  alt={movie.title_pt}
                  className="w-full rounded-lg shadow-2xl"
                  onError={(e) => {
                    e.currentTarget.src = 'https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Sem+Imagem'
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

            {/* Details */}
            <div className="lg:w-2/3 p-6">
              <div className="space-y-6">
                {/* Title and Rating */}
                <div>
                  <h1 className="text-white text-3xl font-bold mb-2">{movie.title_pt}</h1>
                  <p className="text-gray-400 text-lg mb-4">{movie.title_en}</p>
                  
                  <div className="flex items-center space-x-4 mb-4">
                    <div className="flex items-center space-x-1">
                      <Star className="text-yellow-400" size={20} />
                      <span className="text-white font-semibold">{movie.rating}</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-400">
                      <Calendar size={16} />
                      <span>{movie.year}</span>
                    </div>
                    <div className="flex items-center space-x-1 text-gray-400">
                      <Clock size={16} />
                      <span>{movie.duration}</span>
                    </div>
                  </div>
                </div>

                {/* Genre */}
                <div>
                  <span className="bg-gray-800 text-white px-3 py-1 rounded-full text-sm">
                    {movie.genre}
                  </span>
                </div>

                {/* Synopsis */}
                <div>
                  <h3 className="text-white font-semibold text-lg mb-2">Sinopse</h3>
                  <p className="text-gray-300 leading-relaxed">{movie.sinopse}</p>
                </div>

                {/* Cast and Director */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-white font-semibold mb-2 flex items-center">
                      <Users size={16} className="mr-2" />
                      Elenco
                    </h4>
                    <p className="text-gray-300 text-sm">{movie.cast}</p>
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-2 flex items-center">
                      <Award size={16} className="mr-2" />
                      Diretor
                    </h4>
                    <p className="text-gray-300 text-sm">{movie.director}</p>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-4 pt-4">
                  <button
                    onClick={handlePlay}
                    className="bg-netflix-red hover:bg-red-700 text-white px-8 py-3 rounded flex items-center space-x-2 transition-colors"
                  >
                    <Play size={20} />
                    <span>Assistir</span>
                  </button>
                  
                  <button
                    onClick={toggleFavorite}
                    className={`px-8 py-3 rounded flex items-center space-x-2 transition-colors ${
                      isFavorite 
                        ? 'bg-red-600 hover:bg-red-700 text-white' 
                        : 'bg-gray-700 hover:bg-gray-600 text-white'
                    }`}
                  >
                    <Heart size={20} className={isFavorite ? 'fill-current' : ''} />
                    <span>{isFavorite ? 'Favorito' : 'Adicionar aos Favoritos'}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
