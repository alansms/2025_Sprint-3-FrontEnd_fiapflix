import { NextRequest, NextResponse } from 'next/server'
import { Movie } from '@/lib/types'

// Dados dos filmes (mesmo do movies/route.ts)
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
    sinopse: 'O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filho relutante.',
    director: 'Francis Ford Coppola',
    cast: 'Marlon Brando, Al Pacino, James Caan',
    duration: '175 min',
    cluster: 3,
    poster_url: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
  },
  {
    id: '3',
    rank: 3,
    title_en: 'The Dark Knight',
    title_pt: 'Batman: O Cavaleiro das Trevas',
    year: 2008,
    rating: 9.1,
    genre: 'Action, Crime, Drama',
    sinopse: 'Quando uma ameaça conhecida como Coringa causa estragos e caos no povo de Gotham, Batman deve aceitar um dos maiores testes psicológicos e físicos de sua capacidade de lutar contra a injustiça.',
    director: 'Christopher Nolan',
    cast: 'Christian Bale, Heath Ledger, Aaron Eckhart',
    duration: '152 min',
    cluster: 3,
    poster_url: 'https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg'
  },
  {
    id: '4',
    rank: 4,
    title_en: 'The Godfather Part II',
    title_pt: 'O Poderoso Chefão: Parte II',
    year: 1974,
    rating: 9.0,
    genre: 'Crime, Drama',
    sinopse: 'A vida inicial e carreira de Vito Corleone na Nova York dos anos 1920 é retratada, enquanto seu filho, Michael, expande e aperta seu controle sobre o sindicato do crime da família.',
    director: 'Francis Ford Coppola',
    cast: 'Al Pacino, Robert De Niro, Robert Duvall',
    duration: '202 min',
    cluster: 3,
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
    sinopse: 'O júri em um julgamento de assassinato em Nova York é frustrado por um único membro cuja cautela cética os força a considerar mais cuidadosamente a evidência antes de pular para um veredicto apressado.',
    director: 'Sidney Lumet',
    cast: 'Henry Fonda, Lee J. Cobb, Martin Balsam',
    duration: '96 min',
    cluster: 2,
    poster_url: 'https://image.tmdb.org/t/p/w500/3hPNieHxl2VXuqScpR7SmFyaGIU.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/3hPNieHxl2VXuqScpR7SmFyaGIU.jpg'
  },
  {
    id: '6',
    rank: 6,
    title_en: 'The Lord of the Rings: The Return of the King',
    title_pt: 'O Senhor dos Anéis: O Retorno do Rei',
    year: 2003,
    rating: 9.0,
    genre: 'Action, Adventure, Drama',
    sinopse: 'Gandalf e Aragorn lideram o Mundo dos Homens contra o exército de Sauron para desviar seu olhar de Frodo e Sam enquanto eles se aproximam do Monte da Perdição com o Um Anel.',
    director: 'Peter Jackson',
    cast: 'Elijah Wood, Viggo Mortensen, Ian McKellen',
    duration: '201 min',
    cluster: 4,
    poster_url: 'https://image.tmdb.org/t/p/w500/rCzpDGLbOo2sbmQ9yJlEM9L7z3C.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/rCzpDGLbOo2sbmQ9yJlEM9L7z3C.jpg'
  },
  {
    id: '7',
    rank: 7,
    title_en: 'Schindler\'s List',
    title_pt: 'A Lista de Schindler',
    year: 1993,
    rating: 9.0,
    genre: 'Biography, Drama, History',
    sinopse: 'A história de Oskar Schindler, que salvou as vidas de mais de mil refugiados judeus poloneses durante o Holocausto empregando-os em suas fábricas.',
    director: 'Steven Spielberg',
    cast: 'Liam Neeson, Ralph Fiennes, Ben Kingsley',
    duration: '195 min',
    cluster: 1,
    poster_url: 'https://image.tmdb.org/t/p/w500/sF1U4ewgfWKfHFDc29Wc5zC2dza.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/sF1U4ewgfWKfHFDc29Wc5zC2dza.jpg'
  },
  {
    id: '8',
    rank: 8,
    title_en: 'The Lord of the Rings: The Fellowship of the Ring',
    title_pt: 'O Senhor dos Anéis: A Sociedade do Anel',
    year: 2001,
    rating: 8.9,
    genre: 'Action, Adventure, Drama',
    sinopse: 'Um Hobbit manso do Condado e oito companheiros partem em uma jornada para destruir o poderoso Um Anel e salvar a Terra Média do Senhor das Trevas Sauron.',
    director: 'Peter Jackson',
    cast: 'Elijah Wood, Ian McKellen, Orlando Bloom',
    duration: '178 min',
    cluster: 4,
    poster_url: 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg'
  },
  {
    id: '9',
    rank: 9,
    title_en: 'Pulp Fiction',
    title_pt: 'Pulp Fiction: Tempo de Violência',
    year: 1994,
    rating: 8.8,
    genre: 'Crime, Drama',
    sinopse: 'As vidas de dois assassinos da máfia, um boxeador, um gângster e sua esposa, e um par de bandidos de restaurante se entrelaçam em quatro contos de violência e redenção.',
    director: 'Quentin Tarantino',
    cast: 'John Travolta, Uma Thurman, Samuel L. Jackson',
    duration: '154 min',
    cluster: 3,
    poster_url: 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszBPY82WMoVs5U.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/d5iIlFn5s0ImszBPY82WMoVs5U.jpg'
  },
  {
    id: '10',
    rank: 10,
    title_en: 'The Good, the Bad and the Ugly',
    title_pt: 'Três Homens em Conflito',
    year: 1966,
    rating: 8.8,
    genre: 'Western',
    sinopse: 'Um esquema de caça a recompensas une dois homens em uma aliança inquieta contra um terceiro em uma corrida para encontrar uma fortuna em ouro enterrada em um cemitério remoto.',
    director: 'Sergio Leone',
    cast: 'Clint Eastwood, Eli Wallach, Lee Van Cleef',
    duration: '178 min',
    cluster: 0,
    poster_url: 'https://image.tmdb.org/t/p/w500/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg'
  }
]

