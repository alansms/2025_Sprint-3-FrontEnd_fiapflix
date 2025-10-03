#!/usr/bin/env python3
"""
Script para corrigir o clustering e melhorar a distribuição
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

def main():
    print("🔧 Corrigindo clustering...")
    
    # Carregar dados
    with open('imdb_50plus_movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)
    
    df = pd.DataFrame(movies)
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # Usar apenas 3 clusters para melhor distribuição
    n_clusters = 3
    
    # TF-IDF Vectorization
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=500,  # Reduzir features
        min_df=1,          # Reduzir min_df
        max_df=0.8,        # Ajustar max_df
        stop_words=None
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    
    # KMeans com TF-IDF
    print("🤖 Treinando KMeans TF-IDF com 3 clusters...")
    kmeans_tfidf = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    clusters_tfidf = kmeans_tfidf.fit_predict(tfidf_matrix)
    df['cluster_tfidf'] = clusters_tfidf
    
    # Features numéricas
    print("📊 Preparando features numéricas...")
    df['year_norm'] = (df['year'] - df['year'].min()) / (df['year'].max() - df['year'].min())
    df['rating_norm'] = (df['rating'] - df['rating'].min()) / (df['rating'].max() - df['rating'].min())
    
    # Label encoding para gênero
    le_genre = LabelEncoder()
    df['genre_encoded'] = le_genre.fit_transform(df['genre'])
    
    # Features combinadas
    features_all = np.column_stack([
        tfidf_matrix.toarray(),
        df['year_norm'].values,
        df['rating_norm'].values,
        df['genre_encoded'].values
    ])
    
    # KMeans com todas as features
    print("🤖 Treinando KMeans com todas as features...")
    kmeans_all = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    clusters_all = kmeans_all.fit_predict(features_all)
    df['cluster_all'] = clusters_all
    
    # Salvar modelos
    print("💾 Salvando modelos corrigidos...")
    joblib.dump(kmeans_tfidf, 'models/kmeans_tfidf.pkl')
    joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(kmeans_all, 'models/kmeans_all_features.pkl')
    joblib.dump(le_genre, 'models/label_encoder_genre.pkl')
    
    # Salvar dataset
    df.to_csv('imdb_50plus_with_clusters.csv', index=False, sep=';')
    
    # Estatísticas
    print("\n📊 Nova distribuição dos clusters:")
    print("TF-IDF Clusters:")
    for i in range(n_clusters):
        count = (df['cluster_tfidf'] == i).sum()
        print(f"   Cluster {i}: {count} filmes")
    
    print("All Features Clusters:")
    for i in range(n_clusters):
        count = (df['cluster_all'] == i).sum()
        print(f"   Cluster {i}: {count} filmes")
    
    print(f"\n✅ Clustering corrigido com {n_clusters} clusters!")

if __name__ == "__main__":
    main()

