# 🐳 Correção Docker Build - FiapFlix

## ❌ Problema
```bash
npm error The `npm ci` command can only install with an existing package-lock.json or
npm error npm-shrinkwrap.json with lockfileVersion >= 1
```

## 🔍 Causa
- O `package-lock.json` usa **lockfileVersion 3** (muito recente)
- Comando `npm ci --only=production` está **obsoleto** e **incompatível**
- Docker pode estar usando **cache antigo**

## ✅ Solução Implementada

### Arquivos Corrigidos:

#### 1. **Dockerfile** (Principal)
```dockerfile
# Linha 14: Mudado de "npm ci --only=production" para "npm install"
RUN npm install
```

#### 2. **Dockerfile.simple** (Alternativa Simplificada)
```dockerfile
# Usa npm install --no-package-lock para evitar problemas
RUN npm install --no-package-lock
```

## 🚀 Como Usar no VPS

### Método 1: Usando Dockerfile Principal (Recomendado)
```bash
cd /opt/FiapFlix
git pull origin fix/docker-build
docker build -t fiapflix .
docker run -d -p 3001:3001 --name fiapflix fiapflix
```

### Método 2: Usando Dockerfile.simple
```bash
cd /opt/FiapFlix
git pull origin fix/docker-build
docker build -f Dockerfile.simple -t fiapflix .
docker run -d -p 3001:3001 --name fiapflix fiapflix
```

### Método 3: Com Docker Compose
```bash
cd /opt/FiapFlix
git pull origin fix/docker-build
docker-compose down
docker-compose up --build -d
```

## 🧹 Limpeza de Cache (Se Necessário)

```bash
# Parar todos os containers
docker stop $(docker ps -aq)

# Remover containers antigos
docker rm $(docker ps -aq)

# Limpar cache Docker
docker system prune -a -f

# Rebuild
docker build -t fiapflix .
```

## 📊 Comparação: npm ci vs npm install

| Comando | Quando Usar | Pros | Contras |
|---------|-------------|------|---------|
| `npm ci` | CI/CD, produção com lockfile compatível | ✅ Mais rápido<br>✅ Determinístico | ❌ Requer lockfile compatível |
| `npm install` | Desenvolvimento, lockfile v3 | ✅ Funciona sempre<br>✅ Atualiza lockfile | ❌ Mais lento |
| `npm install --no-package-lock` | Sem lockfile | ✅ Sempre funciona | ❌ Não determinístico |

## 🎯 Verificação

Após o build, verifique se está funcionando:

```bash
# Ver logs
docker logs -f fiapflix

# Testar endpoint
curl http://localhost:3001

# Ver status
docker ps
```

## 📝 Checklist

- [ ] Git pull da branch `fix/docker-build`
- [ ] Limpar cache Docker se necessário
- [ ] Build com novo Dockerfile
- [ ] Container rodando na porta 3001
- [ ] Aplicação acessível

## 🆘 Troubleshooting

### Erro: "command not found: docker"
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Erro: "permission denied"
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Erro: "port already in use"
```bash
# Parar processo na porta 3001
sudo lsof -ti:3001 | xargs kill -9
```

## 📞 Próximos Passos

1. **Pull da branch**: `git pull origin fix/docker-build`
2. **Build**: `docker build -t fiapflix .`
3. **Run**: `docker run -d -p 3001:3001 --name fiapflix fiapflix`
4. **Acesse**: `http://SEU_IP:3001`

---

**Atualizado**: 03/10/2025 - Correção do erro de npm ci
