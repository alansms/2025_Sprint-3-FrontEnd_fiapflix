#!/usr/bin/env python3
"""
Script para executar recomendações usando modelos treinados
"""

import sys
import json
import os
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

try:
    from ml_model_trained import get_recommendations_for_synopsis, get_cluster_analysis
except ImportError:
    print(json.dumps({"error": "Não foi possível importar o sistema de recomendação"}))
    sys.exit(1)

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 run_recommendation.py <json_data>")
        sys.exit(1)
    
    try:
        # Parse dos dados de entrada
        input_data = json.loads(sys.argv[1])
        
        synopsis = input_data.get('synopsis', '')
        method = input_data.get('method', 'tfidf')
        year = input_data.get('year', 2000)
        rating = input_data.get('rating', 8.0)
        genre = input_data.get('genre', 'Drama')
        
        if not synopsis:
            print(json.dumps({
                'error': 'Sinopse é obrigatória'
            }))
            sys.exit(1)
        
        # Obter recomendações
        result = get_recommendations_for_synopsis(
            synopsis=synopsis,
            method=method,
            year=year,
            rating=rating,
            genre=genre
        )
        
        # Obter análise do cluster se disponível
        if result.get('cluster') is not None:
            cluster_analysis = get_cluster_analysis(result['cluster'], method)
            result['cluster_analysis'] = cluster_analysis
        
        # Retornar resultado em JSON
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            'error': f'Erro ao fazer parse do JSON: {str(e)}'
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'error': f'Erro interno: {str(e)}'
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()

