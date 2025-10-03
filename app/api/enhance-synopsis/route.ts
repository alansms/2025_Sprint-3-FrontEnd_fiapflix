import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

interface EnhanceRequest {
  title: string
  year: number
  genre: string
  synopsis: string
  style?: string
}

interface EnhanceResponse {
  enhanced_synopsis: string
  method: string
  timestamp: number
  original_synopsis: string
}

export async function POST(request: NextRequest) {
  try {
    const body: EnhanceRequest = await request.json()
    const { title, year, genre, synopsis, style = 'cinematic' } = body

    console.log('🤖 Enriquecendo sinopse com IA Generativa...')
    console.log(`📝 Filme: ${title} (${year})`)
    console.log(`🎭 Gênero: ${genre}`)

    // Verificar se há chave da API OpenAI
    const openaiKey = process.env.OPENAI_API_KEY
    
    if (!openaiKey) {
      console.log('⚠️ Chave OpenAI não encontrada, usando enriquecimento local')
    }

    // Executar script Python para enriquecimento
    const pythonScript = `
import sys
import json
import os
sys.path.append('lib')
from ai_synopsis_enhancer import AISynopsisEnhancer

# Configurar chave da API se disponível
os.environ['OPENAI_API_KEY'] = '${openaiKey || ''}'

# Criar enriquecedor
enhancer = AISynopsisEnhancer()

# Enriquecer sinopse
result = enhancer.enhance_synopsis(
    title='${title.replace(/'/g, "\\'")}',
    year=${year},
    genre='${genre.replace(/'/g, "\\'")}',
    original_synopsis='${synopsis.replace(/'/g, "\\'")}',
    style='${style}'
)

print(json.dumps(result, ensure_ascii=False))
`

    try {
      const { stdout, stderr } = await execAsync(`python3 -c "${pythonScript}"`)
      
      if (stderr) {
        console.error('❌ Erro no script Python:', stderr)
      }

      const result = JSON.parse(stdout.trim())
      
      const response: EnhanceResponse = {
        enhanced_synopsis: result['enhanced_synopsis'],
        method: result['method'],
        timestamp: result['timestamp'],
        original_synopsis: result['original_synopsis']
      }

      console.log('✅ Sinopse enriquecida com sucesso!')
      console.log(`🔧 Método: ${response.method}`)

      return NextResponse.json(response)

    } catch (error) {
      console.error('❌ Erro ao executar enriquecimento:', error)
      
      // Fallback: enriquecimento local simples
      const localEnhanced = enhanceLocally(title, year, genre, synopsis, style)
      
      return NextResponse.json({
        enhanced_synopsis: localEnhanced,
        method: 'local_fallback',
        timestamp: Date.now(),
        original_synopsis: synopsis
      })
    }

  } catch (error) {
    console.error('❌ Erro na API de enriquecimento:', error)
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}

function enhanceLocally(title: string, year: number, genre: string, synopsis: string, style: string): string {
  // Enriquecimento local simples
  const genreTemplates = {
    'Drama': 'Uma narrativa dramática envolvente',
    'Action': 'Uma aventura repleta de ação',
    'Comedy': 'Uma comédia que diverte',
    'Thriller': 'Um thriller que prende',
    'Sci-Fi': 'Uma visão fascinante do futuro'
  }

  const template = genreTemplates[genre as keyof typeof genreTemplates] || 'Uma história cinematográfica'
  
  return `${template}: ${synopsis}. Uma experiência visual e emocional que cativa o público.`
}
