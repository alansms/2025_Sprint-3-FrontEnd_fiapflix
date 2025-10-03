# 🚀 FiapFlix - Guia de Deploy em VPS

## 📋 Pré-requisitos

### VPS/Servidor
- **Sistema Operacional**: Ubuntu 20.04+ ou Debian 11+
- **RAM**: Mínimo 2GB (recomendado 4GB)
- **CPU**: Mínimo 2 cores
- **Disco**: Mínimo 20GB
- **Acesso**: Root ou sudo

### Provedores Recomendados
- **DigitalOcean**: Droplet $12/mês (2GB RAM)
- **Linode**: Linode 2GB $10/mês
- **AWS**: EC2 t3.small
- **Vultr**: High Frequency $12/mês
- **Contabo**: VPS S (4GB) €5.99/mês
- **Proxmox**: LXC Container local

---

## 🎯 Instalação Automática (Recomendado)

### Passo 1: Conectar ao Servidor
```bash
ssh root@SEU_IP_DO_SERVIDOR
```

### Passo 2: Executar Script de Instalação
```bash
curl -fsSL https://raw.githubusercontent.com/alansms/2025_Sprint-3-FrontEnd_fiapflix/main/install-vps.sh | sudo bash
```

**Pronto!** A aplicação estará disponível em:
- **HTTP**: `http://SEU_IP`
- **Porta Direta**: `http://SEU_IP:3001`

### Tempo de Instalação
⏱️ Aproximadamente 5-10 minutos (dependendo da conexão)

---

## 🔧 Instalação Manual

### 1. Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Docker
```bash
# Instalar dependências
sudo apt install -y curl ca-certificates gnupg

# Adicionar repositório Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Clonar Repositório
```bash
cd /opt
sudo git clone https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix.git FiapFlix
cd FiapFlix
```

### 4. Configurar Variáveis de Ambiente
```bash
sudo nano .env.production
```

Adicionar:
```env
NODE_ENV=production
PORT=3001
HOSTNAME=0.0.0.0
OMDB_API_KEY=668159f8
NEXT_PUBLIC_APP_URL=http://SEU_IP
```

### 5. Construir e Iniciar
```bash
sudo docker compose build
sudo docker compose up -d
```

### 6. Configurar Firewall
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## 🐳 Gerenciamento via Docker

### Comandos Úteis

```bash
# Ver status dos containers
cd /opt/FiapFlix
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f fiapflix

# Reiniciar aplicação
docker compose restart

# Parar aplicação
docker compose down

# Iniciar aplicação
docker compose up -d

# Rebuild completo
docker compose up -d --build

# Limpar volumes e rebuild
docker compose down -v
docker compose up -d --build
```

### Usando o Script de Gerenciamento

Se usou a instalação automática, você tem o comando `fiapflix`:

```bash
fiapflix start    # Iniciar
fiapflix stop     # Parar
fiapflix restart  # Reiniciar
fiapflix logs     # Ver logs
fiapflix update   # Atualizar do GitHub
fiapflix status   # Ver status
```

---

## 🔒 Configurar HTTPS com Let's Encrypt (Opcional)

### Pré-requisito: Ter um Domínio

### 1. Instalar Certbot
```bash
sudo apt install -y certbot
```

### 2. Obter Certificado SSL
```bash
sudo certbot certonly --standalone -d seu-dominio.com -d www.seu-dominio.com
```

### 3. Configurar Nginx
Editar `nginx.conf` e descomentar a seção HTTPS:

```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    # ... resto da configuração
}
```

### 4. Copiar Certificados
```bash
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem /opt/FiapFlix/ssl/
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem /opt/FiapFlix/ssl/
```

### 5. Reiniciar
```bash
cd /opt/FiapFlix
docker compose restart nginx
```

### 6. Configurar Renovação Automática
```bash
sudo crontab -e
```

Adicionar:
```
0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/seu-dominio.com/*.pem /opt/FiapFlix/ssl/ && docker compose -f /opt/FiapFlix/docker-compose.yml restart nginx
```

---

## 📊 Monitoramento

### Ver Uso de Recursos
```bash
# CPU e Memória dos containers
docker stats

# Espaço em disco
df -h

# Logs do sistema
journalctl -u docker -f
```

### Health Check
```bash
# Verificar se a aplicação está respondendo
curl http://localhost:3001

# Status dos containers
docker compose ps
```

---

## 🔄 Atualizar Aplicação

### Método Automático
```bash
fiapflix update
```

### Método Manual
```bash
cd /opt/FiapFlix
git pull
docker compose down
docker compose up -d --build
```

---

## 🐛 Troubleshooting

### Aplicação não inicia
```bash
# Ver logs detalhados
docker compose logs -f

# Verificar se as portas estão em uso
sudo netstat -tulpn | grep :3001
sudo netstat -tulpn | grep :80
```

### Erro de memória
```bash
# Aumentar memória do Docker (editar daemon.json)
sudo nano /etc/docker/daemon.json
```

Adicionar:
```json
{
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

Reiniciar Docker:
```bash
sudo systemctl restart docker
```

### Limpar espaço em disco
```bash
# Remover imagens não utilizadas
docker system prune -a

# Remover volumes não utilizados
docker volume prune
```

### Logs de erro do Next.js
```bash
docker compose logs fiapflix | grep error
```

---

## 🌐 Configurar Domínio

### 1. Configurar DNS
No painel do seu provedor de domínio:

- **Tipo A**: `@` → `SEU_IP_DO_SERVIDOR`
- **Tipo A**: `www` → `SEU_IP_DO_SERVIDOR`

### 2. Aguardar Propagação
⏱️ Pode levar até 24h (geralmente 1-2h)

### 3. Verificar
```bash
nslookup seu-dominio.com
ping seu-dominio.com
```

---

## 💾 Backup e Restauração

### Fazer Backup
```bash
cd /opt
sudo tar -czf fiapflix-backup-$(date +%Y%m%d).tar.gz FiapFlix/
```

### Restaurar Backup
```bash
cd /opt
sudo tar -xzf fiapflix-backup-YYYYMMDD.tar.gz
cd FiapFlix
docker compose up -d
```

### Backup Automático (Cron)
```bash
sudo crontab -e
```

Adicionar (backup diário às 3h):
```
0 3 * * * tar -czf /opt/backups/fiapflix-$(date +\%Y\%m\%d).tar.gz /opt/FiapFlix/
```

---

## 🎯 Proxmox LXC Container

### Criar Container
```bash
# No Proxmox
pct create 100 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname fiapflix \
  --memory 4096 \
  --cores 2 \
  --storage local-lvm \
  --rootfs local-lvm:20 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp
```

### Iniciar e Configurar
```bash
pct start 100
pct enter 100

# Seguir instalação automática
curl -fsSL https://raw.githubusercontent.com/alansms/2025_Sprint-3-FrontEnd_fiapflix/main/install-vps.sh | bash
```

---

## 📞 Suporte

**Problemas?** Abra uma issue no GitHub:
https://github.com/alansms/2025_Sprint-3-FrontEnd_fiapflix/issues

---

## ✅ Checklist de Deploy

- [ ] VPS provisionada (2GB+ RAM)
- [ ] SSH configurado
- [ ] Docker instalado
- [ ] Repositório clonado
- [ ] Containers rodando
- [ ] Firewall configurado
- [ ] Aplicação acessível via IP
- [ ] (Opcional) Domínio configurado
- [ ] (Opcional) SSL/HTTPS configurado
- [ ] (Opcional) Backup configurado

---

**🎬 FiapFlix está pronto para produção!**

