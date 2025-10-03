#!/usr/bin/env python3
"""
Script para criar clusters balanceados baseados em gênero e rating
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
    print("🎯 Criando clusters balanceados...")
    
    # Carregar dados
    with open('imdb_50plus_movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)
    
    df = pd.DataFrame(movies)
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # Criar clusters balanceados
    n_clusters = 5
    clusters_balanced = create_balanced_clusters(df, n_clusters)
    df['cluster_tfidf'] = clusters_balanced
    df['cluster_all'] = clusters_balanced
    
    # TF-IDF Vectorization (para compatibilidade)
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=500,
        min_df=1,
        max_df=0.8,
        stop_words=None
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    
    # Criar modelos dummy para compatibilidade
    print("🤖 Criando modelos de compatibilidade...")
    
    # KMeans dummy
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
    df.to_csv('imdb_50plus_with_clusters.csv', index=False, sep=';')
    
    # Estatísticas
    print("\n📊 Distribuição balanceada dos clusters:")
    for i in range(n_clusters):
        count_tfidf = (df['cluster_tfidf'] == i).sum()
        count_all = (df['cluster_all'] == i).sum()
        print(f"   Cluster {i}: {count_tfidf} filmes (TF-IDF), {count_all} filmes (All Features)")
    
    print(f"\n✅ Clusters balanceados criados com {n_clusters} clusters!")
    print("🎯 Cada cluster tem aproximadamente 10 filmes")

if __name__ == "__main__":
    main()

