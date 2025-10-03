#!/usr/bin/env python3
"""
🔧 Script para corrigir filmes duplicados no dataset
"""

import json
import os
from collections import defaultdict

def fix_duplicate_movies():
    """Corrigir filmes duplicados e garantir IDs únicos"""
    print("🔧 Corrigindo filmes duplicados...")
    
    # Arquivos para verificar
    files_to_check = [
        'imdb_100plus_movies.json',
        'imdb_50plus_movies.json', 
        'imdb_expanded_real.json',
        'imdb_final_real.json',
        'imdb_top250_real.json'
    ]
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            continue
            
        print(f"\n📁 Processando {filename}...")
        
        # Carregar dados
        with open(filename, 'r', encoding='utf-8') as f:
            movies = json.load(f)
        
        print(f"📊 Filmes originais: {len(movies)}")
        
        # Identificar duplicatas por ID
        id_counts = defaultdict(int)
        for movie in movies:
            id_counts[movie['id']] += 1
        
        duplicates = {id: count for id, count in id_counts.items() if count > 1}
        print(f"🔍 IDs duplicados encontrados: {len(duplicates)}")
        
        if duplicates:
            # Remover duplicatas mantendo apenas a primeira ocorrência
            seen_ids = set()
            unique_movies = []
            
            for movie in movies:
                movie_id = movie['id']
                if movie_id not in seen_ids:
                    seen_ids.add(movie_id)
                    unique_movies.append(movie)
                else:
                    print(f"  ❌ Removendo duplicata: {movie['title_pt']} (ID: {movie_id})")
            
            print(f"✅ Filmes únicos após remoção: {len(unique_movies)}")
            
            # Salvar arquivo corrigido
            backup_filename = f"{filename}.backup"
            os.rename(filename, backup_filename)
            print(f"💾 Backup criado: {backup_filename}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(unique_movies, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Arquivo corrigido: {filename}")
        else:
            print("✅ Nenhuma duplicata encontrada")

def verify_unique_ids():
    """Verificar se todos os IDs são únicos"""
    print("\n🔍 Verificando IDs únicos...")
    
    files_to_check = [
        'imdb_100plus_movies.json',
        'imdb_50plus_movies.json'
    ]
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            movies = json.load(f)
        
        ids = [movie['id'] for movie in movies]
        unique_ids = set(ids)
        
        print(f"📁 {filename}:")
        print(f"  Total de filmes: {len(movies)}")
        print(f"  IDs únicos: {len(unique_ids)}")
        print(f"  Status: {'✅ Único' if len(ids) == len(unique_ids) else '❌ Duplicatas'}")
        
        if len(ids) != len(unique_ids):
            # Mostrar duplicatas
            from collections import Counter
            id_counts = Counter(ids)
            duplicates = {id: count for id, count in id_counts.items() if count > 1}
            print(f"  🔍 IDs duplicados: {duplicates}")

def main():
    print("🚀 Iniciando correção de filmes duplicados...")
    
    # Corrigir duplicatas
    fix_duplicate_movies()
    
    # Verificar resultado
    verify_unique_ids()
    
    print("\n✅ Correção de duplicatas concluída!")

if __name__ == '__main__':
    main()
