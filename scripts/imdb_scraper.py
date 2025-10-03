#!/usr/bin/env python3
"""
Script de Web Scraping do IMDb Top 250
Baseado no Notebook1_IMDb_WebScraping_KMeans.ipynb
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import json
import os
from pathlib import Path

def scrape_imdb_top250():
    """
    Função para fazer web scraping dos top 250 filmes do IMDb
    Baseada no notebook Notebook1_IMDb_WebScraping_KMeans.ipynb
    """
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🌐 Acessando IMDb Top 250...")
        response = requests.get(url, headers=headers, timeout=10)
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
                # Título e link
                title_element = item.find('h3', class_='ipc-title__text')
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                # Remover número do ranking do título
                if title and title[0].isdigit():
                    title = title.split('.', 1)[1].strip() if '.' in title else title
                
                # Link do filme
                link_element = item.find('a', href=True)
                movie_url = "https://www.imdb.com" + link_element['href'] if link_element else None
                
                # Rating - tentar diferentes seletores
                rating = "N/A"
                rating_selectors = [
                    'span.ipc-rating-star',
                    '.ipc-rating-star',
                    '[data-testid="rating-button"]',
                    '.rating'
                ]
                
                for selector in rating_selectors:
                    rating_element = item.select_one(selector)
                    if rating_element:
                        rating_text = rating_element.get('aria-label', '') or rating_element.text
                        if 'rated' in rating_text.lower():
                            rating = rating_text.split('rated')[1].split('/')[0].strip()
                        elif rating_text.replace('.', '').replace(',', '').isdigit():
                            rating = rating_text
                        break
                
                # Ano - tentar diferentes seletores
                year = "N/A"
                year_selectors = [
                    'span.sc-479f9703-8',
                    '.sc-479f9703-8',
                    '[data-testid="title-year"]',
                    '.title-year'
                ]
                
                for selector in year_selectors:
                    year_element = item.select_one(selector)
                    if year_element:
                        year_text = year_element.text.strip()
                        if year_text.isdigit():
                            year = year_text
                        break
                
                print(f"🎬 Processando filme {i+1}/250: {title} ({year})")
                
                movie_details = scrape_movie_details(movie_url, headers) if movie_url else {}
                
                movie_data = {
                    'rank': i + 1,
                    'title_en': title,
                    'year': int(year) if year.isdigit() else 0,
                    'rating': float(rating) if rating.replace('.', '').isdigit() else 0.0,
                    'genre': movie_details.get('genre', 'N/A'),
                    'sinopse': movie_details.get('plot', 'N/A'),
                    'director': movie_details.get('director', 'N/A'),
                    'cast': movie_details.get('cast', 'N/A'),
                    'duration': movie_details.get('duration', 'N/A')
                }
                
                movies_data.append(movie_data)
                time.sleep(0.5)  # Pausa para evitar sobrecarga
                
            except Exception as e:
                print(f"⚠️ Erro ao processar filme {i+1}: {str(e)}")
                continue
                
        return movies_data
        
    except Exception as e:
        print(f"❌ Erro ao acessar a página: {str(e)}")
        return None

def scrape_movie_details(movie_url, headers):
    """
    Função para extrair detalhes adicionais de cada filme
    Baseada no notebook Notebook1_IMDb_WebScraping_KMeans.ipynb
    """
    try:
        response = requests.get(movie_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        details = {}
        
        # Gênero
        genre_element = soup.find('div', {'data-testid': 'genres'})
        if genre_element:
            genres = [span.text.strip() for span in genre_element.find_all('span')]
            details['genre'] = ', '.join(genres)
        
        # Sinopse/Plot
        plot_element = soup.find('span', {'data-testid': 'plot-xl'})
        if plot_element:
            details['plot'] = plot_element.text.strip()
        else:
            plot_alt = soup.find('div', class_='summary_text')
            if plot_alt:
                details['plot'] = plot_alt.text.strip()
        
        # Diretor
        director_element = soup.find('a', {'data-testid': 'title-pc-principal-credit'})
        if director_element:
            details['director'] = director_element.text.strip()
        
        # Duração
        duration_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})
        if duration_element:
            details['duration'] = duration_element.find('div').text.strip()
        
        return details
        
    except Exception as e:
        print(f"⚠️ Erro ao extrair detalhes do filme: {str(e)}")
        return {}

def save_to_csv(movies_data, filename='imdb_top250_scraped.csv'):
    """Salva os dados em CSV"""
    if not movies_data:
        print("❌ Nenhum dado para salvar")
        return False
    
    df = pd.DataFrame(movies_data)
    df.to_csv(filename, index=False, sep=';')
    print(f"✅ Dados salvos em {filename}")
    return True

def save_to_json(movies_data, filename='imdb_top250_scraped.json'):
    """Salva os dados em JSON para uso na API"""
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
            'title_pt': movie['title_en'],  # Será traduzido depois
            'year': movie['year'],
            'rating': movie['rating'],
            'genre': movie['genre'],
            'sinopse': movie['sinopse'],
            'director': movie['director'],
            'cast': movie['cast'],
            'duration': movie['duration'],
            'cluster': 0,  # Será calculado depois
            'poster_url': f'https://image.tmdb.org/t/p/w500/placeholder.jpg',
            'backdrop_url': f'https://image.tmdb.org/t/p/w1280/placeholder.jpg'
        }
        api_movies.append(api_movie)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(api_movies, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dados da API salvos em {filename}")
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando Web Scraping do IMDb Top 250...")
    print("📋 Baseado no Notebook1_IMDb_WebScraping_KMeans.ipynb")
    
    # Fazer scraping
    movies_data = scrape_imdb_top250()
    
    if movies_data:
        print(f"✅ Scraping concluído! {len(movies_data)} filmes coletados")
        
        # Salvar dados
        save_to_csv(movies_data)
        save_to_json(movies_data)
        
        # Estatísticas
        print(f"\n📊 Estatísticas:")
        print(f"   - Total de filmes: {len(movies_data)}")
        print(f"   - Rating médio: {np.mean([m['rating'] for m in movies_data if m['rating'] > 0]):.2f}")
        print(f"   - Ano médio: {np.mean([m['year'] for m in movies_data if m['year'] > 0]):.0f}")
        
        # Mostrar primeiros filmes
        print(f"\n🎬 Primeiros 5 filmes:")
        for i, movie in enumerate(movies_data[:5]):
            print(f"   {i+1}. {movie['title_en']} ({movie['year']}) - {movie['rating']}/10")
        
        return movies_data
    else:
        print("❌ Falha no scraping")
        return None

if __name__ == "__main__":
    main()
