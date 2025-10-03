export interface Movie {
  id: string
  rank: number
  title_en: string
  title_pt?: string
  year: number
  rating: number
  genre: string
  sinopse: string
  director?: string
  cast?: string
  duration?: string
  cluster?: number
  poster_url?: string
  backdrop_url?: string
}

export interface RecommendationRequest {
  method: 'method1' | 'method2'
  selectedSynopsis?: string
  customSynopsis?: string
}

export interface RecommendationResponse {
  recommendations: Movie[]
  cluster: number
  method: string
  confidence: number
  evidence?: {
    processed_text: string
    keyword_scores: Array<{ cluster: number; score: number }>
    selected_cluster: number
    confidence: number
    analysis_method: string
  }
  cluster_analysis?: {
    cluster_id: number
    movie_count: number
    avg_rating: number
    genres: string[]
    representative_movies: Array<{
      title: string
      rating: number
      year: number
    }>
  }
}

export interface ClusterAnalysis {
  cluster_id: number
  movie_count: number
  avg_rating: number
  avg_year: number
  top_genres: string[]
  representative_movies: Movie[]
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}
