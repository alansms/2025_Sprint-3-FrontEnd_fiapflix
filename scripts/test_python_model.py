#!/usr/bin/env python3
"""
🧪 Script para testar o modelo Python diretamente
"""

import sys
import json
import os
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from lib.ml_model_trained import get_recommendations_for_synopsis, get_cluster_analysis
    print("✅ Modelo importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar modelo: {e}")
    sys.exit(1)

def test_recommendations():
    """Testar recomendações"""
    print("🧪 Testando recomendações...")
    
    synopsis = "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido"
    method = "tfidf"
    
    try:
        result = get_recommendations_for_synopsis(
            synopsis=synopsis,
            method=method,
            year=2000,
            rating=8.0,
            genre="Drama"
        )
        
        print(f"✅ Resultado obtido:")
        print(f"  - Recomendações: {len(result.get('recommendations', []))}")
        print(f"  - Cluster: {result.get('cluster')}")
        print(f"  - Confiança: {result.get('confidence')}")
        print(f"  - Método: {result.get('method')}")
        
        if result.get('recommendations'):
            print(f"\n🎬 Filmes recomendados:")
            for i, movie in enumerate(result['recommendations'][:5], 1):
                print(f"  {i}. {movie.get('title_pt', 'N/A')} ({movie.get('year', 'N/A')}) - {movie.get('rating', 'N/A')}")
        
        if result.get('error'):
            print(f"❌ Erro: {result['error']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erro ao obter recomendações: {e}")
        return None

if __name__ == '__main__':
    test_recommendations()
