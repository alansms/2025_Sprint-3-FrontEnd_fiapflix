#!/usr/bin/env python3
"""
🧠 Script para criar um fallback inteligente baseado em palavras-chave
"""

import pandas as pd
import re
import json
import random

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

def create_smart_fallback():
    """Criar fallback inteligente baseado em palavras-chave"""
    print("🧠 Criando fallback inteligente...")
    
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
    
    # Definir categorias baseadas em palavras-chave
    categories = {
        'acao': {
            'keywords': ['ação', 'luta', 'combate', 'guerra', 'soldado', 'batalha', 'vigilante', 'mascarado', 'criminoso', 'justiça', 'vingança'],
            'movies': []
        },
        'drama': {
            'keywords': ['drama', 'emocional', 'família', 'relacionamento', 'amor', 'paixão', 'jovem', 'diferente', 'preconceito', 'obstáculo'],
            'movies': []
        },
        'ficcao': {
            'keywords': ['ficção', 'científica', 'espaço', 'astronauta', 'universo', 'futuro', 'tecnologia', 'mágico', 'poder', 'reino'],
            'movies': []
        },
        'terror': {
            'keywords': ['terror', 'assombrado', 'espírito', 'sobrenatural', 'morte', 'assassinato', 'mistério', 'detetive', 'investigação'],
            'movies': []
        },
        'comedia': {
            'keywords': ['comédia', 'hilário', 'cômico', 'viagem', 'amigo', 'situação', 'mal-entendido', 'musical', 'cantora', 'famoso'],
            'movies': []
        }
    }
    
    # Classificar filmes por categoria
    for _, movie in df.iterrows():
        sinopse_clean = clean_text(movie['sinopse'])
        title_clean = clean_text(movie['title_pt'])
        genre_clean = clean_text(movie['genre'])
        
        # Combinar texto para análise
        combined_text = f"{sinopse_clean} {title_clean} {genre_clean}"
        
        # Contar matches por categoria
        category_scores = {}
        for category, data in categories.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in combined_text:
                    score += 1
            category_scores[category] = score
        
        # Atribuir à categoria com maior score
        if max(category_scores.values()) > 0:
            best_category = max(category_scores, key=category_scores.get)
            categories[best_category]['movies'].append(movie.to_dict())
    
    # Mostrar distribuição
    print(f"\n📊 Distribuição por categoria:")
    for category, data in categories.items():
        print(f"  {category.title()}: {len(data['movies'])} filmes")
    
    # Criar função de recomendação inteligente
    def get_smart_recommendations(synopsis, n=5):
        """Obter recomendações baseadas em palavras-chave"""
        synopsis_clean = clean_text(synopsis)
        
        # Contar matches por categoria
        category_scores = {}
        for category, data in categories.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in synopsis_clean:
                    score += 1
            category_scores[category] = score
        
        # Se não há matches, usar categoria aleatória
        if max(category_scores.values()) == 0:
            category_scores = {cat: 1 for cat in categories.keys()}
        
        # Selecionar categoria com maior score
        best_category = max(category_scores, key=category_scores.get)
        available_movies = categories[best_category]['movies']
        
        if len(available_movies) < n:
            # Se não há filmes suficientes, adicionar de outras categorias
            all_movies = []
            for cat_data in categories.values():
                all_movies.extend(cat_data['movies'])
            available_movies = all_movies
        
        # Selecionar filmes aleatórios
        selected_movies = random.sample(available_movies, min(n, len(available_movies)))
        
        return selected_movies, best_category
    
    # Testar com diferentes sinopses
    test_synopses = [
        "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
        "Um detetive investiga uma série de assassinatos brutais em uma cidade pequena, descobrindo segredos sombrios",
        "Um vigilante mascarado protege sua cidade de criminosos perigosos, enfrentando dilemas morais",
        "Dois jovens de classes sociais diferentes se apaixonam, mas precisam superar preconceitos",
        "Um grupo de astronautas embarca em uma missão espacial para salvar a humanidade"
    ]
    
    print(f"\n🧪 Testando recomendações inteligentes:")
    for i, synopsis in enumerate(test_synopses, 1):
        recommendations, category = get_smart_recommendations(synopsis, 5)
        
        print(f"\n  {i}. {synopsis[:50]}...")
        print(f"     Categoria: {category.title()}")
        print(f"     Filmes: {[m['title_pt'] for m in recommendations]}")
    
    # Salvar dados para uso na API
    fallback_data = {
        'categories': categories,
        'total_movies': len(df)
    }
    
    with open('smart_fallback_data.json', 'w', encoding='utf-8') as f:
        json.dump(fallback_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fallback inteligente criado!")
    print(f"📁 Arquivo: smart_fallback_data.json")

if __name__ == '__main__':
    create_smart_fallback()
