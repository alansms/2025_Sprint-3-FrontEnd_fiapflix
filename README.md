# 🎬 FiapFlix - Sistema de Recomendação de Filmes com IA

[![Next.js](https://img.shields.io/badge/Next.js-14.0-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18.0-blue?style=for-the-badge&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)

> Plataforma de streaming inteligente com sistema de recomendação baseado em Machine Learning e Inteligência Artificial Generativa.

## 📋 Sobre o Projeto

FiapFlix é uma aplicação web moderna que simula uma plataforma de streaming (inspirada na Netflix), desenvolvida como projeto acadêmico da FIAP. O diferencial está no sistema de recomendação inteligente que utiliza técnicas de Machine Learning (KMeans + TF-IDF) e IA Generativa para sugerir filmes personalizados baseados em sinopses e preferências do usuário.

### 🎯 Principais Características

- **Interface Netflix-like**: Design moderno e responsivo inspirado nas melhores plataformas de streaming
- **Splash Screen**: Animação de abertura personalizada
- **Sistema de Recomendação Inteligente**: 2 métodos de recomendação baseados em ML
- **Busca Semântica com IA**: Busca inteligente usando Inteligência Artificial Generativa
- **Dados Reais do IMDb**: 50+ filmes do Top 250 do IMDb
- **Posters Reais**: Integração com OMDb API para capas autênticas
- **Favoritos Persistentes**: Sistema de lista personalizada usando LocalStorage
- **Detalhes dos Filmes**: Modal com informações completas e trailer

---

## 🚀 Funcionalidades Detalhadas

### 1. 🎭 Splash Screen
- Vídeo de abertura personalizado (`abertura.mp4`)
- Texto animado "Sistema de Recomendação de Filmes com IA"
- Botão "Pular" após 3 segundos
- Transição suave para a tela principal

### 2. 🏠 Tela Principal
- **Hero Section**: Banner destacado com filme principal
- **Carrosséis de Filmes**: Organizados por categorias
  - Populares no FiapFlix
  - Em Alta
  - Dramas Aclamados
  - Filmes de Ação
- **Navegação Fluida**: Scroll horizontal com animações suaves
- **Responsivo**: Adapta-se a diferentes tamanhos de tela

### 3. 🔍 Sistema de Busca

#### Busca Tradicional
- Campo de busca no header
- Filtragem em tempo real por título
- Resultados instantâneos

#### Busca Inteligente com IA Generativa
- Botão "Busca IA" no header
- Interpreta consultas em linguagem natural
- Exemplos:
  - "Filmes de drama com rating alto"
  - "Filmes de ação dos anos 90"
  - "Filmes com rating baixo"
- Análise semântica de filtros (gênero, ano, rating)
- Resposta em linguagem natural
- Fallback inteligente quando não encontra resultados exatos

### 4. 🤖 Sistema de Recomendação com ML

#### Método 1: Recomendação por Sinopse (Baseado em Clusters)
1. Sistema apresenta 3-5 sinopses de filmes (sem revelar o título)
2. Usuário escolhe a sinopse mais interessante
3. ML identifica o cluster do filme escolhido
4. Recomenda 5 filmes do mesmo cluster
5. Exibe evidências do modelo:
   - Cluster identificado
   - Características do cluster
   - Métricas de similaridade

#### Método 2: Recomendação por Sinopse Personalizada
1. Usuário digita uma sinopse customizada
2. Sistema vetoriza o texto usando TF-IDF
3. Classifica em um dos clusters treinados
4. Recomenda 5 filmes similares
5. Mostra análise detalhada:
   - Cluster mais próximo
   - Confiança da classificação
   - Termos relevantes identificados

**Tecnologias de ML:**
- KMeans Clustering (5 clusters)
- TF-IDF Vectorization
- Scikit-learn
- NLTK para processamento de texto
- StandardScaler e LabelEncoder

### 5. ❤️ Minha Lista (Favoritos)
- Adicionar filmes aos favoritos com um clique
- Botão de coração em cada filme
- Lista persistente usando LocalStorage
- Modal dedicado para visualização dos favoritos
- Remover filmes da lista facilmente
- Funcionamento independente em:
  - Carrosséis principais
  - Resultados de busca
  - Recomendações de IA

### 6. 📊 Detalhes dos Filmes
- **Modal de Informações**: Clique em "Mais informações"
  - Sinopse completa
  - Diretor e elenco
  - Ano, duração, rating
  - Gênero
  - Cluster de classificação
- **Modal Expandido**: Clique na capa do filme
  - Visualização em destaque
  - Opção de adicionar aos favoritos
  - Botão de reprodução (placeholder)

### 7. 🎨 Design e UX
- **Cores**: Esquema Netflix (vermelho #E50914, preto, cinza)
- **Animações**: Framer Motion para transições suaves
- **Ícones**: Lucide React para interface moderna
- **Responsividade**: Mobile-first design
- **Efeitos Hover**: Zoom e destaque nos filmes
- **Loading States**: Indicadores visuais durante carregamento

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **Next.js 14**: Framework React com SSR
- **React 18**: Biblioteca de interfaces
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização utility-first
- **Framer Motion**: Animações
- **Lucide React**: Ícones modernos
- **Axios**: Cliente HTTP

### Backend / ML
- **Next.js API Routes**: Endpoints serverless
- **Python 3.x**: Scripts de Machine Learning
- **Scikit-learn**: Algoritmos de ML (KMeans)
- **NLTK**: Processamento de linguagem natural
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica
- **Joblib**: Persistência de modelos

### APIs Externas
- **OMDb API**: Posters e dados de filmes
  - Chave: `668159f8`
  - Cache em memória para otimização
- **IMDb**: Fonte de dados (Top 250)

### Dados e Modelos
- **imdb_100plus_movies_complete.json**: Dataset principal (50+ filmes)
- **imdb_100plus_with_clusters.csv**: Dados com clusters
- **models/kmeans_tfidf.pkl**: Modelo KMeans treinado
- **models/tfidf_vectorizer.pkl**: Vetorizador TF-IDF
- **model_comparison_summary.csv**: Métricas de avaliação

---

## 📦 Estrutura do Projeto

```
FiapFlix/
├── app/
│   ├── api/
│   │   ├── movies/route.ts          # API de filmes + integração OMDb
│   │   ├── recommend-smart/route.ts # Sistema de recomendação
│   │   └── ai-search/route.ts       # Busca com IA generativa
│   ├── page.tsx                      # Página principal
│   └── layout.tsx                    # Layout base
├── components/
│   ├── Header.tsx                    # Cabeçalho e navegação
│   ├── Hero.tsx                      # Banner principal
│   ├── MovieRow.tsx                  # Carrossel de filmes
│   ├── MovieCard.tsx                 # Card individual de filme
│   ├── SplashScreen.tsx              # Tela de abertura
│   ├── RecommendationModal.tsx       # Modal de recomendações
│   ├── AISearchModal.tsx             # Modal de busca IA
│   ├── FavoritesModal.tsx            # Modal de favoritos
│   ├── MovieDetailsModal.tsx         # Detalhes do filme
│   └── MovieExpandedModal.tsx        # Visualização expandida
├── lib/
│   ├── types.ts                      # Tipos TypeScript
│   ├── ml_model_trained.py           # Modelo ML principal
│   └── utils.ts                      # Funções utilitárias
├── models/                           # Modelos treinados (.pkl)
├── public/
│   └── abertura.mp4                  # Vídeo splash screen
├── scripts/                          # Scripts de processamento
├── Notebook1_IMDb_WebScraping_KMeans.ipynb
├── Notebook2_Modelo_Comparacao_Features.ipynb
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

---

## ⚙️ Instalação e Execução

### Pré-requisitos
- Node.js 20.11+ (recomendado: 20.17+)
- npm 11.6+ (ou yarn)
- Python 3.8+
- Git

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix.git
cd 2025_Sprint-3-FrontEnd_fiapflix
```

### Passo 2: Instalar Dependências Node.js
```bash
npm install
```

### Passo 3: Instalar Dependências Python
```bash
pip install -r requirements.txt
```

Ou usando o script de setup:
```bash
chmod +x setup.sh
./setup.sh
```

### Passo 4: Executar o Servidor de Desenvolvimento
```bash
npm run dev -- --hostname 127.0.0.1 --port 3001
```

### Passo 5: Acessar a Aplicação
Abra o navegador em: **http://127.0.0.1:3001**

---

## 🧪 Testes e Validação

### Testar Sistema de Recomendação

#### Método 1 (Sinopse Pré-definida):
1. Clique em "Recomendação" no header
2. Escolha "Método 1"
3. Selecione uma das sinopses apresentadas
4. Verifique as recomendações e evidências do modelo

#### Método 2 (Sinopse Customizada):
1. Clique em "Recomendação" no header
2. Escolha "Método 2"
3. Digite uma sinopse personalizada, ex:
   > "Uma história épica sobre um hobbit que precisa destruir um anel mágico para salvar o mundo"
4. Veja as recomendações baseadas na sua sinopse

### Testar Busca IA
1. Clique em "Busca IA" no header
2. Digite consultas naturais, ex:
   - "Quero assistir filmes de drama com rating alto"
   - "Me mostre filmes de ação dos anos 2000"
   - "Filmes antigos com rating médio"
3. Veja a resposta em linguagem natural e os resultados

### Testar Favoritos
1. Passe o mouse sobre qualquer filme
2. Clique no ícone de coração
3. Clique em "Minha Lista" no header
4. Veja seus filmes favoritos salvos

---

## 📊 Modelo de Machine Learning

### Arquitetura
1. **Coleta de Dados**: Web scraping do IMDb Top 250
2. **Pré-processamento**:
   - Limpeza de texto
   - Remoção de stopwords
   - Normalização
3. **Vetorização**: TF-IDF (Term Frequency-Inverse Document Frequency)
4. **Clustering**: KMeans com k=5 clusters
5. **Avaliação**:
   - Silhouette Score
   - Calinski-Harabasz Index
   - Davies-Bouldin Index

### Clusters Identificados
- **Cluster 0**: Filmes de Crime/Drama intenso
- **Cluster 1**: Dramas históricos/biográficos
- **Cluster 2**: Ação/Aventura/Ficção Científica
- **Cluster 3**: Thrillers psicológicos
- **Cluster 4**: Comédias dramáticas

### Métricas de Performance
- **Silhouette Score**: 0.18-0.25 (aceitável para dados textuais)
- **Calinski-Harabasz**: ~35-45
- **Davies-Bouldin**: ~1.8-2.2

---

## 🌐 Deploy

### 🐳 VPS com Docker (RECOMENDADO)

**Método mais completo com todas as funcionalidades!**

#### Instalação Automática em 1 Comando:
```bash
curl -fsSL https://raw.githubusercontent.com/alansms/2025_Sprint-3-FrontEnd_fiapflix/main/install-vps.sh | sudo bash
```

**Pronto!** Aplicação estará rodando em `http://SEU_IP`

#### Requisitos:
- Ubuntu 20.04+ ou Debian 11+
- 2GB RAM (recomendado 4GB)
- 2 CPU cores
- 20GB disco

#### Provedores Recomendados:
- **DigitalOcean**: Droplet $12/mês
- **Linode**: $10/mês
- **Contabo**: €5.99/mês
- **Proxmox**: LXC Container local

📖 **Guia Completo**: Ver [DEPLOY-VPS.md](DEPLOY-VPS.md)

---

### Netlify (Limitado - Apenas Frontend)

1. **Criar conta no Netlify**: https://www.netlify.com/

2. **Conectar Repositório**:
   - New site from Git
   - Selecionar GitHub
   - Escolher o repositório

3. **Configurações de Build**:
   ```
   Build command: npm run build
   Publish directory: .next
   ```

4. **Variáveis de Ambiente** (se necessário):
   ```
   NEXT_PUBLIC_APP_URL=https://seu-app.netlify.app
   OMDB_API_KEY=668159f8
   ```

5. **Deploy**: O site será publicado automaticamente

### Vercel (Alternativa)

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 📝 Notebooks Jupyter

### Notebook 1: Web Scraping e KMeans
- Scraping do IMDb Top 250
- Limpeza e preparação dos dados
- Treinamento inicial do KMeans
- Análise exploratória de dados (EDA)

### Notebook 2: Comparação de Modelos
- Comparação entre modelo TF-IDF puro vs. features completas
- Avaliação de métricas
- Seleção do melhor modelo
- Exportação dos modelos treinados

---

## 🤝 Contribuição

Este é um projeto acadêmico, mas contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/MinhaFeature`
3. Commit: `git commit -m 'Adiciona MinhaFeature'`
4. Push: `git push origin feature/MinhaFeature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de Front End & Mobile Development da FIAP.

---

## 👥 Equipe

Desenvolvido por alunos da FIAP - Turma 2025_2

---

## 🙏 Agradecimentos

- **FIAP**: Pela orientação acadêmica
- **IMDb**: Pela fonte de dados
- **OMDb API**: Pelos posters dos filmes
- **Netflix**: Pela inspiração de design
- **Comunidade Open Source**: Pelas ferramentas incríveis

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Abra uma [Issue](https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix/issues)
2. Consulte a documentação nos notebooks
3. Verifique os logs do console

---

## 🔄 Atualizações Recentes

### v2.0.0 (03/10/2024)
- ✅ Integração OMDb API para posters reais
- ✅ Sistema de cache em memória
- ✅ Busca semântica com IA generativa
- ✅ Sistema de favoritos persistentes
- ✅ Modais de detalhes dos filmes
- ✅ 50+ filmes do IMDb
- ✅ Correções de bugs e otimizações

---

## 🎓 Conceitos Aplicados

### Front-End
- Single Page Application (SPA)
- Server-Side Rendering (SSR)
- Responsive Design
- Component-Based Architecture
- State Management
- API Integration
- LocalStorage Persistence

### Machine Learning
- Unsupervised Learning (KMeans)
- Natural Language Processing (NLP)
- TF-IDF Vectorization
- Feature Engineering
- Model Evaluation
- Model Persistence

### UX/UI
- Design Systems
- Animation & Transitions
- Loading States
- Error Handling
- Accessibility (a11y)
- Mobile-First Design

---

**FiapFlix** - Onde a Inteligência Artificial encontra o entretenimento! 🎬🤖
