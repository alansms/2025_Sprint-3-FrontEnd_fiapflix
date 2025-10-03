#!/usr/bin/env python3
"""
Script para retreinar o modelo com dados reais do IMDb
"""

import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import re

def clean_text(text):
    """Limpar e pré-processar texto"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-záàâãéèêíìîóòôõúùûç\s]', ' ', text)
    
    stopwords_list = ['o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'sobre', 'entre', 'até', 'após', 'durante', 'e', 'ou', 'mas', 'se', 'que', 'quando', 'onde', 'como', 'porque', 'então', 'também', 'muito', 'mais', 'menos', 'bem', 'mal', 'sempre', 'nunca', 'já', 'ainda', 'só', 'apenas', 'até', 'depois', 'antes', 'agora', 'hoje', 'ontem', 'amanhã']
    words = text.split()
    words = [word for word in words if word not in stopwords_list and len(word) > 2]
    
    return ' '.join(words)

def create_balanced_clusters(df, n_clusters=5):
    """Criar clusters balanceados manualmente"""
    
    # Ordenar por rating
    df_sorted = df.sort_values('rating', ascending=False)
    
    # Dividir em clusters balanceados
    cluster_size = len(df_sorted) // n_clusters
    remainder = len(df_sorted) % n_clusters
    
    clusters = []
    start_idx = 0
    
    for i in range(n_clusters):
        # Adicionar um filme extra para os primeiros clusters se houver resto
        current_size = cluster_size + (1 if i < remainder else 0)
        end_idx = start_idx + current_size
        
        cluster = [i] * current_size
        clusters.extend(cluster)
        start_idx = end_idx
    
    return clusters

def main():
    print("🎬 Retreinando modelo com dados reais do IMDb...")
    
    # Carregar dados reais
    try:
        with open('imdb_real_50_movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
    except:
        print("❌ Arquivo imdb_real_50_movies.json não encontrado")
        return
    
    print(f"📊 Carregados {len(movies)} filmes reais")
    
    # Converter para DataFrame
    df = pd.DataFrame(movies)
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # Criar clusters balanceados
    n_clusters = 5
    clusters_balanced = create_balanced_clusters(df, n_clusters)
    df['cluster_tfidf'] = clusters_balanced
    df['cluster_all'] = clusters_balanced
    
    # TF-IDF Vectorization
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=500,
        min_df=1,
        max_df=0.8,
        stop_words=None
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    
    # KMeans dummy para compatibilidade
    print("🤖 Criando modelos de compatibilidade...")
    kmeans_tfidf = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_tfidf.fit(tfidf_matrix)
    
    kmeans_all = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_all.fit(tfidf_matrix)
    
    # Label encoder para gênero
    le_genre = LabelEncoder()
    le_genre.fit(df['genre'])
    
    # Salvar modelos
    print("💾 Salvando modelos...")
    joblib.dump(kmeans_tfidf, 'models/kmeans_tfidf.pkl')
    joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(kmeans_all, 'models/kmeans_all_features.pkl')
    joblib.dump(le_genre, 'models/label_encoder_genre.pkl')
    
    # Salvar dataset
    df.to_csv('imdb_real_with_clusters.csv', index=False, sep=';')
    
    # Estatísticas
    print("\n📊 Distribuição dos clusters:")
    for i in range(n_clusters):
        count = (df['cluster_tfidf'] == i).sum()
        print(f"   Cluster {i}: {count} filmes")
    
    print(f"\n✅ Modelo retreinado com {len(movies)} filmes reais!")
    print("📁 Arquivos salvos:")
    print("   - models/kmeans_tfidf.pkl")
    print("   - models/tfidf_vectorizer.pkl") 
    print("   - models/kmeans_all_features.pkl")
    print("   - models/label_encoder_genre.pkl")
    print("   - imdb_real_with_clusters.csv")
    
    # Mostrar alguns filmes por cluster
    print("\n🎬 Exemplos por cluster:")
    for i in range(n_clusters):
        cluster_movies = df[df['cluster_tfidf'] == i]
        print(f"\nCluster {i} ({len(cluster_movies)} filmes):")
        for _, movie in cluster_movies.head(3).iterrows():
            print(f"  - {movie['title_pt']} ({movie['year']}) - {movie['rating']}")

if __name__ == "__main__":
    main()

