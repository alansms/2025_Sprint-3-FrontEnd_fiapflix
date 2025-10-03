# 🧪 Guia Completo de Testes - FiapFlix

## 📋 Índice

1. [Testes de Clusters](#-testes-de-clusters)
2. [Testes do Modelo Python](#-testes-do-modelo-python)
3. [Testes da API](#-testes-da-api)
4. [Testes da Interface](#-testes-da-interface)
5. [Validação dos Métodos 1 e 2](#-validação-dos-métodos-1-e-2)
6. [Análise de Métricas](#-análise-de-métricas)
7. [Testes de Deploy](#-testes-de-deploy)

---

## 🎯 Testes de Clusters

### 1. Visualizar Distribuição de Clusters

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

# Contar filmes por cluster TF-IDF
tail -n +2 imdb_100plus_with_clusters.csv | cut -d';' -f16 | sort | uniq -c

# Contar filmes por cluster All Features
tail -n +2 imdb_100plus_with_clusters.csv | cut -d';' -f20 | sort | uniq -c
```

**Resultado Esperado:**
```
   12 0
   8 1
   15 2
   10 3
   5 4
```

---

### 2. Ver Filmes de um Cluster Específico

```bash
# Ver todos os filmes do Cluster 2
awk -F';' '$16 == 2' imdb_100plus_with_clusters.csv | cut -d';' -f3,4,6,7

# Top 5 filmes do Cluster 2 por rating
awk -F';' '$16 == 2' imdb_100plus_with_clusters.csv | sort -t';' -k6 -rn | head -5 | cut -d';' -f3,4,6
```

**Exemplo de Saída:**
```
The Shawshank Redemption;Um Sonho de Liberdade;9.3
The Godfather;O Poderoso Chefão;9.2
The Dark Knight;O Cavaleiro das Trevas;9.1
```

---

### 3. Análise Completa dos Clusters (Python)

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

python3 << 'EOF'
import pandas as pd

df = pd.read_csv('imdb_100plus_with_clusters.csv', sep=';')

print("╔══════════════════════════════════════════════════╗")
print("║       ANÁLISE COMPLETA DOS CLUSTERS             ║")
print("╚══════════════════════════════════════════════════╝\n")

print(f"📊 Total de filmes: {len(df)}")
print(f"🎬 Anos: {df['year'].min():.0f} - {df['year'].max():.0f}")
print(f"⭐ Rating médio: {df['rating'].mean():.2f}\n")

for cluster in sorted(df['cluster_tfidf'].unique()):
    cluster_df = df[df['cluster_tfidf'] == cluster]
    
    print(f"\n{'='*70}")
    print(f"🎯 CLUSTER {cluster}")
    print(f"{'='*70}")
    print(f"  📈 Quantidade: {len(cluster_df)} filmes")
    print(f"  ⭐ Rating médio: {cluster_df['rating'].mean():.2f}")
    print(f"  📅 Ano médio: {cluster_df['year'].mean():.0f}")
    print(f"  🎭 Gênero predominante: {cluster_df['genre'].mode().iloc[0] if len(cluster_df['genre'].mode()) > 0 else 'N/A'}")
    
    print(f"\n  🏆 Top 3 Filmes:")
    top3 = cluster_df.nlargest(3, 'rating')[['title_pt', 'rating', 'year']]
    for idx, row in top3.iterrows():
        print(f"     {row['rating']:.1f} ⭐ {row['title_pt']} ({row['year']:.0f})")

print("\n" + "="*70)
print("Análise concluída!")
EOF
```

**Teste Passou:** ✅ Se mostrar estatísticas de todos os clusters

---

## 🐍 Testes do Modelo Python

### 1. Teste Básico do Modelo

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

python3 lib/run_recommendation.py '{"synopsis":"Um filme sobre amizade em uma prisão","method":"tfidf","year":2000,"rating":8,"genre":"Drama"}'
```

**Resultado Esperado:**
```json
{
  "recommendations": [
    {
      "title_en": "Movie name",
      "title_pt": "Nome do filme",
      "rating": 9.3,
      "cluster": 2
    }
  ],
  "cluster": 2,
  "confidence": 0.85,
  "method": "tfidf"
}
```

**Teste Passou:** ✅ Se retornar 5 filmes do mesmo cluster

---

### 2. Teste com Diferentes Sinopses

```bash
# Teste 1: Drama em prisão
python3 lib/run_recommendation.py '{"synopsis":"Um banqueiro condenado forma uma amizade em uma prisão","method":"tfidf","year":1994,"rating":9,"genre":"Drama"}'

# Teste 2: Ação com super-heróis
python3 lib/run_recommendation.py '{"synopsis":"Um super-herói mascarado luta contra o crime em uma cidade","method":"tfidf","year":2008,"rating":9,"genre":"Action"}'

# Teste 3: Ficção científica
python3 lib/run_recommendation.py '{"synopsis":"Viagem no tempo e paradoxos temporais","method":"tfidf","year":2014,"rating":8,"genre":"Sci-Fi"}'

# Teste 4: Crime organizado
python3 lib/run_recommendation.py '{"synopsis":"Uma família do crime organizado luta pelo poder","method":"tfidf","year":1972,"rating":9,"genre":"Crime"}'

# Teste 5: Fantasia épica
python3 lib/run_recommendation.py '{"synopsis":"Uma jornada épica para destruir um anel mágico","method":"tfidf","year":2001,"rating":8,"genre":"Fantasy"}'
```

**Teste Passou:** ✅ Se cada sinopse retornar cluster diferente e consistente

---

### 3. Teste de Consistência do Modelo

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

python3 << 'EOF'
import json
import subprocess

# Testar mesma sinopse 5 vezes
synopsis = "Um filme sobre um detetive que investiga crimes"

clusters = []
for i in range(5):
    cmd = f'python3 lib/run_recommendation.py \'{{"synopsis":"{synopsis}","method":"tfidf","year":2000,"rating":8,"genre":"Crime"}}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        clusters.append(data.get('cluster', None))
    except:
        print(f"Tentativa {i+1}: Erro ao processar resposta")

print(f"Clusters retornados: {clusters}")
print(f"Consistente: {len(set(clusters)) == 1}")
print(f"✅ PASSOU" if len(set(clusters)) == 1 else "❌ FALHOU")
EOF
```

**Teste Passou:** ✅ Se retornar sempre o mesmo cluster

---

## 🌐 Testes da API

### 1. Teste do Endpoint de Filmes

```bash
# Servidor local
curl -s http://localhost:3001/api/movies | python3 -m json.tool | head -50

# Servidor de produção
curl -s http://191.252.203.163:3001/api/movies | python3 -m json.tool | head -50
```

**Teste Passou:** ✅ Se retornar array com 50+ filmes

---

### 2. Teste do Endpoint de Recomendação (Método 1)

```bash
# Teste com sinopse pré-definida
curl -X POST http://localhost:3001/api/recommend-smart \
  -H "Content-Type: application/json" \
  -d '{
    "synopsis": "Um banqueiro condenado por uxoricídio forma uma amizade ao longo de um quarto de século com um criminoso endurecido",
    "method": "tfidf",
    "year": null,
    "rating": null,
    "genre": null
  }' | python3 -m json.tool
```

**Resultado Esperado:**
```json
{
  "recommendations": [...],
  "cluster": 2,
  "confidence": 0.85,
  "evidence": {
    "processed_text": "...",
    "selected_cluster": 2,
    "confidence": 0.85
  }
}
```

**Teste Passou:** ✅ Se retornar 5 recomendações com cluster e confiança

---

### 3. Teste do Endpoint de Recomendação (Método 2)

```bash
# Teste com sinopse personalizada
curl -X POST http://localhost:3001/api/recommend-smart \
  -H "Content-Type: application/json" \
  -d '{
    "synopsis": "Quero um filme sobre viagens espaciais e exploração do universo",
    "method": "tfidf",
    "year": null,
    "rating": null,
    "genre": null
  }' | python3 -m json.tool
```

**Teste Passou:** ✅ Se processar sinopse personalizada e retornar recomendações

---

### 4. Teste do Endpoint de Busca IA

```bash
# Teste de busca semântica
curl -X POST http://localhost:3001/api/ai-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Filmes de drama com rating alto"
  }' | python3 -m json.tool
```

**Teste Passou:** ✅ Se retornar análise e lista de filmes

---

## 🎨 Testes da Interface

### 1. Teste de Carregamento da Página

```bash
# Verificar se a página carrega
curl -I http://localhost:3001

# Verificar se o CSS carrega
curl -I http://localhost:3001/_next/static/css/app/layout.css
```

**Teste Passou:** ✅ Se retornar status 200

---

### 2. Checklist Manual da Interface

- [ ] **Splash Screen**
  - [ ] Vídeo de abertura aparece
  - [ ] Botão "Skip" funciona após 3 segundos
  - [ ] Transição suave para página principal

- [ ] **Página Principal**
  - [ ] Header com logo e navegação
  - [ ] Hero section com filme em destaque
  - [ ] Carrosséis de filmes carregam
  - [ ] Imagens dos filmes aparecem
  - [ ] Hover nos cards mostra informações

- [ ] **Método 1: Escolha de Sinopse**
  - [ ] Modal abre ao clicar "Recomendação IA"
  - [ ] 5 sinopses aparecem sem títulos
  - [ ] Ao selecionar, mostra loading
  - [ ] Retorna 5 filmes do mesmo cluster
  - [ ] Mostra evidências do modelo (cluster, confiança)

- [ ] **Método 2: Sinopse Personalizada**
  - [ ] Campo textarea funciona
  - [ ] Placeholder com exemplo aparece
  - [ ] Botão "Analisar Sinopse" desabilitado quando vazio
  - [ ] Processa texto e retorna recomendações
  - [ ] Mostra evidências do modelo

- [ ] **Busca com IA**
  - [ ] Modal abre ao clicar "Busca IA"
  - [ ] Campo de busca aceita texto natural
  - [ ] Retorna resposta em linguagem natural
  - [ ] Mostra filmes relevantes

- [ ] **Minha Lista**
  - [ ] Botão de favoritar funciona
  - [ ] Modal "Minha Lista" mostra favoritos
  - [ ] Favoritos persistem após reload
  - [ ] Pode remover favoritos

- [ ] **Detalhes do Filme**
  - [ ] Botão "Mais informações" abre modal
  - [ ] Modal mostra informações completas
  - [ ] Pode adicionar aos favoritos no modal

---

## ✅ Validação dos Métodos 1 e 2

### Método 1: Checklist de Conformidade

```bash
# Verificar se sinopses não têm título
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

grep -A 5 "const sampleSynopses" components/RecommendationModal.tsx | grep -c "title"
```

**Teste Passou:** ✅ Se retornar 0 (nenhum campo `title`)

---

### Método 2: Verificar Uso Exclusivo do TF-IDF

```bash
# Verificar que método 2 usa apenas TF-IDF
grep -A 10 "methodType === 'method2'" components/RecommendationModal.tsx | grep "tfidf"
```

**Teste Passou:** ✅ Se encontrar `method: 'tfidf'`

---

### Critério de Seleção: Rating Decrescente

```bash
# Verificar ordenação no código Python
grep -A 2 "sort_values" lib/ml_model_trained.py | grep "rating"
```

**Teste Passou:** ✅ Se encontrar `sort_values('rating', ascending=False)`

---

## 📊 Análise de Métricas

### 1. Calcular Métricas do Modelo

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

python3 << 'EOF'
import pandas as pd
import joblib
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Carregar dados e modelo
df = pd.read_csv('imdb_100plus_with_clusters.csv', sep=';')
kmeans = joblib.load('models/kmeans_tfidf.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')

# Vetorizar sinopses
X = vectorizer.transform(df['sinopse_clean'].fillna(''))
labels = kmeans.labels_

# Calcular métricas
silhouette = silhouette_score(X, labels)
calinski = calinski_harabasz_score(X.toarray(), labels)
davies = davies_bouldin_score(X.toarray(), labels)

print("╔══════════════════════════════════════════════════╗")
print("║       MÉTRICAS DO MODELO KMEANS TF-IDF          ║")
print("╚══════════════════════════════════════════════════╝\n")

print(f"📊 Silhouette Score:     {silhouette:.4f}")
print(f"   → Interpretação:      {'Bom' if silhouette > 0.3 else 'Regular'}")
print(f"   → Range:              -1 a 1 (maior é melhor)")
print()

print(f"📈 Calinski-Harabasz:    {calinski:.2f}")
print(f"   → Interpretação:      {'Bom' if calinski > 100 else 'Regular'}")
print(f"   → Range:              0+ (maior é melhor)")
print()

print(f"📉 Davies-Bouldin:       {davies:.4f}")
print(f"   → Interpretação:      {'Bom' if davies < 1.0 else 'Regular'}")
print(f"   → Range:              0+ (menor é melhor)")
print()

# Avaliação geral
if silhouette > 0.3 and davies < 1.0:
    print("✅ MODELO APROVADO - Boa qualidade de clusterização")
else:
    print("⚠️  MODELO ACEITÁVEL - Pode ser melhorado")
EOF
```

**Teste Passou:** ✅ Se métricas estiverem dentro do esperado

---

### 2. Comparar Modelo TF-IDF vs All Features

```bash
cd /Users/alansms/Documents/FIAP/2025/FiapFlix

python3 << 'EOF'
import pandas as pd

df = pd.read_csv('imdb_100plus_with_clusters.csv', sep=';')

print("╔══════════════════════════════════════════════════╗")
print("║     COMPARAÇÃO: TF-IDF vs ALL FEATURES          ║")
print("╚══════════════════════════════════════════════════╝\n")

print("📊 Distribuição TF-IDF:")
print(df['cluster_tfidf'].value_counts().sort_index())
print(f"\nDesvio padrão: {df['cluster_tfidf'].value_counts().std():.2f}\n")

print("📊 Distribuição All Features:")
print(df['cluster_all'].value_counts().sort_index())
print(f"\nDesvio padrão: {df['cluster_all'].value_counts().std():.2f}\n")

# Avaliar qual é mais equilibrado
std_tfidf = df['cluster_tfidf'].value_counts().std()
std_all = df['cluster_all'].value_counts().std()

if std_tfidf < std_all:
    print("✅ TF-IDF tem distribuição mais equilibrada")
else:
    print("⚠️  All Features tem distribuição mais equilibrada")
EOF
```

**Teste Passou:** ✅ Se análise for consistente

---

## 🚀 Testes de Deploy

### 1. Verificar Servidor de Produção

```bash
# Ping ao servidor
ping -c 3 191.252.203.163

# Verificar porta 3001
nc -zv 191.252.203.163 3001

# Testar página principal
curl -I http://191.252.203.163:3001
```

**Teste Passou:** ✅ Se retornar status 200

---

### 2. Testar Endpoints em Produção

```bash
# Testar API de filmes
curl -s http://191.252.203.163:3001/api/movies | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'✅ {len(data)} filmes carregados')"

# Testar API de recomendação
curl -X POST http://191.252.203.163:3001/api/recommend-smart \
  -H "Content-Type: application/json" \
  -d '{"synopsis":"teste","method":"tfidf"}' \
  -s | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'✅ Cluster: {data.get(\"cluster\", \"N/A\")}')"
```

**Teste Passou:** ✅ Se APIs responderem corretamente

---

### 3. Teste de Performance

```bash
# Medir tempo de resposta da API
time curl -s http://191.252.203.163:3001/api/movies > /dev/null

# Teste de carga (10 requisições paralelas)
for i in {1..10}; do
  curl -s http://191.252.203.163:3001/api/movies > /dev/null &
done
wait
echo "✅ Teste de carga concluído"
```

**Teste Passou:** ✅ Se todas as requisições retornarem sucesso

---

## 📝 Checklist Final

### ✅ Pré-Entrega

- [ ] Todos os testes de clusters passaram
- [ ] Modelo Python funciona corretamente
- [ ] API responde em < 2 segundos
- [ ] Interface carrega sem erros
- [ ] Método 1 retorna 5 filmes sem mostrar títulos
- [ ] Método 2 usa exclusivamente TF-IDF
- [ ] Critério de seleção é rating decrescente
- [ ] Deploy está online e acessível
- [ ] README.md está completo
- [ ] VALIDACAO_METODO1.md existe
- [ ] VALIDACAO_METODO2.md existe
- [ ] GitHub está atualizado

### ✅ Documentação

- [ ] README com dados do desenvolvedor
- [ ] README com URL do deploy
- [ ] README com objetivos do projeto
- [ ] Justificativa da escolha do modelo
- [ ] Screenshots (opcional)

---

## 🎯 Resultado Esperado

**Status Geral:**
```
✅ Testes de Clusters:        PASSOU
✅ Testes do Modelo Python:   PASSOU
✅ Testes da API:             PASSOU
✅ Testes da Interface:       PASSOU
✅ Validação Métodos 1 e 2:   PASSOU
✅ Análise de Métricas:       PASSOU
✅ Testes de Deploy:          PASSOU

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 PROJETO FIAPFLIX: 100% PRONTO PARA ENTREGA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📞 Suporte

**Desenvolvedor:** Alan de Souza Maximiano  
**RM:** 557088  
**Turma:** 2TIAPY  
**Email:** RM557088@fiap.com.br

**Deploy:** [http://191.252.203.163:3001](http://191.252.203.163:3001)  
**GitHub:** [https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix](https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix)

---

**Data de Criação:** 03/10/2025  
**Versão:** 1.0  
**Status:** ✅ Completo

