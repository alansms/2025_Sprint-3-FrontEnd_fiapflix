#!/usr/bin/env python3
"""
Sistema de Recomendação de Filmes usando Modelos Treinados
Baseado no Notebook2_Modelo_Comparacao_Features.ipynb
"""

import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import re

class MovieRecommendationSystem:
    """
    Sistema de recomendação de filmes usando modelos treinados
    """
    
    def __init__(self):
        """Inicializa o sistema carregando os modelos treinados"""
        self.models_loaded = False
        self.df_movies = None
        self.kmeans_tfidf = None
        self.vectorizer = None
        self.kmeans_all = None
        self.scaler = None
        self.le_genre = None
        
        # Carregar modelos
        self.load_models()
    
    def load_models(self):
        """Carrega os modelos treinados"""
        try:
            # Carregar modelos
            self.kmeans_tfidf = joblib.load('models/kmeans_tfidf.pkl')
            self.vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
            self.kmeans_all = joblib.load('models/kmeans_all_features.pkl')
            self.scaler = joblib.load('models/standard_scaler.pkl')
            self.le_genre = joblib.load('models/label_encoder_genre.pkl')
            
            # Carregar dataset
            try:
                self.df_movies = pd.read_csv('imdb_real_with_clusters.csv', sep=';')
            except:
                try:
                    self.df_movies = pd.read_csv('imdb_50plus_with_clusters.csv', sep=';')
                except:
                    self.df_movies = pd.read_csv('imdb_top250_with_clusters.csv', sep=';')
            
            self.models_loaded = True
            
        except Exception as e:
            self.models_loaded = False
    
    def preprocess_text(self, text):
        """
        Pré-processa texto para análise
        """
        if not text or pd.isna(text):
            return ""
        
        # Converter para minúsculas
        text = str(text).lower()
        
        # Remover caracteres especiais
        text = re.sub(r'[^a-zA-Záàâãéèêíìîóòôõúùûç\s]', '', text)
        
        # Remover espaços extras
        text = ' '.join(text.split())
        
        return text
    
    def predict_cluster_tfidf(self, synopsis):
        """
        Prediz cluster usando modelo TF-IDF (Modelo 1)
        """
        if not self.models_loaded:
            return None, 0.0
        
        try:
            # Pré-processar texto
            processed_text = self.preprocess_text(synopsis)
            
            # Vetorizar
            X = self.vectorizer.transform([processed_text])
            
            # Predizer cluster
            cluster = self.kmeans_tfidf.predict(X)[0]
            
            # Calcular confiança (distância ao centroide)
            distances = self.kmeans_tfidf.transform(X)[0]
            confidence = 1.0 / (1.0 + distances[cluster])
            
            return cluster, confidence
            
        except Exception as e:
            print(f"Erro na predição TF-IDF: {str(e)}")
            return None, 0.0
    
    def predict_cluster_all_features(self, synopsis, year=None, rating=None, genre=None):
        """
        Prediz cluster usando modelo com todas as features (Modelo 2)
        """
        if not self.models_loaded:
            return None, 0.0
        
        try:
            # Valores padrão
            if year is None:
                year = 2000
            if rating is None:
                rating = 8.0
            if genre is None:
                genre = 'Drama'
            
            # Contar palavras na sinopse
            word_count = len(synopsis.split()) if synopsis else 10
            
            # Preparar features numéricas
            numeric_features = np.array([[year, rating, word_count]])
            X_numeric = self.scaler.transform(numeric_features)
            
            # Preparar features categóricas
            try:
                genre_encoded = self.le_genre.transform([genre])[0]
            except:
                genre_encoded = 0  # Valor padrão
            
            X_genre = np.array([[genre_encoded]])
            
            # Combinar features
            X_all = np.hstack([X_numeric, X_genre])
            
            # Predizer cluster
            cluster = self.kmeans_all.predict(X_all)[0]
            
            # Calcular confiança
            distances = self.kmeans_all.transform(X_all)[0]
            confidence = 1.0 / (1.0 + distances[cluster])
            
            return cluster, confidence
            
        except Exception as e:
            print(f"Erro na predição com todas as features: {str(e)}")
            return None, 0.0
    
    def get_recommendations(self, synopsis, method='tfidf', year=None, rating=None, genre=None, n_recommendations=5):
        """
        Obtém recomendações baseadas na sinopse
        """
        if not self.models_loaded:
            return {
                'recommendations': [],
                'cluster': None,
                'confidence': 0.0,
                'method': method,
                'error': 'Modelos não carregados'
            }
        
        try:
            # Predizer cluster
            if method == 'tfidf':
                cluster, confidence = self.predict_cluster_tfidf(synopsis)
            else:
                cluster, confidence = self.predict_cluster_all_features(synopsis, year, rating, genre)
            
            if cluster is None:
                return {
                    'recommendations': [],
                    'cluster': None,
                    'confidence': 0.0,
                    'method': method,
                    'error': 'Erro na predição do cluster'
                }
            
            # Filtrar filmes do mesmo cluster
            cluster_movies = self.df_movies[self.df_movies[f'cluster_{method}'] == cluster]
            
            if len(cluster_movies) == 0:
                # Fallback: usar todos os filmes
                cluster_movies = self.df_movies
            
            # Ordenar por rating (melhores primeiro)
            cluster_movies = cluster_movies.sort_values('rating', ascending=False)
            
            # Selecionar top N
            recommendations = cluster_movies.head(n_recommendations)
            
            # Converter para formato da API
            api_recommendations = []
            for _, movie in recommendations.iterrows():
                api_movie = {
                    'id': str(movie.get('rank', 0)),
                    'rank': int(movie.get('rank', 0)),
                    'title_en': movie.get('title_en', 'N/A'),
                    'title_pt': movie.get('title_pt', movie.get('title_en', 'N/A')),
                    'year': int(movie.get('year', 2000)),
                    'rating': float(movie.get('rating', 8.0)),
                    'genre': movie.get('genre', 'Drama'),
                    'sinopse': movie.get('sinopse', 'Sinopse não disponível'),
                    'director': 'Diretor não informado',
                    'cast': 'Elenco não informado',
                    'duration': '120 min',
                    'cluster': int(cluster),
                    'poster_url': f'https://image.tmdb.org/t/p/w500/placeholder.jpg',
                    'backdrop_url': f'https://image.tmdb.org/t/p/w1280/placeholder.jpg'
                }
                api_recommendations.append(api_movie)
            
            return {
                'recommendations': api_recommendations,
                'cluster': int(cluster),
                'confidence': float(confidence),
                'method': method,
                'cluster_size': len(cluster_movies),
                'total_movies': len(self.df_movies)
            }
            
        except Exception as e:
            print(f"Erro ao obter recomendações: {str(e)}")
            return {
                'recommendations': [],
                'cluster': None,
                'confidence': 0.0,
                'method': method,
                'error': str(e)
            }
    
    def get_cluster_analysis(self, cluster_id, method='tfidf'):
        """
        Obtém análise de um cluster específico
        """
        if not self.models_loaded:
            return None
        
        try:
            cluster_movies = self.df_movies[self.df_movies[f'cluster_{method}'] == cluster_id]
            
            if len(cluster_movies) == 0:
                return None
            
            analysis = {
                'cluster_id': int(cluster_id),
                'movie_count': len(cluster_movies),
                'avg_rating': float(cluster_movies['rating'].mean()),
                'genres': cluster_movies['genre'].unique().tolist(),
                'years': {
                    'min': int(cluster_movies['year'].min()),
                    'max': int(cluster_movies['year'].max()),
                    'avg': float(cluster_movies['year'].mean())
                },
                'representative_movies': []
            }
            
            # Filmes representativos (top 3 por rating)
            top_movies = cluster_movies.nlargest(3, 'rating')
            for _, movie in top_movies.iterrows():
                analysis['representative_movies'].append({
                    'title': movie.get('title_en', 'N/A'),
                    'rating': float(movie.get('rating', 8.0)),
                    'year': int(movie.get('year', 2000))
                })
            
            return analysis
            
        except Exception as e:
            print(f"Erro na análise do cluster: {str(e)}")
            return None

# Instância global do sistema
movie_system = MovieRecommendationSystem()

def get_recommendations_for_synopsis(synopsis, method='tfidf', year=None, rating=None, genre=None):
    """
    Função principal para obter recomendações
    """
    return movie_system.get_recommendations(synopsis, method, year, rating, genre)

def get_cluster_analysis(cluster_id, method='tfidf'):
    """
    Função para obter análise de cluster
    """
    return movie_system.get_cluster_analysis(cluster_id, method)

