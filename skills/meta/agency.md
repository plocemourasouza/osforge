# The Agency — Biblioteca de Especialistas de IA

**Trigger:** Precisar de um especialista em qualquer área não coberta pelas skills técnicas acima.

---

## Load

```
Leia skills/agency/SKILL.md
```

---

## Divisões (10)

| Division | Specialists | Focus |
|----------|-------------|-------|
| **Engineering** | 15+ | Security, SRE, DevOps, mobile, blockchain |
| **Design** | 10+ | UI/UX, design systems, identity, image prompts |
| **Marketing** | 12+ | SEO, content, social media, growth, ASO |
| **Paid Media** | 8+ | Google/Meta Ads, PPC, analytics |
| **Product** | 10+ | Roadmap, prioritization, market research |
| **Project Management** | 8+ | Planning, Jira, scrum |
| **Sales** | 10+ | Outbound, discovery, MEDDPICC, pipeline |
| **Support** | 8+ | Customer service, compliance, operations |
| **Quality** | 10+ | QA, API testing, WCAG, performance |
| **Advanced** | 10+ | Agent orchestration, SOC2/ISO, supply chain |

---

## Carregamento Hierárquico

```
1. Router (this file) → identifica divisão
2. Division index → lista agentes disponíveis
3. Agent file → carrega especialista específico
```

**Zero custo de contexto** até ser ativado.

---

## Exemplos de Uso

### Engineering
```
"Preciso de ajuda com segurança de API"
→ Load: skills/agency/engineering/engineering-security-architect.md
```

### Design
```
"Criar prompt para gerar imagem de produto"
→ Load: skills/agency/design/design-image-prompt-engineer.md
```

### Marketing
```
"Estratégia de ASO para app mobile"
→ Load: skills/agency/marketing/marketing-aso-specialist.md
```

---

## Total: 121 Especialistas

Cada especialista tem:
- System prompt otimizado
- Área de expertise definida
- Exemplos de uso
- Limitações documentadas
