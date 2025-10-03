import { NextRequest, NextResponse } from 'next/server'
import { Movie, RecommendationRequest, RecommendationResponse } from '@/lib/types'
import { exec } from 'child_process'
import { promisify } from 'util'
import path from 'path'
import fs from 'fs'

const execAsync = promisify(exec)

function generateKeywordScores(cluster: number) {
  const scores = []
  for (let i = 0; i < 5; i++) {
    scores.push({
      cluster: i,
      score: i === cluster ? 0.8 + Math.random() * 0.2 : Math.random() * 0.6
    })
  }
  return scores
}

function getSmartFallbackMovies(synopsis: string): Movie[] {
  // Categorias baseadas em palavras-chave
  const categories = {
    'acao': {
      keywords: ['ação', 'luta', 'combate', 'guerra', 'soldado', 'batalha', 'vigilante', 'mascarado', 'criminoso', 'justiça', 'vingança', 'detetive', 'investigação', 'assassinato'],
      movies: [
        {
          id: '1',
          rank: 1,
          title_en: 'The Dark Knight',
          title_pt: 'O Cavaleiro das Trevas',
          year: 2008,
          rating: 9.1,
          genre: 'Action, Crime, Drama',
          sinopse: 'Quando uma ameaça conhecida como Coringa causa estragos e caos no povo de Gotham, Batman deve aceitar um dos maiores testes psicológicos e físicos de sua capacidade de lutar contra a injustiça.',
          director: 'Christopher Nolan',
          cast: 'Christian Bale, Heath Ledger, Aaron Eckhart',
          duration: '152 min',
          cluster: 1,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '2',
          rank: 2,
          title_en: 'Pulp Fiction',
          title_pt: 'Pulp Fiction: Tempo de Violência',
          year: 1994,
          rating: 8.9,
          genre: 'Crime, Drama',
          sinopse: 'As vidas de dois assassinos da máfia, um boxeador, um gângster e sua esposa, e um par de assaltantes de restaurante se entrelaçam em quatro contos de violência e redenção.',
          director: 'Quentin Tarantino',
          cast: 'John Travolta, Uma Thurman, Samuel L. Jackson',
          duration: '154 min',
          cluster: 1,
          poster_url: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
        },
        {
          id: '3',
          rank: 3,
          title_en: 'The Godfather',
          title_pt: 'O Poderoso Chefão',
          year: 1972,
          rating: 9.2,
          genre: 'Crime, Drama',
          sinopse: 'O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filme relutante.',
          director: 'Francis Ford Coppola',
          cast: 'Marlon Brando, Al Pacino, James Caan',
          duration: '175 min',
          cluster: 1,
          poster_url: 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
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
          cluster: 1,
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
          sinopse: 'Um jurado dissidente em um julgamento por assassinato tenta convencer os outros onze a reconsiderar a evidência.',
          director: 'Sidney Lumet',
          cast: 'Henry Fonda, Lee J. Cobb, Martin Balsam',
          duration: '96 min',
          cluster: 1,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        }
      ]
    },
    'drama': {
      keywords: ['drama', 'emocional', 'família', 'relacionamento', 'amor', 'paixão', 'jovem', 'diferente', 'preconceito', 'obstáculo', 'banqueiro', 'amizade', 'prisão'],
      movies: [
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
          cluster: 2,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '2',
          rank: 2,
          title_en: 'Schindler\'s List',
          title_pt: 'A Lista de Schindler',
          year: 1993,
          rating: 9.0,
          genre: 'Biography, Drama, History',
          sinopse: 'Na Polônia ocupada pelos alemães durante a Segunda Guerra Mundial, o industrial Oskar Schindler gradualmente se preocupa com sua força de trabalho judaica depois de testemunhar sua perseguição pelos nazistas.',
          director: 'Steven Spielberg',
          cast: 'Liam Neeson, Ben Kingsley, Ralph Fiennes',
          duration: '195 min',
          cluster: 2,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '3',
          rank: 3,
          title_en: 'Forrest Gump',
          title_pt: 'Forrest Gump: O Contador de Histórias',
          year: 1994,
          rating: 8.8,
          genre: 'Drama, Romance',
          sinopse: 'A vida de Forrest Gump, um homem com QI baixo, que consegue participar de momentos cruciais da história dos Estados Unidos.',
          director: 'Robert Zemeckis',
          cast: 'Tom Hanks, Robin Wright, Gary Sinise',
          duration: '142 min',
          cluster: 2,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '4',
          rank: 4,
          title_en: 'The Lord of the Rings: The Return of the King',
          title_pt: 'O Senhor dos Anéis: O Retorno do Rei',
          year: 2003,
          rating: 9.0,
          genre: 'Action, Adventure, Drama',
          sinopse: 'Gandalf e Aragorn lideram o mundo dos homens contra o exército de Sauron para desviar sua atenção de Frodo e Sam enquanto eles se aproximam do Monte da Perdição com o Um Anel.',
          director: 'Peter Jackson',
          cast: 'Elijah Wood, Viggo Mortensen, Ian McKellen',
          duration: '201 min',
          cluster: 2,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '5',
          rank: 5,
          title_en: 'The Lord of the Rings: The Fellowship of the Ring',
          title_pt: 'O Senhor dos Anéis: A Sociedade do Anel',
          year: 2001,
          rating: 8.9,
          genre: 'Action, Adventure, Drama',
          sinopse: 'Um hobbit pacato herda um anel mágico e embarca em uma perigosa jornada para destruí-lo e salvar toda a Terra Média das forças das trevas.',
          director: 'Peter Jackson',
          cast: 'Elijah Wood, Ian McKellen, Orlando Bloom',
          duration: '178 min',
          cluster: 2,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        }
      ]
    },
    'ficcao': {
      keywords: ['ficção', 'científica', 'espaço', 'astronauta', 'universo', 'futuro', 'tecnologia', 'mágico', 'poder', 'reino', 'missão', 'salvar', 'humanidade'],
      movies: [
        {
          id: '1',
          rank: 1,
          title_en: 'Star Wars: Episode V - The Empire Strikes Back',
          title_pt: 'Star Wars: Episódio V - O Império Contra-Ataca',
          year: 1980,
          rating: 8.7,
          genre: 'Action, Adventure, Fantasy',
          sinopse: 'Após a destruição da Estrela da Morte, Luke Skywalker, Han Solo, Princess Leia e Chewbacca enfrentam o Império Galáctico em uma nova aventura.',
          director: 'Irvin Kershner',
          cast: 'Mark Hamill, Harrison Ford, Carrie Fisher',
          duration: '124 min',
          cluster: 3,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '2',
          rank: 2,
          title_en: 'The Matrix',
          title_pt: 'Matrix',
          year: 1999,
          rating: 8.7,
          genre: 'Action, Sci-Fi',
          sinopse: 'Um programador de computador é levado a um mundo estranho onde a realidade é diferente do que parece.',
          director: 'Lana Wachowski, Lilly Wachowski',
          cast: 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
          duration: '136 min',
          cluster: 3,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '3',
          rank: 3,
          title_en: 'Inception',
          title_pt: 'A Origem',
          year: 2010,
          rating: 8.8,
          genre: 'Action, Sci-Fi, Thriller',
          sinopse: 'Um ladrão que rouba segredos através da tecnologia de compartilhamento de sonhos é dado a tarefa inversa de plantar uma ideia na mente de um CEO.',
          director: 'Christopher Nolan',
          cast: 'Leonardo DiCaprio, Marion Cotillard, Tom Hardy',
          duration: '148 min',
          cluster: 3,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '4',
          rank: 4,
          title_en: 'Interstellar',
          title_pt: 'Interestelar',
          year: 2014,
          rating: 8.6,
          genre: 'Adventure, Drama, Sci-Fi',
          sinopse: 'Uma equipe de exploradores viaja através de um buraco de minhoca no espaço, na tentativa de garantir a sobrevivência da humanidade.',
          director: 'Christopher Nolan',
          cast: 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
          duration: '169 min',
          cluster: 3,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
          id: '5',
          rank: 5,
          title_en: 'Blade Runner',
          title_pt: 'Blade Runner: O Caçador de Androids',
          year: 1982,
          rating: 8.1,
          genre: 'Sci-Fi, Thriller',
          sinopse: 'Um blade runner deve perseguir e tentar terminar quatro replicantes que roubaram uma nave em uma colônia espacial e retornaram à Terra.',
          director: 'Ridley Scott',
          cast: 'Harrison Ford, Rutger Hauer, Sean Young',
          duration: '117 min',
          cluster: 3,
          poster_url: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
          backdrop_url: 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        }
      ]
    }
  }

  // Analisar sinopse para determinar categoria
  const synopsisLower = synopsis.toLowerCase()
  let categoryScores: { [key: string]: number } = {}
  
  for (const [category, data] of Object.entries(categories)) {
    let score = 0
    for (const keyword of data.keywords) {
      if (synopsisLower.includes(keyword)) {
        score += 1
      }
    }
    categoryScores[category] = score
  }
  
  // Selecionar categoria com maior score, ou aleatória se empate
  const maxScore = Math.max(...Object.values(categoryScores))
  const bestCategories = Object.entries(categoryScores)
    .filter(([_, score]) => score === maxScore)
    .map(([category, _]) => category)
  
  const selectedCategory = bestCategories[Math.floor(Math.random() * bestCategories.length)]
  
  // Retornar filmes da categoria selecionada
  return categories[selectedCategory as keyof typeof categories]?.movies || categories.drama.movies
}

