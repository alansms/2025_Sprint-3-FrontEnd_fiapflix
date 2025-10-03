import { NextResponse } from 'next/server'
import { Movie } from '@/lib/types'

export async function GET() {
  try {
    // Simular coleta de dados do IMDb
    // Em produção, aqui seria implementado o web scraping real
    
    const mockScrapedMovies: Movie[] = [
      {
        id: '1',
        rank: 1,
        title_en: 'The Shawshank Redemption',
        title_pt: 'Um Sonho de Liberdade',
        year: 1994,
        rating: 9.3,
        genre: 'Drama',
        sinopse: 'A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict, while gradually becoming involved in the prison warden\'s money laundering scheme.',
        director: 'Frank Darabont',
        cast: 'Tim Robbins, Morgan Freeman, Bob Gunton',
        duration: '142 min',
        cluster: 1,
        poster_url: '/api/placeholder/300/450',
        backdrop_url: '/api/placeholder/1920/1080'
      },
      {
        id: '2',
        rank: 2,
        title_en: 'The Godfather',
        title_pt: 'O Poderoso Chefão',
        year: 1972,
        rating: 9.2,
        genre: 'Crime, Drama',
        sinopse: 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
        director: 'Francis Ford Coppola',
        cast: 'Marlon Brando, Al Pacino, James Caan',
        duration: '175 min',
        cluster: 3,
        poster_url: '/api/placeholder/300/450',
        backdrop_url: '/api/placeholder/1920/1080'
      },
      {
        id: '3',
        rank: 3,
        title_en: 'The Dark Knight',
        title_pt: 'Batman: O Cavaleiro das Trevas',
        year: 2008,
        rating: 9.1,
        genre: 'Action, Crime, Drama',
        sinopse: 'When a menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
        director: 'Christopher Nolan',
        cast: 'Christian Bale, Heath Ledger, Aaron Eckhart',
        duration: '152 min',
        cluster: 3,
        poster_url: '/api/placeholder/300/450',
        backdrop_url: '/api/placeholder/1920/1080'
      }
    ]

    return NextResponse.json({
      success: true,
      message: 'Dados coletados com sucesso',
      data: mockScrapedMovies,
      count: mockScrapedMovies.length
    })

  } catch (error) {
    console.error('Erro ao coletar dados:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: 'Erro ao coletar dados do IMDb',
        message: error instanceof Error ? error.message : 'Erro desconhecido'
      },
      { status: 500 }
    )
  }
}