// Função de IA generativa para análise de consultas
// Normalizar texto (remover acentos) para matching robusto
function normalize(text: string): string {
  return text
    .normalize('NFD')
    .replace(/\p{Diacritic}+/gu, '')
}

function analyzeQuery(query: string): {
  intent: string
  keywords: string[]
  filters: {
    genre?: string
    year?: { min?: number; max?: number }
    rating?: { min?: number }
    director?: string
    actor?: string
  }
  searchType: 'semantic' | 'exact' | 'recommendation'
} {
  const lowerQuery = normalize(query.toLowerCase())
  
  // Detectar intenção
  let intent = 'search'
  if (lowerQuery.includes('recomend') || lowerQuery.includes('sugest')) {
    intent = 'recommendation'
  } else if (lowerQuery.includes('melhor') || lowerQuery.includes('top') || lowerQuery.includes('classific')) {
    intent = 'ranking'
  }
  
  // Extrair palavras-chave
  const keywords = lowerQuery
    .replace(/[^\w\s]/g, ' ')
    .split(' ')
    .filter(word => word.length > 2)
    .filter(word => !['filme', 'filmes', 'movie', 'movies', 'sobre', 'com', 'para', 'que', 'uma', 'um'].includes(word))
  
  // Extrair filtros
  const filters: any = {}
  
  // Gênero
  const genreKeywords = {
    drama: ['drama', 'dramatica'],
    action: ['acao', 'action', 'aventura', 'adventure'],
    crime: ['crime', 'criminoso', 'mafia', 'gangster'],
    comedy: ['comedia', 'comedy', 'engracado', 'humor'],
    horror: ['terror', 'horror', 'assustador', 'medo'],
    romance: ['romance', 'romantico', 'amor'],
    thriller: ['thriller', 'suspense', 'tensao'],
    western: ['western', 'cowboy', 'faroeste'],
    fantasy: ['fantasia', 'fantasy', 'magico', 'magica'],
    'sci-fi': ['ficcao', 'cientifica', 'futuro', 'espaco', 'scifi']
  } as Record<string, string[]>
  
  for (const [genre, terms] of Object.entries(genreKeywords)) {
    if (terms.some(term => lowerQuery.includes(term))) {
      filters.genre = genre
      break
    }
  }
  
  // Ano
  const yearMatch = lowerQuery.match(/(\d{4})/g)
  if (yearMatch) {
    const years = yearMatch.map(Number)
    if (years.length === 1) {
      filters.year = { min: years[0] - 2, max: years[0] + 2 }
    } else if (years.length === 2) {
      filters.year = { min: Math.min(...years), max: Math.max(...years) }
    }
  }
  
  // Rating
  if (lowerQuery.includes('melhor') || lowerQuery.includes('top') || lowerQuery.includes('alto')) {
    filters.rating = { min: 8.5 }
  }
  
  // Diretor
  const directorMatch = lowerQuery.match(/diretor[:\s]+([^,]+)/i)
  if (directorMatch) {
    filters.director = directorMatch[1].trim()
  }
  
  // Ator
  const actorMatch = lowerQuery.match(/ator[:\s]+([^,]+)/i) || lowerQuery.match(/estrelado por[:\s]+([^,]+)/i)
  if (actorMatch) {
    filters.actor = actorMatch[1].trim()
  }
  
  // Tipo de busca
  let searchType: 'semantic' | 'exact' | 'recommendation' = 'semantic'
  if (intent === 'recommendation') {
    searchType = 'recommendation'
  } else if (keywords.length === 1 && keywords[0].length > 3) {
    searchType = 'exact'
  }
  
  return {
    intent,
    keywords,
    filters,
    searchType
  }
}

