'use client'

import { useState, useEffect } from 'react'
import Header from '@/components/Header'
import AISearchModal from '@/components/AISearchModal'
import Hero from '@/components/Hero'
import MovieRow from '@/components/MovieRow'
import RecommendationModal from '@/components/RecommendationModal'
import SplashScreen from '@/components/SplashScreen'
import { Movie } from '@/lib/types'

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([])
  const [filteredMovies, setFilteredMovies] = useState<Movie[]>([])
  const [loading, setLoading] = useState(true)
  const [showRecommendation, setShowRecommendation] = useState(false)
  const [selectedMethod, setSelectedMethod] = useState<'method1' | 'method2' | null>(null)
  const [showSplash, setShowSplash] = useState(true)
  const [showAISearch, setShowAISearch] = useState(false)

  useEffect(() => {
    fetchMovies()
  }, [])

  const fetchMovies = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/movies')
      const data = await response.json()
      setMovies(data)
      setFilteredMovies(data)
    } catch (error) {
      console.error('Erro ao carregar filmes:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (query: string) => {
    if (!query.trim()) {
      setFilteredMovies(movies)
      return
    }
    
    const filtered = movies.filter(movie => 
      movie.title_en.toLowerCase().includes(query.toLowerCase()) ||
      movie.title_pt?.toLowerCase().includes(query.toLowerCase()) ||
      movie.genre.toLowerCase().includes(query.toLowerCase()) ||
      movie.sinopse.toLowerCase().includes(query.toLowerCase())
    )
    setFilteredMovies(filtered)
  }

  const handleRecommendation = (method: 'method1' | 'method2') => {
    setSelectedMethod(method)
    setShowRecommendation(true)
  }

  const handleSplashComplete = () => {
    setShowSplash(false)
  }

  // Mostrar splash screen primeiro
  if (showSplash) {
    return <SplashScreen onComplete={handleSplashComplete} />
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-netflix-black flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white text-lg">Carregando FiapFlix...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-netflix-black">
      <Header onRecommendation={handleRecommendation} onSearch={handleSearch} onAISearch={() => setShowAISearch(true)} />
      
      <main>
        <Hero movies={movies.slice(0, 5)} />
        
        <div className="px-4 md:px-8 lg:px-16 py-8">
          <MovieRow 
            title="Top 250 Filmes do IMDb" 
            movies={filteredMovies} 
            featured={true}
            id="filmes"
          />
          
          <MovieRow 
            title="Filmes de Ação" 
            movies={filteredMovies.filter(movie => 
              movie.genre?.toLowerCase().includes('action') || 
              movie.genre?.toLowerCase().includes('adventure')
            )} 
            id="series"
          />
          
          <MovieRow 
            title="Filmes de Drama" 
            movies={filteredMovies.filter(movie => 
              movie.genre?.toLowerCase().includes('drama')
            )} 
          />
          
          <MovieRow 
            title="Filmes de Crime" 
            movies={filteredMovies.filter(movie => 
              movie.genre?.toLowerCase().includes('crime')
            )} 
          />
        </div>
      </main>

      {showRecommendation && (
        <RecommendationModal
          method={selectedMethod!}
          movies={movies}
          onClose={() => {
            setShowRecommendation(false)
            setSelectedMethod(null)
          }}
        />
      )}

      {showAISearch && (
        <AISearchModal onClose={() => setShowAISearch(false)} />
      )}
    </div>
  )
}
