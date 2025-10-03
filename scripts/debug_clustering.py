#!/usr/bin/env python3
"""
🐛 Script para debugar o problema de clustering
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
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

def debug_clustering():
    """Debugar sistema de clustering"""
    print("🐛 Debugando sistema de clustering...")
    
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
    
    print(f"\n📊 Distribuição dos clusters:")
    cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Verificar se o modelo existe
    models_dir = 'models'
    if not os.path.exists(models_dir):
        print("❌ Diretório de modelos não encontrado!")
        return
    
    # Carregar modelo
    try:
        kmeans = joblib.load(os.path.join(models_dir, 'kmeans_tfidf.pkl'))
        vectorizer = joblib.load(os.path.join(models_dir, 'tfidf_vectorizer.pkl'))
        print("✅ Modelos carregados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar modelos: {e}")
        return
    
    # Testar diferentes sinopses
    test_synopses = [
        "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
        "Um detetive investiga uma série de assassinatos brutais em uma cidade pequena, descobrindo segredos sombrios",
        "Um vigilante mascarado protege sua cidade de criminosos perigosos, enfrentando dilemas morais",
        "Dois jovens de classes sociais diferentes se apaixonam, mas precisam superar preconceitos",
        "Um grupo de astronautas embarca em uma missão espacial para salvar a humanidade"
    ]
    
    print(f"\n🧪 Testando predições:")
    for i, synopsis in enumerate(test_synopses, 1):
        # Limpar texto
        clean_synopsis = clean_text(synopsis)
        
        # Vectorizar
        synopsis_vector = vectorizer.transform([clean_synopsis])
        
        # Predizer cluster
        predicted_cluster = kmeans.predict(synopsis_vector)[0]
        
        # Calcular distâncias para todos os clusters
        distances = kmeans.transform(synopsis_vector)[0]
        
        print(f"\n  {i}. Sinopse: {synopsis[:50]}...")
        print(f"     Cluster predito: {predicted_cluster}")
        print(f"     Distâncias: {[f'{d:.3f}' for d in distances]}")
        
        # Verificar se há diversidade nas distâncias
        min_dist = min(distances)
        max_dist = max(distances)
        diversity = max_dist - min_dist
        
        if diversity < 0.1:
            print(f"     ⚠️ Baixa diversidade: {diversity:.3f}")
        else:
            print(f"     ✅ Diversidade OK: {diversity:.3f}")
    
    # Verificar centroides dos clusters
    print(f"\n📊 Centroides dos clusters:")
    centroids = kmeans.cluster_centers_
    for i, centroid in enumerate(centroids):
        # Encontrar palavras mais importantes para este cluster
        feature_names = vectorizer.get_feature_names_out()
        top_indices = centroid.argsort()[-10:][::-1]  # Top 10
        top_words = [feature_names[idx] for idx in top_indices]
        print(f"  Cluster {i}: {', '.join(top_words)}")
    
    # Verificar se o modelo está funcionando
    print(f"\n🔍 Verificando funcionamento do modelo:")
    print(f"  Número de clusters: {kmeans.n_clusters}")
    print(f"  Número de features: {len(vectorizer.get_feature_names_out())}")
    print(f"  Inertia: {kmeans.inertia_:.2f}")

if __name__ == '__main__':
    debug_clustering()
