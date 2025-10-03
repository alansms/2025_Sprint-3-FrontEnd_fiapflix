# 🎬 FiapFlix - Sistema de Recomendação de Filmes com IA

![FiapFlix Logo](https://img.shields.io/badge/FiapFlix-IA%20Powered-red?style=for-the-badge&logo=netflix)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)

## 📋 Sobre o Projeto

O **FiapFlix** é uma plataforma de streaming moderna que utiliza **Inteligência Artificial** para recomendar filmes personalizados. O sistema implementa algoritmos de **clusterização** e **processamento de linguagem natural** para analisar sinopses e sugerir filmes similares.

### 🎯 Características Principais

- ✅ **Interface Netflix-like** com design moderno
- ✅ **Sistema de Recomendação IA** com 2 métodos
- ✅ **Busca Generativa** com análise semântica
- ✅ **Dados Reais do IMDb** (Top 250 filmes)
- ✅ **Splash Screen** com vídeo de abertura
- ✅ **Responsivo** para mobile e desktop

## 🚀 Tecnologias Utilizadas

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Framer Motion** - Animações
- **Lucide React** - Ícones

### Backend & IA
- **Python 3.13** - Processamento de dados
- **Scikit-learn** - Machine Learning
- **NLTK** - Processamento de linguagem natural
- **TF-IDF** - Vetorização de texto
- **KMeans** - Algoritmo de clusterização
- **BeautifulSoup** - Web scraping

### APIs & Dados
- **IMDb Top 250** - Base de dados de filmes
- **TMDB API** - Imagens e metadados
- **Next.js API Routes** - Backend

## 🎭 Funcionalidades

### 1. Sistema de Recomendação IA

#### **Método 1: Seleção de Sinopses**
- Apresenta 3-5 sinopses de filmes (sem títulos)
- Usuário escolhe a sinopse preferida
- Sistema identifica o cluster correspondente
- Recomenda 5 filmes do mesmo cluster

#### **Método 2: Sinopse Personalizada**
- Usuário escreve uma sinopse personalizada
- Sistema processa o texto com NLP
- Classifica em um dos clusters
- Recomenda 5 filmes similares

### 2. Busca IA Generativa
- **Análise semântica** de consultas em linguagem natural
- **Filtros inteligentes** por gênero, rating, ano
- **Resposta natural** em português
- **Interface moderna** com scroll e navegação

### 3. Interface Moderna
- **Splash Screen** com vídeo de abertura
- **Header** com navegação e busca
- **Hero Section** com carrossel de filmes
- **Movie Rows** horizontais responsivas
- **Modais** funcionais para recomendações

## 📊 Modelo de IA

### Algoritmos Implementados
- **TF-IDF Vectorization** - Extração de features de texto
- **KMeans Clustering** - Agrupamento de filmes similares
- **Silhouette Score** - Avaliação da qualidade dos clusters
- **Text Preprocessing** - Limpeza e normalização de texto

### Dataset
- **25 filmes reais** do IMDb Top 250
- **5 clusters balanceados** (5 filmes cada)
- **Dados autênticos** (títulos, ratings, anos, gêneros)
- **Sinopses em português** para melhor compreensão

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Node.js 18+ 
- Python 3.13+
- npm ou yarn

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/fiapflix.git
cd fiapflix
```

### 2. Instale as dependências
```bash
# Dependências Node.js
npm install

# Dependências Python
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env.local
```

### 4. Execute o projeto
```bash
# Desenvolvimento
npm run dev

# Produção
npm run build
npm start
```

## 📁 Estrutura do Projeto

```
fiapflix/
├── app/                    # Next.js App Router
│   ├── api/               # API Routes
│   │   ├── movies/        # Endpoint de filmes
│   │   ├── recommend-fixed/ # Sistema de recomendação
│   │   └── ai-search/     # Busca IA generativa
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Página inicial
├── components/            # Componentes React
│   ├── Header.tsx        # Cabeçalho com navegação
│   ├── Hero.tsx          # Seção principal
│   ├── MovieRow.tsx      # Carrossel de filmes
│   ├── RecommendationModal.tsx # Modal de recomendações
│   ├── AISearchModal.tsx # Modal de busca IA
│   └── SplashScreen.tsx  # Tela de abertura
├── lib/                   # Utilitários e modelos
│   ├── types.ts          # Tipos TypeScript
│   ├── ml_model_trained.py # Modelo de IA
│   └── run_recommendation.py # Execução do modelo
├── scripts/              # Scripts Python
│   ├── create_real_imdb_dataset.py # Scraping IMDb
│   └── retrain_with_real_data.py   # Treinamento
├── models/               # Modelos treinados (.pkl)
├── public/              # Arquivos estáticos
└── README.md            # Documentação
```

## 🎯 Como Usar

### 1. Acesse a aplicação
- Abra http://localhost:3001
- Aguarde o splash screen carregar
- Navegue pela interface

### 2. Sistema de Recomendação
- Clique em "Recomendação IA" no header
- Escolha entre Método 1 ou Método 2
- Siga as instruções para receber recomendações

### 3. Busca IA
- Clique em "Busca IA" no header
- Digite sua consulta em linguagem natural
- Receba resultados inteligentes

## 📈 Performance

### Métricas do Sistema
- **5 filmes** por recomendação
- **Confiança média**: 80%+
- **Tempo de resposta**: < 2 segundos
- **Clusters balanceados**: 5 filmes cada
- **Dados reais**: 25 filmes do IMDb

### Evidências do Modelo
- **Cluster identificado** com confiança
- **Análise de features** (gênero, rating, ano)
- **Filmes representativos** do cluster
- **Métricas de qualidade** (Silhouette Score)

## 🚀 Deploy

### Netlify (Recomendado)
1. Conecte o repositório ao Netlify
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Vercel
1. Importe o projeto no Vercel
2. Configure as variáveis de ambiente
3. Deploy com zero configuração

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

- **Desenvolvimento**: [Seu Nome]
- **IA/ML**: [Nome do Especialista]
- **Design**: [Nome do Designer]

## 📞 Contato

- **Email**: seu.email@fiap.com.br
- **LinkedIn**: [Seu LinkedIn]
- **GitHub**: [Seu GitHub]

---

<div align="center">

**🎬 FiapFlix - Sistema de Recomendação de Filmes com IA**

*Desenvolvido com ❤️ para o Checkpoint 2 - Front End & Mobile Development*

[![Netlify Status](https://api.netlify.com/api/v1/badges/your-badge-id/deploy-status)](https://app.netlify.com/sites/your-site-name/deploys)

</div>