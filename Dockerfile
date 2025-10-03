# ==================================
# FiapFlix - Dockerfile Multi-Stage
# ==================================

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS runner

WORKDIR /app

# Instalar Python e dependências
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-numpy \
    py3-pandas

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copiar apenas o necessário do builder
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Copiar arquivos Python e modelos
COPY --chown=nextjs:nodejs lib/*.py ./lib/
COPY --chown=nextjs:nodejs models ./models/
COPY --chown=nextjs:nodejs requirements.txt ./

# Instalar dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar datasets
COPY --chown=nextjs:nodejs *.json ./
COPY --chown=nextjs:nodejs *.csv ./

# Mudar para usuário não-root
USER nextjs

# Expor porta
EXPOSE 3001

# Variáveis de ambiente
ENV NODE_ENV=production
ENV PORT=3001
ENV HOSTNAME=0.0.0.0

# Comando de inicialização
CMD ["npm", "start", "--", "--hostname", "0.0.0.0", "--port", "3001"]

