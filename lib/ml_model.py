"""
Sistema de Recomendação de Filmes baseado em Clusterização
Integração com os notebooks desenvolvidos nas aulas 01-04
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import nltk
from nltk.corpus import stopwords
import re
import pickle
import os
from typing import List, Dict, Tuple

class MovieRecommendationSystem:
    def __init__(self):
        self.vectorizer = None
        self.kmeans_model = None
        self.movies_df = None
        self.clusters_info = {}
        
    def load_data(self, csv_path: str = 'imdb_top250_with_clusters.csv'):
        """Carrega os dados dos filmes do CSV"""
        try:
            self.movies_df = pd.read_csv(csv_path, sep=';')
            print(f"Dados carregados: {len(self.movies_df)} filmes")
            return True
        except FileNotFoundError:
            print(f"Arquivo {csv_path} não encontrado. Usando dados mock.")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """Pré-processa texto para análise"""
        if pd.isna(text) or text == 'N/A':
            return ""
        
        # Converter para minúsculas
        text = str(text).lower()
        
        # Remover caracteres especiais e números
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remover stopwords
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words = text.split()
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return ' '.join(words)
    
    def train_model(self, n_clusters: int = 5):
        """Treina o modelo de clusterização"""
        if self.movies_df is None:
            print("Dados não carregados. Use load_data() primeiro.")
            return False
        
        # Preparar dados
        df_clean = self.movies_df.copy()
        df_clean['sinopse_clean'] = df_clean['sinopse'].apply(self.preprocess_text)
        df_clean = df_clean[df_clean['sinopse_clean'].str.len() > 10]
        
        # Aplicar TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2)
        )
        
        X_tfidf = self.vectorizer.fit_transform(df_clean['sinopse_clean'])
        
        # Treinar KMeans
        self.kmeans_model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        
        cluster_labels = self.kmeans_model.fit_predict(X_tfidf)
        df_clean['cluster'] = cluster_labels
        
        # Calcular métricas
        silhouette_avg = silhouette_score(X_tfidf, cluster_labels)
        print(f"Modelo treinado com {n_clusters} clusters")
        print(f"Silhouette Score: {silhouette_avg:.3f}")
        
        # Salvar modelo
        self.save_model()
        
        return True
    
    def predict_cluster(self, synopsis: str) -> Tuple[int, float]:
        """Prediz o cluster de uma sinopse"""
        if self.vectorizer is None or self.kmeans_model is None:
            print("Modelo não treinado. Use train_model() primeiro.")
            return 0, 0.0
        
        # Pré-processar texto
        clean_synopsis = self.preprocess_text(synopsis)
        
        # Vetorizar
        X = self.vectorizer.transform([clean_synopsis])
        
        # Predizer cluster
        cluster = self.kmeans_model.predict(X)[0]
        
        # Calcular confiança (distância ao centroide)
        distances = self.kmeans_model.transform(X)[0]
        confidence = 1.0 / (1.0 + distances[cluster])
        
        return cluster, confidence
    
    def get_recommendations(self, cluster: int, n_recommendations: int = 5) -> List[Dict]:
        """Obtém recomendações baseadas no cluster"""
        if self.movies_df is None:
            return []
        
        # Filtrar filmes do cluster
        cluster_movies = self.movies_df[self.movies_df['cluster'] == cluster]
        
        # Ordenar por rating e retornar top N
        recommendations = cluster_movies.nlargest(n_recommendations, 'rating')
        
        return recommendations.to_dict('records')
    
    def analyze_cluster(self, cluster: int) -> Dict:
        """Analisa características de um cluster"""
        if self.movies_df is None:
            return {}
        
        cluster_movies = self.movies_df[self.movies_df['cluster'] == cluster]
        
        if len(cluster_movies) == 0:
            return {}
        
        analysis = {
            'cluster_id': cluster,
            'movie_count': len(cluster_movies),
            'avg_rating': cluster_movies['rating'].mean(),
            'avg_year': cluster_movies['year'].mean(),
            'top_genres': cluster_movies['genre'].value_counts().head(3).to_dict(),
            'representative_movies': cluster_movies.nlargest(3, 'rating')[['title_en', 'rating', 'year']].to_dict('records')
        }
        
        return analysis
    
    def save_model(self):
        """Salva o modelo treinado"""
        model_data = {
            'vectorizer': self.vectorizer,
            'kmeans_model': self.kmeans_model,
            'movies_df': self.movies_df
        }
        
        with open('movie_recommendation_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("Modelo salvo em movie_recommendation_model.pkl")
    
    def load_model(self):
        """Carrega modelo salvo"""
        try:
            with open('movie_recommendation_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.kmeans_model = model_data['kmeans_model']
            self.movies_df = model_data['movies_df']
            
            print("Modelo carregado com sucesso")
            return True
        except FileNotFoundError:
            print("Modelo não encontrado. Treine um novo modelo primeiro.")
            return False

# Função para integração com a API
def get_recommendations_for_synopsis(synopsis: str, method: str) -> Dict:
    """Função principal para obter recomendações"""
    system = MovieRecommendationSystem()
    
    # Tentar carregar modelo existente
    if not system.load_model():
        # Se não conseguir carregar, treinar novo modelo
        system.load_data()
        system.train_model()
    
    # Predizer cluster
    cluster, confidence = system.predict_cluster(synopsis)
    
    # Obter recomendações
    recommendations = system.get_recommendations(cluster)
    
    # Analisar cluster
    cluster_analysis = system.analyze_cluster(cluster)
    
    return {
        'recommendations': recommendations,
        'cluster': cluster,
        'confidence': confidence,
        'method': method,
        'cluster_analysis': cluster_analysis
    }

if __name__ == "__main__":
    # Exemplo de uso
    system = MovieRecommendationSystem()
    
    # Carregar dados
    system.load_data()
    
    # Treinar modelo
    system.train_model()
    
    # Testar recomendação
    test_synopsis = "A story about a man who escapes from prison and builds a new life"
    cluster, confidence = system.predict_cluster(test_synopsis)
    recommendations = system.get_recommendations(cluster)
    
    print(f"Cluster predito: {cluster}")
    print(f"Confiança: {confidence:.3f}")
    print(f"Recomendações: {len(recommendations)} filmes")
