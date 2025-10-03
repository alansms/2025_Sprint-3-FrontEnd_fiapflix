#!/usr/bin/env python3
"""
Sistema de Enriquecimento de Sinopses com IA Generativa
Desenvolvido por: Alan de Souza Maximiano (RM: 557088)
"""

import json
import requests
import time
from typing import Dict, List, Optional
import os

class AISynopsisEnhancer:
    """
    Classe para enriquecimento de sinopses usando IA Generativa
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o enriquecedor de sinopses
        
        Args:
            api_key: Chave da API OpenAI (opcional)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.enhanced_synopses = {}
        
    def enhance_synopsis(self, 
                        title: str, 
                        year: int, 
                        genre: str, 
                        original_synopsis: str,
                        style: str = "cinematic") -> Dict:
        """
        Enriquece uma sinopse usando IA Generativa
        
        Args:
            title: Título do filme
            year: Ano do filme
            genre: Gênero do filme
            original_synopsis: Sinopse original
            style: Estilo da sinopse (cinematic, dramatic, action, etc.)
            
        Returns:
            Dict com sinopse enriquecida e metadados
        """
        
        # Se não há API key, usar enriquecimento local
        if not self.api_key:
            return self._local_enhancement(title, year, genre, original_synopsis, style)
        
        # Prompt para IA Generativa
        prompt = self._create_prompt(title, year, genre, original_synopsis, style)
        
        try:
            # Chamada para OpenAI API
            response = self._call_openai_api(prompt)
            
            if response:
                enhanced_synopsis = response.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                return {
                    'title': title,
                    'year': year,
                    'genre': genre,
                    'original_synopsis': original_synopsis,
                    'enhanced_synopsis': enhanced_synopsis,
                    'style': style,
                    'method': 'openai_api',
                    'timestamp': time.time()
                }
            else:
                # Fallback para enriquecimento local
                return self._local_enhancement(title, year, genre, original_synopsis, style)
                
        except Exception as e:
            print(f"❌ Erro na API OpenAI: {e}")
            # Fallback para enriquecimento local
            return self._local_enhancement(title, year, genre, original_synopsis, style)
    
    def _create_prompt(self, title: str, year: int, genre: str, 
                      original_synopsis: str, style: str) -> str:
        """
        Cria prompt para IA Generativa
        """
        return f"""
        Enriqueça a seguinte sinopse de filme de forma mais envolvente e cinematográfica:
        
        Título: {title}
        Ano: {year}
        Gênero: {genre}
        Sinopse Original: {original_synopsis}
        
        Instruções:
        1. Mantenha a essência da história original
        2. Adicione detalhes visuais e emocionais
        3. Use linguagem cinematográfica e envolvente
        4. Mantenha o gênero {genre}
        5. Estilo: {style}
        6. Tamanho: 2-3 parágrafos
        7. Idioma: Português brasileiro
        
        Sinopse Enriquecida:
        """
    
    def _call_openai_api(self, prompt: str) -> Optional[Dict]:
        """
        Chama a API OpenAI
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erro na chamada da API: {e}")
            return None
    
    def _local_enhancement(self, title: str, year: int, genre: str, 
                          original_synopsis: str, style: str) -> Dict:
        """
        Enriquecimento local usando templates e regras
        """
        
        # Templates por gênero
        genre_templates = {
            'Drama': {
                'intro': f"Em {year}, uma história comovente se desenrola",
                'middle': "Os personagens enfrentam desafios profundos",
                'end': "Uma jornada emocional que toca o coração"
            },
            'Action': {
                'intro': f"Em {year}, a ação explode na tela",
                'middle': "Sequências de ação espetaculares",
                'end': "Uma aventura repleta de adrenalina"
            },
            'Comedy': {
                'intro': f"Em {year}, o humor toma conta",
                'middle': "Situações hilárias se sucedem",
                'end': "Uma comédia que diverte do início ao fim"
            },
            'Thriller': {
                'intro': f"Em {year}, o suspense domina",
                'middle': "Tensões se acumulam a cada momento",
                'end': "Um thriller que prende até o último segundo"
            },
            'Sci-Fi': {
                'intro': f"Em {year}, o futuro se torna presente",
                'middle': "Tecnologia e imaginação se encontram",
                'end': "Uma visão fascinante do que está por vir"
            }
        }
        
        # Obter template do gênero
        template = genre_templates.get(genre, genre_templates['Drama'])
        
        # Enriquecer sinopse
        enhanced = f"{template['intro']}. {original_synopsis}. {template['middle']}. {template['end']}."
        
        # Adicionar elementos cinematográficos
        if style == "cinematic":
            enhanced = f"Uma experiência cinematográfica única: {enhanced}"
        elif style == "dramatic":
            enhanced = f"Uma narrativa dramática envolvente: {enhanced}"
        elif style == "action":
            enhanced = f"Uma aventura repleta de ação: {enhanced}"
        
        return {
            'title': title,
            'year': year,
            'genre': genre,
            'original_synopsis': original_synopsis,
            'enhanced_synopsis': enhanced,
            'style': style,
            'method': 'local_enhancement',
            'timestamp': time.time()
        }
    
    def enhance_dataset(self, movies: List[Dict], 
                       batch_size: int = 5, 
                       delay: float = 1.0) -> List[Dict]:
        """
        Enriquece um dataset completo de filmes
        
        Args:
            movies: Lista de filmes
            batch_size: Tamanho do lote
            delay: Delay entre requisições (segundos)
            
        Returns:
            Lista de filmes com sinopses enriquecidas
        """
        
        enhanced_movies = []
        
        print(f"🤖 Iniciando enriquecimento de {len(movies)} filmes...")
        
        for i, movie in enumerate(movies):
            try:
                print(f"📝 Processando {i+1}/{len(movies)}: {movie.get('title_pt', 'N/A')}")
                
                # Enriquecer sinopse
                enhanced = self.enhance_synopsis(
                    title=movie.get('title_pt', ''),
                    year=movie.get('year', 2020),
                    genre=movie.get('genre', 'Drama'),
                    original_synopsis=movie.get('synopsis_pt', ''),
                    style='cinematic'
                )
                
                # Adicionar sinopse enriquecida ao filme
                movie['synopsis_enhanced'] = enhanced['enhanced_synopsis']
                movie['synopsis_enhancement_method'] = enhanced['method']
                movie['synopsis_enhancement_timestamp'] = enhanced['timestamp']
                
                enhanced_movies.append(movie)
                
                # Delay para evitar rate limiting
                if i < len(movies) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Erro ao processar filme {i+1}: {e}")
                # Adicionar filme sem enriquecimento
                movie['synopsis_enhanced'] = movie.get('synopsis_pt', '')
                movie['synopsis_enhancement_method'] = 'error'
                enhanced_movies.append(movie)
        
        print(f"✅ Enriquecimento concluído: {len(enhanced_movies)} filmes processados")
        return enhanced_movies
    
    def save_enhanced_dataset(self, enhanced_movies: List[Dict], 
                             filename: str = 'movies_enhanced.json'):
        """
        Salva dataset enriquecido
        
        Args:
            enhanced_movies: Lista de filmes enriquecidos
            filename: Nome do arquivo
        """
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_movies, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Dataset enriquecido salvo em: {filename}")
            print(f"📊 Total de filmes: {len(enhanced_movies)}")
            
            # Estatísticas
            methods = {}
            for movie in enhanced_movies:
                method = movie.get('synopsis_enhancement_method', 'unknown')
                methods[method] = methods.get(method, 0) + 1
            
            print(f"📈 Métodos de enriquecimento:")
            for method, count in methods.items():
                print(f"  • {method}: {count} filmes")
                
        except Exception as e:
            print(f"❌ Erro ao salvar dataset: {e}")

def main():
    """
    Função principal para teste
    """
    print("🤖 Sistema de Enriquecimento de Sinopses com IA Generativa")
    print("=" * 60)
    
    # Exemplo de uso
    enhancer = AISynopsisEnhancer()
    
    # Exemplo de filme
    sample_movie = {
        'title_pt': 'O Poderoso Chefão',
        'year': 1972,
        'genre': 'Drama',
        'synopsis_pt': 'A história de uma família de mafiosos italianos.'
    }
    
    # Enriquecer sinopse
    enhanced = enhancer.enhance_synopsis(
        title=sample_movie['title_pt'],
        year=sample_movie['year'],
        genre=sample_movie['genre'],
        original_synopsis=sample_movie['synopsis_pt'],
        style='cinematic'
    )
    
    print(f"📝 Sinopse Original: {enhanced['original_synopsis']}")
    print(f"✨ Sinopse Enriquecida: {enhanced['enhanced_synopsis']}")
    print(f"🔧 Método: {enhanced['method']}")

if __name__ == "__main__":
    main()
