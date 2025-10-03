'use client'

import { useState, useRef } from 'react'
import { ChevronLeft, ChevronRight, Star, Play, Info } from 'lucide-react'
import Image from 'next/image'
import { Movie } from '@/lib/types'

interface MovieRowProps {
  title: string
  movies: Movie[]
  featured?: boolean
  id?: string
  onMovieClick?: (movie: Movie) => void
  onMovieInfo?: (movie: Movie) => void
}

export default function MovieRow({ title, movies, featured = false, id, onMovieClick, onMovieInfo }: MovieRowProps) {
  const [scrollPosition, setScrollPosition] = useState(0)
  const rowRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: 'left' | 'right') => {
    if (!rowRef.current) return

    const scrollAmount = 300
    const newPosition = direction === 'left' 
      ? scrollPosition - scrollAmount 
      : scrollPosition + scrollAmount

    setScrollPosition(newPosition)
    rowRef.current.scrollTo({
      left: newPosition,
      behavior: 'smooth'
    })
  }

  if (movies.length === 0) return null

  return (
    <div className="mb-8" id={id}>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl md:text-3xl font-bold text-white">
          {title}
        </h2>
        
        <div className="flex space-x-2">
          <button
            onClick={() => scroll('left')}
            className="bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-colors"
            disabled={scrollPosition <= 0}
          >
            <ChevronLeft size={20} />
          </button>
          <button
            onClick={() => scroll('right')}
            className="bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-colors"
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>

      <div className="relative">
        <div
          ref={rowRef}
          className="flex space-x-4 overflow-x-auto scrollbar-hide"
          style={{ scrollBehavior: 'smooth' }}
        >
          {movies.map((movie) => (
            <MovieCard 
              key={movie.id} 
              movie={movie} 
              featured={featured}
              onMovieClick={onMovieClick}
              onMovieInfo={onMovieInfo}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

interface MovieCardProps {
  movie: Movie
  featured?: boolean
  onMovieClick?: (movie: Movie) => void
  onMovieInfo?: (movie: Movie) => void
}

function MovieCard({ movie, featured = false, onMovieClick, onMovieInfo }: MovieCardProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      className={`movie-card relative flex-shrink-0 cursor-pointer ${
        featured ? 'w-64 md:w-80' : 'w-48 md:w-56'
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative overflow-hidden rounded-lg bg-gray-800">
        {/* Movie Poster */}
        <div className={`relative ${featured ? 'h-96' : 'h-72'} bg-gray-700 overflow-hidden`}>
          {movie.poster_url ? (
            <Image
              src={movie.poster_url}
              alt={movie.title_en}
              fill
              className="object-cover"
              sizes={featured ? "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw" : "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-700 to-gray-800">
              <div className="text-center text-gray-400">
                <Play size={48} className="mx-auto mb-2" />
                <p className="text-sm">{movie.title_en}</p>
              </div>
            </div>
          )}

          {/* Overlay on Hover */}
          {isHovered && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center space-x-2">
              <button 
                onClick={() => onMovieClick?.(movie)}
                className="bg-netflix-red text-white p-3 rounded-full hover:bg-red-700 transition-colors"
                title="Assistir"
              >
                <Play size={24} fill="currentColor" />
              </button>
              <button 
                onClick={() => onMovieInfo?.(movie)}
                className="bg-gray-600 text-white p-3 rounded-full hover:bg-gray-700 transition-colors"
                title="Mais Informações"
              >
                <Info size={24} />
              </button>
            </div>
          )}

          {/* Rating Badge */}
          <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded flex items-center space-x-1">
            <Star size={12} fill="currentColor" className="text-yellow-400" />
            <span className="text-xs font-semibold">{movie.rating}</span>
          </div>
        </div>

        {/* Movie Info */}
        <div className="p-4">
          <h3 className="text-white font-semibold text-sm md:text-base mb-1 line-clamp-2">
            {movie.title_en}
          </h3>
          
          <div className="flex items-center justify-between text-gray-400 text-xs">
            <span>{movie.year}</span>
            <span className="truncate ml-2">{movie.genre}</span>
          </div>

          {/* Synopsis Preview */}
          {featured && movie.sinopse && (
            <p className="text-gray-300 text-xs mt-2 line-clamp-3">
              {movie.sinopse.length > 100 
                ? `${movie.sinopse.substring(0, 100)}...` 
                : movie.sinopse
              }
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
