#!/bin/bash

# FiapFlix - Script de Configuração
# Desenvolvido por: FIAP - Front End & Mobile Development

echo "🚀 Configurando FiapFlix - Sistema de Recomendação de Filmes com IA"
echo "=================================================================="

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 18+ primeiro."
    echo "   Download: https://nodejs.org/"
    exit 1
fi

# Verificar versão do Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js versão 18+ é necessária. Versão atual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detectado"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+ primeiro."
    echo "   Download: https://python.org/"
    exit 1
fi

echo "✅ Python $(python3 --version) detectado"

# Instalar dependências Node.js
echo ""
echo "📦 Instalando dependências Node.js..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências Node.js"
    exit 1
fi

echo "✅ Dependências Node.js instaladas"

# Instalar dependências Python
echo ""
echo "🐍 Instalando dependências Python..."
pip3 install pandas numpy scikit-learn nltk

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências Python"
    exit 1
fi

echo "✅ Dependências Python instaladas"

# Criar diretórios necessários
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p data logs public/images

# Verificar se os notebooks existem
echo ""
echo "📊 Verificando notebooks de referência..."
if [ -f "Notebook1_IMDb_WebScraping_KMeans.ipynb" ]; then
    echo "✅ Notebook 1 encontrado"
else
    echo "⚠️ Notebook 1 não encontrado"
fi

if [ -f "Notebook2_Modelo_Comparacao_Features.ipynb" ]; then
    echo "✅ Notebook 2 encontrado"
else
    echo "⚠️ Notebook 2 não encontrado"
fi

# Executar integração dos notebooks
echo ""
echo "🔄 Executando integração dos notebooks..."
python3 scripts/integrate_notebooks.py

if [ $? -eq 0 ]; then
    echo "✅ Integração dos notebooks concluída"
else
    echo "⚠️ Erro na integração dos notebooks (continuando...)"
fi

# Verificar se o build funciona
echo ""
echo "🔨 Testando build do projeto..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build realizado com sucesso"
else
    echo "❌ Erro no build do projeto"
    exit 1
fi

# Criar arquivo de configuração
echo ""
echo "⚙️ Criando arquivo de configuração..."
cat > .env.local << EOF
# FiapFlix Configuration
NODE_ENV=development
NEXT_PUBLIC_APP_NAME=FiapFlix
NEXT_PUBLIC_APP_DESCRIPTION=Sistema de Recomendação de Filmes com IA
NEXT_PUBLIC_API_URL=http://localhost:3000
ML_MODEL_PATH=./lib/ml_model.py
ML_DATA_PATH=./data/movies.csv
CACHE_TTL=3600
LOG_LEVEL=info
EOF

echo "✅ Arquivo de configuração criado"

# Executar testes básicos
echo ""
echo "🧪 Executando testes básicos..."
npm run lint

if [ $? -eq 0 ]; then
    echo "✅ Linting passou"
else
    echo "⚠️ Alguns problemas de linting encontrados"
fi

# Mostrar resumo
echo ""
echo "🎉 Configuração concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Execute 'npm run dev' para iniciar o servidor de desenvolvimento"
echo "   2. Acesse http://localhost:3000 no seu navegador"
echo "   3. Teste o sistema de recomendação"
echo ""
echo "🚀 Para deploy no Netlify:"
echo "   1. Faça commit e push para o GitHub"
echo "   2. Conecte o repositório ao Netlify"
echo "   3. Configure as variáveis de ambiente"
echo "   4. Faça o deploy"
echo ""
echo "📚 Documentação:"
echo "   - README.md: Documentação completa"
echo "   - deploy.md: Guia de deploy"
echo "   - data/integration_report.json: Relatório de integração"
echo ""
echo "🎯 Funcionalidades implementadas:"
echo "   ✅ Interface Netflix-like responsiva"
echo "   ✅ Sistema de recomendação com IA"
echo "   ✅ Dois métodos de recomendação"
echo "   ✅ Integração com notebooks"
echo "   ✅ API RESTful"
echo "   ✅ Deploy no Netlify"
echo ""
echo "🔗 Links úteis:"
echo "   - Netlify: https://netlify.com"
echo "   - Next.js: https://nextjs.org"
echo "   - Tailwind CSS: https://tailwindcss.com"
echo ""
echo "Desenvolvido por: FIAP - Front End & Mobile Development"
echo "Período: 2º Semestre 2025"
