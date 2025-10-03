#!/usr/bin/env python3
"""
🐛 Script para debugar o problema de recomendações
"""

import pandas as pd
import json
import os

def debug_recommendations():
    """Debugar sistema de recomendações"""
    print("🐛 Debugando sistema de recomendações...")
    
    # Carregar dataset
    try:
        df = pd.read_csv('imdb_100plus_with_clusters.csv', sep=';')
        print(f"✅ Dataset carregado: {len(df)} filmes")
    except:
        try:
            df = pd.read_csv('imdb_50plus_with_clusters.csv', sep=';')
            print(f"✅ Dataset carregado: {len(df)} filmes")
        except:
            df = pd.read_csv('imdb_top250_with_clusters.csv', sep=';')
            print(f"✅ Dataset carregado: {len(df)} filmes")
    
    print(f"\n📊 Colunas disponíveis: {list(df.columns)}")
    
    # Verificar clusters
    if 'cluster_tfidf' in df.columns:
        print(f"\n📊 Distribuição cluster_tfidf:")
        cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
        for cluster_id, count in cluster_counts.items():
            print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Testar com cluster 1 (que está retornando apenas 2 filmes)
    cluster_id = 1
    cluster_movies = df[df['cluster_tfidf'] == cluster_id]
    
    print(f"\n🧪 Testando cluster {cluster_id}:")
    print(f"📊 Filmes no cluster: {len(cluster_movies)}")
    
    if len(cluster_movies) > 0:
        # Ordenar por rating
        cluster_movies = cluster_movies.sort_values('rating', ascending=False)
        
        # Selecionar top 5
        recommendations = cluster_movies.head(5)
        
        print(f"🎬 Recomendações geradas: {len(recommendations)} filmes")
        for i, (_, movie) in enumerate(recommendations.iterrows(), 1):
            print(f"  {i}. {movie.get('title_pt', 'N/A')} ({movie.get('year', 'N/A')}) - {movie.get('rating', 'N/A')}")
    else:
        print("⚠️ Cluster vazio!")
    
    # Verificar se há problema com IDs duplicados
    print(f"\n🔍 Verificando IDs únicos:")
    ids = df['id'].tolist()
    unique_ids = set(ids)
    print(f"  Total de IDs: {len(ids)}")
    print(f"  IDs únicos: {len(unique_ids)}")
    
    if len(ids) != len(unique_ids):
        print("❌ Há IDs duplicados!")
        from collections import Counter
        id_counts = Counter(ids)
        duplicates = {id: count for id, count in id_counts.items() if count > 1}
        print(f"  IDs duplicados: {duplicates}")
    else:
        print("✅ Todos os IDs são únicos")

def test_api_call():
    """Testar chamada da API"""
    print("\n🌐 Testando chamada da API...")
    
    import subprocess
    
    test_data = {
        "synopsis": "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
        "method": "tfidf"
    }
    
    try:
        result = subprocess.run([
            'python3', 'lib/run_recommendation.py', 
            json.dumps(test_data)
        ], capture_output=True, text=True, cwd='.')
        
        print(f"📤 Comando executado")
        print(f"📥 stdout: {result.stdout}")
        if result.stderr:
            print(f"❌ stderr: {result.stderr}")
        
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
    debug_recommendations()
    test_api_call()
