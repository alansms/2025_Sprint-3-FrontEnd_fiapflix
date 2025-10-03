#!/usr/bin/env python3
"""
Script para retreinar o modelo com os 50 filmes
"""

import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import joblib
import re
import nltk
from nltk.corpus import stopwords

# Download NLTK data
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords', quiet=True)

def clean_text(text):
    """Limpar e pré-processar texto"""
    if pd.isna(text):
        return ""
    
    # Converter para minúsculas
    text = str(text).lower()
    
    # Remover caracteres especiais
    text = re.sub(r'[^a-záàâãéèêíìîóòôõúùûç\s]', ' ', text)
    
    # Remover stopwords básicas
    stopwords_list = ['o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'sobre', 'entre', 'até', 'após', 'durante', 'e', 'ou', 'mas', 'se', 'que', 'quando', 'onde', 'como', 'porque', 'então', 'também', 'muito', 'mais', 'menos', 'bem', 'mal', 'sempre', 'nunca', 'já', 'ainda', 'só', 'apenas', 'até', 'depois', 'antes', 'agora', 'hoje', 'ontem', 'amanhã']
    words = text.split()
    words = [word for word in words if word not in stopwords_list and len(word) > 2]
    
    return ' '.join(words)

def main():
    print("🚀 Retreinando modelo com 50 filmes...")
    
    # Carregar dados dos 50 filmes
    with open('imdb_50plus_movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)
    
    print(f"📊 Carregados {len(movies)} filmes")
    
    # Converter para DataFrame
    df = pd.DataFrame(movies)
    
    # Limpar sinopses
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # TF-IDF Vectorization
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=1000,
        min_df=2,
        max_df=0.95,
        stop_words=None
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    
    # KMeans com TF-IDF
    print("🤖 Treinando KMeans TF-IDF...")
    kmeans_tfidf = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters_tfidf = kmeans_tfidf.fit_predict(tfidf_matrix)
    df['cluster_tfidf'] = clusters_tfidf
    
    # Preparar features numéricas
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
    kmeans_all = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters_all = kmeans_all.fit_predict(features_all)
    df['cluster_all'] = clusters_all
    
    # Avaliar clusters
    print("📈 Avaliando clusters...")
    
    # TF-IDF clusters
    silhouette_tfidf = silhouette_score(tfidf_matrix, clusters_tfidf)
    calinski_tfidf = calinski_harabasz_score(tfidf_matrix.toarray(), clusters_tfidf)
    davies_tfidf = davies_bouldin_score(tfidf_matrix.toarray(), clusters_tfidf)
    
    # All features clusters
    silhouette_all = silhouette_score(features_all, clusters_all)
    calinski_all = calinski_harabasz_score(features_all, clusters_all)
    davies_all = davies_bouldin_score(features_all, clusters_all)
    
    print(f"📊 Métricas TF-IDF:")
    print(f"   Silhouette: {silhouette_tfidf:.3f}")
    print(f"   Calinski-Harabasz: {calinski_tfidf:.3f}")
    print(f"   Davies-Bouldin: {davies_tfidf:.3f}")
    
    print(f"📊 Métricas All Features:")
    print(f"   Silhouette: {silhouette_all:.3f}")
    print(f"   Calinski-Harabasz: {calinski_all:.3f}")
    print(f"   Davies-Bouldin: {davies_all:.3f}")
    
    # Salvar modelos
    print("💾 Salvando modelos...")
    joblib.dump(kmeans_tfidf, 'models/kmeans_tfidf.pkl')
    joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(kmeans_all, 'models/kmeans_all_features.pkl')
    joblib.dump(le_genre, 'models/label_encoder_genre.pkl')
    
    # Salvar dataset com clusters
    df.to_csv('imdb_50plus_with_clusters.csv', index=False, sep=';')
    
    # Estatísticas dos clusters
    print("\n📊 Distribuição dos clusters:")
    print("TF-IDF Clusters:")
    for i in range(5):
        count = (df['cluster_tfidf'] == i).sum()
        print(f"   Cluster {i}: {count} filmes")
    
    print("All Features Clusters:")
    for i in range(5):
        count = (df['cluster_all'] == i).sum()
        print(f"   Cluster {i}: {count} filmes")
    
    print(f"\n✅ Modelo retreinado com {len(movies)} filmes!")
    print("📁 Arquivos salvos:")
    print("   - models/kmeans_tfidf.pkl")
    print("   - models/tfidf_vectorizer.pkl") 
    print("   - models/kmeans_all_features.pkl")
    print("   - models/label_encoder_genre.pkl")
    print("   - imdb_50plus_with_clusters.csv")

if __name__ == "__main__":
    main()
