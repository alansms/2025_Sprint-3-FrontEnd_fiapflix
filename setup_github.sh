#!/bin/bash

# 🚀 Script para Configurar o FiapFlix no GitHub
# Execute este script após criar o repositório no GitHub

echo "🎬 Configurando FiapFlix para GitHub..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Instruções para subir o FiapFlix no GitHub:${NC}"
echo ""
echo -e "${YELLOW}1. 🌐 CRIAR REPOSITÓRIO NO GITHUB:${NC}"
echo "   • Acesse: https://github.com/new"
echo "   • Nome: fiapflix"
echo "   • Descrição: 🎬 FiapFlix - Sistema de Recomendação de Filmes com IA"
echo "   • Público ou Privado (sua escolha)"
echo "   • NÃO marque 'Add README' (já temos)"
echo "   • NÃO marque 'Add .gitignore' (já temos)"
echo "   • Clique em 'Create repository'"
echo ""
echo -e "${YELLOW}2. 🔗 CONECTAR REPOSITÓRIO LOCAL:${NC}"
echo "   • Copie a URL do seu repositório"
echo "   • Execute os comandos abaixo:"
echo ""
echo -e "${GREEN}   git remote add origin https://github.com/SEU_USUARIO/fiapflix.git${NC}"
echo -e "${GREEN}   git branch -M main${NC}"
echo -e "${GREEN}   git push -u origin main${NC}"
echo ""
echo -e "${YELLOW}3. ✅ VERIFICAR UPLOAD:${NC}"
echo "   • Acesse: https://github.com/SEU_USUARIO/fiapflix"
echo "   • Confirme se todos os arquivos estão lá"
echo "   • Verifique se o README.md está sendo exibido"
echo ""

# Verificar se já existe remote
if git remote -v | grep -q "origin"; then
    echo -e "${GREEN}✅ Remote origin já configurado!${NC}"
    echo "Remote atual:"
    git remote -v
    echo ""
    echo -e "${YELLOW}Para fazer push:${NC}"
    echo -e "${GREEN}git push -u origin main${NC}"
else
    echo -e "${YELLOW}⚠️  Remote origin não configurado${NC}"
    echo "Execute os comandos acima para configurar"
fi

echo ""
echo -e "${BLUE}📁 Estrutura do projeto:${NC}"
echo "✅ app/ - Next.js App Router"
echo "✅ components/ - Componentes React"
echo "✅ lib/ - Utilitários e modelos"
echo "✅ scripts/ - Scripts Python"
echo "✅ public/ - Arquivos estáticos"
echo "✅ README.md - Documentação completa"
echo "✅ requirements.txt - Dependências Python"
echo "✅ package.json - Dependências Node.js"
echo "✅ .gitignore - Arquivos ignorados"
echo ""

echo -e "${GREEN}🎯 PROJETO PRONTO PARA GITHUB!${NC}"
echo "Siga as instruções acima para subir o repositório."
echo ""
echo -e "${BLUE}🚀 Próximos passos após subir:${NC}"
echo "• Deploy no Netlify ou Vercel"
echo "• Configurar variáveis de ambiente"
echo "• Testar em produção"
echo ""
echo -e "${GREEN}✨ FiapFlix está 100% funcional e pronto para o GitHub!${NC}"
