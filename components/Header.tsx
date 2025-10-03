'use client'

import { useState } from 'react'
import { Search, Menu, X, Sparkles } from 'lucide-react'

interface HeaderProps {
  onRecommendation: (method: 'method1' | 'method2') => void
  onSearch?: (query: string) => void
  onAISearch?: () => void
}

export default function Header({ onRecommendation, onSearch, onAISearch }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-black/80 to-transparent">
      <div className="flex items-center justify-between px-4 md:px-8 lg:px-16 py-4">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-netflix-red rounded flex items-center justify-center">
            <span className="text-white font-bold text-lg">F</span>
          </div>
          <span className="text-white font-bold text-xl">FiapFlix</span>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <button 
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="text-white hover:text-gray-300 transition-colors"
          >
            Início
          </button>
          <button 
            onClick={() => document.getElementById('filmes')?.scrollIntoView({ behavior: 'smooth' })}
            className="text-white hover:text-gray-300 transition-colors"
          >
            Filmes
          </button>
          <button 
            onClick={() => document.getElementById('series')?.scrollIntoView({ behavior: 'smooth' })}
            className="text-white hover:text-gray-300 transition-colors"
          >
            Séries
          </button>
          <button 
            onClick={() => onRecommendation('method1')}
            className="text-white hover:text-gray-300 transition-colors"
          >
            Minha Lista
          </button>
        </nav>

        {/* Actions */}
        <div className="flex items-center space-x-4">
          {/* Search */}
          <button
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            className="text-white hover:text-gray-300 transition-colors"
          >
            <Search size={20} />
          </button>

          {/* AI Recommendation Button */}
          <button
            onClick={() => onRecommendation('method1')}
            className="flex items-center space-x-2 bg-netflix-red text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
          >
            <Sparkles size={16} />
            <span className="hidden sm:inline">Recomendação IA</span>
          </button>

        {/* AI Search Quick */}
        {onAISearch && (
          <button
            onClick={onAISearch}
            className="hidden md:inline text-white hover:text-gray-300 transition-colors"
            title="Busca IA"
          >
            <span className="underline">Busca IA</span>
          </button>
        )}

          {/* Mobile Menu */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-white"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-netflix-black border-t border-gray-800">
          <div className="px-4 py-4 space-y-4">
            <a href="#" className="block text-white hover:text-gray-300">
              Início
            </a>
            <a href="#" className="block text-white hover:text-gray-300">
              Filmes
            </a>
            <a href="#" className="block text-white hover:text-gray-300">
              Séries
            </a>
            <a href="#" className="block text-white hover:text-gray-300">
              Minha Lista
            </a>
            <div className="pt-4 border-t border-gray-800">
              <button
                onClick={() => {
                  onRecommendation('method1')
                  setIsMenuOpen(false)
                }}
                className="flex items-center space-x-2 text-netflix-red hover:text-red-400"
              >
                <Sparkles size={16} />
                <span>Recomendação IA</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Search Bar */}
      {isSearchOpen && (
        <div className="px-4 md:px-8 lg:px-16 py-4 bg-netflix-black border-t border-gray-800">
          <div className="relative">
            <input
              type="text"
              placeholder="Buscar filmes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && onSearch) {
                  onSearch(searchQuery)
                }
              }}
              className="w-full bg-gray-800 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-netflix-red"
            />
            <button
              onClick={() => onSearch && onSearch(searchQuery)}
              className="absolute right-3 top-2.5 text-gray-400 hover:text-white transition-colors"
            >
              <Search size={20} />
            </button>
          </div>
        </div>
      )}
    </header>
  )
}
