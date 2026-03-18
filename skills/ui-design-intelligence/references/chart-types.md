# Chart Types — UI Design Intelligence

25 tipos de chart para dashboards e analytics. Para cada tipo: quando usar, quando NÃO usar, e biblioteca recomendada.

---

## Comparação

### Bar Chart (Barras verticais)
**Usar quando:** Comparar valores entre categorias distintas (receita por mês, usuários por plano)  
**Não usar:** Para mais de 12 categorias, ou quando a ordem temporal é o foco principal  
**Bibliotecas:** Recharts `<BarChart>` | Chart.js | Victory  
**Tip:** Ordenar da maior para menor barra quando a ordem não é temporal

### Horizontal Bar Chart
**Usar quando:** Labels longas (nomes de produto, países), ou quando comparar rankings  
**Não usar:** Para séries temporais  
**Tip:** Ideal para "top 10" com nomes que não cabem no eixo X

### Grouped Bar Chart
**Usar quando:** Comparar múltiplas séries para as mesmas categorias (receita vs meta por mês)  
**Não usar:** Mais de 3 séries no mesmo grupo — vira poluição visual  
**Tip:** Máximo 3 grupos de barras lado a lado

### Stacked Bar Chart
**Usar quando:** Mostrar composição de um total (breakdown de receita por categoria)  
**Não usar:** Quando o usuário precisa comparar valores intermediários exatos  
**Tip:** Colocar a série mais importante na base

---

## Tendência / Temporal

### Line Chart
**Usar quando:** Evolução de um valor ao longo do tempo (MAU, receita mensal, tickets abertos)  
**Não usar:** Para categorias não ordenadas (preferir barras)  
**Bibliotecas:** Recharts `<LineChart>` | Chart.js  
**Tip:** Máximo 4 linhas no mesmo gráfico antes de ficar ilegível

### Area Chart
**Usar quando:** Enfatizar magnitude além da tendência (volume, tráfego)  
**Não usar:** Para múltiplas séries que se sobrepõem muito  
**Tip:** Use fill com opacidade 0.1–0.2 para não esconder linhas subjacentes

### Stacked Area Chart
**Usar quando:** Composição de um total ao longo do tempo (tráfego por canal)  
**Não usar:** Mais de 4 séries empilhadas  
**Tip:** Cada área precisa ter cor suficientemente diferente

### Spark Line
**Usar quando:** Mini-tendência dentro de um KPI card (sem eixos, sem labels)  
**Tip:** Ideal em StatCard — apenas a forma da curva importa, não os valores exatos

---

## Proporção / Composição

### Pie Chart
**Usar quando:** Mostrar partes de um todo com no máximo 5 categorias  
**Não usar:** Mais de 5 fatias, ou quando as proporções são muito parecidas  
**Tip:** Ordenar do maior para menor, começando às 12h

### Donut Chart
**Usar quando:** Mesmo caso do Pie, mas com espaço central para exibir o total  
**Tip:** Exibir o valor total ou a maior categoria no centro

### Treemap
**Usar quando:** Hierarquia de dados com proporção (categorias de gasto, portfolios)  
**Não usar:** Quando há muitos itens pequenos (>20)  
**Tip:** Colorir por categoria, tamanho pelo valor

---

## Distribuição

### Histogram
**Usar quando:** Distribuição de uma variável contínua (tempo de resposta de API, idade dos usuários)  
**Não usar:** Para dados categóricos  
**Tip:** Escolher largura de bucket que mostre a distribuição sem ser granular demais

### Box Plot
**Usar quando:** Comparar distribuições entre grupos (tempo de resposta por endpoint)  
**Não usar:** Para audiências não técnicas — preferir bar chart com error bars  

### Scatter Plot
**Usar quando:** Correlação entre duas variáveis (churn vs NPS, custo vs performance)  
**Não usar:** Quando há mais de 500 pontos sem clustering  
**Tip:** Adicionar linha de tendência (regression line) para deixar a correlação visível

---

## Progresso / Status

### Gauge / Radial
**Usar quando:** Um único KPI com range conhecido (NPS de -100 a 100, CPU de 0–100%)  
**Não usar:** Para comparar múltiplos valores  
**Tip:** Adicionar zonas de cor (verde/amarelo/vermelho) para contexto rápido

### Progress Bar
**Usar quando:** Progresso em direção a uma meta (meta de vendas, onboarding, storage usado)  
**Tip:** Sempre mostrar o valor numérico além da barra

### Bullet Chart
**Usar quando:** Mostrar performance atual vs meta vs range (velocímetro de KPI)  
**Nota:** Menos conhecido mas muito eficiente para dashboards executivos

---

## Geográfico

### Choropleth Map
**Usar quando:** Métricas por região, estado ou país (receita por estado, usuários por país)  
**Biblioteca:** Recharts + GeoJSON | D3.js | deck.gl  
**Tip:** Usar escala de cor sequencial (claro → escuro), nunca divergente para valores absolutos

### Bubble Map
**Usar quando:** Concentração de eventos geográficos com magnitude  

---

## Relacionamento

### Network Graph
**Usar quando:** Relações entre entidades (grafo de referências, dependências de sistema)  
**Biblioteca:** D3.js force simulation | Cytoscape.js  
**Não usar:** Para audiências não técnicas — prefira table ou lista

### Sankey Diagram
**Usar quando:** Fluxo de volume entre estados (funil de vendas, jornada do usuário)  
**Biblioteca:** d3-sankey | Recharts (não tem nativo — usar biblioteca específica)

---

## Tabelas Especiais

### Heatmap Table
**Usar quando:** Comparar intensidade em duas dimensões (hora × dia, métrica × segmento)  
**Tip:** Usar escala de cor sequencial, adicionar legenda com range

### Funnel Chart
**Usar quando:** Conversão em etapas sequenciais (cadastro → ativação → retenção → receita)  
**Tip:** Sempre mostrar a taxa de conversão entre cada etapa, não apenas o volume

---

## Regras gerais de charts

1. **Título descritivo** — não "Receita" mas "Receita Mensal (Jan–Dez 2024)"
2. **Eixos com labels e unidades** — "R$ mil", "usuários", "%"
3. **Tooltips informativos** — ao hover, mostrar o valor exato + contexto
4. **Legenda** — apenas quando necessário; se há só uma série, dispensa
5. **Cores** — usar paleta consistente com o design system; nunca vermelho/verde sem semântica
6. **Responsive** — usar `ResponsiveContainer` (Recharts) ou equivalente
7. **Empty state** — chart sem dados precisa de estado vazio claro, não gráfico em branco
8. **Loading** — skeleton de chart durante carregamento de dados