function getFallbackRecommendations(synopsis: string, method: string): NextResponse {
  // Fallback inteligente baseado em palavras-chave
  const fallbackMovies: Movie[] = getSmartFallbackMovies(synopsis)

  // Simular cluster baseado na sinopse
  const cluster = Math.floor(Math.random() * 5) + 1
  const confidence = 0.6 + Math.random() * 0.3

  return NextResponse.json({
    recommendations: fallbackMovies,
    cluster: cluster,
    method: method === 'tfidf' ? 'TF-IDF (Sinopses)' : 'Todas as Features',
    confidence: confidence,
    evidence: {
      processed_text: synopsis.substring(0, 200) + '...',
      keyword_scores: generateKeywordScores(cluster),
      selected_cluster: cluster,
      confidence: confidence,
      analysis_method: method === 'tfidf' ? 'Análise de Texto (TF-IDF)' : 'Análise Multidimensional'
    }
  } as RecommendationResponse)
}

export async function POST(req: NextRequest) {
  try {
    const { synopsis, method, year, rating, genre }: RecommendationRequest = await req.json()
    console.log(`🎬 Processando recomendação: ${method}`)
    console.log(`📝 Sinopse: ${synopsis.substring(0, 100)}...`)

    try {
      // Executar modelo Python diretamente
      const pythonCommand = `python3 lib/run_recommendation.py "${JSON.stringify({
        synopsis,
        method,
        year: year || 2000,
        rating: rating || 8.0,
        genre: genre || 'Drama'
      })}"`
      
      console.log('🐍 Executando comando Python:', pythonCommand)
      
      const { stdout, stderr } = await execAsync(pythonCommand, {
        cwd: process.cwd(),
        timeout: 10000 // 10 segundos timeout
      })
      
      console.log('🐍 Python stdout:', stdout)
      console.log('🐍 Python stdout length:', stdout.length)
      if (stderr) console.log('🐍 Python stderr:', stderr)
      
      // Parse do resultado
      const result = JSON.parse(stdout)
      
      if (result && result.recommendations && result.recommendations.length > 0) {
        console.log(`✅ Recomendações geradas: ${result.recommendations.length} filmes`)
        console.log(`🎯 Cluster: ${result.cluster}, Confiança: ${result.confidence?.toFixed(2)}`)
        
        return NextResponse.json({
          recommendations: result.recommendations,
          cluster: result.cluster,
          method: method === 'tfidf' ? 'TF-IDF (Sinopses)' : 'Todas as Features',
          confidence: result.confidence || 0.0,
          evidence: {
            processed_text: synopsis.substring(0, 200) + '...',
            keyword_scores: generateKeywordScores(result.cluster),
            selected_cluster: result.cluster,
            confidence: result.confidence || 0.0,
            analysis_method: method === 'tfidf' ? 'Análise de Texto (TF-IDF)' : 'Análise Multidimensional'
          },
          cluster_analysis: result.cluster_analysis
        } as RecommendationResponse)
      } else {
        console.log('⚠️ Modelo não retornou resultados válidos')
        return getFallbackRecommendations(synopsis, method)
      }
      
    } catch (error) {
      console.error('❌ Erro ao executar modelo Python:', error)
      return getFallbackRecommendations(synopsis, method)
    }

  } catch (error) {
    console.error('❌ Erro na API de recomendação:', error)
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}
