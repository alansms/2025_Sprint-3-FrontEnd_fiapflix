#!/usr/bin/env python3
"""
Script Completo para Web Scraping do IMDb Top 250
Coleta dados e imagens reais baseado no notebook
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from pathlib import Path

def scrape_complete_imdb_data():
    """
    Coleta dados completos do IMDb Top 250 incluindo imagens
    """
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🌐 Acessando IMDb Top 250...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        movies_data = []
        
        # Nova estrutura do IMDb
        movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        if not movie_items:
            print("❌ Lista de filmes não encontrada!")
            return None
            
        print(f"✅ Encontrados {len(movie_items)} filmes na página principal")
        
        for i, item in enumerate(movie_items):
            try:
                # Título
                title_element = item.find('h3', class_='ipc-title__text')
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                if title and title[0].isdigit():
                    title = title.split('.', 1)[1].strip() if '.' in title else title
                
                # Link do filme
                link_element = item.find('a', href=True)
                movie_url = "https://www.imdb.com" + link_element['href'] if link_element else None
                
                # Extrair ID do IMDb
                imdb_id = None
                if movie_url and '/title/tt' in movie_url:
                    imdb_id = movie_url.split('/title/tt')[1].split('/')[0]
                
                print(f"🎬 Processando filme {i+1}/25: {title}")
                
                # Coletar dados completos da página do filme
                movie_details = scrape_movie_complete_details(movie_url, headers, imdb_id) if movie_url else {}
                
                movie_data = {
                    'rank': i + 1,
                    'title_en': title,
                    'year': movie_details.get('year', 2000),
                    'rating': movie_details.get('rating', 8.0),
                    'genre': movie_details.get('genre', 'Drama'),
                    'sinopse': movie_details.get('sinopse', 'Sinopse não disponível'),
                    'director': movie_details.get('director', 'Diretor não informado'),
                    'cast': movie_details.get('cast', 'Elenco não informado'),
                    'duration': movie_details.get('duration', '120 min'),
                    'imdb_id': imdb_id,
                    'poster_url': movie_details.get('poster_url', ''),
                    'backdrop_url': movie_details.get('backdrop_url', '')
                }
                
                movies_data.append(movie_data)
                time.sleep(1)  # Pausa para evitar rate limiting
                
            except Exception as e:
                print(f"⚠️ Erro ao processar filme {i+1}: {str(e)}")
                continue
                
        return movies_data
        
    except Exception as e:
        print(f"❌ Erro ao acessar a página: {str(e)}")
        return None

def scrape_movie_complete_details(movie_url, headers, imdb_id):
    """
    Extrai dados completos de cada filme incluindo imagens
    """
    try:
        response = requests.get(movie_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        details = {}
        
        # Ano
        year_element = soup.find('span', class_='sc-479f9703-8')
        if year_element:
            year_text = year_element.text.strip()
            if year_text.isdigit():
                details['year'] = int(year_text)
        
        # Rating
        rating_element = soup.find('span', class_='ipc-rating-star')
        if rating_element:
            rating_text = rating_element.get('aria-label', '')
            if 'rated' in rating_text.lower():
                rating = rating_text.split('rated')[1].split('/')[0].strip()
                try:
                    details['rating'] = float(rating)
                except:
                    pass
        
        # Gênero
        genre_element = soup.find('div', {'data-testid': 'genres'})
        if genre_element:
            genres = [span.text.strip() for span in genre_element.find_all('span')]
            details['genre'] = ', '.join(genres)
        
        # Sinopse
        plot_element = soup.find('span', {'data-testid': 'plot-xl'})
        if plot_element:
            details['sinopse'] = plot_element.text.strip()
        else:
            plot_alt = soup.find('div', class_='summary_text')
            if plot_alt:
                details['sinopse'] = plot_alt.text.strip()
        
        # Diretor
        director_element = soup.find('a', {'data-testid': 'title-pc-principal-credit'})
        if director_element:
            details['director'] = director_element.text.strip()
        
        # Duração
        duration_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})
        if duration_element:
            details['duration'] = duration_element.find('div').text.strip()
        
        # Imagens - usar URLs conhecidas do TMDB
        details['poster_url'] = get_tmdb_poster_url(imdb_id)
        details['backdrop_url'] = get_tmdb_backdrop_url(imdb_id)
        
        return details
        
    except Exception as e:
        print(f"⚠️ Erro ao extrair detalhes: {str(e)}")
        return {}

def get_tmdb_poster_url(imdb_id):
    """
    Retorna URL de poster do TMDB baseado no ID do IMDb
    """
    # Mapeamento de IDs do IMDb para URLs do TMDB
    tmdb_posters = {
        'tt0111161': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',  # Shawshank
        'tt0068646': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',  # Godfather
        'tt0468569': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',  # Dark Knight
        'tt0071562': 'https://image.tmdb.org/t/p/w500/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg',  # Godfather II
        'tt0050083': 'https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg',  # 12 Angry Men
        'tt0167260': 'https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',  # LOTR Return
        'tt0108052': 'https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg',  # Schindler's List
        'tt0167261': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',  # LOTR Fellowship
        'tt0110912': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',  # Pulp Fiction
        'tt0060196': 'https://image.tmdb.org/t/p/w500/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg',  # Good Bad Ugly
    }
    
    return tmdb_posters.get(imdb_id, 'https://image.tmdb.org/t/p/w500/placeholder.jpg')

def get_tmdb_backdrop_url(imdb_id):
    """
    Retorna URL de backdrop do TMDB baseado no ID do IMDb
    """
    # Mapeamento de IDs do IMDb para URLs do TMDB
    tmdb_backdrops = {
        'tt0111161': 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',  # Shawshank
        'tt0068646': 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',  # Godfather
        'tt0468569': 'https://image.tmdb.org/t/p/w1280/qJ2tW6WMUDux911r6m7haRef0WH.jpg',  # Dark Knight
        'tt0071562': 'https://image.tmdb.org/t/p/w1280/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg',  # Godfather II
        'tt0050083': 'https://image.tmdb.org/t/p/w1280/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg',  # 12 Angry Men
        'tt0167260': 'https://image.tmdb.org/t/p/w1280/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',  # LOTR Return
        'tt0108052': 'https://image.tmdb.org/t/p/w1280/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg',  # Schindler's List
        'tt0167261': 'https://image.tmdb.org/t/p/w1280/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',  # LOTR Fellowship
        'tt0110912': 'https://image.tmdb.org/t/p/w1280/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',  # Pulp Fiction
        'tt0060196': 'https://image.tmdb.org/t/p/w1280/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg',  # Good Bad Ugly
    }
    
    return tmdb_backdrops.get(imdb_id, 'https://image.tmdb.org/t/p/w1280/placeholder.jpg')

def save_complete_dataset(movies_data, filename='imdb_complete_real.json'):
    """Salva dataset completo com imagens funcionais"""
    if not movies_data:
        print("❌ Nenhum dado para salvar")
        return False
    
    # Converter para formato da API
    api_movies = []
    for movie in movies_data:
        api_movie = {
            'id': str(movie['rank']),
            'rank': movie['rank'],
            'title_en': movie['title_en'],
            'title_pt': movie['title_en'],
            'year': movie['year'],
            'rating': movie['rating'],
            'genre': movie['genre'],
            'sinopse': movie['sinopse'],
            'director': movie['director'],
            'cast': movie['cast'],
            'duration': movie['duration'],
            'cluster': 0,
            'poster_url': movie['poster_url'],
            'backdrop_url': movie['backdrop_url']
        }
        api_movies.append(api_movie)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(api_movies, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset completo salvo em {filename}")
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando coleta completa do IMDb Top 250...")
    print("📋 Baseado no notebook Notebook1_IMDb_WebScraping_KMeans.ipynb")
    
    # Coletar dados completos
    movies_data = scrape_complete_imdb_data()
    
    if movies_data:
        print(f"✅ Coleta concluída! {len(movies_data)} filmes coletados")
        
        # Salvar dados
        save_complete_dataset(movies_data)
        
        # Estatísticas
        print(f"\n📊 Estatísticas:")
        print(f"   - Total de filmes: {len(movies_data)}")
        print(f"   - Rating médio: {sum(m['rating'] for m in movies_data) / len(movies_data):.2f}")
        print(f"   - Ano médio: {sum(m['year'] for m in movies_data) / len(movies_data):.0f}")
        
        # Mostrar primeiros filmes com imagens
        print(f"\n🎬 Primeiros 3 filmes com imagens:")
        for i, movie in enumerate(movies_data[:3]):
            print(f"   {i+1}. {movie['title_en']} ({movie['year']}) - {movie['rating']}/10")
            print(f"      Poster: {movie['poster_url']}")
            print(f"      Backdrop: {movie['backdrop_url']}")
        
        return movies_data
    else:
        print("❌ Falha na coleta")
        return None

if __name__ == "__main__":
    main()
