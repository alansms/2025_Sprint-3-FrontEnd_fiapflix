#!/usr/bin/env python3
"""
🎭 Script para criar sinopses mais diversas e testar clustering
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import joblib
import os
import re

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

def create_diverse_synopses():
    """Criar sinopses mais diversas"""
    print("🎭 Criando sinopses diversas...")
    
    # Sinopses com temas muito diferentes
    diverse_synopses = [
        # Ação/Super-herói
        "Um vigilante mascarado protege sua cidade de criminosos perigosos, enfrentando dilemas morais sobre justiça e vingança",
        
        # Romance/Drama
        "Dois jovens de classes sociais diferentes se apaixonam, mas precisam superar preconceitos e obstáculos familiares para ficarem juntos",
        
        # Ficção Científica
        "Um grupo de astronautas embarca em uma missão espacial para salvar a humanidade, descobrindo segredos sobre o universo e a existência",
        
        # Terror/Suspense
        "Uma família se muda para uma casa assombrada e descobre que os espíritos dos antigos moradores ainda habitam o local, causando eventos sobrenaturais",
        
        # Comédia
        "Um grupo de amigos embarca em uma viagem maluca que resulta em uma série de situações hilárias e mal-entendidos cômicos",
        
        # Drama Histórico
        "Durante a Segunda Guerra Mundial, um soldado deve escolher entre seguir ordens ou salvar civis inocentes, enfrentando dilemas éticos profundos",
        
        # Mistério/Detetive
        "Um detetive investiga uma série de assassinatos brutais em uma cidade pequena, descobrindo segredos sombrios que envolvem a elite local",
        
        # Fantasia
        "Um jovem descobre que é o herdeiro de um reino mágico e deve aprender a usar seus poderes para salvar seu mundo de uma ameaça sombria",
        
        # Western
        "Um pistoleiro solitário chega a uma cidade do Velho Oeste e deve escolher entre a lei e a justiça quando confrontado com um bandido notório",
        
        # Musical
        "Uma jovem cantora sonha em se tornar famosa, mas deve superar obstáculos e preconceitos para alcançar seu sonho na Broadway"
    ]
    
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
    
    # Limpar sinopses existentes
    df['sinopse_clean'] = df['sinopse'].apply(clean_text)
    
    # TF-IDF Vectorization
    print("🔤 Aplicando TF-IDF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_features=300,
        min_df=1,
        max_df=0.9,
        ngram_range=(1, 2)
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['sinopse_clean'])
    print(f"📊 Matriz TF-IDF: {tfidf_matrix.shape}")
    
    # KMeans com parâmetros otimizados
    print("🤖 Treinando KMeans...")
    kmeans_tfidf = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=50,  # Muitas inicializações
        max_iter=500,  # Muitas iterações
        init='k-means++',
        algorithm='lloyd'  # Algoritmo mais estável
    )
    
    df['cluster_tfidf'] = kmeans_tfidf.fit_predict(tfidf_matrix)
    
    # Verificar distribuição
    print(f"\n📊 Distribuição dos clusters:")
    cluster_counts = df['cluster_tfidf'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} filmes")
    
    # Salvar modelos
    os.makedirs('models', exist_ok=True)
    joblib.dump(kmeans_tfidf, 'models/kmeans_tfidf.pkl')
    joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    
    # Salvar dataset atualizado
    df.to_csv('imdb_100plus_with_clusters_diverse.csv', index=False, sep=';')
    
    print(f"\n✅ Modelos salvos!")
    
    # Testar predições com sinopses diversas
    print(f"\n🧪 Testando predições com sinopses diversas:")
    for i, synopsis in enumerate(diverse_synopses, 1):
        clean_synopsis = clean_text(synopsis)
        synopsis_vector = tfidf_vectorizer.transform([clean_synopsis])
        predicted_cluster = kmeans_tfidf.predict(synopsis_vector)[0]
        
        # Calcular distâncias
        distances = kmeans_tfidf.transform(synopsis_vector)[0]
        min_dist = min(distances)
        max_dist = max(distances)
        diversity = max_dist - min_dist
        
        print(f"  {i}. {synopsis[:60]}...")
        print(f"     Cluster: {predicted_cluster}, Diversidade: {diversity:.3f}")
        print(f"     Distâncias: {[f'{d:.3f}' for d in distances]}")
    
    # Verificar se há diversidade nas predições
    print(f"\n📊 Análise de diversidade:")
    clusters_predicted = []
    for synopsis in diverse_synopses:
        clean_synopsis = clean_text(synopsis)
        synopsis_vector = tfidf_vectorizer.transform([clean_synopsis])
        predicted_cluster = kmeans_tfidf.predict(synopsis_vector)[0]
        clusters_predicted.append(predicted_cluster)
    
    unique_clusters = set(clusters_predicted)
    print(f"  Clusters únicos preditos: {len(unique_clusters)}")
    print(f"  Clusters: {sorted(unique_clusters)}")
    
    if len(unique_clusters) == 1:
        print("⚠️ ATENÇÃO: Todas as sinopses ainda estão sendo classificadas no mesmo cluster!")
        print("🔍 Possíveis causas:")
        print("  - Dataset com sinopses muito similares")
        print("  - Modelo de clustering inadequado")
        print("  - Features insuficientes para diferenciação")
    else:
        print("✅ Diversidade de clusters detectada!")

if __name__ == '__main__':
    create_diverse_synopses()