// Função de busca semântica
function semanticSearch(query: string, movies: Movie[]): { results: Movie[]; analysis: any; relaxed: boolean } {
  const analysis = analyzeQuery(query)
  let results = [...movies]
  let relaxed = false

  const genreAlias: Record<string, string[]> = {
    horror: ['horror', 'terror', 'thriller', 'suspense'],
    thriller: ['thriller', 'suspense', 'crime', 'drama'],
    action: ['action', 'acao', 'adventure', 'aventura']
  }
  
  // Aplicar filtros
  if (analysis.filters.genre) {
    const wanted = analysis.filters.genre.toLowerCase()
    const aliases = genreAlias[wanted] || [wanted]
    results = results.filter(movie => {
      const mg = movie.genre.toLowerCase()
      return aliases.some(a => mg.includes(a))
    })
  }
  
  if (analysis.filters.year) {
    results = results.filter(movie => {
      if (analysis.filters.year!.min && movie.year < analysis.filters.year!.min) return false
      if (analysis.filters.year!.max && movie.year > analysis.filters.year!.max) return false
      return true
    })
  }
  
  if (analysis.filters.rating) {
    results = results.filter(movie => movie.rating >= analysis.filters.rating!.min!)
  }
  
  if (analysis.filters.director) {
    results = results.filter(movie => 
      movie.director.toLowerCase().includes(analysis.filters.director!.toLowerCase())
    )
  }
  
  if (analysis.filters.actor) {
    results = results.filter(movie => 
      movie.cast.toLowerCase().includes(analysis.filters.actor!.toLowerCase())
    )
  }
  
  // Busca por palavras-chave na sinopse e título
  if (analysis.keywords.length > 0) {
    results = results.filter(movie => {
      const searchText = `${movie.title_pt} ${movie.title_en} ${movie.sinopse} ${movie.genre}`.toLowerCase()
      return analysis.keywords.some(keyword => searchText.includes(keyword))
    })
  }
  
  // Ordenar por relevância
  results.sort((a, b) => {
    // Priorizar por rating
    if (analysis.intent === 'ranking') {
      return b.rating - a.rating
    }
    
    // Contar matches de palavras-chave
    const aMatches = analysis.keywords.filter(keyword => 
      `${a.title_pt} ${a.title_en} ${a.sinopse}`.toLowerCase().includes(keyword)
    ).length
    
    const bMatches = analysis.keywords.filter(keyword => 
      `${b.title_pt} ${b.title_en} ${b.sinopse}`.toLowerCase().includes(keyword)
    ).length
    
    if (aMatches !== bMatches) {
      return bMatches - aMatches
    }
    
    return b.rating - a.rating
  })
  
  // Relaxamento progressivo se vazio
  if (results.length === 0) {
    relaxed = true
    let fallback = [...movies]
    if (analysis.filters.genre) {
      const wanted = analysis.filters.genre.toLowerCase()
      const aliases = genreAlias[wanted] || [wanted]
      fallback = fallback.filter(m => aliases.some(a => m.genre.toLowerCase().includes(a)))
    }
    if (analysis.filters.rating) {
      fallback = fallback.filter(m => m.rating >= 8.0)
    }
    if (analysis.keywords.length > 0) {
      fallback = fallback.filter(m => {
        const text = `${m.title_pt} ${m.title_en} ${m.genre}`.toLowerCase()
        return analysis.keywords.some(k => text.includes(k))
      })
    }
    if (fallback.length === 0) {
      fallback = [...movies]
      if (analysis.filters.rating) fallback = fallback.filter(m => m.rating >= 8.0)
    }
    fallback.sort((a, b) => b.rating - a.rating)
    results = fallback.slice(0, 10)
  }

  return { results: results.slice(0, 10), analysis, relaxed }
}

