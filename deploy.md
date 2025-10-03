# 🚀 Guia de Deploy - FiapFlix

## Deploy no Netlify

### 1. Preparação do Projeto

```bash
# Instalar dependências
npm install

# Build do projeto
npm run build

# Testar localmente
npm start
```

### 2. Configuração no Netlify

1. **Acesse** [netlify.com](https://netlify.com)
2. **Conecte** seu repositório GitHub
3. **Configure** as seguintes configurações:

#### Build Settings
- **Build command**: `npm run build`
- **Publish directory**: `.next`
- **Node version**: 18

#### Environment Variables
```bash
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://your-site.netlify.app
```

### 3. Deploy Automático

O Netlify irá automaticamente:
- Detectar mudanças no repositório
- Executar o build
- Fazer deploy da aplicação
- Gerar URL pública

### 4. Configurações Avançadas

#### netlify.toml
```toml
[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Headers de Segurança
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
```

### 5. Verificação do Deploy

1. **Acesse** a URL fornecida pelo Netlify
2. **Teste** todas as funcionalidades
3. **Verifique** se as APIs estão funcionando
4. **Confirme** se o sistema de recomendação está operacional

### 6. Monitoramento

- **Netlify Analytics**: Métricas de performance
- **Logs**: Acompanhamento de erros
- **Uptime**: Monitoramento de disponibilidade

## Troubleshooting

### Problemas Comuns

1. **Build falha**
   - Verificar versão do Node.js
   - Limpar cache: `npm run clean`
   - Reinstalar dependências

2. **APIs não funcionam**
   - Verificar variáveis de ambiente
   - Testar endpoints localmente
   - Verificar logs do Netlify

3. **Performance lenta**
   - Otimizar imagens
   - Implementar cache
   - Usar CDN

### Comandos Úteis

```bash
# Deploy manual
netlify deploy --prod

# Ver logs
netlify logs

# Status do site
netlify status
```

## URLs de Produção

- **Site Principal**: https://fiapflix.netlify.app
- **API Movies**: https://fiapflix.netlify.app/api/movies
- **API Recommend**: https://fiapflix.netlify.app/api/recommend
- **API Scrape**: https://fiapflix.netlify.app/api/scrape

## Monitoramento e Analytics

### Métricas Importantes
- **Page Views**: Visualizações de página
- **Unique Visitors**: Visitantes únicos
- **Bounce Rate**: Taxa de rejeição
- **Load Time**: Tempo de carregamento

### Alertas Configurados
- **Uptime**: < 99%
- **Response Time**: > 3s
- **Error Rate**: > 5%

## Backup e Recuperação

### Backup Automático
- **Código**: GitHub
- **Dados**: Netlify Functions
- **Configurações**: netlify.toml

### Recuperação de Desastres
1. **Restaurar** do GitHub
2. **Redeploy** no Netlify
3. **Verificar** funcionalidades
4. **Testar** APIs

## Otimizações de Performance

### Frontend
- **Lazy Loading**: Componentes sob demanda
- **Image Optimization**: Compressão automática
- **Code Splitting**: Divisão de código
- **Caching**: Cache de assets

### Backend
- **API Caching**: Cache de respostas
- **Database**: Otimização de queries
- **CDN**: Distribuição global
- **Compression**: Compressão gzip

## Segurança

### Headers de Segurança
- **CSP**: Content Security Policy
- **HSTS**: HTTP Strict Transport Security
- **X-Frame-Options**: Proteção contra clickjacking
- **X-Content-Type-Options**: Proteção MIME

### Autenticação
- **JWT**: Tokens seguros
- **Rate Limiting**: Limite de requisições
- **CORS**: Configuração adequada
- **HTTPS**: Certificado SSL

## Manutenção

### Atualizações Regulares
- **Dependências**: Atualização mensal
- **Security Patches**: Aplicação imediata
- **Performance**: Otimizações contínuas
- **Monitoring**: Acompanhamento 24/7

### Backup Strategy
- **Daily**: Backup automático
- **Weekly**: Backup completo
- **Monthly**: Backup de arquivos
- **Yearly**: Backup de longo prazo
