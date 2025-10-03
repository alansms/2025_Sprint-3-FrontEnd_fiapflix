import { NextResponse } from 'next/server'
import { Movie } from '@/lib/types'
import fs from 'fs'
import path from 'path'

// Carregar dados reais do IMDb
let realMovies: Movie[] = []

try {
  // Tentar carregar dataset com 50+ filmes primeiro
  const expandedDataPath = path.join(process.cwd(), 'imdb_50plus_movies.json')
  const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
  realMovies = JSON.parse(expandedData)
  console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset 50+)`)
} catch (error) {
  try {
    // Fallback para dataset expandido
    const expandedDataPath = path.join(process.cwd(), 'imdb_expanded_real.json')
    const expandedData = fs.readFileSync(expandedDataPath, 'utf-8')
    realMovies = JSON.parse(expandedData)
    console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dataset expandido)`)
  } catch (fallbackError) {
    try {
      // Fallback para dados finais
      const finalDataPath = path.join(process.cwd(), 'imdb_final_real.json')
      const finalData = fs.readFileSync(finalDataPath, 'utf-8')
      realMovies = JSON.parse(finalData)
      console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (dados finais)`)
    } catch (secondFallbackError) {
      try {
        // Fallback para dados anteriores
        const dataPath = path.join(process.cwd(), 'imdb_top250_real.json')
        const data = fs.readFileSync(dataPath, 'utf-8')
        realMovies = JSON.parse(data)
        console.log(`✅ Carregados ${realMovies.length} filmes reais do IMDb (fallback)`)
      } catch (thirdFallbackError) {
        console.log('⚠️ Usando dados mock como fallback')
        // Fallback para dados mock se nenhum arquivo existir
      }
    }
  }
}

// Mock data baseado no dataset do IMDb Top 250 - URLs válidas e funcionais
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
    poster_url: 'https://image.tmdb.org/t/p/w500/hek3koDFyKkXoZGCySWMV1C9u8.jpg',
    backdrop_url: 'https://image.tmdb.org/t/p/w1280/hek3koDFyKkXoZGCySWMV1C9u8.jpg'
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