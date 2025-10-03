#!/usr/bin/env python3
"""
Script para expandir o dataset para 50+ filmes do IMDb Top 250
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin

def scrape_imdb_top_250():
    """Scraping do IMDb Top 250 para obter 50+ filmes"""
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("🎬 Iniciando scraping do IMDb Top 250...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        movies = []
        
        # Encontrar todos os filmes na lista
        movie_rows = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        
        print(f"📊 Encontrados {len(movie_rows)} filmes na página")
        
        for i, row in enumerate(movie_rows[:60]):  # Pegar os primeiros 60 para ter 50+ válidos
            try:
                # Título
                title_element = row.find('h3', class_='ipc-title__text')
                if not title_element:
                    continue
                    
                title_text = title_element.get_text(strip=True)
                # Remover número do ranking
                title = title_text.split('. ', 1)[1] if '. ' in title_text else title_text
                
                # Ano
                year_element = row.find('span', class_='sc-479f9703-8')
                year = None
                if year_element:
                    year_text = year_element.get_text(strip=True)
                    # Extrair ano (formato: (2023))
                    if '(' in year_text and ')' in year_text:
                        year = year_text.split('(')[1].split(')')[0]
                        try:
                            year = int(year)
                        except:
                            year = None
                
                # Rating
                rating_element = row.find('span', class_='ipc-rating-star')
                rating = None
                if rating_element:
                    rating_text = rating_element.get_text(strip=True)
                    try:
                        rating = float(rating_text.split('/')[0])
                    except:
                        rating = None
                
                # Link do filme
                link_element = row.find('a')
                movie_url = None
                if link_element and link_element.get('href'):
                    movie_url = urljoin('https://www.imdb.com', link_element['href'])
                
                if title and year and rating:
                    movie_data = {
                        'id': str(i + 1),
                        'rank': i + 1,
                        'title_en': title,
                        'title_pt': title,  # Mesmo título por enquanto
                        'year': year,
                        'rating': rating,
                        'genre': 'Drama',  # Default
                        'sinopse': f'Sinopse do filme {title} ({year}) - Um filme com rating {rating}/10.',
                        'director': 'Diretor não informado',
                        'cast': 'Elenco não informado',
                        'duration': '120 min',
                        'cluster': random.randint(0, 4),  # Cluster aleatório
                        'poster_url': f'https://picsum.photos/500/750?random={i+1}',
                        'backdrop_url': f'https://picsum.photos/1280/720?random={i+1}',
                        'imdb_url': movie_url
                    }
                    
                    movies.append(movie_data)
                    print(f"✅ {i+1}. {title} ({year}) - {rating}/10")
                    
                    # Delay para não sobrecarregar
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ Erro ao processar filme {i+1}: {e}")
                continue
        
        print(f"\n🎯 Total de filmes coletados: {len(movies)}")
        return movies
        
    except Exception as e:
        print(f"❌ Erro no scraping: {e}")
        return []

def save_movies(movies, filename):
    """Salvar filmes em arquivo JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
        print(f"💾 Filmes salvos em: {filename}")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return False

def main():
    print("🚀 Expandindo dataset para 50+ filmes...")
    
    # Scraping do IMDb
    movies = scrape_imdb_top_250()
    
    if len(movies) >= 50:
        # Salvar dataset expandido
        save_movies(movies, 'imdb_50plus_movies.json')
        
        # Estatísticas
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   • Total de filmes: {len(movies)}")
        print(f"   • Anos: {min(m['year'] for m in movies)} - {max(m['year'] for m in movies)}")
        print(f"   • Ratings: {min(m['rating'] for m in movies):.1f} - {max(m['rating'] for m in movies):.1f}")
        
        # Distribuição por década
        decades = {}
        for movie in movies:
            decade = (movie['year'] // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        
        print(f"   • Distribuição por década:")
        for decade in sorted(decades.keys()):
            print(f"     {decade}s: {decades[decade]} filmes")
            
        print(f"\n✅ Dataset expandido com sucesso!")
        return True
    else:
        print(f"❌ Não foi possível coletar 50+ filmes. Coletados: {len(movies)}")
        return False

if __name__ == "__main__":
    main()

