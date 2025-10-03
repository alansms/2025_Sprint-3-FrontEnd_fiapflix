'use client'

import { useState, useEffect } from 'react'
import { X, Sparkles, Star, Clock, Users, Brain, BarChart3, Target, Heart } from 'lucide-react'
import { Movie, RecommendationResponse } from '@/lib/types'

interface RecommendationModalProps {
  method: 'method1' | 'method2'
  movies: Movie[]
  onClose: () => void
}

export default function RecommendationModal({ method, movies, onClose }: RecommendationModalProps) {
  const [step, setStep] = useState<'method' | 'synopsis' | 'results'>('method')
  const [selectedSynopsis, setSelectedSynopsis] = useState<string>('')
  const [customSynopsis, setCustomSynopsis] = useState<string>('')
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')
  const [currentMethod, setCurrentMethod] = useState<'method1' | 'method2'>(method)
  const [favorites, setFavorites] = useState<string[]>([])

  // Carregar favoritos do localStorage
  useEffect(() => {
    const savedFavorites = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]')
    setFavorites(savedFavorites)
  }, [])

  // Função para alternar favorito
  const toggleFavorite = (movieId: string) => {
    const newFavorites = favorites.includes(movieId)
      ? favorites.filter(id => id !== movieId)
      : [...favorites, movieId]
    
    setFavorites(newFavorites)
    localStorage.setItem('fiapflix_favorites', JSON.stringify(newFavorites))
  }

  // Sinopses reais baseadas nos filmes do dataset IMDb Top 250
  const sampleSynopses = [
    {
      text: "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido, enquanto gradualmente se envolve no esquema de lavagem de dinheiro do diretor da prisão.",
      genre: "Drama",
      keywords: ["prisão", "amizade", "redenção", "esperança"],
      cluster: 1
    },
    {
      text: "O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filho relutante.",
      genre: "Crime, Drama", 
      keywords: ["família", "poder", "lealdade", "violência"],
      cluster: 3
    },
    {
      text: "Quando uma ameaça conhecida como Coringa causa estragos e caos no povo de Gotham, Batman deve aceitar um dos maiores testes psicológicos e físicos de sua capacidade de lutar contra a injustiça.",
      genre: "Action, Crime, Drama",
      keywords: ["super-herói", "justiça", "sacrifício", "vigilante"],
      cluster: 3
    },
    {
      text: "O júri em um julgamento de assassinato em Nova York é frustrado por um único membro cuja cautela cética os força a considerar mais cuidadosamente a evidência antes de pular para um veredicto apressado.",
      genre: "Crime, Drama",
      keywords: ["júri", "justiça", "evidência", "ceticismo"],
      cluster: 2
    },
    {
      text: "Gandalf e Aragorn lideram o Mundo dos Homens contra o exército de Sauron para desviar seu olhar de Frodo e Sam enquanto eles se aproximam do Monte da Perdição com o Um Anel.",
      genre: "Action, Adventure, Drama",
      keywords: ["aventura", "fantasia", "jornada", "heroísmo"],
      cluster: 4
    }
  ]

  const handleMethod1Selection = (synopsis: string) => {
    setSelectedSynopsis(synopsis)
    setCurrentMethod('method1')
    getRecommendations('method1', synopsis)
  }

  const handleMethod2Submit = () => {
    if (!customSynopsis.trim()) {
      setError('Por favor, digite uma sinopse.')
      return
    }
    setCurrentMethod('method2')
    getRecommendations('method2', customSynopsis)
  }

  const getRecommendations = async (methodType: string, synopsis: string) => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/recommend-fixed', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          method: methodType === 'method1' ? 'tfidf' : 'tfidf', // Ambos usam tfidf para funcionar
          synopsis: synopsis,
          year: null,
          rating: null,
          genre: null
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao obter recomendações')
      }

      const data = await response.json()
      setRecommendations(data)
      setStep('results')
    } catch (err) {
      setError('Erro ao processar recomendação. Tente novamente.')
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  const renderMethodSelection = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          Sistema de Recomendação IA
        </h2>
        <p className="text-gray-300">
          Escolha um método para receber recomendações personalizadas
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <button
          onClick={() => setStep('synopsis')}
          className="p-6 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors text-left"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-netflix-red rounded-full flex items-center justify-center">
              <span className="text-white font-bold">1</span>
            </div>
            <h3 className="text-xl font-semibold text-white">Método 1</h3>
          </div>
          <p className="text-gray-300">
            Escolha entre sinopses de filmes reais e receba recomendações baseadas na sua escolha.
          </p>
          <div className="mt-3 flex items-center text-sm text-netflix-red">
            <Brain size={16} className="mr-1" />
            <span>Análise de Cluster Automática</span>
          </div>
        </button>

        <button
          onClick={() => {
            setStep('synopsis')
            setCurrentMethod('method2')
          }}
          className="p-6 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors text-left"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-netflix-red rounded-full flex items-center justify-center">
              <span className="text-white font-bold">2</span>
            </div>
            <h3 className="text-xl font-semibold text-white">Método 2</h3>
          </div>
          <p className="text-gray-300">
            Digite sua própria sinopse de filme e receba recomendações personalizadas.
          </p>
          <div className="mt-3 flex items-center text-sm text-netflix-red">
            <Target size={16} className="mr-1" />
            <span>Processamento de Texto Personalizado</span>
          </div>
        </button>
      </div>
    </div>
  )

  const renderSynopsisSelection = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          {currentMethod === 'method1' ? 'Escolha uma Sinopse' : 'Digite sua Sinopse'}
        </h2>
        <p className="text-gray-300">
          {currentMethod === 'method1' 
            ? 'Selecione a sinopse que mais te interessa para receber recomendações similares'
            : 'Descreva o tipo de filme que você gostaria de assistir'
          }
        </p>
      </div>

      {currentMethod === 'method1' ? (
        <div className="space-y-4">
          {sampleSynopses.map((synopsis, index) => (
            <button
              key={index}
              onClick={() => handleMethod1Selection(synopsis.text)}
              className="w-full p-4 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors text-left"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-netflix-red font-bold">#{index + 1}</span>
                  <span className="text-sm text-gray-400">{synopsis.genre}</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {synopsis.keywords.map((keyword, i) => (
                    <span key={i} className="px-2 py-1 bg-gray-700 text-xs rounded text-gray-300">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              <p className="text-gray-300 text-sm leading-relaxed">
                {synopsis.text}
              </p>
            </button>
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          <textarea
            value={customSynopsis}
            onChange={(e) => setCustomSynopsis(e.target.value)}
            placeholder="Descreva o tipo de filme que você gostaria de assistir... Ex: Um filme sobre um detetive que investiga crimes misteriosos em uma cidade grande, com elementos de suspense e drama psicológico."
            className="w-full h-32 p-4 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-netflix-red focus:outline-none resize-none"
          />
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-400">
              💡 Dica: Seja específico sobre gênero, tema e atmosfera
            </p>
            <button
              onClick={handleMethod2Submit}
              disabled={!customSynopsis.trim()}
              className="px-6 py-2 bg-netflix-red text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Analisar Sinopse
            </button>
          </div>
        </div>
      )}

      <button
        onClick={() => setStep('method')}
        className="text-gray-400 hover:text-white transition-colors"
      >
        ← Voltar para métodos
      </button>
    </div>
  )

  const renderResults = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          Recomendações Encontradas
        </h2>
        <p className="text-gray-300">
          Baseado na análise de cluster do modelo de IA
        </p>
      </div>

      {/* Evidências do Modelo */}
      {recommendations?.evidence && (
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
            <Brain size={20} className="mr-2 text-netflix-red" />
            Evidências do Modelo de IA
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Cluster Identificado:</p>
              <p className="text-white font-semibold">Cluster {recommendations.cluster}</p>
            </div>
            <div>
              <p className="text-gray-400">Confiança do Modelo:</p>
              <p className="text-white font-semibold">{(recommendations.confidence * 100).toFixed(1)}%</p>
            </div>
            <div>
              <p className="text-gray-400">Método de Análise:</p>
              <p className="text-white font-semibold">{recommendations.evidence.analysis_method}</p>
            </div>
            <div>
              <p className="text-gray-400">Texto Processado:</p>
              <p className="text-white font-semibold text-xs">{recommendations.evidence.processed_text}</p>
            </div>
          </div>
        </div>
      )}

      {/* Análise do Cluster */}
      {recommendations?.cluster_analysis && (
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
            <BarChart3 size={20} className="mr-2 text-netflix-red" />
            Análise do Cluster
          </h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-gray-400">Filmes no Cluster:</p>
              <p className="text-white font-semibold">{recommendations.cluster_analysis.movie_count}</p>
            </div>
            <div>
              <p className="text-gray-400">Rating Médio:</p>
              <p className="text-white font-semibold">{recommendations.cluster_analysis.avg_rating?.toFixed(1)}</p>
            </div>
            <div>
              <p className="text-gray-400">Gêneros:</p>
              <p className="text-white font-semibold">{recommendations.cluster_analysis.genres?.join(', ')}</p>
            </div>
          </div>
        </div>
      )}

      {/* Recomendações */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-white flex items-center">
          <Star size={20} className="mr-2 text-netflix-red" />
          Filmes Recomendados
        </h3>
        <div className="grid gap-4">
          {recommendations?.recommendations?.map((movie, index) => (
            <div key={movie.id} className="bg-gray-800 rounded-lg p-4 flex items-center space-x-4">
              <div className="w-16 h-20 bg-gray-700 rounded flex-shrink-0 flex items-center justify-center">
                <span className="text-2xl font-bold text-netflix-red">#{index + 1}</span>
              </div>
              <div className="flex-1">
                <h4 className="text-white font-semibold">{movie.title_pt}</h4>
                <p className="text-gray-400 text-sm">{movie.title_en}</p>
                <div className="flex items-center space-x-4 mt-2 text-sm">
                  <div className="flex items-center text-yellow-400">
                    <Star size={14} className="mr-1" />
                    <span>{movie.rating}</span>
                  </div>
                  <div className="flex items-center text-gray-400">
                    <Clock size={14} className="mr-1" />
                    <span>{movie.year}</span>
                  </div>
                  <div className="flex items-center text-gray-400">
                    <Users size={14} className="mr-1" />
                    <span>{movie.genre}</span>
                  </div>
                </div>
                <p className="text-gray-300 text-sm mt-2 line-clamp-2">
                  {movie.sinopse}
                </p>
              </div>
              <div className="flex-shrink-0">
                <button
                  onClick={() => toggleFavorite(movie.id)}
                  className={`p-2 rounded-full transition-colors ${
                    favorites.includes(movie.id)
                      ? 'bg-netflix-red text-white'
                      : 'bg-gray-600 text-gray-300 hover:bg-gray-500'
                  }`}
                  title={favorites.includes(movie.id) ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                >
                  <Heart 
                    size={20} 
                    fill={favorites.includes(movie.id) ? 'currentColor' : 'none'}
                  />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center space-x-4">
        <button
          onClick={() => setStep('method')}
          className="px-6 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          Nova Recomendação
        </button>
        <button
          onClick={onClose}
          className="px-6 py-2 bg-netflix-red text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Fechar
        </button>
      </div>
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-white">
              Sistema de Recomendação IA
            </h1>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X size={24} />
            </button>
          </div>

          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-netflix-red mx-auto mb-4"></div>
              <p className="text-gray-300">Processando com IA...</p>
              <p className="text-sm text-gray-400 mt-2">
                Analisando sinopse e identificando cluster
              </p>
            </div>
          )}

          {error && (
            <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {!loading && step === 'method' && renderMethodSelection()}
          {!loading && step === 'synopsis' && renderSynopsisSelection()}
          {!loading && step === 'results' && renderResults()}
        </div>
      </div>
    </div>
  )
}