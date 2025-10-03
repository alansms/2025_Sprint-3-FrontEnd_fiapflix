# 📁 Estrutura do Projeto FiapFlix

## 🗂️ Arquivos Principais

```
FiapFlix/
├── 📄 README.md                              # Documentação principal
├── 📄 GUIA_TESTES.md                         # Guia completo de testes
├── 📄 VALIDACAO_METODO1.md                   # Validação Método 1 (escolha)
├── 📄 VALIDACAO_METODO2.md                   # Validação Método 2 (personalizado)
├── 📄 ESTRUTURA_PROJETO.md                   # Este arquivo
│
├── 📓 Notebook1_IMDb_WebScraping_KMeans.ipynb    # Web scraping + EDA
├── 📓 Notebook2_Modelo_Comparacao_Features.ipynb  # Comparação de modelos
│
├── 📊 imdb_100plus_movies_complete.json      # Dataset JSON completo
├── 📊 imdb_100plus_with_clusters.csv         # Dataset processado com clusters
├── 📊 model_comparison_summary.csv           # Comparação de métricas
│
├── 📦 package.json                           # Dependências Node.js
├── 📦 package-lock.json                      # Lock de dependências
├── 📦 requirements.txt                       # Dependências Python
│
├── ⚙️  next.config.js                         # Configuração Next.js
├── ⚙️  tsconfig.json                          # Configuração TypeScript
├── ⚙️  tailwind.config.js                     # Configuração Tailwind
├── ⚙️  postcss.config.js                      # Configuração PostCSS
├── ⚙️  next-env.d.ts                          # Tipos Next.js
│
├── 🔒 .gitignore                             # Ignorar arquivos Git
├── 🐳 .dockerignore                          # Ignorar arquivos Docker
│
└── 📂 Diretórios Principais
    ├── app/                                  # Next.js App Router
    │   ├── layout.tsx                        # Layout global
    │   ├── page.tsx                          # Página principal
    │   └── api/                              # API Routes
    │       ├── movies/route.ts               # Endpoint filmes
    │       ├── recommend-smart/route.ts      # Endpoint recomendação
    │       └── ai-search/route.ts            # Endpoint busca IA
    │
    ├── components/                           # Componentes React
    │   ├── Header.tsx                        # Cabeçalho
    │   ├── Hero.tsx                          # Hero section
    │   ├── MovieRow.tsx                      # Carrossel de filmes
    │   ├── RecommendationModal.tsx           # Modal Métodos 1 e 2
    │   ├── AISearchModal.tsx                 # Modal busca IA
    │   ├── MovieDetailsModal.tsx             # Modal detalhes
    │   ├── MovieExpandedModal.tsx            # Modal expandido
    │   ├── FavoritesModal.tsx                # Modal favoritos
    │   └── SplashScreen.tsx                  # Tela splash
    │
    ├── lib/                                  # Bibliotecas e utils
    │   ├── types.ts                          # Tipos TypeScript
    │   ├── ml_model_trained.py               # Sistema ML
    │   └── run_recommendation.py             # Script recomendação
    │
    ├── models/                               # Modelos treinados
    │   ├── kmeans_tfidf.pkl                  # Modelo TF-IDF
    │   ├── tfidf_vectorizer.pkl              # Vetorizador
    │   ├── kmeans_all_features.pkl           # Modelo All Features
    │   ├── standard_scaler.pkl               # Scaler
    │   └── label_encoder_genre.pkl           # Encoder
    │
    ├── public/                               # Assets públicos
    │   └── abertura.mp4                      # Vídeo splash screen
    │
    ├── docs/                                 # Documentação deploy
    │   ├── DEPLOY-VPS.md                     # Guia deploy VPS
    │   ├── Dockerfile                        # Docker config
    │   ├── docker-compose.yml                # Docker compose
    │   ├── nginx.conf                        # Nginx config
    │   └── install-vps.sh                    # Script instalação
    │
    ├── .next/                                # Build Next.js (gerado)
    ├── node_modules/                         # Dependências (gerado)
    └── .git/                                 # Repositório Git
```

---

## 📊 Estatísticas

- **Linhas de Código:** ~5.000+
- **Componentes React:** 8
- **API Routes:** 3
- **Modelos ML:** 2 (TF-IDF + All Features)
- **Dataset:** 50+ filmes
- **Clusters:** 5

---

## 🗑️ Arquivos Removidos na Limpeza

### Scripts de Teste (32 arquivos)
- ❌ `scripts/complete_imdb_scraper.py`
- ❌ `scripts/complete_movie_replacement.py`
- ❌ `scripts/create_balanced_clusters.py`
- ❌ `scripts/debug_clustering.py`
- ❌ `scripts/expand_to_100_movies.py`
- ❌ `scripts/fix_*.py` (múltiplos)
- ❌ `scripts/test_*.py` (múltiplos)
- ❌ E mais 20+ scripts temporários...

### Arquivos Duplicados
- ❌ `imdb_100plus_movies.json` (mantido `_complete.json`)

### Arquivos Não Usados
- ❌ `netlify.toml` (não usando Netlify)
- ❌ `setup.sh` (script antigo)
- ❌ `styles/` (diretório vazio)

### Movidos para `docs/`
- 📦 `DEPLOY-VPS.md`
- 📦 `Dockerfile`
- 📦 `docker-compose.yml`
- 📦 `nginx.conf`
- 📦 `install-vps.sh`

---

## 📈 Tamanho do Projeto

### Antes da Limpeza
- **Arquivos:** ~70 arquivos
- **Tamanho:** ~550 MB (com node_modules)

### Depois da Limpeza
- **Arquivos:** ~38 arquivos essenciais
- **Tamanho:** ~530 MB (com node_modules)
- **Scripts removidos:** 32 arquivos (~250 KB)

---

## 🎯 Arquivos Essenciais para Apresentação

1. ✅ **README.md** - Documentação completa
2. ✅ **GUIA_TESTES.md** - Como testar
3. ✅ **VALIDACAO_METODO1.md** - Validação Método 1
4. ✅ **VALIDACAO_METODO2.md** - Validação Método 2
5. ✅ **Notebooks** - Análise e treinamento
6. ✅ **Dataset CSV** - Dados processados
7. ✅ **Modelos PKL** - Modelos treinados
8. ✅ **Código fonte** - app/, components/, lib/

---

## 🚀 Deploy

**URL Produção:** [http://191.252.203.163:3001](http://191.252.203.163:3001)

**Repositório:** [GitHub - FiapFlix](https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix)

---

## 👨‍💻 Desenvolvedor

**Nome:** Alan de Souza Maximiano  
**RM:** 557088  
**Turma:** 2TIAPY  
**Email:** RM557088@fiap.com.br

---

**Última Atualização:** 03/10/2025  
**Status:** ✅ Projeto limpo e organizado

