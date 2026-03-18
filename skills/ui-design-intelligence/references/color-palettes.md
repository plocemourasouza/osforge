# Color Palettes — UI Design Intelligence

Paletas curadas por indústria e tipo de produto. Cada paleta inclui tokens hex e mapeamento semântico.

---

## SaaS / B2B

### SaaS Confiável (padrão)
| Token | Hex | Uso |
|---|---|---|
| primary | #2563eb | CTAs, links |
| primary-dark | #1d4ed8 | Hover |
| background | #ffffff | Fundo |
| surface | #f8fafc | Cards, sidebar |
| text-primary | #0f172a | Textos |
| text-muted | #64748b | Labels |
| border | #e2e8f0 | Dividers |
| success | #16a34a | Confirmações |
| warning | #d97706 | Alertas |
| error | #dc2626 | Erros |

### SaaS Dark Premium
| Token | Hex | Uso |
|---|---|---|
| primary | #6366f1 | CTAs |
| background | #0f172a | Fundo |
| surface | #1e293b | Cards |
| text-primary | #f1f5f9 | Textos |
| text-muted | #94a3b8 | Labels |
| border | #334155 | Dividers |
| success | #22c55e | Positivo |
| error | #ef4444 | Negativo |

---

## Fintech / Banking

### Fintech Moderno
| Token | Hex | Uso |
|---|---|---|
| primary | #0ea5e9 | Ações principais |
| positive | #00c896 | Ganho, saldo positivo |
| negative | #ff4757 | Perda, saldo negativo |
| background | #060b18 | Fundo dark |
| surface | #0d1b2a | Cards |
| surface-2 | #162236 | Cards elevados |
| text-primary | #e2e8f0 | Textos |
| text-muted | #64748b | Valores secundários |
| gold | #f59e0b | Tier premium, destaque |

### Banco Tradicional / Confiável
| Token | Hex | Uso |
|---|---|---|
| primary | #1e3a5f | Marca, cabeçalhos |
| secondary | #2d6a9f | Links, CTAs secundários |
| accent | #f0a500 | Destaques, ícones de produto |
| background | #f4f7fb | Fundo |
| surface | #ffffff | Cards |
| text-primary | #1a202c | Textos |
| success | #276749 | Transações positivas |
| error | #c53030 | Alertas críticos |

---

## Healthcare / Wellness

### Healthcare Humanizado
| Token | Hex | Uso |
|---|---|---|
| primary | #0891b2 | Ações (azul teal confiável) |
| calm | #d1fae5 | Backgrounds de sucesso |
| background | #f0fdf4 | Fundo levemente esverdeado |
| surface | #ffffff | Cards |
| text-primary | #134e4a | Textos escuros |
| text-muted | #6b7280 | Secundários |
| alert | #f59e0b | Avisos (nunca vermelho para alertas não críticos) |
| emergency | #dc2626 | Apenas para emergências reais |

### Wellness / Mental Health
| Token | Hex | Uso |
|---|---|---|
| primary | #8b5cf6 | Accent suave |
| warm | #fef3c7 | Backgrounds quentes |
| calm-blue | #dbeafe | Cards de tranquilidade |
| background | #fafaf9 | Levemente quente |
| surface | #ffffff | Cards |
| text-primary | #292524 | Textos |

---

## E-commerce

### Marketplace Popular
| Token | Hex | Uso |
|---|---|---|
| primary | #f97316 | CTAs de compra |
| deal | #ef4444 | Badges de desconto |
| rating | #fbbf24 | Estrelas |
| background | #f9fafb | Fundo |
| surface | #ffffff | Cards de produto |
| text-primary | #111827 | Preços, títulos |
| text-muted | #6b7280 | Descrições |

### Fashion / Premium
| Token | Hex | Uso |
|---|---|---|
| primary | #1c1917 | Texto e ações (quase preto) |
| accent | #d4af37 | Dourado, detalhes premium |
| background | #fafaf9 | Off-white quente |
| surface | #ffffff | Cards |
| text-primary | #1c1917 | Textos |
| text-muted | #78716c | Descrições |

---

## Educação / EdTech

### Plataforma de Aprendizado
| Token | Hex | Uso |
|---|---|---|
| primary | #7c3aed | Roxo engajante |
| secondary | #f97316 | Laranja motivador |
| progress | #22c55e | Barras de progresso |
| background | #fafafa | Fundo |
| surface | #ffffff | Cards de curso |
| text-primary | #1e1b4b | Textos |
| badge-gold | #f59e0b | Conquistas |
| badge-silver | #94a3b8 | Conquistas intermediárias |

---

## Turismo / Travel

### Marketplace de Turismo
| Token | Hex | Uso |
|---|---|---|
| primary | #0369a1 | Azul oceano — CTAs |
| nature | #15803d | Verde natureza |
| sunset | #ea580c | Laranja amanhecer — destaque |
| background | #f0f9ff | Azul claríssimo |
| surface | #ffffff | Cards |
| text-primary | #0c4a6e | Textos |
| rating | #fbbf24 | Estrelas de avaliação |

---

## Jurídico / Compliance

### Sistema Jurídico
| Token | Hex | Uso |
|---|---|---|
| primary | #1e3a5f | Azul formal |
| secondary | #374151 | Ações secundárias |
| background | #f9fafb | Fundo neutro |
| surface | #ffffff | Cards |
| text-primary | #111827 | Textos — máximo contraste |
| text-muted | #6b7280 | Metadados |
| alert | #b45309 | Prazos, alertas |
| critical | #991b1b | Situações críticas |

---

## Contabilidade / ERP

### Sistema Contábil
| Token | Hex | Uso |
|---|---|---|
| primary | #1d4ed8 | Ações principais |
| positive | #166534 | Créditos, entradas |
| negative | #991b1b | Débitos, saídas |
| neutral | #374151 | Neutros, transferências |
| background | #f8fafc | Fundo |
| surface | #ffffff | Tabelas, cards |
| text-primary | #0f172a | Valores, textos |
| text-muted | #64748b | Labels, categorias |
| border | #e2e8f0 | Divisores de tabela |

---

## Como selecionar

1. Identificar a indústria principal do produto
2. Verificar se há restrições regulatórias de cor (healthcare: evitar vermelho primário)
3. Adaptar modo claro/escuro conforme o contexto de uso
4. Mapear os tokens para as variáveis CSS do projeto (CSS vars, Tailwind extend, etc.)
