"""
Script para integrar os notebooks desenvolvidos nas aulas 01-04
com o sistema FiapFlix
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

def load_notebook_data():
    """Carrega dados dos notebooks existentes"""
    
    # Caminhos dos arquivos
    notebook1_data = 'imdb_top250_with_clusters.csv'
    notebook2_data = 'model_comparison_summary.csv'
    
    data = {}
    
    # Carregar dados do Notebook 1
    if os.path.exists(notebook1_data):
        df1 = pd.read_csv(notebook1_data, sep=';')
        data['movies'] = df1
        print(f"✅ Dados do Notebook 1 carregados: {len(df1)} filmes")
    else:
        print("⚠️ Arquivo imdb_top250_with_clusters.csv não encontrado")
    
    # Carregar dados do Notebook 2
    if os.path.exists(notebook2_data):
        df2 = pd.read_csv(notebook2_data, sep=';')
        data['model_comparison'] = df2
        print(f"✅ Dados do Notebook 2 carregados: {len(df2)} modelos")
    else:
        print("⚠️ Arquivo model_comparison_summary.csv não encontrado")
    
    return data

def create_api_data(data):
    """Converte dados dos notebooks para formato da API"""
    
    if 'movies' not in data:
        print("❌ Dados de filmes não encontrados")
        return None
    
    movies_df = data['movies']
    api_movies = []
    
    for _, movie in movies_df.iterrows():
        api_movie = {
            'id': str(movie.get('rank', '')),
            'rank': int(movie.get('rank', 0)),
            'title_en': str(movie.get('title_en', '')),
            'title_pt': str(movie.get('title_pt', '')),
            'year': int(movie.get('year', 0)) if pd.notna(movie.get('year')) else 0,
            'rating': float(movie.get('rating', 0)) if pd.notna(movie.get('rating')) else 0,
            'genre': str(movie.get('genre', '')),
            'sinopse': str(movie.get('sinopse', '')),
            'director': str(movie.get('director', '')),
            'cast': str(movie.get('cast', '')),
            'duration': str(movie.get('duration', '')),
            'cluster': int(movie.get('cluster', 0)) if pd.notna(movie.get('cluster')) else 0,
            'poster_url': f'/api/placeholder/300/450',
            'backdrop_url': f'/api/placeholder/1920/1080'
        }
        api_movies.append(api_movie)
    
    return api_movies

def create_model_config(data):
    """Cria configuração do modelo baseada nos notebooks"""
    
    config = {
        'model_info': {
            'name': 'FiapFlix Recommendation Model',
            'version': '1.0.0',
            'description': 'Modelo de recomendação baseado em clusterização KMeans',
            'created_by': 'FIAP - Front End & Mobile Development',
            'date': '2025'
        },
        'clusters': {},
        'model_comparison': {}
    }
    
    if 'movies' in data:
        movies_df = data['movies']
        
        # Análise por cluster
        for cluster_id in sorted(movies_df['cluster'].unique()):
            cluster_movies = movies_df[movies_df['cluster'] == cluster_id]
            
            config['clusters'][str(cluster_id)] = {
                'movie_count': len(cluster_movies),
                'avg_rating': float(cluster_movies['rating'].mean()),
                'avg_year': float(cluster_movies['year'].mean()),
                'top_genres': cluster_movies['genre'].value_counts().head(3).to_dict(),
                'representative_movies': cluster_movies.nlargest(3, 'rating')['title_en'].tolist()
            }
    
    if 'model_comparison' in data:
        comparison_df = data['model_comparison']
        config['model_comparison'] = comparison_df.to_dict('records')
    
    return config

def save_integration_files(api_movies, model_config):
    """Salva arquivos de integração"""
    
    # Criar diretório de dados
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Salvar dados da API
    with open(data_dir / 'api_movies.json', 'w', encoding='utf-8') as f:
        json.dump(api_movies, f, ensure_ascii=False, indent=2)
    
    # Salvar configuração do modelo
    with open(data_dir / 'model_config.json', 'w', encoding='utf-8') as f:
        json.dump(model_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Arquivos de integração salvos em {data_dir}")

def generate_summary_report(data, api_movies, model_config):
    """Gera relatório de integração"""
    
    report = {
        'integration_summary': {
            'total_movies': len(api_movies),
            'total_clusters': len(model_config['clusters']),
            'notebooks_integrated': ['Notebook 1: Web Scraping e KMeans', 'Notebook 2: Comparação de Modelos'],
            'features_implemented': [
                'Sistema de recomendação baseado em clusterização',
                'Interface Netflix-like responsiva',
                'Dois métodos de recomendação',
                'Integração com modelos treinados',
                'API RESTful para frontend'
            ]
        },
        'cluster_analysis': model_config['clusters'],
        'model_performance': model_config.get('model_comparison', {})
    }
    
    # Salvar relatório
    with open('data/integration_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("✅ Relatório de integração gerado")

def main():
    """Função principal de integração"""
    
    print("🚀 Iniciando integração dos notebooks com FiapFlix...")
    
    # 1. Carregar dados dos notebooks
    print("\n📊 Carregando dados dos notebooks...")
    data = load_notebook_data()
    
    if not data:
        print("❌ Nenhum dado encontrado. Verifique se os notebooks foram executados.")
        return
    
    # 2. Converter para formato da API
    print("\n🔄 Convertendo dados para formato da API...")
    api_movies = create_api_data(data)
    
    if not api_movies:
        print("❌ Erro ao converter dados para API")
        return
    
    # 3. Criar configuração do modelo
    print("\n🤖 Criando configuração do modelo...")
    model_config = create_model_config(data)
    
    # 4. Salvar arquivos de integração
    print("\n💾 Salvando arquivos de integração...")
    save_integration_files(api_movies, model_config)
    
    # 5. Gerar relatório
    print("\n📋 Gerando relatório de integração...")
    generate_summary_report(data, api_movies, model_config)
    
    print("\n✅ Integração concluída com sucesso!")
    print(f"📁 Arquivos gerados:")
    print(f"   - data/api_movies.json")
    print(f"   - data/model_config.json")
    print(f"   - data/integration_report.json")
    
    print(f"\n📊 Estatísticas:")
    print(f"   - Total de filmes: {len(api_movies)}")
    print(f"   - Clusters identificados: {len(model_config['clusters'])}")
    print(f"   - Notebooks integrados: 2")

if __name__ == "__main__":
    main()
