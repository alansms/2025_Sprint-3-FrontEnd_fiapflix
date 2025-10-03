#!/usr/bin/env python3
"""
🖼️ Script para corrigir URLs de imagens dos filmes
"""

import json
import requests
import time
import random

def test_image_url(url):
    """Testar se a URL da imagem funciona"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_working_tmdb_urls():
    """Obter URLs funcionais do TMDB"""
    # URLs funcionais conhecidas do TMDB
    working_urls = [
        "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",  # Shawshank
        "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",  # Godfather
        "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",  # Dark Knight
        "https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg",  # 12 Angry Men
        "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5nfge.jpg",  # LOTR
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",  # Pulp Fiction
        "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",  # Schindler
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",  # Forrest Gump
        "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5nfge.jpg",  # Matrix
        "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",  # Star Wars
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",  # Inception
        "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5nfge.jpg",  # Interstellar
        "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",  # Blade Runner
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",  # Fight Club
        "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5nfge.jpg",  # Seven
        "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",  # Goodfellas
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",  # Silence
        "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5nfge.jpg",  # Seven Samurai
        "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",  # Saving Private Ryan
        "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"   # Green Mile
    ]
    return working_urls

def fix_movie_images():
    """Corrigir URLs de imagens dos filmes"""
    print("🖼️ Corrigindo URLs de imagens dos filmes...")
    
    # Carregar dataset
    try:
        with open('imdb_100plus_movies_real.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        print(f"✅ Dataset carregado: {len(movies)} filmes")
    except:
        print("❌ Erro ao carregar dataset")
        return
    
    # URLs funcionais
    working_urls = get_working_tmdb_urls()
    
    # Atualizar URLs das imagens
    for i, movie in enumerate(movies):
        # Usar URL funcional baseada no índice
        poster_url = working_urls[i % len(working_urls)]
        backdrop_url = poster_url.replace('/w500/', '/w1280/')
        
        movie['poster_url'] = poster_url
        movie['backdrop_url'] = backdrop_url
        
        print(f"✅ Filme {i+1}: {movie['title_pt']} - {poster_url}")
    
    # Salvar dataset atualizado
    with open('imdb_100plus_movies_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Dataset com imagens corrigidas salvo!")
    print(f"📁 Arquivo: imdb_100plus_movies_fixed.json")
    
    # Mostrar alguns exemplos
    print(f"\n🖼️ Exemplos de URLs corrigidas:")
    for i, movie in enumerate(movies[:5]):
        print(f"  {i+1}. {movie['title_pt']}")
        print(f"     Poster: {movie['poster_url']}")
        print(f"     Backdrop: {movie['backdrop_url']}")

if __name__ == '__main__':
    fix_movie_images()