// Função para gerar resposta em linguagem natural
function generateNaturalResponse(query: string, results: Movie[], analysis: any): string {
  const resultCount = results.length
  
  if (resultCount === 0) {
    return "Desculpe, não encontrei filmes que correspondam à sua pesquisa. Tente usar termos diferentes ou ser mais específico sobre o que você está procurando."
  }
  
  let response = ""
  
  if (analysis.intent === 'recommendation') {
    response = `Baseado na sua consulta, encontrei ${resultCount} filmes que podem te interessar:\n\n`
  } else if (analysis.intent === 'ranking') {
    response = `Aqui estão os melhores filmes que correspondem à sua pesquisa:\n\n`
  } else {
    response = `Encontrei ${resultCount} filmes relacionados à sua pesquisa:\n\n`
  }
  
  // Adicionar informações sobre os filmes encontrados
  results.slice(0, 5).forEach((movie, index) => {
    response += `${index + 1}. **${movie.title_pt}** (${movie.year})\n`
    response += `   - Gênero: ${movie.genre}\n`
    response += `   - Diretor: ${movie.director}\n`
    response += `   - Rating: ${movie.rating}/10\n`
    response += `   - Sinopse: ${movie.sinopse.substring(0, 100)}...\n\n`
  })
  
  if (results.length > 5) {
    response += `E mais ${results.length - 5} filmes...`
  }
  
  // Adicionar insights baseados na análise
  if (analysis.filters.genre) {
    response += `\n\n**Insight:** Filtrei por filmes do gênero ${analysis.filters.genre}.`
  }
  
  if (analysis.filters.year) {
    response += `\n\n**Insight:** Foquei em filmes do período ${analysis.filters.year.min}-${analysis.filters.year.max}.`
  }
  
  if (analysis.filters.rating) {
    response += `\n\n**Insight:** Priorizei filmes com rating alto (${analysis.filters.rating.min}+).`
  }
  
  return response
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { query } = body

    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { error: 'Query é obrigatória e deve ser uma string' },
        { status: 400 }
      )
    }

    // Simular delay de processamento IA
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Analisar a consulta
    const initial = analyzeQuery(query)
    
    // Realizar busca semântica com relaxamento
    const { results, analysis, relaxed } = semanticSearch(query, mockMovies)
    
    // Gerar resposta em linguagem natural
    const naturalResponse = generateNaturalResponse(query, results, analysis)
    
    // Análise da consulta para debug
    const queryAnalysis = {
      original_query: query,
      detected_intent: analysis.intent,
      extracted_keywords: analysis.keywords,
      applied_filters: analysis.filters,
      search_type: analysis.searchType,
      relaxed_filters: relaxed,
      results_count: results.length
    }

    return NextResponse.json({
      query: query,
      results: results,
      natural_response: naturalResponse,
      analysis: queryAnalysis,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Erro ao processar busca IA:', error)
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'API de Busca IA - FiapFlix',
    description: 'Endpoint para busca inteligente de filmes usando IA generativa',
    usage: 'POST com { "query": "sua pergunta sobre filmes" }',
    examples: [
      'Filmes de drama com rating alto',
      'Melhores filmes de 1990 a 2000',
      'Filmes do diretor Christopher Nolan',
      'Recomendações de filmes de ação',
      'Filmes estrelados por Morgan Freeman'
    ]
  })
}
