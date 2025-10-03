'use client'

import { useState } from 'react'
import { X, Sparkles, Loader2, Wand2, RefreshCw } from 'lucide-react'

interface AIEnhancementModalProps {
  onClose: () => void
  movie?: {
    title: string
    year: number
    genre: string
    synopsis: string
  }
}

interface EnhancementResult {
  enhanced_synopsis: string
  method: string
  timestamp: number
  original_synopsis: string
}

export default function AIEnhancementModal({ onClose, movie }: AIEnhancementModalProps) {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<EnhancementResult | null>(null)
  const [error, setError] = useState<string>('')
  const [style, setStyle] = useState('cinematic')

  const enhanceSynopsis = async () => {
    if (!movie) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('/api/enhance-synopsis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: movie.title,
          year: movie.year,
          genre: movie.genre,
          synopsis: movie.synopsis,
          style: style
        })
      })

      if (!response.ok) {
        throw new Error('Erro ao enriquecer sinopse')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Erro ao enriquecer sinopse. Tente novamente.')
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  const styles = [
    { value: 'cinematic', label: 'Cinematográfico' },
    { value: 'dramatic', label: 'Dramático' },
    { value: 'action', label: 'Ação' },
    { value: 'romantic', label: 'Romântico' }
  ]

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center space-x-3">
            <Sparkles className="text-yellow-400" size={24} />
            <h2 className="text-2xl font-bold text-white">
              Enriquecimento com IA Generativa
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {movie && (
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">
                {movie.title} ({movie.year})
              </h3>
              <p className="text-gray-300 text-sm mb-2">
                <span className="font-medium">Gênero:</span> {movie.genre}
              </p>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-300">
                  Estilo de Enriquecimento:
                </label>
                <select
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full bg-gray-700 text-white rounded-lg px-3 py-2 border border-gray-600 focus:border-yellow-400 focus:outline-none"
                >
                  {styles.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          )}

          {/* Sinopse Original */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
              <span className="mr-2">📝</span>
              Sinopse Original
            </h4>
            <p className="text-gray-300 leading-relaxed">
              {movie?.synopsis || 'Nenhuma sinopse disponível'}
            </p>
          </div>

          {/* Botão de Enriquecimento */}
          <div className="flex justify-center">
            <button
              onClick={enhanceSynopsis}
              disabled={loading}
              className="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  <span>Enriquecendo com IA...</span>
                </>
              ) : (
                <>
                  <Wand2 size={20} />
                  <span>Enriquecer Sinopse</span>
                </>
              )}
            </button>
          </div>

          {/* Resultado */}
          {result && (
            <div className="bg-gradient-to-r from-green-900 to-blue-900 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
                <Sparkles className="mr-2 text-yellow-400" size={20} />
                Sinopse Enriquecida
              </h4>
              <p className="text-gray-100 leading-relaxed mb-4">
                {result.enhanced_synopsis}
              </p>
              <div className="flex items-center justify-between text-sm text-gray-300">
                <span>Método: {result.method}</span>
                <button
                  onClick={enhanceSynopsis}
                  className="flex items-center space-x-1 text-yellow-400 hover:text-yellow-300 transition-colors"
                >
                  <RefreshCw size={16} />
                  <span>Reenriquecer</span>
                </button>
              </div>
            </div>
          )}

          {/* Erro */}
          {error && (
            <div className="bg-red-900 border border-red-700 rounded-lg p-4">
              <p className="text-red-200">{error}</p>
            </div>
          )}

          {/* Informações sobre IA Generativa */}
          <div className="bg-blue-900 border border-blue-700 rounded-lg p-4">
            <h4 className="text-lg font-semibold text-white mb-2 flex items-center">
              <span className="mr-2">🤖</span>
              Sobre o Enriquecimento com IA
            </h4>
            <div className="text-blue-100 text-sm space-y-2">
              <p>
                • <strong>IA Generativa:</strong> Enriquece sinopses usando inteligência artificial
              </p>
              <p>
                • <strong>Múltiplos Estilos:</strong> Cinematográfico, dramático, ação, romântico
              </p>
              <p>
                • <strong>Fallback Local:</strong> Sistema funciona mesmo sem API externa
              </p>
              <p>
                • <strong>Ponto Extra:</strong> Funcionalidade opcional para enriquecimento
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-700">
          <button
            onClick={onClose}
            className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  )
}
