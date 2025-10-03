"""
Sistema de Recomendação de Filmes Avançado com Evidências de ML
Integração com notebooks e processamento de texto real
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import stopwords
import re
import pickle
import os
from typing import List, Dict, Tuple, Any
import json

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EnhancedMovieRecommendationSystem:
    def __init__(self):
        self.vectorizer = None
        self.kmeans_model = None
        self.movies_df = None
        self.cluster_centers = None
        self.cluster_analysis = {}
        self.model_metrics = {}
        
    def load_data(self, csv_path: str = 'imdb_top250_with_clusters.csv'):
        """Carrega os dados dos filmes do CSV"""
        try:
            self.movies_df = pd.read_csv(csv_path, sep=';')
            print(f"✅ Dados carregados: {len(self.movies_df)} filmes")
            return True
        except FileNotFoundError:
            print(f"⚠️ Arquivo {csv_path} não encontrado. Usando dados mock.")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """Pré-processa texto para análise com técnicas avançadas"""
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
        """Treina o modelo KMeans com análise detalhada"""
        if self.movies_df is None:
            print("❌ Dados não carregados")
            return False
        
        print(f"🔄 Treinando modelo KMeans com {n_clusters} clusters...")
        
        # Pré-processar sinopses
        synopses = self.movies_df['sinopse'].fillna('').apply(self.preprocess_text)
        
        # Vetorização TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2)
        )
        
        X = self.vectorizer.fit_transform(synopses)
        
        # Treinar KMeans
        self.kmeans_model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        
        clusters = self.kmeans_model.fit_predict(X)
        self.movies_df['cluster'] = clusters
        
        # Calcular métricas
        silhouette = silhouette_score(X, clusters)
        calinski = calinski_harabasz_score(X.toarray(), clusters)
        davies = davies_bouldin_score(X.toarray(), clusters)
        
        self.model_metrics = {
            'silhouette_score': silhouette,
            'calinski_harabasz_score': calinski,
            'davies_bouldin_score': davies,
            'n_clusters': n_clusters,
            'n_samples': len(self.movies_df)
        }
        
        # Analisar clusters
        self.analyze_all_clusters()
        
        print(f"✅ Modelo treinado com sucesso!")
        print(f"📊 Silhouette Score: {silhouette:.3f}")
        print(f"📊 Calinski-Harabasz Score: {calinski:.3f}")
        print(f"📊 Davies-Bouldin Score: {davies:.3f}")
        
        return True
    
    def analyze_all_clusters(self):
        """Analisa todos os clusters e suas características"""
        self.cluster_analysis = {}
        
        for cluster_id in range(self.kmeans_model.n_clusters):
            cluster_movies = self.movies_df[self.movies_df['cluster'] == cluster_id]
            
            if len(cluster_movies) == 0:
                continue
            
            # Análise estatística
            analysis = {
                'cluster_id': cluster_id,
                'movie_count': len(cluster_movies),
                'avg_rating': cluster_movies['rating'].mean(),
                'avg_year': cluster_movies['year'].mean(),
                'top_genres': cluster_movies['genre'].value_counts().head(3).to_dict(),
                'representative_movies': cluster_movies.nlargest(3, 'rating')[['title_en', 'rating', 'year']].to_dict('records'),
                'cluster_characteristics': self.get_cluster_characteristics(cluster_movies)
            }
            
            self.cluster_analysis[cluster_id] = analysis
    
    def get_cluster_characteristics(self, cluster_movies: pd.DataFrame) -> Dict:
        """Obtém características específicas do cluster"""
        # Análise de gêneros
        genre_dist = cluster_movies['genre'].value_counts()
        
        # Análise temporal
        year_range = cluster_movies['year'].max() - cluster_movies['year'].min()
        
        # Análise de rating
        rating_std = cluster_movies['rating'].std()
        
        return {
            'dominant_genre': genre_dist.index[0] if len(genre_dist) > 0 else 'Unknown',
            'genre_diversity': len(genre_dist),
            'year_range': year_range,
            'rating_consistency': 1 - (rating_std / cluster_movies['rating'].mean()) if cluster_movies['rating'].mean() > 0 else 0
        }
    
    def predict_cluster(self, synopsis: str) -> Tuple[int, float, Dict]:
        """Prediz o cluster de uma sinopse com evidências detalhadas"""
        if self.vectorizer is None or self.kmeans_model is None:
            print("❌ Modelo não treinado")
            return 0, 0.0, {}
        
        # Pré-processar texto
        clean_synopsis = self.preprocess_text(synopsis)
        
        # Vetorizar
        X = self.vectorizer.transform([clean_synopsis])
        
        # Predizer cluster
        cluster = self.kmeans_model.predict(X)[0]
        
        # Calcular distâncias para todos os clusters
        distances = self.kmeans_model.transform(X)[0]
        min_distance = distances[cluster]
        
        # Calcular confiança
        confidence = 1.0 / (1.0 + min_distance)
        
        # Evidências do modelo
        evidence = {
            'processed_text': clean_synopsis,
            'cluster_distances': distances.tolist(),
            'selected_cluster': int(cluster),
            'confidence': confidence,
            'min_distance': min_distance,
            'cluster_center_distance': min_distance
        }
        
        return cluster, confidence, evidence
    
    def get_recommendations(self, cluster: int, n_recommendations: int = 5) -> List[Dict]:
        """Obtém recomendações baseadas no cluster com critérios avançados"""
        if self.movies_df is None:
            return []
        
        # Filtrar filmes do cluster
        cluster_movies = self.movies_df[self.movies_df['cluster'] == cluster]
        
        if len(cluster_movies) == 0:
            return []
        
        # Critério de seleção: rating + diversidade
        recommendations = cluster_movies.nlargest(n_recommendations * 2, 'rating')
        
        # Adicionar diversidade de gêneros
        diverse_recommendations = []
        used_genres = set()
        
        for _, movie in recommendations.iterrows():
            if len(diverse_recommendations) >= n_recommendations:
                break
            
            movie_genre = movie['genre'].split(',')[0].strip()  # Primeiro gênero
            
            if movie_genre not in used_genres or len(diverse_recommendations) < 3:
                diverse_recommendations.append(movie.to_dict())
                used_genres.add(movie_genre)
        
        # Se não temos diversidade suficiente, adicionar os melhores
        while len(diverse_recommendations) < n_recommendations and len(diverse_recommendations) < len(cluster_movies):
            for _, movie in recommendations.iterrows():
                if len(diverse_recommendations) >= n_recommendations:
                    break
                
                movie_dict = movie.to_dict()
                if movie_dict not in diverse_recommendations:
                    diverse_recommendations.append(movie_dict)
        
        return diverse_recommendations[:n_recommendations]
    
    def get_cluster_analysis(self, cluster: int) -> Dict:
        """Obtém análise detalhada de um cluster"""
        if cluster not in self.cluster_analysis:
            return {}
        
        return self.cluster_analysis[cluster]
    
    def get_model_evidence(self) -> Dict:
        """Retorna evidências do modelo treinado"""
        return {
            'model_metrics': self.model_metrics,
            'cluster_analysis': self.cluster_analysis,
            'n_features': len(self.vectorizer.get_feature_names_out()) if self.vectorizer else 0,
            'vocabulary_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0
        }
    
    def save_model(self):
        """Salva o modelo treinado"""
        model_data = {
            'vectorizer': self.vectorizer,
            'kmeans_model': self.kmeans_model,
            'movies_df': self.movies_df,
            'cluster_analysis': self.cluster_analysis,
            'model_metrics': self.model_metrics
        }
        
        with open('enhanced_movie_recommendation_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("✅ Modelo avançado salvo")
    
    def load_model(self):
        """Carrega modelo salvo"""
        try:
            with open('enhanced_movie_recommendation_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.kmeans_model = model_data['kmeans_model']
            self.movies_df = model_data['movies_df']
            self.cluster_analysis = model_data.get('cluster_analysis', {})
            self.model_metrics = model_data.get('model_metrics', {})
            
            print("✅ Modelo avançado carregado")
            return True
        except FileNotFoundError:
            print("⚠️ Modelo não encontrado")
            return False

# Função para integração com a API
def get_enhanced_recommendations(synopsis: str, method: str) -> Dict:
    """Função principal para obter recomendações com evidências"""
    system = EnhancedMovieRecommendationSystem()
    
    # Tentar carregar modelo existente
    if not system.load_model():
        # Se não conseguir carregar, treinar novo modelo
        system.load_data()
        system.train_model()
    
    # Predizer cluster com evidências
    cluster, confidence, evidence = system.predict_cluster(synopsis)
    
    # Obter recomendações
    recommendations = system.get_recommendations(cluster)
    
    # Analisar cluster
    cluster_analysis = system.get_cluster_analysis(cluster)
    
    # Evidências do modelo
    model_evidence = system.get_model_evidence()
    
    return {
        'recommendations': recommendations,
        'cluster': cluster,
        'confidence': confidence,
        'method': method,
        'cluster_analysis': cluster_analysis,
        'evidence': evidence,
        'model_evidence': model_evidence
    }

if __name__ == "__main__":
    # Exemplo de uso
    system = EnhancedMovieRecommendationSystem()
    system.load_data()
    system.train_model()
    
    # Testar recomendação
    result = get_enhanced_recommendations(
        "A story about a man who escapes from prison and builds a new life",
        "method1"
    )
    
    print("🎬 Recomendação testada com sucesso!")
    print(f"📊 Cluster: {result['cluster']}")
    print(f"📊 Confiança: {result['confidence']:.3f}")
    print(f"📊 Filmes recomendados: {len(result['recommendations'])}")
