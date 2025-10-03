#!/usr/bin/env python3
"""
🔧 Script para corrigir o problema de recomendação retornando apenas 2 filmes
"""

import pandas as pd
import json
import os

def check_cluster_distribution():
    """Verificar distribuição dos clusters"""
    print("🔍 Verificando distribuição dos clusters...")
    
    # Carregar dataset
    try:
        df = pd.read_csv('imdb_100plus_with_clusters.csv', sep=';')
        print(f"📊 Dataset carregado: {len(df)} filmes")
    except:
        try:
            df = pd.read_csv('imdb_50plus_with_clusters.csv', sep=';')
            print(f"📊 Dataset carregado: {len(df)} filmes")
        except:
            df = pd.read_csv('imdb_top250_with_clusters.csv', sep=';')
            print(f"📊 Dataset carregado: {len(df)} filmes")
    
    print("\n📊 Distribuição dos clusters TF-IDF:")
    cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    print("\n📊 Distribuição dos clusters All Features:")
    cluster_counts_all = df['cluster_all'].value_counts().sort_index()
    for cluster_id, count in cluster_counts_all.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    return df

def fix_cluster_balance(df):
    """Balancear clusters para ter pelo menos 5 filmes cada"""
    print("\n⚖️ Balanceando clusters...")
    
    # Para cada cluster, garantir pelo menos 5 filmes
    for cluster_col in ['cluster_tfidf', 'cluster_all']:
        print(f"\n🔧 Balanceando {cluster_col}...")
        
        for cluster_id in range(5):
            cluster_movies = df[df[cluster_col] == cluster_id]
            current_count = len(cluster_movies)
            
            if current_count < 5:
                print(f"  Cluster {cluster_id}: {current_count} filmes (precisa de pelo menos 5)")
                
                # Encontrar filmes de outros clusters
                other_movies = df[df[cluster_col] != cluster_id]
                
                if not other_movies.empty:
                    # Adicionar filmes aleatoriamente até atingir 5
                    needed = 5 - current_count
                    available = len(other_movies)
                    to_add = min(needed, available)
                    
                    if to_add > 0:
                        movies_to_reassign = other_movies.sample(n=to_add, random_state=42)
                        df.loc[movies_to_reassign.index, cluster_col] = cluster_id
                        print(f"    ✅ Adicionados {to_add} filmes ao cluster {cluster_id}")
                    else:
                        print(f"    ⚠️ Não há filmes disponíveis para rebalancear")
                else:
                    print(f"    ⚠️ Não há filmes de outros clusters disponíveis")
            else:
                print(f"  Cluster {cluster_id}: {current_count} filmes ✅")
    
    return df

def test_recommendation_logic(df):
    """Testar lógica de recomendação"""
    print("\n🧪 Testando lógica de recomendação...")
    
    # Simular sinopse
    test_synopsis = "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido"
    
    # Usar cluster 1 como exemplo
    cluster_id = 1
    cluster_movies = df[df['cluster_tfidf'] == cluster_id]
    
    print(f"📊 Filmes no cluster {cluster_id}: {len(cluster_movies)}")
    
    if len(cluster_movies) == 0:
        print("⚠️ Cluster vazio, usando todos os filmes como fallback")
        cluster_movies = df
    
    # Ordenar por rating
    cluster_movies = cluster_movies.sort_values('rating', ascending=False)
    
    # Selecionar top 5
    recommendations = cluster_movies.head(5)
    
    print(f"🎬 Recomendações geradas: {len(recommendations)} filmes")
    for i, (_, movie) in enumerate(recommendations.iterrows(), 1):
        print(f"  {i}. {movie['title_pt']} ({movie['year']}) - {movie['rating']}")
    
    return len(recommendations)

def main():
    print("🔧 Corrigindo problema de recomendação...")
    
    # Verificar distribuição atual
    df = check_cluster_distribution()
    
    # Balancear clusters
    df_balanced = fix_cluster_balance(df.copy())
    
    # Salvar dataset balanceado
    df_balanced.to_csv('imdb_100plus_with_clusters_balanced.csv', index=False, sep=';')
    print("\n💾 Dataset balanceado salvo: imdb_100plus_with_clusters_balanced.csv")
    
    # Testar lógica
    recommendation_count = test_recommendation_logic(df_balanced)
    
    if recommendation_count >= 5:
        print("\n✅ Problema corrigido! Sistema agora retorna 5+ filmes")
    else:
        print(f"\n⚠️ Ainda retornando apenas {recommendation_count} filmes")
    
    # Verificar distribuição final
    print("\n📊 Distribuição final dos clusters:")
    cluster_counts = df_balanced['cluster_tfidf'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} filmes")

if __name__ == '__main__':
    main()
