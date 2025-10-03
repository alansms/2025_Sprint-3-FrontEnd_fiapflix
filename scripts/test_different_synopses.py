#!/usr/bin/env python3
"""
🧪 Script para testar diferentes sinopses e verificar se retornam filmes diferentes
"""

import sys
import json
import os
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from lib.ml_model_trained import get_recommendations_for_synopsis
    print("✅ Modelo importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar modelo: {e}")
    sys.exit(1)

def test_different_synopses():
    """Testar diferentes sinopses"""
    print("🧪 Testando diferentes sinopses...")
    
    test_synopses = [
        {
            "name": "Drama/Prisão",
            "synopsis": "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido"
        },
        {
            "name": "Crime/Detetive", 
            "synopsis": "Um detetive investiga uma série de assassinatos brutais em uma cidade pequena, descobrindo segredos sombrios que envolvem a elite local"
        },
        {
            "name": "Ação/Super-herói",
            "synopsis": "Um vigilante mascarado protege sua cidade de criminosos perigosos, enfrentando dilemas morais sobre justiça e vingança"
        },
        {
            "name": "Romance/Drama",
            "synopsis": "Dois jovens de classes sociais diferentes se apaixonam, mas precisam superar preconceitos e obstáculos familiares para ficarem juntos"
        },
        {
            "name": "Ficção Científica",
            "synopsis": "Um grupo de astronautas embarca em uma missão espacial para salvar a humanidade, descobrindo segredos sobre o universo"
        }
    ]
    
    results = {}
    
    for test in test_synopses:
        print(f"\n🎬 Testando: {test['name']}")
        print(f"📝 Sinopse: {test['synopsis'][:50]}...")
        
        try:
            result = get_recommendations_for_synopsis(
                synopsis=test['synopsis'],
                method="tfidf",
                year=2000,
                rating=8.0,
                genre="Drama"
            )
            
            if result.get('recommendations'):
                movies = result['recommendations'][:3]  # Primeiros 3 filmes
                movie_titles = [m.get('title_pt', 'N/A') for m in movies]
                
                results[test['name']] = {
                    'cluster': result.get('cluster'),
                    'confidence': result.get('confidence'),
                    'movies': movie_titles
                }
                
                print(f"  🎯 Cluster: {result.get('cluster')}")
                print(f"  📊 Confiança: {result.get('confidence', 0):.3f}")
                print(f"  🎬 Filmes: {', '.join(movie_titles)}")
            else:
                print(f"  ❌ Nenhuma recomendação")
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    # Verificar se há diversidade
    print(f"\n📊 Análise de Diversidade:")
    all_movies = set()
    for name, data in results.items():
        all_movies.update(data['movies'])
        print(f"  {name}: {len(set(data['movies']))} filmes únicos")
    
    print(f"\n🎯 Total de filmes únicos: {len(all_movies)}")
    print(f"🎯 Filmes recomendados: {sorted(all_movies)}")
    
    # Verificar clusters
    clusters = [data['cluster'] for data in results.values()]
    unique_clusters = set(clusters)
    print(f"\n📊 Clusters únicos: {len(unique_clusters)}")
    print(f"📊 Clusters: {sorted(unique_clusters)}")
    
    if len(unique_clusters) == 1:
        print("⚠️ ATENÇÃO: Todas as sinopses estão sendo classificadas no mesmo cluster!")
    else:
        print("✅ Diversidade de clusters detectada")

if __name__ == '__main__':
    test_different_synopses()
