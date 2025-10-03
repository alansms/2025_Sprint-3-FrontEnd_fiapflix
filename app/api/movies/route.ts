import { NextResponse } from 'next/server'
import { Movie } from '@/lib/types'
import fs from 'fs'
import path from 'path'

// Cache para evitar chamadas repetidas ao OMDb
const imageCache = new Map<string, string>()
const OMDB_API_KEY = '668159f8'

// Função para buscar poster do OMDb
async function fetchOMDbPoster(title: string, year: number): Promise<string> {
  const cacheKey = `${title}_${year}`
  
  // Verificar cache
  if (imageCache.has(cacheKey)) {
    return imageCache.get(cacheKey)!
  }
  
  try {
    const response = await fetch(
      `http://www.omdbapi.com/?apikey=${OMDB_API_KEY}&t=${encodeURIComponent(title)}&y=${year}&type=movie`
    )
    
    if (!response.ok) {
      throw new Error('Falha ao buscar do OMDb')
    }
    
    const data = await response.json()
    
    if (data.Response === 'True' && data.Poster && data.Poster !== 'N/A') {
      imageCache.set(cacheKey, data.Poster)
      return data.Poster
    }
  } catch (error) {
    console.error(`❌ Erro ao buscar poster para ${title}:`, error)
  }
  
  // Fallback para placeholder
  return `https://picsum.photos/seed/${title.replace(/\s+/g, '')}/500/750`
}

// Carregar dados reais do IMDb
let realMovies: Movie[] = []

try {
  const completeDataPath = path.join(process.cwd(), 'imdb_100plus_movies_complete.json')
  const completeData = fs.readFileSync(completeDataPath, 'utf-8')
  realMovies = JSON.parse(completeData)
  console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset completo)`)
} catch (error) {
  try {
    const realDataPath = path.join(process.cwd(), 'imdb_100plus_movies_real.json')
    const realData = fs.readFileSync(realDataPath, 'utf-8')
    realMovies = JSON.parse(realData)
    console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset real)`)
  } catch (fallbackError) {
    try {
      const expandedDataPath = path.join(process.cwd(), 'imdb_50plus_movies.json')
      const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
      realMovies = JSON.parse(expandedData)
      console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset 50+)`)
    } catch (thirdFallbackError) {
      console.log('⚠️ Usando dados mock como fallback')
    }
  }
}

export async function GET() {
  try {
    // Simular delay de carregamento
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Enriquecer filmes com posters do OMDb (apenas para os primeiros 10 para não sobrecarregar)
    const enrichedMovies = await Promise.all(
      realMovies.slice(0, 50).map(async (movie) => {
        // Se já tem poster válido, manter
        if (movie.poster_url && !movie.poster_url.includes('9gk7adHYeDvHkCSEqAvQNLV5nfge')) {
          return movie
        }
        
        // Buscar do OMDb
        const omdbPoster = await fetchOMDbPoster(movie.title_en, movie.year)
        
        return {
          ...movie,
          poster_url: omdbPoster,
          backdrop_url: omdbPoster
        }
      })
    )
    
    console.log(`✅ Enriquecidos ${enrichedMovies.length} filmes com posters do OMDb`)
    
    return NextResponse.json(enrichedMovies)
  } catch (error) {
    console.error('Erro ao carregar filmes:', error)
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}
