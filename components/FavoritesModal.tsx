'use client'

import { useState, useEffect } from 'react'
import { X, Heart, Star, Play, Info, Trash2 } from 'lucide-react'
import { Movie } from '@/lib/types'

interface FavoritesModalProps {
  onClose: () => void
  onMovieClick?: (movie: Movie) => void
  onMovieInfo?: (movie: Movie) => void
}

export default function FavoritesModal({ onClose, onMovieClick, onMovieInfo }: FavoritesModalProps) {
  const [favorites, setFavorites] = useState<Movie[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFavorites()
  }, [])

  const loadFavorites = async () => {
    try {
      setLoading(true)
      
      // Carregar IDs dos favoritos do localStorage
      const favoriteIds = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]')
      
      if (favoriteIds.length === 0) {
        setFavorites([])
        setLoading(false)
        return
      }

      // Carregar dados dos filmes
      const response = await fetch('/api/movies')
      const allMovies = await response.json()
      
      // Filtrar apenas os favoritos e remover duplicatas
      const favoriteMovies = allMovies.filter((movie: Movie) => 
        favoriteIds.includes(movie.id)
      )
      
      // Remover duplicatas por ID (caso ainda existam)
      const uniqueFavorites = favoriteMovies.filter((movie, index, self) => 
        index === self.findIndex(m => m.id === movie.id)
      )
      
      setFavorites(uniqueFavorites)
    } catch (error) {
      console.error('Erro ao carregar favoritos:', error)
      setFavorites([])
    } finally {
      setLoading(false)
    }
  }

  const removeFavorite = (movieId: string) => {
    const favoriteIds = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]')
    const newFavorites = favoriteIds.filter((id: string) => id !== movieId)
    localStorage.setItem('fiapflix_favorites', JSON.stringify(newFavorites))
    
    // Atualizar lista local
    setFavorites(favorites.filter(movie => movie.id !== movieId))
  }

  const handleMovieClick = (movie: Movie) => {
    if (onMovieClick) {
      onMovieClick(movie)
    }
  }

  const handleMovieInfo = (movie: Movie) => {
    if (onMovieInfo) {
      onMovieInfo(movie)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div 
        className="bg-gray-900 w-full max-w-6xl max-h-[90vh] rounded-lg overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-800">
          <div className="flex items-center space-x-3">
            <Heart size={24} className="text-netflix-red" />
            <h2 className="text-2xl font-bold text-white">Minha Lista</h2>
            <span className="bg-gray-700 text-gray-300 px-2 py-1 rounded-full text-sm">
              {favorites.length} {favorites.length === 1 ? 'filme' : 'filmes'}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-700 rounded"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <div className="spinner mx-auto mb-4"></div>
                <p className="text-gray-400">Carregando sua lista...</p>
              </div>
            </div>
          ) : favorites.length === 0 ? (
            <div className="text-center py-16">
              <Heart size={64} className="mx-auto text-gray-600 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Sua lista está vazia</h3>
              <p className="text-gray-400 mb-6">
                Adicione filmes aos seus favoritos clicando no ícone de coração
              </p>
              <button
                onClick={onClose}
                className="bg-netflix-red text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors"
              >
                Explorar Filmes
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {favorites.map((movie) => (
                <div key={movie.id} className="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-700 transition-colors">
                  {/* Movie Poster */}
                  <div className="relative aspect-[2/3] bg-gray-700">
                    {movie.poster_url ? (
                      <img
                        src={movie.poster_url}
                        alt={movie.title_pt}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-600 to-gray-800">
                        <Play size={48} className="text-gray-400" />
                      </div>
                    )}
                    
                    {/* Overlay on Hover */}
                    <div className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center space-x-2">
                      <button 
                        onClick={() => handleMovieClick(movie)}
                        className="bg-netflix-red text-white p-3 rounded-full hover:bg-red-700 transition-colors"
                        title="Assistir"
                      >
                        <Play size={20} fill="currentColor" />
                      </button>
                      <button 
                        onClick={() => handleMovieInfo(movie)}
                        className="bg-gray-600 text-white p-3 rounded-full hover:bg-gray-700 transition-colors"
                        title="Mais Informações"
                      >
                        <Info size={20} />
                      </button>
                    </div>

                    {/* Remove from Favorites */}
                    <button
                      onClick={() => removeFavorite(movie.id)}
                      className="absolute top-2 right-2 bg-black/70 text-red-400 p-2 rounded-full hover:bg-red-500 hover:text-white transition-colors"
                      title="Remover dos Favoritos"
                    >
                      <Trash2 size={16} />
                    </button>

                    {/* Rating Badge */}
                    <div className="absolute top-2 left-2 bg-black/70 text-white px-2 py-1 rounded flex items-center space-x-1">
                      <Star size={12} fill="currentColor" className="text-yellow-400" />
                      <span className="text-xs font-semibold">{movie.rating}</span>
                    </div>
                  </div>

                  {/* Movie Info */}
                  <div className="p-4">
                    <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2">
                      {movie.title_pt}
                    </h3>
                    <p className="text-gray-400 text-xs mb-2 line-clamp-1">
                      {movie.title_en} • {movie.year}
                    </p>
                    <p className="text-gray-500 text-xs line-clamp-2">
                      {movie.genre}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {favorites.length > 0 && (
          <div className="border-t border-gray-800 p-6">
            <div className="flex items-center justify-between">
              <div className="text-gray-400 text-sm">
                {favorites.length} {favorites.length === 1 ? 'filme salvo' : 'filmes salvos'} na sua lista
              </div>
              <button
                onClick={onClose}
                className="bg-gray-700 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors"
              >
                Fechar
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

