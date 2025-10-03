import { NextResponse } from 'next/server'
import { Movie } from '@/lib/types'
import fs from 'fs'
import path from 'path'

// Carregar dados reais do IMDb
let realMovies: Movie[] = []

try {
  // Tentar carregar dataset real primeiro
  const realDataPath = path.join(process.cwd(), 'imdb_100plus_movies_real.json')
  const realData = fs.readFileSync(realDataPath, 'utf-8')
  realMovies = JSON.parse(realData)
  console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset real)`)
} catch (error) {
  try {
    // Fallback para dataset com 100+ filmes
    const expandedDataPath = path.join(process.cwd(), 'imdb_100plus_movies.json')
    const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
    realMovies = JSON.parse(expandedData)
    console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset 100+)`)
  } catch (fallbackError) {
    try {
      // Fallback para dataset com 50+ filmes
      const expandedDataPath = path.join(process.cwd(), 'imdb_50plus_movies.json')
      const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
      realMovies = JSON.parse(expandedData)
      console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset 50+)`)
    } catch (secondFallbackError) {
      try {
        // Fallback para dataset expandido
        const expandedDataPath = path.join(process.cwd(), 'imdb_expanded_real.json')
        const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
        realMovies = JSON.parse(expandedData)
        console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset expandido)`)
      } catch (thirdFallbackError) {
        try {
          // Fallback para dados finais
          const finalDataPath = path.join(process.cwd(), 'imdb_final_real.json')
          const finalData = fs.readFileSync(finalDataPath, 'utf-8')
          realMovies = JSON.parse(finalData)
          console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dados finais)`)
        } catch (fourthFallbackError) {
          try {
            // Fallback para dados do IMDb Top 250
            const dataPath = path.join(process.cwd(), 'imdb_top250_real.json')
            const data = fs.readFileSync(dataPath, 'utf-8')
            realMovies = JSON.parse(data)
            console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (fallback)`)
          } catch (fifthFallbackError) {
            console.log('⚠️ Usando dados mock como fallback')
          }
        }
      }
    }
  }
}

const mockMovies: Movie[] = [
  {
    id: '1',
    rank: 1,
    title_en: 'The Shawshank Redemption',
    title_pt: 'Um Sonho de Liberdade',
    year: 1994,
    rating: 9.3,
    genre: 'Drama',
    sinopse: 'Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido, enquanto gradualmente se envolve no esquema de lavagem de dinheiro do diretor da prisão.',
    director: 'Frank Darabont',
    cast: 'Tim Robbins, Morgan Freeman, Bob Gunton',
    duration: '142 min',
    cluster: 1,
    poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
  },
  {
    id: '2',
    rank: 2,
    title_en: 'The Godfather',
    title_pt: 'O Poderoso Chefão',
    year: 1972,
    rating: 9.2,
    genre: 'Crime, Drama',
    sinopse: 'O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filme relutante.',
    director: 'Francis Ford Coppola',
    cast: 'Marlon Brando, Al Pacino, James Caan',
    duration: '175 min',
    cluster: 0,
    poster_url: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
  },
  {
    id: '3',
    rank: 3,
    title_en: 'The Dark Knight',
    title_pt: 'O Cavaleiro das Trevas',
    year: 2008,
    rating: 9.1,
    genre: 'Action, Crime, Drama',
    sinopse: 'Quando uma ameaça conhecida como Coringa causa estragos e caos no povo de Gotham, Batman deve aceitar um dos maiores testes psicológicos e físicos de sua capacidade de lutar contra a injustiça.',
    director: 'Christopher Nolan',
    cast: 'Christian Bale, Heath Ledger, Aaron Eckhart',
    duration: '152 min',
    cluster: 2,
    poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
  },
  {
    id: '4',
    rank: 4,
    title_en: 'The Godfather Part II',
    title_pt: 'O Poderoso Chefão: Parte II',
    year: 1974,
    rating: 9.0,
    genre: 'Crime, Drama',
    sinopse: 'A vida inicial e carreira de Vito Corleone na Nova York dos anos 1920 é retratada, enquanto seu filho Michael expande o controle da família.',
    director: 'Francis Ford Coppola',
    cast: 'Al Pacino, Robert De Niro, Robert Duvall',
    duration: '202 min',
    cluster: 0,
    poster_url: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
  },
  {
    id: '5',
    rank: 5,
    title_en: '12 Angry Men',
    title_pt: '12 Homens e uma Sentença',
    year: 1957,
    rating: 9.0,
    genre: 'Crime, Drama',
    sinopse: 'Um júri tem que decidir se um jovem acusado de assassinato é culpado ou não. Baseado na peça, todos os homens do júri tentam descobrir se há alguma dúvida razoável.',
    director: 'Sidney Lumet',
    cast: 'Henry Fonda, Lee J. Cobb, Martin Balsam',
    duration: '96 min',
    cluster: 1,
    poster_url: 'https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg'
  }
]

export async function GET() {
  try {
    // Simular delay de carregamento
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Usar dados reais se disponíveis, senão usar mock
    const movies = realMovies.length > 0 ? realMovies : mockMovies
    
    return NextResponse.json(movies)
  } catch (error) {
    console.error('Erro ao carregar filmes:', error)
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}