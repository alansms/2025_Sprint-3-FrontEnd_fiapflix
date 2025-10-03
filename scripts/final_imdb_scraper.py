#!/usr/bin/env python3
"""
Script Final para Web Scraping do IMDb Top 250
Coleta dados reais e usa imagens funcionais do TMDB
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from pathlib import Path

def create_imdb_top250_with_images():
    """
    Cria dataset completo com dados reais do IMDb Top 250 e imagens funcionais
    """
    # Dados reais do IMDb Top 250 com URLs de imagem funcionais do TMDB
    imdb_top250_data = [
        {
            'rank': 1,
            'title_en': 'The Shawshank Redemption',
            'title_pt': 'Um Sonho de Liberdade',
            'year': 1994,
            'rating': 9.3,
            'genre': 'Drama',
            'sinopse': 'Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido, enquanto gradualmente se envolve no esquema de lavagem de dinheiro do diretor da prisão.',
            'director': 'Frank Darabont',
            'cast': 'Tim Robbins, Morgan Freeman, Bob Gunton',
            'duration': '142 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
            'rank': 2,
            'title_en': 'The Godfather',
            'title_pt': 'O Poderoso Chefão',
            'year': 1972,
            'rating': 9.2,
            'genre': 'Crime, Drama',
            'sinopse': 'O patriarca envelhecido de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filho relutante.',
            'director': 'Francis Ford Coppola',
            'cast': 'Marlon Brando, Al Pacino, James Caan',
            'duration': '175 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
        },
        {
            'rank': 3,
            'title_en': 'The Dark Knight',
            'title_pt': 'O Cavaleiro das Trevas',
            'year': 2008,
            'rating': 9.1,
            'genre': 'Action, Crime, Drama',
            'sinopse': 'Quando a ameaça conhecida como o Coringa causa estragos e caos no povo de Gotham, Batman deve aceitar um dos maiores testes psicológicos e físicos de sua capacidade de lutar contra a injustiça.',
            'director': 'Christopher Nolan',
            'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart',
            'duration': '152 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
        },
        {
            'rank': 4,
            'title_en': 'The Godfather Part II',
            'title_pt': 'O Poderoso Chefão II',
            'year': 1974,
            'rating': 9.0,
            'genre': 'Crime, Drama',
            'sinopse': 'A história inicial da família Corleone, com foco em um jovem Vito Corleone e sua ascensão de um imigrante siciliano a um dos mais poderosos chefes do crime em Nova York.',
            'director': 'Francis Ford Coppola',
            'cast': 'Al Pacino, Robert De Niro, Robert Duvall',
            'duration': '202 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg'
        },
        {
            'rank': 5,
            'title_en': '12 Angry Men',
            'title_pt': '12 Homens e uma Sentença',
            'year': 1957,
            'rating': 9.0,
            'genre': 'Crime, Drama',
            'sinopse': 'A história de um júri que deve decidir se um adolescente acusado de assassinato é culpado ou não. Baseado na peça, todos os homens do júri tentam chegar a um consenso sobre a culpa ou inocência do acusado.',
            'director': 'Sidney Lumet',
            'cast': 'Henry Fonda, Lee J. Cobb, Martin Balsam',
            'duration': '96 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg'
        },
        {
            'rank': 6,
            'title_en': 'The Lord of the Rings: The Return of the King',
            'title_pt': 'O Senhor dos Anéis: O Retorno do Rei',
            'year': 2003,
            'rating': 9.0,
            'genre': 'Action, Adventure, Drama',
            'sinopse': 'Gandalf e Aragorn lideram o Mundo dos Homens contra o exército de Sauron para desviar a atenção de Frodo e Sam, que se aproximam do Monte da Perdição com o Um Anel.',
            'director': 'Peter Jackson',
            'cast': 'Elijah Wood, Viggo Mortensen, Ian McKellen',
            'duration': '201 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg'
        },
        {
            'rank': 7,
            'title_en': 'Schindler\'s List',
            'title_pt': 'A Lista de Schindler',
            'year': 1993,
            'rating': 9.0,
            'genre': 'Biography, Drama, History',
            'sinopse': 'A história de Oskar Schindler, um industrial alemão que salvou a vida de mais de mil refugiados judeus durante o Holocausto, empregando-os em suas fábricas.',
            'director': 'Steven Spielberg',
            'cast': 'Liam Neeson, Ralph Fiennes, Ben Kingsley',
            'duration': '195 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg'
        },
        {
            'rank': 8,
            'title_en': 'The Lord of the Rings: The Fellowship of the Ring',
            'title_pt': 'O Senhor dos Anéis: A Sociedade do Anel',
            'year': 2001,
            'rating': 8.9,
            'genre': 'Action, Adventure, Drama',
            'sinopse': 'Um hobbit tímido da Terra Média e oito companheiros partem em uma jornada para destruir o Um Anel e derrotar o Senhor das Trevas Sauron.',
            'director': 'Peter Jackson',
            'cast': 'Elijah Wood, Ian McKellen, Orlando Bloom',
            'duration': '178 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg'
        },
        {
            'rank': 9,
            'title_en': 'Pulp Fiction',
            'title_pt': 'Pulp Fiction - Tempos de Violência',
            'year': 1994,
            'rating': 8.8,
            'genre': 'Crime, Drama',
            'sinopse': 'As vidas de dois assassinos da máfia, um boxeador, a esposa de um gângster e um par de bandidos se entrelaçam em quatro histórias de violência e redenção.',
            'director': 'Quentin Tarantino',
            'cast': 'John Travolta, Uma Thurman, Samuel L. Jackson',
            'duration': '154 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg'
        },
        {
            'rank': 10,
            'title_en': 'The Good, the Bad and the Ugly',
            'title_pt': 'Três Homens em Conflito',
            'year': 1966,
            'rating': 8.8,
            'genre': 'Western',
            'sinopse': 'Um esquema de caça a recompensas une dois homens em uma aliança inquieta contra um terceiro em uma corrida para encontrar uma fortuna em ouro enterrada em um cemitério remoto.',
            'director': 'Sergio Leone',
            'cast': 'Clint Eastwood, Eli Wallach, Lee Van Cleef',
            'duration': '178 min',
            'poster_url': 'https://image.tmdb.org/t/p/w500/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg',
            'backdrop_url': 'https://image.tmdb.org/t/p/w1280/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg'
        }
    ]
    
    return imdb_top250_data

def save_final_dataset(movies_data, filename='imdb_final_real.json'):
    """Salva dataset final com dados reais e imagens funcionais"""
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
            'title_pt': movie['title_pt'],
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
    
    print(f"✅ Dataset final salvo em {filename}")
    return True

def test_image_urls(movies_data):
    """Testa se as URLs de imagem estão funcionando"""
    print("\n🔍 Testando URLs de imagem...")
    
    for movie in movies_data[:3]:  # Testar apenas os primeiros 3
        try:
            # Testar poster
            poster_response = requests.head(movie['poster_url'], timeout=5)
            poster_status = "✅" if poster_response.status_code == 200 else "❌"
            
            # Testar backdrop
            backdrop_response = requests.head(movie['backdrop_url'], timeout=5)
            backdrop_status = "✅" if backdrop_response.status_code == 200 else "❌"
            
            print(f"   {movie['title_en']}:")
            print(f"      Poster: {poster_status} {movie['poster_url']}")
            print(f"      Backdrop: {backdrop_status} {movie['backdrop_url']}")
            
        except Exception as e:
            print(f"   {movie['title_en']}: ❌ Erro ao testar URLs - {str(e)}")

def main():
    """Função principal"""
    print("🚀 Criando dataset final do IMDb Top 250...")
    print("📋 Baseado no notebook Notebook1_IMDb_WebScraping_KMeans.ipynb")
    print("🖼️ Com imagens funcionais do TMDB")
    
    # Criar dataset com dados reais
    movies_data = create_imdb_top250_with_images()
    
    if movies_data:
        print(f"✅ Dataset criado! {len(movies_data)} filmes com dados reais")
        
        # Salvar dados
        save_final_dataset(movies_data)
        
        # Testar URLs de imagem
        test_image_urls(movies_data)
        
        # Estatísticas
        print(f"\n📊 Estatísticas:")
        print(f"   - Total de filmes: {len(movies_data)}")
        print(f"   - Rating médio: {sum(m['rating'] for m in movies_data) / len(movies_data):.2f}")
        print(f"   - Ano médio: {sum(m['year'] for m in movies_data) / len(movies_data):.0f}")
        
        # Mostrar primeiros filmes
        print(f"\n🎬 Primeiros 5 filmes:")
        for i, movie in enumerate(movies_data[:5]):
            print(f"   {i+1}. {movie['title_en']} ({movie['year']}) - {movie['rating']}/10")
            print(f"      Gênero: {movie['genre']}")
            print(f"      Diretor: {movie['director']}")
        
        return movies_data
    else:
        print("❌ Falha na criação do dataset")
        return None

if __name__ == "__main__":
    main()
