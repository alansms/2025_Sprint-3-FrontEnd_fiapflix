'use client'

import { useState, useEffect } from 'react'
import { X, Search, Loader2 } from 'lucide-react'
import { Movie } from '@/lib/types'

interface AISearchModalProps {
  onClose: () => void
}

interface AISearchResponse {
  query: string
  results: Movie[]
  natural_response: string
  analysis: any
  timestamp: string
}

export default function AISearchModal({ onClose }: AISearchModalProps) {
  const [query, setQuery] = useState('Filmes de drama com rating alto')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')
  const [data, setData] = useState<AISearchResponse | null>(null)

  // Fechar modal com tecla ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [onClose])

  const runSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/api/ai-search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      if (!res.ok) throw new Error('Falha na busca IA')
      const json = await res.json()
      setData(json)
    } catch (e: any) {
      setError('Erro ao processar busca. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-2 sm:p-4">
      <div className="bg-gray-900 w-full max-w-6xl max-h-[95vh] rounded-lg overflow-hidden flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-gray-800 flex-shrink-0">
          <h2 className="text-white font-semibold text-lg">Busca IA - FiapFlix</h2>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-white transition-colors p-1 hover:bg-gray-700 rounded"
            title="Fechar"
          >
            <X size={22} />
          </button>
        </div>

        <div className="p-4 space-y-4 overflow-y-auto flex-1">
          <div className="relative">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') runSearch() }}
              placeholder="Pergunte algo: filmes de drama com rating alto, melhores filmes de 1990 a 2000, filmes do Nolan..."
              className="w-full bg-gray-800 text-white px-4 py-3 pr-12 rounded border border-gray-700 focus:outline-none focus:border-netflix-red"
            />
            <button onClick={runSearch} className="absolute right-3 top-2.5 text-gray-300 hover:text-white">
              {loading ? <Loader2 size={20} className="animate-spin" /> : <Search size={20} />}
            </button>
          </div>

          {error && (
            <div className="bg-red-900/40 border border-red-800 text-red-200 px-3 py-2 rounded">
              {error}
            </div>
          )}

          {data && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
              <div className="space-y-3">
                <h3 className="text-white font-semibold">Resposta da IA</h3>
                <div className="bg-gray-800 rounded p-4 text-gray-200 whitespace-pre-wrap text-sm max-h-48 lg:max-h-60 overflow-y-auto">
                  {data.natural_response}
                </div>
                <div className="bg-gray-800 rounded p-4">
                  <h4 className="text-white font-semibold mb-2">Análise da Consulta</h4>
                  <div className="text-sm text-gray-300 space-y-1">
                    <p><span className="text-gray-400">Intenção:</span> {data.analysis?.detected_intent}</p>
                    <p><span className="text-gray-400">Palavras-chave:</span> {data.analysis?.extracted_keywords?.join(', ')}</p>
                    <p><span className="text-gray-400">Filtros:</span> {JSON.stringify(data.analysis?.applied_filters)}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-white font-semibold">Resultados</h3>
                  <span className="text-gray-400 text-sm">{data.results?.length} filmes encontrados</span>
                </div>
                <div className="space-y-3 max-h-80 lg:max-h-96 overflow-y-auto pr-2">
                  {data.results?.map((m) => (
                    <div key={m.id} className="bg-gray-800 rounded p-3 hover:bg-gray-700 transition-colors">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-white font-semibold truncate">{m.title_pt}</p>
                          <p className="text-gray-400 text-sm truncate">{m.title_en} • {m.year} • {m.genre}</p>
                          <p className="text-gray-300 text-sm mt-2 line-clamp-2">{m.sinopse}</p>
                        </div>
                        <span className="text-yellow-400 font-semibold flex-shrink-0">{m.rating}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Botão de fechar adicional quando há resultados */}
          {data && (
            <div className="flex justify-center pt-4 border-t border-gray-800">
              <button 
                onClick={onClose}
                className="bg-netflix-red hover:bg-red-700 text-white px-6 py-2 rounded transition-colors"
              >
                Fechar
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}




