#!/usr/bin/env python3
"""
🐛 Script para debugar o problema de recomendação
"""

import sys
import json
import pandas as pd
import joblib
import os

def debug_recommendation():
    """Debugar o sistema de recomendação"""
    print("🐛 Debugando sistema de recomendação...")
    
    # Testar carregamento do dataset
    datasets_to_try = [
        'imdb_100plus_with_clusters.csv',
        'imdb_50plus_with_clusters.csv', 
        'imdb_top250_with_clusters.csv'
    ]
    
    df = None
    for dataset in datasets_to_try:
        try:
            df = pd.read_csv(dataset, sep=';')
            print(f"✅ Dataset carregado: {dataset} ({len(df)} filmes)")
            break
        except Exception as e:
            print(f"❌ Erro ao carregar {dataset}: {e}")
    
    if df is None:
        print("❌ Nenhum dataset encontrado!")
        return
    
    # Verificar colunas
    print(f"\n📊 Colunas disponíveis: {list(df.columns)}")
    
    # Verificar clusters
    if 'cluster_tfidf' in df.columns:
        print(f"\n📊 Distribuição cluster_tfidf:")
        cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
        for cluster_id, count in cluster_counts.items():
            print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Simular recomendação
    print(f"\n🧪 Simulando recomendação...")
    
    # Usar cluster 1 como exemplo
    cluster_id = 1
    cluster_movies = df[df['cluster_tfidf'] == cluster_id]
    
    print(f"📊 Filmes no cluster {cluster_id}: {len(cluster_movies)}")
    
    if len(cluster_movies) == 0:
        print("⚠️ Cluster vazio!")
        return
    
    # Ordenar por rating
    cluster_movies = cluster_movies.sort_values('rating', ascending=False)
    
    # Selecionar top 5
    recommendations = cluster_movies.head(5)
    
    print(f"🎬 Recomendações geradas: {len(recommendations)} filmes")
    for i, (_, movie) in enumerate(recommendations.iterrows(), 1):
        print(f"  {i}. {movie.get('title_pt', 'N/A')} ({movie.get('year', 'N/A')}) - {movie.get('rating', 'N/A')}")
    
    # Testar com diferentes clusters
    print(f"\n🔍 Testando todos os clusters:")
    for cluster_id in range(5):
        cluster_movies = df[df['cluster_tfidf'] == cluster_id]
        print(f"  Cluster {cluster_id}: {len(cluster_movies)} filmes")
        
        if len(cluster_movies) > 0:
            top_movies = cluster_movies.sort_values('rating', ascending=False).head(3)
            for _, movie in top_movies.iterrows():
                print(f"    - {movie.get('title_pt', 'N/A')} ({movie.get('rating', 'N/A')})")

def test_api_call():
    """Testar chamada da API"""
    print("\n🌐 Testando chamada da API...")
    
    import subprocess
    
    # Simular chamada da API
    test_data = {
        "synopsis": "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
        "method": "tfidf"
    }
    
    try:
        # Executar script Python diretamente
        result = subprocess.run([
            'python3', 'lib/run_recommendation.py', 
            json.dumps(test_data)
        ], capture_output=True, text=True, cwd='.')
        
        print(f"📤 Comando executado")
        print(f"📥 stdout: {result.stdout}")
        if result.stderr:
            print(f"❌ stderr: {result.stderr}")
        
        # Parse do resultado
        if result.stdout:
            try:
                api_result = json.loads(result.stdout)
                print(f"✅ API retornou {len(api_result.get('recommendations', []))} filmes")
                for i, movie in enumerate(api_result.get('recommendations', [])[:3], 1):
                    print(f"  {i}. {movie.get('title_pt', 'N/A')} ({movie.get('rating', 'N/A')})")
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao fazer parse do JSON: {e}")
                print(f"Raw output: {result.stdout}")
        
    except Exception as e:
        print(f"❌ Erro ao executar API: {e}")

if __name__ == '__main__':
    debug_recommendation()
    test_api_call()

