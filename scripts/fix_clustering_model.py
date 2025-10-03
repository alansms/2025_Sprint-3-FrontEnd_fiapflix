#!/usr/bin/env python3
"""
🔧 Script para corrigir o modelo de clustering
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os
import re
import nltk

# Ensure NLTK stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords', quiet=True)

def clean_text(text):
    """Limpar e pré-processar texto"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-záàâãéèêíìîóòôõúùûç\s]', ' ', text)
    
    # Stopwords básicas
    stopwords_list = ['o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'sobre', 'entre', 'até', 'após', 'durante', 'e', 'ou', 'mas', 'se', 'que', 'quando', 'onde', 'como', 'porque', 'então', 'também', 'muito', 'mais', 'menos', 'bem', 'mal', 'sempre', 'nunca', 'já', 'ainda', 'só', 'apenas', 'até', 'depois', 'antes', 'agora', 'hoje', 'ontem', 'amanhã']
    words = text.split()
    words = [word for word in words if word not in stopwords_list and len(word) > 2]
    
    return ' '.join(words)

def fix_clustering():
    """Corrigir modelo de clustering"""
    print("🔧 Corrigindo modelo de clustering...")
    
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
    
    # Limpar sinopses
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # TF-IDF Vectorization com parâmetros otimizados
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=500,  # Reduzir features
        min_df=2,          # Palavras que aparecem em pelo menos 2 documentos
        max_df=0.8,        # Palavras que aparecem em no máximo 80% dos documentos
        ngram_range=(1, 2) # Unigramas e bigramas
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    print(f"📊 Matriz TF-IDF: {tfidf_matrix.shape}")
    
    # KMeans com parâmetros otimizados
    print("🤖 Treinando KMeans...")
    kmeans_tfidf = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=20,  # Mais inicializações
        max_iter=300,  # Mais iterações
        init='k-means++'  # Inicialização inteligente
    )
    
    df['cluster_tfidf'] = kmeans_tfidf.fit_predict(tfidf_matrix)
    
    # Verificar distribuição
    print(f"\n📊 Nova distribuição dos clusters:")
    cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Preparar features para KMeans com todas as features
    df['year_norm'] = (df['year'] - df['year'].min()) / (df['year'].max() - df['year'].min())
    df['rating_norm'] = (df['rating'] - df['rating'].min()) / (df['rating'].max() - df['rating'].min())
    
    le_genre = LabelEncoder()
    df['genre_encoded'] = le_genre.fit_transform(df['genre'])
    
    features_all = df[['year_norm', 'rating_norm', 'genre_encoded']]
    
    # Adicionar features TF-IDF
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    features_all = pd.concat([features_all, tfidf_df], axis=1)
    
    # StandardScaler
    scaler = StandardScaler()
    scaled_features_all = scaler.fit_transform(features_all)
    
    # KMeans com todas as features
    print("🤖 Treinando KMeans com todas as features...")
    kmeans_all_features = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=20,
        max_iter=300,
        init='k-means++'
    )
    
    df['cluster_all'] = kmeans_all_features.fit_predict(scaled_features_all)
    
    # Verificar distribuição
    print(f"\n📊 Distribuição cluster_all:")
    cluster_counts_all = df['cluster_all'].value_counts().sort_index()
    for cluster_id, count in cluster_counts_all.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Salvar modelos
    os.makedirs('models', exist_ok=True)
    joblib.dump(kmeans_tfidf, 'models/kmeans_tfidf.pkl')
    joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(kmeans_all_features, 'models/kmeans_all_features.pkl')
    joblib.dump(scaler, 'models/standard_scaler.pkl')
    joblib.dump(le_genre, 'models/label_encoder_genre.pkl')
    
    # Salvar dataset atualizado
    df.to_csv('imdb_100plus_with_clusters_fixed.csv', index=False, sep=';')
    
    print(f"\n✅ Modelos salvos!")
    print(f"📁 Arquivos:")
    print(f"  - models/kmeans_tfidf.pkl")
    print(f"  - models/tfidf_vectorizer.pkl")
    print(f"  - models/kmeans_all_features.pkl")
    print(f"  - models/standard_scaler.pkl")
    print(f"  - models/label_encoder_genre.pkl")
    print(f"  - imdb_100plus_with_clusters_fixed.csv")
    
    # Testar predições
    print(f"\n🧪 Testando predições:")
    test_synopses = [
        "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
        "Um detetive investiga uma série de assassinatos brutais em uma cidade pequena, descobrindo segredos sombrios",
        "Um vigilante mascarado protege sua cidade de criminosos perigosos, enfrentando dilemas morais",
        "Dois jovens de classes sociais diferentes se apaixonam, mas precisam superar preconceitos",
        "Um grupo de astronautas embarca em uma missão espacial para salvar a humanidade"
    ]
    
    for i, synopsis in enumerate(test_synopses, 1):
        clean_synopsis = clean_text(synopsis)
        synopsis_vector = tfidf_vectorizer.transform([clean_synopsis])
        predicted_cluster = kmeans_tfidf.predict(synopsis_vector)[0]
        
        print(f"  {i}. {synopsis[:50]}... -> Cluster {predicted_cluster}")

if __name__ == '__main__':
    fix_clustering()
