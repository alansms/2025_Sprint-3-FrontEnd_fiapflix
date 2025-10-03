# 🎬 FiapFlix - Sistema de Recomendação de Filmes com IA

<div align="center">

![FiapFlix Banner](https://img.shields.io/badge/FiapFlix-Sistema%20de%20Recomenda%C3%A7%C3%A3o-E50914?style=for-the-badge&logo=netflix&logoColor=white)

**Sistema de Recomendação de Filmes baseado em Machine Learning e Clusterização**

[![Deploy](https://img.shields.io/badge/Deploy-Online-success?style=flat-square)](http://191.252.203.163:3001)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)

[🚀 Aplicação Online](http://191.252.203.163:3001) | [📊 Notebooks](./notebooks) | [📋 Validações](./VALIDACAO_METODO1.md)

</div>

---

## 👨‍💻 Desenvolvedor

| Campo | Informação |
|-------|------------|
| **Nome** | Alan de Souza Maximiano |
| **RM** | 557088 |
| **Turma** | 2TIAPY |
| **Email** | RM557088@fiap.com.br |
| **Instituição** | FIAP - Faculdade de Informática e Administração Paulista |

---

## 🎯 Objetivo do Projeto

A partir dos notebooks desenvolvidos nas aulas 01 a 04 do 2º semestre, onde foram aplicadas técnicas de **processamento de texto** e biblioteca de **AutoML PyCaret** para modelos de clusterização, este projeto visa:

### 📚 Objetivos Técnicos

1. ✅ **Incluir as demais features do dataset** para o treinamento dos modelos utilizando a biblioteca de AutoML **PyCaret**.
   - **Implementado:** `Notebook3_PyCaret_Comparison.ipynb`
   - **Features:** year, rating, word_count, genre
   - **Status:** 100% Conforme

2. ✅ **Escolher a melhor opção entre os modelos** (via PyCaret ou Scikit-learn), com ou sem o uso de todas as features, **justificando a escolha**.
   - **Implementado:** Comparação completa PyCaret vs Scikit-learn
   - **Métricas:** Silhouette, Calinski-Harabasz, Davies-Bouldin
   - **Status:** 100% Conforme

3. ✅ **Desenvolver um webapp** onde o usuário receba recomendações de filmes baseadas no modelo de clusterização treinado. Em uma tela inicial o usuário poderá escolher entre 2 métodos:

   - ✅ **Método 1:** Apresentar 3 a 5 opções de sinopses de filme (sem mostrar o título) e solicitar ao usuário que escolha 1 deles. Identificar a qual cluster pertence a sinopse escolhida e recomendar uma lista de 5 filmes pertencentes ao mesmo cluster. Definir o melhor critério para a seleção dos 5 filmes do cluster em questão a serem recomendados.
     - **Status:** 100% Conforme (`VALIDACAO_METODO1.md`)

   - ✅ **Método 2:** Solicitar ao usuário que escreva um exemplo de sinopse de filme que agradaria a ele, e então esta sinopse deverá passar pelo processamento de texto e ser submetida ao modelo, que a classificará em um dos clusters. **Para este método deverá ser utilizado o modelo treinado somente com as sinopses vetorizadas.** Daí em diante o processo é o mesmo do método 1.
     - **Status:** 100% Conforme (`VALIDACAO_METODO2.md`)

4. ✅ **Realizar o deploy do webapp** em ambiente de produção.
   - **URL:** http://191.252.203.163:3001
   - **Status:** 100% Funcional

5. ✅ **(Opcional, 1 ponto extra)** - Enriquecer as sinopses de cada filme da base de dados utilizando **IA Generativa**.
   - **Implementado:** `lib/ai_synopsis_enhancer.py`
   - **API:** `/api/enhance-synopsis`
   - **Componente:** `AIEnhancementModal.tsx`
   - **Status:** 100% Implementado

---

## 🚀 Deploy

### 🌐 Aplicação Online

**URL:** [http://191.252.203.163:3001](http://191.252.203.163:3001)

**Status:** ✅ Online e Funcional

**Infraestrutura:**
- Servidor: VPS Linux
- Container: Docker
- Proxy: Nginx
- CI/CD: GitHub Actions

---

## 📊 Modelos de Machine Learning

### 🔬 Modelos Treinados

#### 1️⃣ **Modelo TF-IDF (Apenas Sinopses)**
- **Arquivo:** `models/kmeans_tfidf.pkl`
- **Vetorizador:** `models/tfidf_vectorizer.pkl`
- **Features:** Sinopses vetorizadas (TF-IDF)
- **Clusters:** 5
- **Uso:** Métodos 1 e 2

#### 2️⃣ **Modelo All Features (Multidimensional)**
- **Arquivo:** `models/kmeans_all_features.pkl`
- **Scaler:** `models/standard_scaler.pkl`
- **Encoder:** `models/label_encoder_genre.pkl`
- **Features:** Sinopse (TF-IDF) + Ano + Rating + Gênero
- **Clusters:** 5
- **Uso:** Análise comparativa

### 🎯 Escolha do Modelo

**Modelo Escolhido:** `kmeans_tfidf.pkl` (TF-IDF + Sinopses)

**Justificativa (Comparação PyCaret vs Scikit-learn):**
1. ✅ **Melhor Silhouette Score:** 0.42 vs 0.31 (All Features)
2. ✅ **Clusters mais coesos:** Davies-Bouldin Index menor
3. ✅ **Interpretabilidade:** Clusters baseados em similaridade textual
4. ✅ **Alinhamento com objetivo:** Recomendações por tema/estilo narrativo
5. ✅ **Desempenho:** Mais rápido e eficiente
6. ✅ **Comparação PyCaret:** Ver `Notebook3_PyCaret_Comparison.ipynb`

**Detalhes:** Ver `model_comparison_summary.csv` e `pycaret_vs_sklearn_comparison.csv`

---

## 📓 Notebooks de Desenvolvimento

### 1️⃣ **Notebook1_IMDb_WebScraping_KMeans.ipynb**
- 🌐 **Web Scraping** do IMDb Top 250
- 📝 **Processamento de texto** das sinopses
- 🤖 **Treinamento KMeans** com TF-IDF
- 📊 **Análise exploratória** dos dados
- 📈 **Visualizações** dos clusters

### 2️⃣ **Notebook2_Modelo_Comparacao_Features.ipynb**
- 🔍 **Comparação** de modelos KMeans (Scikit-learn)
- 📊 **Features:** TF-IDF vs Todas as features
- 📈 **Métricas:** Silhouette, Calinski-Harabasz, Davies-Bouldin
- ✅ **Justificativa** da escolha do modelo
- 💾 **Salvamento** dos modelos treinados

### 3️⃣ **Notebook3_PyCaret_Comparison.ipynb** ⭐ **NOVO**
- 🤖 **Implementação PyCaret** para clustering
- ⚖️ **Comparação PyCaret vs Scikit-learn**
- 🚀 **AutoML** com múltiplos algoritmos (KMeans, DBSCAN, Hierarchical, GMM)
- 📊 **Features completas:** year, rating, word_count, genre
- ✅ **Justificativa** baseada em performance e métricas
- 📈 **Visualizações** interativas dos resultados
- 💾 **Exportação** de comparações: `pycaret_vs_sklearn_comparison.csv`

---

## 🎬 Funcionalidades

### ✨ Sistema de Recomendação

#### 📝 **Método 1: Escolha de Sinopse**
- Apresenta 5 sinopses reais (sem revelar títulos)
- Usuário escolhe a que mais agrada
- Sistema identifica cluster via TF-IDF + KMeans
- Recomenda **5 filmes** do mesmo cluster
- **Critério de seleção:** Rating (IMDb) decrescente

#### ✍️ **Método 2: Sinopse Personalizada**
- Campo de texto livre para o usuário
- Processamento: lowercase + limpeza + normalização
- Vetorização TF-IDF
- Classificação em cluster
- Recomenda **5 filmes** do mesmo cluster
- **Modelo:** Exclusivamente TF-IDF (sinopses vetorizadas)

### 🤖 **IA Generativa para Enriquecimento de Sinopses** ⭐ **NOVO - PONTO EXTRA**

#### 📝 **Sistema de Enriquecimento**
- **Arquivo Python:** `lib/ai_synopsis_enhancer.py`
- **API Route:** `/api/enhance-synopsis`
- **Componente React:** `AIEnhancementModal.tsx`

#### ✨ **Funcionalidades**
- 🎭 **Múltiplos Estilos:** Cinematográfico, Dramático, Ação, Romântico
- 🤖 **Integração OpenAI:** Suporte para GPT-3.5-turbo (opcional)
- 🔄 **Fallback Local:** Sistema funciona sem API externa
- 📊 **Templates por Gênero:** Drama, Action, Comedy, Thriller, Sci-Fi
- 💾 **Processamento em Lote:** Enriquecimento de datasets completos
- 📈 **Estatísticas:** Tracking de métodos de enriquecimento

#### 🎯 **Como Funciona**
1. Usuário seleciona um filme
2. Sistema analisa: título, ano, gênero, sinopse original
3. IA enriquece a sinopse com:
   - Detalhes visuais e emocionais
   - Linguagem cinematográfica
   - Contexto do gênero
4. Resultado apresentado lado a lado com original

#### 💡 **Exemplo de Uso**
```python
from ai_synopsis_enhancer import AISynopsisEnhancer

enhancer = AISynopsisEnhancer()
result = enhancer.enhance_synopsis(
    title="O Poderoso Chefão",
    year=1972,
    genre="Drama",
    original_synopsis="História de uma família de mafiosos",
    style="cinematic"
)
print(result['enhanced_synopsis'])
```

### 🎨 Interface Netflix-Style

- ✅ Design moderno inspirado em Netflix
- ✅ Splash screen com vídeo de abertura
- ✅ Navegação intuitiva
- ✅ Carrosséis de filmes por categoria
- ✅ Hero section com destaque
- ✅ Busca por IA generativa
- ✅ Sistema de favoritos (localStorage)
- ✅ Modal de detalhes dos filmes
- ✅ Modal de player expandido
- ✅ **Modal de enriquecimento com IA** ⭐ **NOVO**
- ✅ Responsivo (mobile-first)

### 🤖 Busca com IA Generativa

- Busca semântica por linguagem natural
- Exemplos:
  - "Filmes de drama com rating alto"
  - "Filmes de ação dos anos 90"
  - "Filmes com rating baixo"
- Análise de intenção e filtros
- Resposta em linguagem natural
- Recomendações contextualizadas

### 📈 Evidências do Modelo

- **Cluster identificado:** 0-4
- **Confiança do modelo:** 0-100%
- **Método de análise:** TF-IDF / All Features
- **Texto processado:** Preview do texto analisado
- **Análise do cluster:** Tamanho, rating médio, principais gêneros

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **Next.js 14** - Framework React com SSR
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização utility-first
- **Framer Motion** - Animações fluidas
- **Lucide React** - Ícones modernos
- **Axios** - Cliente HTTP

### Backend
- **Next.js API Routes** - Backend serverless
- **Python 3.13** - Machine Learning
- **Scikit-learn** - Modelos de clustering
- **Pandas & NumPy** - Processamento de dados
- **Joblib** - Serialização de modelos
- **NLTK** - Processamento de linguagem natural

### Machine Learning
- **KMeans** - Algoritmo de clusterização
- **TF-IDF** - Vetorização de texto
- **StandardScaler** - Normalização de features
- **LabelEncoder** - Encoding de categorias
- **PyCaret** ⭐ **NOVO** - AutoML para clustering
- **DBSCAN, Hierarchical, GMM** - Algoritmos adicionais (via PyCaret)

### Deploy & DevOps
- **Docker** - Containerização
- **Nginx** - Proxy reverso
- **PM2** - Process manager
- **Git & GitHub** - Controle de versão

### APIs Externas
- **OMDb API** - Posters de filmes
- **TMDB API** - Metadados de filmes (fallback)
- **OpenAI API** ⭐ **NOVO** - IA Generativa (opcional)

---

## 📁 Estrutura do Projeto

```
FiapFlix/
├── app/                          # Next.js App Router
│   ├── api/                      # API Routes
│   │   ├── movies/route.ts       # Endpoint de filmes
│   │   ├── recommend-smart/route.ts  # Sistema de recomendação
│   │   ├── ai-search/route.ts    # Busca com IA generativa
│   │   └── enhance-synopsis/route.ts ⭐ # Enriquecimento IA (NOVO)
│   ├── page.tsx                  # Página principal
│   └── layout.tsx                # Layout global
├── components/                   # Componentes React
│   ├── Header.tsx                # Cabeçalho
│   ├── Hero.tsx                  # Seção hero
│   ├── MovieRow.tsx              # Carrossel de filmes
│   ├── RecommendationModal.tsx   # Modal Métodos 1 e 2
│   ├── AISearchModal.tsx         # Modal busca IA
│   ├── AIEnhancementModal.tsx    ⭐ # Modal enriquecimento (NOVO)
│   ├── MovieDetailsModal.tsx     # Modal de detalhes
│   ├── MovieExpandedModal.tsx    # Modal expandido
│   ├── FavoritesModal.tsx        # Modal de favoritos
│   └── SplashScreen.tsx          # Tela de abertura
├── lib/                          # Bibliotecas e utilitários
│   ├── types.ts                  # Tipos TypeScript
│   ├── ml_model_trained.py       # Sistema de ML
│   ├── run_recommendation.py     # Script de recomendação
│   └── ai_synopsis_enhancer.py   ⭐ # Enriquecedor IA (NOVO)
├── models/                       # Modelos treinados
│   ├── kmeans_tfidf.pkl          # Modelo TF-IDF
│   ├── tfidf_vectorizer.pkl      # Vetorizador
│   ├── kmeans_all_features.pkl   # Modelo All Features
│   ├── standard_scaler.pkl       # Scaler
│   └── label_encoder_genre.pkl   # Encoder
├── public/                       # Assets públicos
│   └── abertura.mp4              # Vídeo splash screen
├── Notebook1_IMDb_WebScraping_KMeans.ipynb  # Web Scraping + KMeans
├── Notebook2_Modelo_Comparacao_Features.ipynb  # Comparação Modelos
├── Notebook3_PyCaret_Comparison.ipynb ⭐ # PyCaret vs Scikit (NOVO)
├── imdb_100plus_with_clusters.csv  # Dataset processado
├── pycaret_vs_sklearn_comparison.csv ⭐ # Comparação ML (NOVO)
├── VALIDACAO_METODO1.md          # Relatório Método 1
├── VALIDACAO_METODO2.md          # Relatório Método 2
├── REVISAO_OBJETIVOS.md          ⭐ # Revisão Completa (NOVO)
├── GUIA_TESTES.md                # Guia de Testes
├── ESTRUTURA_PROJETO.md          # Estrutura Detalhada
├── package.json                  # Dependências Node.js
├── tsconfig.json                 # Config TypeScript
├── tailwind.config.ts            # Config Tailwind
├── next.config.js                # Config Next.js
├── Dockerfile                    # Container Docker
└── README.md                     # Este arquivo
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- **Node.js** 20.x ou superior
- **Python** 3.13 ou superior
- **npm** ou **yarn**
- **Git**

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix.git
cd 2025_Sprint-3-FrontEnd_fiapflix
```

### 2️⃣ Instale Dependências Node.js

```bash
npm install
```

### 3️⃣ Instale Dependências Python

```bash
pip3 install pandas numpy scikit-learn joblib
```

### 4️⃣ Execute o Servidor de Desenvolvimento

```bash
npm run dev
```

### 5️⃣ Acesse a Aplicação

Abra o navegador em: [http://localhost:3000](http://localhost:3000)

---

## 🐳 Deploy com Docker

### Build da Imagem

```bash
docker build -t fiapflix .
```

### Executar Container

```bash
docker run -p 3001:3000 fiapflix
```

### Docker Compose

```bash
docker-compose up -d
```

---

## 📊 Dataset

### 📁 Fonte de Dados

- **IMDb Top 250 Movies** (web scraping)
- **50+ filmes** processados e clusterizados
- **Features:** Título (EN/PT), Ano, Rating, Gênero, Sinopse, Diretor, Elenco

### 🔄 Processamento

1. **Web Scraping:** BeautifulSoup4 + Requests
2. **Limpeza:** Remoção de caracteres especiais, normalização
3. **TF-IDF:** Vetorização de sinopses
4. **Clustering:** KMeans (k=5)
5. **Enriquecimento:** OMDb API para posters

### 📈 Métricas dos Modelos

| Modelo | Silhouette Score | Calinski-Harabasz | Davies-Bouldin |
|--------|------------------|-------------------|----------------|
| **TF-IDF** | **0.42** | 156.3 | **0.81** |
| All Features | 0.31 | 142.7 | 1.02 |

**Vencedor:** TF-IDF (melhor coesão e separação de clusters)

---

## 📋 Validações

### ✅ Método 1: Escolha de Sinopse

**Documento:** [VALIDACAO_METODO1.md](./VALIDACAO_METODO1.md)

**Status:** ✅ **100% CONFORME**

- ✅ Apresenta 5 sinopses sem mostrar títulos
- ✅ Usuário escolhe 1 sinopse
- ✅ Identifica cluster via TF-IDF + KMeans
- ✅ Recomenda 5 filmes do mesmo cluster
- ✅ Critério: Rating (IMDb) decrescente

### ✅ Método 2: Sinopse Personalizada

**Documento:** [VALIDACAO_METODO2.md](./VALIDACAO_METODO2.md)

**Status:** ✅ **100% CONFORME**

- ✅ Campo textarea para sinopse personalizada
- ✅ Processamento de texto completo
- ✅ **Usa EXCLUSIVAMENTE modelo TF-IDF (sinopses vetorizadas)**
- ✅ Classifica em cluster
- ✅ Recomenda 5 filmes do mesmo cluster
- ✅ Critério: Rating (IMDb) decrescente

---

## 🎨 Screenshots

### 🏠 Tela Principal
Interface Netflix-style com hero section e carrosséis de filmes.

### 🎬 Sistema de Recomendação
Modal interativo com Método 1 (escolha) e Método 2 (personalizado).

### 🤖 Busca com IA
Busca semântica com linguagem natural e resposta contextualizada.

### ❤️ Minha Lista
Sistema de favoritos persistente com localStorage.

---

## 🧪 Testes

### Teste dos Modelos Python

```bash
cd /path/to/FiapFlix
python3 lib/run_recommendation.py '{"synopsis":"Um filme sobre um detetive","method":"tfidf","year":2000,"rating":8,"genre":"Drama"}'
```

### Teste da API

```bash
curl -X POST http://localhost:3000/api/recommend-smart \
  -H "Content-Type: application/json" \
  -d '{"synopsis":"Filme sobre super-heróis","method":"tfidf"}'
```

---

## 📚 Notebooks

### 1️⃣ **Notebook1_IMDb_WebScraping_KMeans.ipynb**
- Web scraping do IMDb Top 250
- Limpeza e processamento de dados
- Análise exploratória (EDA)
- Primeira versão do modelo KMeans

### 2️⃣ **Notebook2_Modelo_Comparacao_Features.ipynb**
- Comparação de modelos (TF-IDF vs All Features)
- Avaliação com múltiplas métricas
- Análise de clusters
- Seleção do melhor modelo
- Geração dos arquivos `.pkl`

---

## 🔮 Funcionalidades Futuras

- [ ] Integração com mais APIs de filmes
- [ ] Sistema de avaliação de usuários
- [ ] Recomendações personalizadas por perfil
- [ ] Análise de sentimento nas sinopses
- [ ] Exportação de listas para PDF
- [ ] Sistema de notificações
- [ ] Modo offline com PWA

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte do curso de **Análise e Desenvolvimento de Sistemas** da **FIAP**.

---

## 🙏 Agradecimentos

- **FIAP** - Pela excelente formação acadêmica
- **Professores** - Pelo conhecimento compartilhado
- **Comunidade Open Source** - Pelas ferramentas incríveis
- **IMDb** - Pelos dados públicos de filmes
- **OMDb API** - Pelos posters de filmes

---

## 📞 Contato

**Alan de Souza Maximiano**

- 📧 Email: RM557088@fiap.com.br
- 🎓 RM: 557088
- 🏫 Turma: 2TIAPY
- 🔗 GitHub: [@alansms](https://github.com/alansms)

---

<div align="center">

**Desenvolvido com ❤️ para FIAP**

🎬 **[Acesse a Aplicação](http://191.252.203.163:3001)** 🎬

![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-2TIAPY-red?style=for-the-badge)

</div>
