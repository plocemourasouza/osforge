---
name: predictive-failure
description: >
  Analyze implemented code to predict potential failure points that tests
  may not catch. Uses pattern matching against common production failure modes.
  Use after implementation is complete, when asked to predict failures,
  find hidden bugs, check what could go wrong, production readiness check,
  or pre-deploy analysis. Triggers on: predict failures, what could go wrong,
  hidden bugs, production readiness, pre-deploy check, failure analysis.
metadata:
  author: paulo-cursor-setup
  version: "1.0.0"
---

# Predictive Failure Analysis

Após implementação e testes passando, esta skill busca falhas que testes
tradicionais NÃO capturam — usando pattern matching contra failure modes
comuns em apps de produção.

## Quando Usar
- Testes passam mas quer validação extra antes de deploy
- Após implementação de feature complexa
- Antes de release para produção
- Quando pedido: "o que pode dar errado?", "predict failures"

## Processo

### 1. Scan do Código Implementado
Leia todos os arquivos modificados recentemente (git diff ou lista de arquivos).
Identifique: componentes, API routes, Server Actions, hooks, utils.

### 2. Análise por Categoria

#### Race Conditions & Timing
- Requests concorrentes ao mesmo recurso (ex: double-click em botão de submit)
- State updates fora de ordem em async operations
- Debounce/throttle ausente em inputs rápidos (search, resize)
- useEffect com dependências async sem cleanup/abort controller
- Optimistic updates sem rollback quando server falha

#### Edge Cases de Dados
- Strings com unicode/emojis em campos de texto (quebra length validation)
- Números no limite de precisão float (0.1 + 0.2 !== 0.3)
- Arrays vazios onde se espera pelo menos 1 item
- Null/undefined em nested objects (optional chaining ausente)
- Datas em timezones diferentes (UTC vs local)
- Valores monetários com arredondamento incorreto

#### Network & Infra
- Timeout de API sem tratamento (o que acontece após 30s?)
- Retry sem exponential backoff (DDoS no próprio backend)
- Cache stale após deploy (versão old no browser)
- CORS em produção diferente de desenvolvimento
- WebSocket reconnection sem backoff
- Rate limiting ausente em endpoints públicos

#### State Management
- Memory leaks em useEffect sem cleanup
- Stale closures em callbacks async com state
- Hydration mismatch (server vs client rendering diferente)
- State local que deveria ser global (ou vice-versa)
- Form state perdido em navegação (back button)

#### Security em Produção
- CSRF em mutations (Server Actions protegem, Route Handlers não)
- XSS em conteúdo dinâmico renderizado com dangerouslySetInnerHTML
- SQL injection em queries raw (Prisma parametriza, mas raw queries não)
- Exposed stack traces em error responses de produção
- Tokens em URL parameters (aparecem em logs e referrer headers)

#### UX sob Stress
- Lista com 10.000+ items sem virtualização
- Upload de arquivo grande sem progress indicator
- Muitas tabs/janelas abertas com mesmo auth state
- Slow 3G: o que o usuário vê durante carregamento?
- Acessibilidade: funciona sem mouse? sem visão?

### 3. Output

Para cada issue encontrada, reporte:

| Campo | Formato |
|-------|---------|
| **Severidade** | 🔴 Crítica / 🟠 Alta / 🟡 Média / 🔵 Baixa |
| **Probabilidade** | Comum / Ocasional / Raro |
| **Categoria** | Uma das 6 categorias acima |
| **Cenário** | Como reproduzir em 1-2 frases |
| **Impacto** | O que o usuário experiencia |
| **Arquivo** | Localização no código |
| **Fix sugerido** | Código ou pattern para resolver |

### 4. Priorização

Ordene issues por: Severidade × Probabilidade
- 🔴 Crítica + Comum → BLOQUEIA deploy
- 🔴 Crítica + Raro → Resolver antes de v1.0
- 🟠 Alta + Comum → Resolver nesta sprint
- Demais → Backlog priorizado

## Importante
- NÃO liste problemas teóricos — apenas issues com evidência no código
- Aponte o ARQUIVO e LINHA onde o problema existe
- O fix sugerido deve ser implementável (não genérico)
- Se não encontrar nenhum issue, diga honestamente — não invente problemas
