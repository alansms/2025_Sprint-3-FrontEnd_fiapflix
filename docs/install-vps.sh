#!/bin/bash

# ============================================
# FiapFlix - Script de Instalação Automática
# Para VPS/Servidor Ubuntu/Debian
# ============================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║     FiapFlix - Instalação VPS       ║"
echo "║  Sistema de Recomendação com IA     ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se é root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Este script precisa ser executado como root (sudo)${NC}" 
   exit 1
fi

echo -e "${YELLOW}📋 Verificando sistema...${NC}"
sleep 1

# Atualizar sistema
echo -e "${BLUE}🔄 Atualizando sistema...${NC}"
apt-get update -qq
apt-get upgrade -y -qq

# Instalar dependências básicas
echo -e "${BLUE}📦 Instalando dependências básicas...${NC}"
apt-get install -y -qq \
    curl \
    wget \
    git \
    ufw \
    ca-certificates \
    gnupg \
    lsb-release

# Instalar Docker
echo -e "${BLUE}🐳 Instalando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    # Adicionar repositório Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Habilitar Docker
    systemctl enable docker
    systemctl start docker
    
    echo -e "${GREEN}✅ Docker instalado com sucesso${NC}"
else
    echo -e "${GREEN}✅ Docker já está instalado${NC}"
fi

# Instalar Docker Compose (se não vier com plugin)
echo -e "${BLUE}🔧 Verificando Docker Compose...${NC}"
if ! docker compose version &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose instalado${NC}"
else
    echo -e "${GREEN}✅ Docker Compose já está instalado${NC}"
fi

# Configurar Firewall
echo -e "${BLUE}🔥 Configurando Firewall...${NC}"
ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3001/tcp  # Aplicação (opcional, para debug)
echo -e "${GREEN}✅ Firewall configurado${NC}"

# Clonar repositório
echo -e "${BLUE}📥 Clonando repositório FiapFlix...${NC}"
cd /opt
if [ -d "FiapFlix" ]; then
    echo -e "${YELLOW}⚠️  Diretório já existe, atualizando...${NC}"
    cd FiapFlix
    git pull
else
    git clone https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix.git FiapFlix
    cd FiapFlix
fi

# Criar diretório para SSL (opcional)
mkdir -p ssl
echo -e "${GREEN}✅ Repositório clonado/atualizado${NC}"

# Configurar variáveis de ambiente
echo -e "${BLUE}⚙️  Configurando variáveis de ambiente...${NC}"
cat > .env.production << EOF
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
OMDB_API_KEY=668159f8
NEXT_PUBLIC_APP_URL=http://$(curl -s ifconfig.me)
EOF
echo -e "${GREEN}✅ Variáveis configuradas${NC}"

# Build da imagem Docker
echo -e "${BLUE}🔨 Construindo imagem Docker (pode demorar alguns minutos)...${NC}"
docker compose build

# Iniciar containers
echo -e "${BLUE}🚀 Iniciando FiapFlix...${NC}"
docker compose up -d

# Aguardar aplicação iniciar
echo -e "${YELLOW}⏳ Aguardando aplicação inicializar...${NC}"
sleep 10

# Verificar status
if docker compose ps | grep -q "Up"; then
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║         ✅ FiapFlix instalado com sucesso!          ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Informações de acesso
    PUBLIC_IP=$(curl -s ifconfig.me)
    echo -e "${BLUE}📍 Informações de Acesso:${NC}"
    echo -e "   ${GREEN}• URL Local:${NC}     http://localhost"
    echo -e "   ${GREEN}• URL Pública:${NC}   http://${PUBLIC_IP}"
    echo -e "   ${GREEN}• Porta Direta:${NC}  http://${PUBLIC_IP}:3001"
    echo ""
    echo -e "${BLUE}🔧 Comandos Úteis:${NC}"
    echo -e "   ${YELLOW}• Ver logs:${NC}         cd /opt/FiapFlix && docker compose logs -f"
    echo -e "   ${YELLOW}• Reiniciar:${NC}        cd /opt/FiapFlix && docker compose restart"
    echo -e "   ${YELLOW}• Parar:${NC}            cd /opt/FiapFlix && docker compose down"
    echo -e "   ${YELLOW}• Atualizar:${NC}        cd /opt/FiapFlix && git pull && docker compose up -d --build"
    echo ""
    echo -e "${GREEN}🎬 FiapFlix está rodando!${NC}"
    
else
    echo -e "${RED}❌ Erro ao iniciar a aplicação. Verifique os logs:${NC}"
    echo -e "   docker compose logs"
    exit 1
fi

# Criar script de gerenciamento
cat > /usr/local/bin/fiapflix << 'EOF'
#!/bin/bash
cd /opt/FiapFlix

case "$1" in
    start)
        docker compose up -d
        echo "✅ FiapFlix iniciado"
        ;;
    stop)
        docker compose down
        echo "✅ FiapFlix parado"
        ;;
    restart)
        docker compose restart
        echo "✅ FiapFlix reiniciado"
        ;;
    logs)
        docker compose logs -f
        ;;
    update)
        git pull
        docker compose up -d --build
        echo "✅ FiapFlix atualizado"
        ;;
    status)
        docker compose ps
        ;;
    *)
        echo "Uso: fiapflix {start|stop|restart|logs|update|status}"
        exit 1
        ;;
esac
EOF

chmod +x /usr/local/bin/fiapflix
echo -e "${GREEN}✅ Script de gerenciamento 'fiapflix' instalado${NC}"
echo -e "${BLUE}   Use: ${YELLOW}fiapflix {start|stop|restart|logs|update|status}${NC}"

echo ""
echo -e "${GREEN}🎉 Instalação completa! Aproveite o FiapFlix!${NC}"

